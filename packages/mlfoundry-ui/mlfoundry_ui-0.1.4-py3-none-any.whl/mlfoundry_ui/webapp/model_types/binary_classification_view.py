import logging

import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
import streamlit as st
from matplotlib.pyplot import figure
from sklearn.metrics import accuracy_score, auc

from mlfoundry_ui.webapp.dashboard_constants import *
from mlfoundry_ui.webapp.model_types.classification_view import ClassificationView

logger = logging.getLogger(__name__)


class BinaryClassificationView(ClassificationView):
    def __init__(self, mlfoundry_data):
        super().__init__(mlfoundry_data)
        self.mlfoundry_data = mlfoundry_data

    def plot_roc_pr(self, plot_dict):
        auc_score = round(auc(plot_dict["x"], plot_dict["y"]), 3)
        title = f"AUC Score: {auc_score}"
        fig = px.area(
            x=plot_dict["x"], y=plot_dict["y"], labels=plot_dict["labels"], title=title
        )
        fig.add_shape(type="line", line=dict(dash="dash"), x0=0, x1=1, y0=0, y1=1)

        return fig

    def roc_pr_helper(self, multi_dim_metric_dict):
        """Helper function to generate roc and pr curve

        Args:
            model_type (str)
            multi_dim_metric_dict (dict): multi_dim_metrics fetched from S3

        """
        for metric_name in [MULTIDIM_METRICS_ROC, MULTIDIM_METRICS_PRECISION_RECALL]:
            for data_slice, multi_dim_metrics in multi_dim_metric_dict.items():

                if metric_name == MULTIDIM_METRICS_ROC:
                    result_dict = self.get_roc(multi_dim_metrics)
                    if result_dict is None:
                        continue
                    plot_dict = {
                        "x": result_dict[MULTIDIM_METRICS_FPR],
                        "y": result_dict[MULTIDIM_METRICS_TPR],
                        "title": f"(AUC={auc(result_dict[MULTIDIM_METRICS_FPR], result_dict[MULTIDIM_METRICS_TPR]):.4f})",
                        "labels": dict(x="False Positive Rate", y="True Positive Rate"),
                    }

                elif metric_name == MULTIDIM_METRICS_PRECISION_RECALL:
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
