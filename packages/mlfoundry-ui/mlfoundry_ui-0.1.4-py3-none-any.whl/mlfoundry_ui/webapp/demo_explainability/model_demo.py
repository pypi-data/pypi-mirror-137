import logging

import streamlit as st

from mlfoundry_ui.constants import MLFOUNDRY_DOCUMENTATION_LINK

logger = logging.getLogger(__name__)


class ModelDemo:
    def __init__(self, mlfoundry_data, file_path):
        self.file_path = file_path
        self.mlfoundry_data = mlfoundry_data

    def start_tab(self, run_id):
        if self.file_path == "":
            self.file_path = self.mlfoundry_data.get_webapp_file_path(run_id)
            if self.file_path is None:
                st.info(
                    f"No webapp logged for run_id {run_id}. "
                    f"Follow tutorial at {MLFOUNDRY_DOCUMENTATION_LINK} to add webapp."
                )
                return
        try:
            with open(self.file_path, "r") as f:
                code = f.read()
            # updated_code = get_new_content_with_wide_layout(code)
            exec(code, globals())
            # exec(content)
        except Exception as e:
            err_msg = f"Cannot execute streamlit {self.file_path}. Error {e}"
            logger.warning(err_msg)
            st.warning(err_msg)
            return
