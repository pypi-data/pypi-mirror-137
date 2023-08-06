import logging
import os

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from mlfoundry_ui.webapp.dashboard_constants import *
from mlfoundry_ui.webapp.model_types.base_view import BaseClass

logger = logging.getLogger(__name__)


class TimeSeriesView(BaseClass):
    def __init__(self, mlfoundry_data) -> None:
        self.mlfoundry_data = mlfoundry_data

    def plot_actual_vs_prediction_time_series(self, actual_vs_preds):
        for data_slice_name, actual_vs_pred in actual_vs_preds.items():
            predictions = actual_vs_pred[PREDICTION_COLUMN_NAME_VALUES]
            actuals = actual_vs_pred[ACTUAL_COLUMN_NAME_VALUES]
            preds_col = actual_vs_pred[PREDICTION_COLUMN_NAME]
            actual_col = actual_vs_pred[ACTUAL_COLUMN_NAME]

            st.subheader(f"Actuals vs Prediction - {data_slice_name} data")
            fig = go.Figure()
            fig.add_trace(
                go.Scatter(
                    x=list(range(len(predictions))), y=predictions, name=preds_col
                )
            )
            fig.add_trace(
                go.Scatter(x=list(range(len(actuals))), y=actuals, name=actual_col)
            )
            fig.update_layout(showlegend=True, xaxis_title="time", yaxis_title="value")
            st.write(fig)

    def get_actual_vs_prediction_time_series(self, dir_path, dataslice_schemas):
        """
        Actual vs Prediction is plotted for the timeseries dataset
        """
        if not os.path.isdir(dir_path) or dir_path is None:
            err_msg = f"{dir_path} is not a valid directory for stats."
            logger.warning(err_msg)
            return

        actual_vs_preds = {}
        for data_slice_name in dataslice_schemas.keys():
            for file_name in os.listdir(dir_path):
                if (
                    data_slice_name not in file_name
                    or TIME_SERIES_ACTUAL_PREDS_FILE_NAME not in file_name
                ):
                    continue
                # In mlfoundry we are storing as follows: "actuals_predictions_test.parquet" for time series model
                try:
                    preds_vs_actual = pd.read_parquet(os.path.join(dir_path, file_name))
                except Exception as e:
                    err_msg = (
                        f"Not able to open {file_name} for actual_vs_prediction_time_series."
                        f"Please check if the model is timeseries or if mlfoundry has been used correctly to log_dataset_stats"
                    )
                    logger.warning(err_msg)
                    continue

                preds_col, actual_col = self.get_actual_prediction_column(
                    dataslice_schemas, data_slice_name
                )
                if preds_col is None or actual_col is None:
                    continue

                predictions = preds_vs_actual[preds_col]
                actuals = preds_vs_actual[actual_col]

                actual_vs_preds[data_slice_name] = {
                    ACTUAL_COLUMN_NAME_VALUES: actuals,
                    PREDICTION_COLUMN_NAME_VALUES: predictions,
                    ACTUAL_COLUMN_NAME: actual_col,
                    PREDICTION_COLUMN_NAME: preds_col,
                }

        return actual_vs_preds

    def model_health(self):
        pass

    def feature_health(self, dir_path, dataslice_schemas):
        actual_vs_preds = self.get_actual_vs_prediction_time_series(
            dir_path, dataslice_schemas
        )
        self.plot_actual_vs_prediction_time_series(actual_vs_preds)
