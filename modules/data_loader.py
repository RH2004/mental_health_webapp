import pandas as pd
import json
import os
import requests
from io import StringIO
import streamlit as st

class DataLoader:
    """
    A class to handle loading and caching data from various sources
    """

    def __init__(self, data_dir='data'):
        """
        Initialize the DataLoader with the data directory path
        """
        self.data_dir = data_dir
        self.cache_dir = os.path.join(data_dir, 'cache')

        # Ensure cache directory exists
        os.makedirs(self.cache_dir, exist_ok=True)

        # Load external sources
        self.sources_file = os.path.join(data_dir, 'external_sources.json')
        if os.path.exists(self.sources_file):
            with open(self.sources_file, 'r') as f:
                self.external_sources = json.load(f)
        else:
            self.external_sources = {}

    def load_mental_health_data(self):
        return self._load_csv_cached(os.path.join(self.data_dir, 'mental_health_cleaned.csv'))

    def load_stackoverflow_data(self):
        return self._load_csv_cached(os.path.join(self.data_dir, 'stackoverflow_cleaned.csv'))

    def load_external_data(self, source_key):
        if source_key not in self.external_sources:
            st.error(f"External source '{source_key}' not found")
            return None

        url = self.external_sources[source_key]
        cache_file = os.path.join(self.cache_dir, f"{source_key}.csv")

        # Try cached version
        if os.path.exists(cache_file):
            return self._load_csv_cached(cache_file)

        # Fetch from source
        try:
            response = requests.get(url)
            response.raise_for_status()

            try:
                df = pd.read_csv(StringIO(response.text))
                df.to_csv(cache_file, index=False)  # Cache it
                return df
            except Exception as e:
                st.error(f"Error parsing data from {url}: {str(e)}")
                return None
        except Exception as e:
            st.error(f"Error fetching data from {url}: {str(e)}")
            return None

    def get_available_sources(self):
        return list(self.external_sources.keys())

    @staticmethod
    @st.cache_data
    def _load_csv_cached(path):
        try:
            return pd.read_csv(path)
        except Exception as e:
            st.error(f"Error loading data from {path}: {str(e)}")
            return pd.DataFrame()
