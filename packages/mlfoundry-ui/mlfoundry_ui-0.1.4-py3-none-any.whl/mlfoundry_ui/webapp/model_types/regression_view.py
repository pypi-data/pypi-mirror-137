import logging
import os
import pickle

import plotly.graph_objects as go
import streamlit as st
from itsdangerous import exc

from mlfoundry_ui.webapp.dashboard_constants import *
from mlfoundry_ui.webapp.model_types.base_view import BaseClass

logger = logging.getLogger(__name__)


class RegressionView(BaseClass):
    def __init__(self, mlfoundry_data) -> None:
        self.mlfoundry_data = mlfoundry_data
        pass

    @staticmethod
    def whylogs_histogram(histogram):
        """
        Preprocesses the histogram data obtained from whylogs

        >>values = whylogs_histogram({'bin_edges': [2, 4, 6, 10], 'counts': [2, 3, 1]})
        >>values == [3, 3, 5, 5, 5, 8]
        True
        """
        values = []
        for i in range(len(histogram[WHYLOGS_BINEDGES]) - 1):
            value = (
                histogram[WHYLOGS_BINEDGES][i + 1] + histogram[WHYLOGS_BINEDGES][i]
            ) / 2
            values += [value] * histogram[WHYLOGS_COUNTS][i]
        return values

    def plot_actual_vs_preds_regression(self, actual_vs_preds):
        for data_slice_name, actual_vs_pred in actual_vs_preds.items():

            predictions = actual_vs_pred[PREDICTION_COLUMN_NAME_VALUES]
            actuals = actual_vs_pred[ACTUAL_COLUMN_NAME_VALUES]
            preds_col = actual_vs_pred[PREDICTION_COLUMN_NAME]
            actual_col = actual_vs_pred[ACTUAL_COLUMN_NAME]

            st.subheader(f"Actuals vs Prediction - {data_slice_name} data")
            fig = go.Figure()
            fig.add_trace(go.Histogram(x=actuals, name=actual_col))
            fig.add_trace(go.Histogram(x=predictions, name=preds_col))
            fig.update_layout(barmode="overlay")
            fig.update_traces(opacity=0.6)
            st.write(fig)

    def get_actual_vs_preds_regression(self, dir_path, dataslice_schemas):
        if not os.path.isdir(dir_path) or dir_path is None:
            err_msg = f"{dir_path} is not a valid directory for stats."
            logger.warning(err_msg)
            return

        actual_vs_preds = {}
        for data_slice_name in dataslice_schemas.keys():
            for file_name in os.listdir(dir_path):
                if (
                    data_slice_name not in file_name
                    or UNIQUE_COUNTS_FILE_NAME not in file_name
                ):
                    continue
                try:
                    with open(os.path.join(dir_path, file_name), "rb") as f:
                        unique_counts = pickle.load(f)
                except Exception as e:
                    err_msg = f"Not able to open {os.path.join(dir_path, file_name)} for actual_vs_preds_regression. Error msg: {e}"
                    logger.warning(err_msg)
                    continue

                preds_col, actual_col = self.get_actual_prediction_column(
                    dataslice_schemas, data_slice_name
                )
                if preds_col is None or actual_col is None:
                    continue

                if ACTUAL_PREDICTION_REGRESSION not in unique_counts:
                    err_msg = f"{ACTUAL_PREDICTION_REGRESSION} not found in unique_counts for {data_slice_name} data. Make sure MLFoundry logged correctly"
                    logger.warning(err_msg)
                    continue
                if actual_col not in unique_counts[ACTUAL_PREDICTION_REGRESSION]:
                    err_msg = f"{actual_col} column doesnt have unique_counts value for {data_slice_name} data. Make sure MLFoundry logged correctly"
                    logger.warning(err_msg)
                    continue

                actual_histogram = unique_counts[ACTUAL_PREDICTION_REGRESSION][
                    actual_col
                ]
                prediction_histogram = unique_counts[ACTUAL_PREDICTION_REGRESSION][
                    preds_col
                ]

                actual_values = self.whylogs_histogram(actual_histogram)
                prediction_values = self.whylogs_histogram(prediction_histogram)

                actual_vs_preds[data_slice_name] = {
                    ACTUAL_COLUMN_NAME_VALUES: actual_values,
                    PREDICTION_COLUMN_NAME_VALUES: prediction_values,
                    ACTUAL_COLUMN_NAME: actual_col,
                    PREDICTION_COLUMN_NAME: preds_col,
                }
        return actual_vs_preds

    def model_health(self):
        pass

    def feature_health(self, dir_path, dataslice_schemas):
        actual_vs_preds = self.get_actual_vs_preds_regression(
            dir_path, dataslice_schemas
        )
        self.plot_actual_vs_preds_regression(actual_vs_preds)
