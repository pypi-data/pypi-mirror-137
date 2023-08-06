import json
import logging
import os
import pickle

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
import streamlit as st

from mlfoundry_ui.webapp.dashboard_constants import *
from mlfoundry_ui.webapp.model_types.binary_classification_view import (
    BinaryClassificationView,
)
from mlfoundry_ui.webapp.model_types.multiclass_classification_view import (
    MulticlassClassificationView,
)
from mlfoundry_ui.webapp.model_types.regression_view import RegressionView
from mlfoundry_ui.webapp.model_types.timeseries_view import TimeSeriesView

logger = logging.getLogger(__name__)


class FeatureHealth:
    def __init__(self, dataclass):
        self.mlfoundry_data = dataclass
        self.model_type_to_view_map = {
            BINARY_CLASSIFICATION_MODEL_TYPE: BinaryClassificationView,
            MULTICLASS_CLASSIFICATION_MODEL_TYPE: MulticlassClassificationView,
            REGRESSION_MODEL_TYPE: RegressionView,
            TIMESERIES_MODEL_TYPE: TimeSeriesView,
        }

    def get_schema_shap(self, run_id):
        """
        Return the shap and schema corresponding to each dataslice in a dictionary
        """
        dir_path = self.mlfoundry_data.get_artifact(run_id, STATS_FILE_NAME)
        model_type = self.mlfoundry_data.get_model_type(run_id)
        if dir_path is None:
            st.warning(f"Feature Importance doesn't exists for run {run_id}")
            return None
        model_type = self.mlfoundry_data.get_model_type(run_id)

        dataslice_schemas = {}
        dataslice_shap = {}
        for file_name in os.listdir(dir_path):
            file_path = os.path.join(dir_path, file_name)
            for data_slice_name in DATA_SLICES:
                if data_slice_name in file_name and SCHEMA_FILE_NAME in file_name:
                    try:
                        with open(file_path, "rb") as f:
                            dataslice_schema = json.load(f)
                        dataslice_schemas[data_slice_name] = dataslice_schema
                    except Exception as e:
                        err_msg = f"Could not open file {file_path}, error message: {e}"
                        logger.warning(err_msg)
                        continue

                elif SHAP_VALUE_FILE_NAME in file_name and data_slice_name in file_name:
                    try:
                        with open(file_path, "rb") as f:
                            shap_values = pickle.load(f)
                    except Exception as e:
                        err_msg = f"Could not open file {file_path}, error message: {e}"
                        logger.warning(err_msg)
                        continue

                    # shap_values is a list of array, the number of arrays is equal to number of classes, in case of regression,
                    # there is only one array.
                    if model_type == REGRESSION_MODEL_TYPE:
                        shap_values = np.array(shap_values)
                        # The column in the array correspond to each feature and rows are samples. So we take mean across the rows
                        shaps = np.abs(shap_values).mean(0)
                        df = pd.DataFrame(np.reshape(shaps, (-1, 1)), columns=[0])
                        # This df will have 0 as column as it is regression and each row corresponds to a feature
                        dataslice_shap[data_slice_name] = df
                    else:
                        # shap_values is a list of array, the number of arrays is equal to number of classes
                        shaps = []
                        num_class = len(shap_values)
                        # The column in the array correspond to each feature and rows are samples. So we take mean across the rows
                        for ind in range(num_class):
                            global_shap_values = np.abs(shap_values[ind]).mean(0)
                            shaps.append(global_shap_values)
                        shaps = np.array(shaps)
                        df = pd.DataFrame(
                            np.reshape(shaps, (-1, shaps.shape[0])),
                            columns=list(range(num_class)),
                        )
                        # This df will have 0,1,2.. as column according to the number of classes and each row corresponds to a feature
                        dataslice_shap[data_slice_name] = df

        return dir_path, dataslice_schemas, dataslice_shap

    # @st.experimental_memo
    def plot_shap(self, dataslice_schemas, dataslice_shap):
        """
        Shap computation given the dataslice_schemas and dataslice_shap
        """
        cols = list(st.columns(2))
        if len(dataslice_shap) > 2:
            cols += list(st.columns(2))

        for i, (data_slice_name, shap_df) in enumerate(dataslice_shap.items()):
            if data_slice_name not in dataslice_schemas.keys():
                continue
            if not type(shap_df) == pd.DataFrame or shap_df.empty:
                continue
            # for each dataslice getting thre shap corresponding to the dataslice
            shap_df["Features"] = dataslice_schemas[data_slice_name][
                FEATURE_COLUMN_NAME
            ]
            shap_df = shap_df.sort_values(shap_df.columns[0])
            with cols[i]:
                st.subheader(f"Feature Importance - {data_slice_name} data")
                num_class = len(dataslice_schemas[data_slice_name])
                feature_cols = list(shap_df.columns)
                feature_cols.remove("Features")
                fig = px.bar(shap_df, y="Features", x=feature_cols, orientation="h")
                fig.update_layout(
                    xaxis_title="mean(|SHAP value|)(average impact on model output magnitude)"
                )
                st.write(fig)

    def whylogs_histogram(self, histogram):
        """
        Preprocesses the histogram data obtained from whylogs

        >>values = whylogs_histogram({'bin_edges': [37.0, 46.75000110714286, 56.500002214285715, 66.25000332142857], 'counts': [2, 3, 1]})
        >>values == [41.875000553571425, 41.875000553571425, 51.62500166071429, 51.62500166071429, 51.62500166071429, 61.37500276785714]
        True
        """
        values = []
        for i in range(len(histogram[WHYLOGS_BINEDGES]) - 1):
            value = (
                histogram[WHYLOGS_BINEDGES][i + 1] + histogram[WHYLOGS_BINEDGES][i]
            ) / 2
            values += [value] * histogram[WHYLOGS_COUNTS][i]
        return values

    def plot_categorical_feature_distribution(self, cat_feature_option, unique_counts):
        if unique_counts is None or cat_feature_option is None:
            return
        # Getting the unique count
        unique_values, unique_count = unique_counts[cat_feature_option]
        # unique_values corresponds to the unique values
        # unique_count correpons to the counts of the value
        fig = go.Figure(
            [
                go.Bar(
                    x=unique_values,
                    y=unique_count,
                    name=cat_feature_option,
                )
            ]
        )
        fig.update_layout(showlegend=True)
        st.write(fig)

    def get_features_and_cat_feature_dictribution(
        self, dir_path, features, dataslice_schemas
    ):
        """
        unique counts file example:
        {'preds': (array([0, 1]), array([1574,   93])),
        'actuals': (array([0, 1]), array([1443,  224])),
        'state_AZ': (array([0, 1]), array([1642,   25]))
        }
        Each feature contains two array, first array conrresponds to unique values in the feature,
        second array correspond to counts corresponding to the unique values

        Returns:
        numerical_feature_names
        """
        numerical_features = features
        for key in dataslice_schemas.keys():
            data_slice_name = key
            categorical_features = dataslice_schemas[key][CATEGORICAL_FEATURE_COLUMN]
            if categorical_features is not None:
                numerical_features = list(set(features) - set(categorical_features))
                break

        cat_feature_option = None
        if categorical_features is not None:
            st.subheader("Categorcal feature distribution")
            cat_feature_option = st.selectbox(
                "Categorical Feature", categorical_features, 0
            )

        unique_counts = None
        for file in os.listdir(dir_path):
            if data_slice_name in file and UNIQUE_COUNTS_FILE_NAME in file:
                with open(os.path.join(dir_path, file), "rb") as f:
                    unique_counts = pickle.load(f)

        features = {
            CATEGORICAL_FEATURE_COLUMN: cat_feature_option,
            NUMERICAL_FEATURE_COLUMN: numerical_features,
        }
        return features, unique_counts

    def plot_numerical_feature_distribution(self, numerical_features, summary_hist):
        """
        Numercial feature distribution is obtained from whyogs
        """
        st.subheader("Numerical feature distribution")
        with st.form("features availabe"):
            feature_options = st.multiselect(
                "Features", numerical_features, [numerical_features[0]]
            )
            submit_button = st.form_submit_button(label="Submit")

        if len(feature_options) == 0:
            st.warning("Please select a feature")
            return

        if not submit_button:
            return
        values_full = []
        bin_sizes = []
        for feature in feature_options:
            values = []
            for i in range(len(summary_hist[feature][WHYLOGS_BINEDGES]) - 1):
                value = (
                    summary_hist[feature][WHYLOGS_BINEDGES][i]
                    + summary_hist[feature][WHYLOGS_BINEDGES][i + 1]
                ) / 2
                values = values + [value] * summary_hist[feature][WHYLOGS_COUNTS][i]
                if i == 0:
                    bin_size = (
                        summary_hist[feature][WHYLOGS_BINEDGES][i + 1]
                        - summary_hist[feature][WHYLOGS_BINEDGES][i]
                    )
                    bin_sizes.append(bin_size)
            values_full = values_full + [values]
        fig = ff.create_distplot(
            values_full, group_labels=feature_options, bin_size=bin_sizes
        )
        fig.update_layout(width=1000, height=650)
        st.write(fig)

    def feature_histogram(self, dir_path, dataslice_schemas):
        """
        Distributin generation, includes:
        1. categorical variable distribution if any
        2. Prediction vs actuals distribution for all the dataslice available
        3. Numerical features distribution
        """
        ## Getting the whylogs histogram
        profile_summary = self.mlfoundry_data.get_whylogs_summary(
            st.session_state[ID_SESSION_STATE_MODEL_VIEW]
        )
        if profile_summary is None:
            st.warning(
                f"Stats doesn't exist for {st.session_state[ID_SESSION_STATE_MODEL_VIEW]}"
            )
            return
        summary = profile_summary["summary"]
        summary = summary.fillna("null")
        feature_names = list(summary["column"])
        summary_hist = profile_summary["hist"]
        st.header("Feature Histogram")
        ### Actuals vs predictions
        model_type = self.mlfoundry_data.get_model_type(
            st.session_state[ID_SESSION_STATE_MODEL_VIEW]
        )
        model_type_view = self.model_type_to_view_map[model_type](self.mlfoundry_data)
        model_type_view.feature_health(dir_path, dataslice_schemas)

        ### Catergorical feature distribution
        features, unique_counts = self.get_features_and_cat_feature_dictribution(
            dir_path, feature_names, dataslice_schemas
        )
        self.plot_categorical_feature_distribution(
            features[CATEGORICAL_FEATURE_COLUMN], unique_counts
        )

        ### Numerical feature distribution - from whylogs
        self.plot_numerical_feature_distribution(
            features[NUMERICAL_FEATURE_COLUMN], summary_hist
        )

    def start_tab(self, project_name, run_id, run_ids):

        result = self.get_schema_shap(run_id)
        if result is None:
            return

        dir_path, dataslice_schemas, dataslice_shap = result

        self.plot_shap(dataslice_schemas, dataslice_shap)

        self.feature_histogram(dir_path, dataslice_schemas)
