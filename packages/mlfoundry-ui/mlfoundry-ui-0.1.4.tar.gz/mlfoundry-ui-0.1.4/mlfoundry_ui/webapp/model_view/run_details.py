import logging
import os
import pickle
import shutil
import sys
from pathlib import Path

import pandas as pd
import plotly.figure_factory as ff
import streamlit as st
from mlflow.tracking import artifact_utils

from mlfoundry_ui.webapp.dashboard_constants import *

logger = logging.getLogger(__name__)


class RunDetails:
    def __init__(self, mlfoundry_data):
        self.mlfoundry_data = mlfoundry_data

    def __dict_to_dataframe(self, run_dict, key_name, value_name):
        run_dict = {
            key_name: list(run_dict.keys()),
            value_name: list(run_dict.values()),
        }
        run_df = pd.DataFrame(run_dict)
        return run_df

    def show_params(self, run):
        params_dict = run.data.params

        if len(params_dict) == 0:
            return

        params_df = self.__dict_to_dataframe(params_dict, "parameters", "values")

        # Adding red color table to match with the border
        colorscale = [[0, "#FF0000"], [0.5, "#ffffff"], [1, "#ffffff"]]
        fig = ff.create_table(params_df, colorscale=colorscale)

        st.subheader("Parameters")
        st.write(fig)

    def show_metrics(self, run):
        metrics_dict = run.data.metrics

        if len(metrics_dict) == 0:
            return

        metrics_df = self.__dict_to_dataframe(metrics_dict, "Metrics", "Values")
        metrics_df["Values"] = metrics_df["Values"].round(2)

        # Adding red color table to match with the border
        colorscale = [[0, "#FF0000"], [0.5, "#ffffff"], [1, "#ffffff"]]
        fig = ff.create_table(metrics_df, colorscale=colorscale)

        st.subheader("Metrics")
        st.write(fig)

    def is_pickle(self, filename):
        try:
            with open(filename, "rb") as f:
                pickle.load(f)
            return True
        except:
            return False

    def is_binary(self, filename):
        """
        Return true if the given filename is binary.
        """
        fin = open(filename, "rb")
        try:
            CHUNKSIZE = 1024
            while 1:
                chunk = fin.read(CHUNKSIZE)

                if "\0" in chunk:  # found null byte
                    return True

                if len(chunk) < CHUNKSIZE:
                    break  # done
        except Exception as e:
            pass
        finally:
            fin.close()
        return False

    def display_artifact(self, file_name, run_id):
        file_path = self.mlfoundry_data.get_artifact(run_id, file_name)

        st.subheader("Artifact Content")
        if self.is_binary(file_path) or self.is_pickle(file_path):
            st.warning("Chosen file is a binary file which cant be displayed")
            return
        try:
            with open(file_path, "r") as f:
                content = f.read()
            st.code(content)
        except Exception as e:
            st.warning(
                "Content from this file cannot be displayed. Maybe it is binary."
            )
            return

    def get_artifact_files(self, run_id, artifact_info):
        files = []
        for artifact in artifact_info:
            if artifact.is_dir:
                artifact_info_dir = self.mlfoundry_data.mlflow_client.list_artifacts(
                    run_id, artifact.path
                )
                file_list = self.get_artifact_files(run_id, artifact_info_dir)
                files += file_list
            else:
                files.append(artifact.path)

        return files

    def show_artifacts(self, run):

        run_id = run.info.run_id
        artifact_info = self.mlfoundry_data.mlflow_client.list_artifacts(run_id)
        artifact_files = self.get_artifact_files(run_id, artifact_info)

        if len(artifact_files) == 0:
            return

        st.subheader("Artifacts List")
        with st.container():
            artifact_to_show = st.radio("", artifact_files)

        self.display_artifact(artifact_to_show, run_id)

    def start_tab(self, run_id):
        try:
            run = self.mlfoundry_data.mlflow_client.get_run(run_id)
        except Exception as e:
            err_msg = (
                f"Not able to get run for the run_id - {run_id}. Error message: {e}"
            )
            logger.warning(err_msg)
            st.warning(err_msg)
            return

        self.show_params(run)
        self.show_metrics(run)
        self.show_artifacts(run)
