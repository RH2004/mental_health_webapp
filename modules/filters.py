import streamlit as st
import pandas as pd

class Filters:
    """
    A class to handle sidebar filters for the dashboard
    """
    
    @staticmethod
    def add_sidebar_filters(mental_health_df, stackoverflow_df):
        """
        Add sidebar filters based on the available data
        
        Parameters:
        -----------
        mental_health_df : pandas.DataFrame
            The mental health dataset
        stackoverflow_df : pandas.DataFrame
            The Stack Overflow dataset
            
        Returns:
        --------
        dict
            Dictionary of selected filter values
        """
        st.sidebar.title("Dashboard Filters")
        
        filters = {}
        
        # Country filter
        if 'Country' in mental_health_df.columns:
            countries = ['All'] + sorted(mental_health_df['Country'].unique().tolist())
            filters['country'] = st.sidebar.selectbox("Country", countries)
        
        # Age range filter
        if 'Age' in mental_health_df.columns:
            min_age = int(mental_health_df['Age'].min())
            max_age = int(mental_health_df['Age'].max())
            filters['age_range'] = st.sidebar.slider("Age Range", min_age, max_age, (min_age, max_age))
        
        # Gender filter
        if 'Gender' in mental_health_df.columns:
            genders = ['All'] + sorted(mental_health_df['Gender'].unique().tolist())
            filters['gender'] = st.sidebar.selectbox("Gender", genders)
        
        # Organization size filter
        if 'no_employees' in mental_health_df.columns:
            org_sizes = ['All'] + sorted(mental_health_df['no_employees'].unique().tolist())
            filters['org_size'] = st.sidebar.selectbox("Organization Size", org_sizes)
        
        # Remote work filter
        if 'remote_work' in mental_health_df.columns:
            remote_options = ['All'] + sorted(mental_health_df['remote_work'].unique().tolist())
            filters['remote_work'] = st.sidebar.selectbox("Remote Work", remote_options)
        
        # Tech company filter
        if 'tech_company' in mental_health_df.columns:
            tech_options = ['All'] + sorted(mental_health_df['tech_company'].unique().tolist())
            filters['tech_company'] = st.sidebar.selectbox("Tech Company", tech_options)
        
        # Employment type filter (from Stack Overflow data)
        if 'Employment' in stackoverflow_df.columns:
            employment_types = ['All'] + sorted(stackoverflow_df['Employment'].unique().tolist())
            filters['employment'] = st.sidebar.selectbox("Employment Type", employment_types)
        
        # Developer type filter (from Stack Overflow data)
        if 'DevType' in stackoverflow_df.columns:
            dev_types = ['All'] + sorted(stackoverflow_df['DevType'].unique().tolist())
            filters['dev_type'] = st.sidebar.selectbox("Developer Type", dev_types)
        
        return filters
    
    @staticmethod
    def apply_filters(df, filters):
        """
        Apply the selected filters to a dataframe
        
        Parameters:
        -----------
        df : pandas.DataFrame
            The dataframe to filter
        filters : dict
            Dictionary of filter values
            
        Returns:
        --------
        pandas.DataFrame
            The filtered dataframe
        """
        filtered_df = df.copy()
        
        # Apply country filter
        if 'country' in filters and filters['country'] != 'All' and 'Country' in filtered_df.columns:
            filtered_df = filtered_df[filtered_df['Country'] == filters['country']]
        
        # Apply age range filter
        if 'age_range' in filters and 'Age' in filtered_df.columns:
            min_age, max_age = filters['age_range']
            filtered_df = filtered_df[(filtered_df['Age'] >= min_age) & (filtered_df['Age'] <= max_age)]
        
        # Apply gender filter
        if 'gender' in filters and filters['gender'] != 'All' and 'Gender' in filtered_df.columns:
            filtered_df = filtered_df[filtered_df['Gender'] == filters['gender']]
        
        # Apply organization size filter
        if 'org_size' in filters and filters['org_size'] != 'All' and 'no_employees' in filtered_df.columns:
            filtered_df = filtered_df[filtered_df['no_employees'] == filters['org_size']]
        
        # Apply remote work filter
        if 'remote_work' in filters and filters['remote_work'] != 'All' and 'remote_work' in filtered_df.columns:
            filtered_df = filtered_df[filtered_df['remote_work'] == filters['remote_work']]
        
        # Apply tech company filter
        if 'tech_company' in filters and filters['tech_company'] != 'All' and 'tech_company' in filtered_df.columns:
            filtered_df = filtered_df[filtered_df['tech_company'] == filters['tech_company']]
        
        # Apply employment type filter
        if 'employment' in filters and filters['employment'] != 'All' and 'Employment' in filtered_df.columns:
            filtered_df = filtered_df[filtered_df['Employment'] == filters['employment']]
        
        # Apply developer type filter
        if 'dev_type' in filters and filters['dev_type'] != 'All' and 'DevType' in filtered_df.columns:
            filtered_df = filtered_df[filtered_df['DevType'] == filters['dev_type']]
        
        return filtered_df
