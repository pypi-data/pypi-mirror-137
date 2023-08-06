import logging

from mlfoundry_ui.webapp.dashboard_constants import *

logger = logging.getLogger(__name__)


class BaseClass:
    def __init__(self):
        pass

    def get_actual_prediction_column(self, dataslice_schemas, data_slice_name):
        if data_slice_name not in dataslice_schemas:
            return None, None

        if PREDICTION_COLUMN_NAME not in dataslice_schemas[data_slice_name]:
            err_msg = f"{PREDICTION_COLUMN_NAME} not present in schema of {data_slice_name} data. Please use mlfoundry to log schema correctly"
            logger.warning(err_msg)
            return None, None

        preds_col = dataslice_schemas[data_slice_name][PREDICTION_COLUMN_NAME]

        if ACTUAL_COLUMN_NAME not in dataslice_schemas[data_slice_name]:
            err_msg = f"{ACTUAL_COLUMN_NAME} not present in schema of {data_slice_name} data. Please use mlfoundry to log schema correctly"
            logger.warning(err_msg)
            return None, None

        actual_col = dataslice_schemas[data_slice_name][ACTUAL_COLUMN_NAME]

        return actual_col, preds_col
