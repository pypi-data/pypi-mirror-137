import datetime

import plotly.figure_factory as ff
import plotly.graph_objects as go
import streamlit as st


class DataHealth:
    def __init__(self, mlfoundry_data):
        self.mlfoundry_data = mlfoundry_data

    def start_tab(self, run_id):

        ## Whylogs profile summary computation
        profile_summary = self.mlfoundry_data.get_whylogs_summary(run_id)

        if profile_summary is None:
            st.warning(f"Profile summary doesn't exists for run {run_id}")
            return
        summary = profile_summary["summary"]
        summary = summary.fillna("null")
        summary = summary.style.set_precision(2)

        st.subheader("Profile Summary")

        st.dataframe(summary)
