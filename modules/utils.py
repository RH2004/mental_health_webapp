# utils.py

import streamlit as st
import pandas as pd
import numpy as np
import os
import base64
from io import BytesIO
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

class Utils:
    """
    A class with utility functions for the dashboard.
    """

    page_config_set = False  # Class attribute to prevent re-calling set_page_config

    @classmethod
    def set_page_config(cls):
        """
        Set the page configuration for the Streamlit app.
        Only sets once even if called multiple times.
        """
        if not cls.page_config_set:
            st.set_page_config(
                page_title="Mental Health in Tech Dashboard",
                page_icon="🧠",
                layout="wide",
                initial_sidebar_state="expanded",
            )
            cls.page_config_set = True

    @staticmethod
    def load_css():
        """
        Load custom CSS for the dashboard.
        """
        css = """
        <style>
            .main-header {
                font-size: 2.5rem;
                color: #4257B2;
                text-align: center;
                margin-bottom: 1rem;
            }

            .sub-header {
                font-size: 1.8rem;
                color: #3C9D9B;
                margin-top: 2rem;
                margin-bottom: 1rem;
            }

            .insight-box {
                background-color: #f0f2f6;
                border-radius: 10px;
                padding: 20px;
                margin-bottom: 20px;
                border-left: 5px solid #4257B2;
            }

            .metric-container {
                background-color: #ffffff;
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                padding: 20px;
                text-align: center;
                margin-bottom: 20px;
            }

            .metric-value {
                font-size: 2.5rem;
                font-weight: bold;
                color: #4257B2;
            }

            .metric-label {
                font-size: 1rem;
                color: #666666;
            }

            .stPlotlyChart {
                margin-bottom: 2rem;
            }

            @media (max-width: 768px) {
                .main-header {
                    font-size: 2rem;
                }

                .sub-header {
                    font-size: 1.5rem;
                }

                .metric-value {
                    font-size: 2rem;
                }
            }
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)

    @staticmethod
    def display_header(title, description=None):
        """
        Display a main header with optional description.
        """
        st.markdown(f'<h1 class="main-header">{title}</h1>', unsafe_allow_html=True)
        if description:
            st.markdown(f"<p style='text-align: center; margin-bottom: 2rem;'>{description}</p>", unsafe_allow_html=True)

    @staticmethod
    def display_subheader(title):
        """
        Display a stylized subheader.
        """
        st.markdown(f'<h2 class="sub-header">{title}</h2>', unsafe_allow_html=True)

    @staticmethod
    def display_metric(value, label):
        """
        Display a numerical/statistical metric.
        """
        metric_html = f"""
        <div class="metric-container">
            <div class="metric-value">{value}</div>
            <div class="metric-label">{label}</div>
        </div>
        """
        st.markdown(metric_html, unsafe_allow_html=True)

    @staticmethod
    def display_insights(insights_text):
        """
        Display insights in a visually distinct box.
        """
        st.markdown(f'<div class="insight-box">{insights_text}</div>', unsafe_allow_html=True)

    @staticmethod
    def create_download_link(df, filename, text):
        """
        Create a CSV download link from a DataFrame.
        """
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        return f'<a href="data:file/csv;base64,{b64}" download="{filename}">{text}</a>'

    @staticmethod
    def create_download_link_for_fig(fig, filename, text):
        """
        Create a PNG download link for a Plotly figure.
        """
        buffer = BytesIO()
        fig.write_image(buffer, format="png")
        buffer.seek(0)
        b64 = base64.b64encode(buffer.read()).decode()
        return f'<a href="data:image/png;base64,{b64}" download="{filename}">{text}</a>'

    @staticmethod
    def get_color_scale(n_colors, color_scheme='viridis'):
        """
        Generate a list of color hex codes from a matplotlib colormap.
        """
        cmap = plt.get_cmap(color_scheme)
        return [mcolors.rgb2hex(cmap(i / (n_colors - 1))) for i in range(n_colors)]

    @staticmethod
    def bin_age_groups(df, age_col='Age', bins=None, labels=None):
        """
        Categorize age data into defined groups.
        """
        if age_col not in df.columns:
            return df

        result_df = df.copy()

        if bins is None:
            bins = [0, 25, 35, 45, 55, 100]
        if labels is None:
            labels = ['18-24', '25-34', '35-44', '45-54', '55+']

        result_df['age_group'] = pd.cut(result_df[age_col], bins=bins, labels=labels, right=False)
        return result_df
