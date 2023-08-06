import logging
import os
import pickle

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import streamlit as st
from itsdangerous import exc

from mlfoundry_ui.webapp.dashboard_constants import *
from mlfoundry_ui.webapp.model_types.base_view import BaseClass

logger = logging.getLogger(__name__)


class ClassificationView(BaseClass):
    def __init__(self, mlfoundry_data):
        self.mlfoundry_data = mlfoundry_data

    @staticmethod
    def update_count_data(unique_counts, actual_col, preds_col, data_slice_name, data):
        # getting the classes available in actual column
        classes, counts = unique_counts[actual_col]
        ## For each dataslice finding the counts corresponding to classes
        for i, count in enumerate(counts):
            data.append(
                {
                    "class": f"Class {classes[i]}",  # class number
                    "count": count,  # count corresponding to the class
                    "actual_preds": TRUTH_VALUES,
                    "data_slice": data_slice_name,
                }
            )
        classes, counts = unique_counts[preds_col]
        for i, count in enumerate(counts):
            data.append(
                {
                    "class": f"Class {classes[i]}",  # class number
                    "count": count,  # count corresponding to the class
                    "actual_preds": PREDICTION_VALUES,
                    "data_slice": data_slice_name,
                }
            )

        return data

    def show_confusion_matrix(self, multi_dim_metric_dict):

        confusion_matrix_figs = {}
        for data_slice in DATA_SLICES:
            if data_slice not in multi_dim_metric_dict.keys():
                continue

            multi_dim_metrics = multi_dim_metric_dict[data_slice]
            if MULTIDIM_METRICS_CONFUSION_MATRIX in multi_dim_metrics.keys():
                matrix = multi_dim_metrics[MULTIDIM_METRICS_CONFUSION_MATRIX]
            else:
                err_msg = (
                    f"{MULTIDIM_METRICS_CONFUSION_MATRIX} key doesnt exist in {MULTIDIM_METRICS}_{data_slice}."
                    f"Either multi dimensional metrics has not been logged properly or some other error occured in log_dataset_stats"
                )
                logging.warning(err_msg)
                break

            # confusion matrix should look like  0 1 2 along columns and 0 1 2 along rows in this order.
            # So we flip it first and then create heatmap
            matrix = np.flip(matrix, 0)
            fig = ff.create_annotated_heatmap(
                matrix,
                colorscale="Viridis",
                x=[str(x) for x in list(range(len(matrix)))],
                y=[str(x) for x in list(range(len(matrix) - 1, -1, -1))],
                # If we dont reverse read here the labels in the confusion matric along y axis will be flipped.
                # Because by default labels in a plot on y axis starts from bottom left corner
            )
            fig.update_layout(xaxis_title="Predictions", yaxis_title="Actuals")
            confusion_matrix_figs[data_slice] = fig

        cols = list(st.columns(len(confusion_matrix_figs)))
        for i, (data_slice, confusion_matrix) in enumerate(
            confusion_matrix_figs.items()
        ):
            with cols[i]:
                st.subheader(f"Confusion Matrix - {data_slice}")
                st.write(confusion_matrix)

    def get_multi_dim_metric_dict(self):
        """
        Returns multi_dim_metrics as a dictionary where key corresponds to dataslice and
        value corresponds to multi_dim_metricss
        """
        dir_path = self.mlfoundry_data.get_artifact(
            st.session_state[ID_SESSION_STATE_MODEL_VIEW], MULTIDIM_METRICS
        )
        if dir_path is None:
            return None

        multi_dim_metric_dict = {}
        for file_name in os.listdir(dir_path):
            try:
                with open(os.path.join(dir_path, file_name), "rb") as f:
                    multi_dim_metrics = pickle.load(f)
            except Exception as e:
                err_msg = f"Not able to open file {os.path.join(dir_path, file_name)}. Error {e}"
                logger.warning(err_msg)
                continue

            for data_slice in DATA_SLICES:
                if data_slice not in file_name:
                    continue
                multi_dim_metric_dict[data_slice] = multi_dim_metrics

        return multi_dim_metric_dict

    def plot_actual_vs_preds_classification(self, pred_actual_df):
        if pred_actual_df is None or pred_actual_df.empty:
            return

        fig = px.bar(
            pred_actual_df,
            x="actual_preds",
            y="count",
            color="class",
            barmode="group",
            facet_row="data_slice",
        )
        fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
        fig.update_annotations(font=dict(size=20))
        fig.update_layout(showlegend=True, xaxis_title="actual/prediction")
        st.subheader("Predictions and Truth Label distribution")
        st.write(fig)

    def get_actual_vs_preds_classification(self, dir_path, dataslice_schemas):
        """
        unique counts file example:
        {'preds': (array([0, 1]), array([1574,   93])),
        'actuals': (array([0, 1]), array([1443,  224])),
        'state_AZ': (array([0, 1]), array([1642,   25]))
        }
        Each feature contains two array, first array conrresponds to unique values in the feature,
        second array correspond to counts corresponding to the unique values
        Example of unique_counts file name: 'unique_count_test.pkl'.
        The purpose of the unique_count file is to log the distribution of categorical features, actuals and predictions.
        """
        # TODO(Rizwan): unique_counts file format can be made better. change it in mlfoundry first and then here.
        data = []
        for data_slice_name in dataslice_schemas.keys():
            for file_name in os.listdir(dir_path):
                # Cheking if the file is a uniqu_count file
                if (
                    data_slice_name not in file_name
                    or UNIQUE_COUNTS_FILE_NAME not in file_name
                ):
                    continue

                try:
                    with open(os.path.join(dir_path, file_name), "rb") as f:
                        unique_counts = pickle.load(f)
                except Exception as e:
                    err_msg = f"Not able to load {file_name} for actual_vs_preds_classification. error msg: {e}"
                    logger.warning(err_msg)
                    continue

                # getting the prediction and actual column name
                preds_col, actual_col = self.get_actual_prediction_column(
                    dataslice_schemas, data_slice_name
                )
                if preds_col is None or actual_col is None:
                    continue

                data = self.update_count_data(
                    unique_counts, actual_col, preds_col, data_slice_name, data
                )

        if len(data) == 0:
            return

        pred_actual_df = pd.DataFrame(data)
        return pred_actual_df

    def get_roc(self, multi_dim_metrics):
        try:
            fpr = multi_dim_metrics[MULTIDIM_METRICS_ROC][MULTIDIM_METRICS_FPR]
            tpr = multi_dim_metrics[MULTIDIM_METRICS_ROC][MULTIDIM_METRICS_TPR]
            result_dict = {"fpr": fpr, "tpr": tpr}
            return result_dict

        except Exception as e:
            err_msg = f"Error in loading fpr, tpr. Error msg {e}"
            logger.warning(err_msg)
            return

    def get_pr(self, multi_dim_metrics):
        try:
            precision = multi_dim_metrics[MULTIDIM_METRICS_PRECISION_RECALL][
                MULTIDIM_METRICS_PRECISION
            ]
            recall = multi_dim_metrics[MULTIDIM_METRICS_PRECISION_RECALL][
                MULTIDIM_METRICS_RECALL
            ]
            result_dict = {"precision": precision, "recall": recall}
            return result_dict

        except Exception as e:
            err_msg = f"Error in loading precision, recall. Error msg {e}"
            logger.warning(err_msg)
            return

    def plot_pr(self, multi_dim_metric_dict):
        for data_slice, multi_dim_metrics in multi_dim_metric_dict.items():
            result_dict = self.get_pr(multi_dim_metrics)
            if result_dict is None:
                continue
            plot_dict = {
                "x": result_dict[MULTIDIM_METRICS_RECALL],
                "y": result_dict[MULTIDIM_METRICS_PRECISION],
                "labels": dict(x=MULTIDIM_METRICS_RECALL, y=MULTIDIM_METRICS_PRECISION),
            }

            fig = self.plot_roc_pr(plot_dict)
            st.subheader(f"PR Curve - {data_slice} data")
            st.write(fig)

    def plot_roc(self, multi_dim_metric_dict):
        for data_slice, multi_dim_metrics in multi_dim_metric_dict.items():
            result_dict = self.get_roc(multi_dim_metrics)
            if result_dict is None:
                continue
            # print(result_dict[MULTIDIM_METRICS_FPR].shape, result_dict[MULTIDIM_METRICS_TPR].shape)
            plot_dict = {
                "x": result_dict[MULTIDIM_METRICS_FPR],
                "y": result_dict[MULTIDIM_METRICS_TPR],
                "labels": dict(x="False Positive Rate", y="True Positive Rate"),
            }
            fig = self.plot_roc_pr(plot_dict)
            st.subheader(f"ROC Curve - {data_slice} data")
            st.write(fig)

    def model_health(self):
        multi_dim_metric_dict = self.get_multi_dim_metric_dict()

        if multi_dim_metric_dict is None or len(multi_dim_metric_dict) == 0:
            return

        self.show_confusion_matrix(multi_dim_metric_dict)
        self.plot_roc(multi_dim_metric_dict)
        self.plot_pr(multi_dim_metric_dict)
