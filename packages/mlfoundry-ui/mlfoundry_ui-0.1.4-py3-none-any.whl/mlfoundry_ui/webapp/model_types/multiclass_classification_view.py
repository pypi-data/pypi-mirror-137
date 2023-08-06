import logging

import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
import streamlit as st
from sklearn.metrics import auc

from mlfoundry_ui.webapp.dashboard_constants import *
from mlfoundry_ui.webapp.model_types.classification_view import ClassificationView

logger = logging.getLogger(__name__)


class MulticlassClassificationView(ClassificationView):
    def __init__(self, mlfoundry_data):
        super().__init__(mlfoundry_data)
        self.mlfoundry_data = mlfoundry_data

    def plot_roc_pr(self, plot_dict):
        fig = go.Figure()
        fig.add_shape(type="line", line=dict(dash="dash"), x0=0, x1=1, y0=0, y1=1)
        for i in range(len(plot_dict["x"])):
            auc_score = round(auc(plot_dict["x"][i], plot_dict["y"][i]), 3)
            name = f"Class {i} AUC={auc_score}"
            fig.add_trace(
                go.Scatter(
                    x=plot_dict["x"][i], y=plot_dict["y"][i], name=name, mode="lines"
                )
            )
        return fig

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

    def roc_pr_helper(self, multi_dim_metric_dict):
        """Helper function to generate roc and pr curve

        Args:
            model_type (str)
            multi_dim_metrics (dict): multi_dim_metrics fetched from S3

        """
        for metric_name in ["ROC", "PR"]:
            for data_slice, multi_dim_metrics in multi_dim_metric_dict.items():
                if metric_name == "ROC":
                    result_dict = self.get_roc(multi_dim_metrics)
                    if result_dict is None:
                        continue
                    plot_dict = {
                        "x": result_dict[MULTIDIM_METRICS_FPR],
                        "y": result_dict[MULTIDIM_METRICS_TPR],
                        "title": f"",
                        "labels": dict(x="False Positive Rate", y="True Positive Rate"),
                    }

                elif metric_name == "PR":
                    result_dict = self.get_pr(multi_dim_metrics)
                    if result_dict is None:
                        continue
                    plot_dict = {
                        "x": result_dict[MULTIDIM_METRICS_RECALL],
                        "y": result_dict[MULTIDIM_METRICS_PRECISION],
                        "title": f"",
                        "labels": dict(
                            x=MULTIDIM_METRICS_RECALL, y=MULTIDIM_METRICS_PRECISION
                        ),
                    }
                fig = self.plot_roc_pr(plot_dict)
                st.subheader(f"{metric_name} Curve - {data_slice} data")
                st.write(fig)

    def feature_health(self, dir_path, dataslice_schemas):
        pred_actual_df = self.get_actual_vs_preds_classification(
            dir_path, dataslice_schemas
        )
        self.plot_actual_vs_preds_classification(pred_actual_df)
