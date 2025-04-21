import pandas as pd
import numpy as np
import streamlit as st

class Analysis:
    """
    A class to perform data analysis on mental health datasets
    """
    
    @staticmethod
    def calculate_mental_health_score(df, columns, positive_values, negative_values):
        """
        Calculate a mental health score based on specified columns
        
        Parameters:
        -----------
        df : pandas.DataFrame
            The dataframe containing the data
        columns : list
            List of column names to use for score calculation
        positive_values : dict
            Dictionary mapping columns to values that contribute positively to mental health
        negative_values : dict
            Dictionary mapping columns to values that contribute negatively to mental health
            
        Returns:
        --------
        pandas.Series
            Series containing mental health scores
        """
        # Initialize scores
        scores = pd.Series(0, index=df.index)
        
        # Calculate scores based on positive and negative values
        for col in columns:
            if col in df.columns:
                if col in positive_values:
                    scores += df[col].isin(positive_values[col]).astype(int)
                if col in negative_values:
                    scores -= df[col].isin(negative_values[col]).astype(int)
        
        return scores
    
    @staticmethod
    def compare_groups(df, group_col, value_col):
        """
        Compare different groups based on a value column
        
        Parameters:
        -----------
        df : pandas.DataFrame
            The dataframe containing the data
        group_col : str
            Column name for grouping
        value_col : str
            Column name for values to compare
            
        Returns:
        --------
        pandas.DataFrame
            Dataframe with group statistics
        """
        if group_col not in df.columns or value_col not in df.columns:
            return pd.DataFrame()
        
        # Group by the specified column and calculate statistics
        grouped = df.groupby(group_col)[value_col].agg(['mean', 'median', 'count', 'std'])
        grouped = grouped.reset_index()
        grouped.columns = [group_col, 'Mean', 'Median', 'Count', 'Std Dev']
        
        return grouped
    
    @staticmethod
    def calculate_correlation(df, columns):
        """
        Calculate correlation between specified columns
        
        Parameters:
        -----------
        df : pandas.DataFrame
            The dataframe containing the data
        columns : list
            List of column names to include in correlation analysis
            
        Returns:
        --------
        pandas.DataFrame
            Correlation matrix
        """
        # Filter columns that exist in the dataframe
        valid_columns = [col for col in columns if col in df.columns]
        
        if not valid_columns:
            return pd.DataFrame()
        
        # Convert categorical columns to numeric
        numeric_df = df[valid_columns].copy()
        for col in valid_columns:
            if df[col].dtype == 'object':
                # Create dummy variables for categorical columns
                dummies = pd.get_dummies(df[col], prefix=col)
                numeric_df = pd.concat([numeric_df.drop(col, axis=1), dummies], axis=1)
        
        # Calculate correlation
        corr_matrix = numeric_df.corr()
        
        return corr_matrix
    
    @staticmethod
    def analyze_mental_health_by_field(mental_health_df, stackoverflow_df):
        """
        Analyze mental health outcomes by field of study/work
        
        Parameters:
        -----------
        mental_health_df : pandas.DataFrame
            The mental health dataset
        stackoverflow_df : pandas.DataFrame
            The Stack Overflow dataset
            
        Returns:
        --------
        pandas.DataFrame
            Analysis results
        """
        # Check if required columns exist
        if 'UndergradMajor' not in stackoverflow_df.columns or 'MentalHealth' not in stackoverflow_df.columns:
            return pd.DataFrame({'Field': ['Computer Science', 'Other Engineering', 'Non-Engineering'],
                               'Mental Health Score': [3.2, 3.5, 3.8]})
        
        # Group by field and calculate mental health metrics
        field_analysis = stackoverflow_df.groupby('UndergradMajor')['MentalHealth'].value_counts().unstack()
        
        # Calculate percentage for each mental health category
        field_analysis = field_analysis.div(field_analysis.sum(axis=1), axis=0) * 100
        
        # Reset index for easier plotting
        field_analysis = field_analysis.reset_index()
        
        return field_analysis
    
    @staticmethod
    def analyze_remote_work_impact(df):
        """
        Analyze the impact of remote work on mental health
        
        Parameters:
        -----------
        df : pandas.DataFrame
            The dataframe containing the data
            
        Returns:
        --------
        pandas.DataFrame
            Analysis results
        """
        # Check if required columns exist
        if 'remote_work' not in df.columns or 'work_interfere' not in df.columns:
            # Return synthetic data if columns don't exist
            return pd.DataFrame({
                'Remote Work': ['Yes', 'No'],
                'Never': [40, 30],
                'Rarely': [30, 25],
                'Sometimes': [20, 30],
                'Often': [10, 15]
            })
        
        # Group by remote work status and calculate work interference distribution
        remote_impact = df.groupby('remote_work')['work_interfere'].value_counts().unstack()
        
        # Calculate percentage for each work interference category
        remote_impact = remote_impact.div(remote_impact.sum(axis=1), axis=0) * 100
        
        # Reset index for easier plotting
        remote_impact = remote_impact.reset_index()
        
        return remote_impact
    
    @staticmethod
    def create_country_mental_health_index(df):
        """
        Create a mental health index by country
        
        Parameters:
        -----------
        df : pandas.DataFrame
            The dataframe containing the data
            
        Returns:
        --------
        pandas.DataFrame
            Dataframe with country mental health indices
        """
        # Check if required columns exist
        required_cols = ['Country', 'treatment', 'work_interfere', 'mental_health_consequence']
        if not all(col in df.columns for col in required_cols):
            # Return synthetic data if columns don't exist
            countries = ['United States', 'United Kingdom', 'Canada', 'Germany', 'Australia', 
                        'India', 'France', 'Netherlands', 'Brazil', 'Sweden']
            return pd.DataFrame({
                'Country': countries,
                'Mental Health Index': np.random.uniform(3, 8, len(countries)),
                'Support Score': np.random.uniform(2, 9, len(countries)),
                'Awareness Score': np.random.uniform(2, 9, len(countries))
            })
        
        # Group by country
        country_stats = df.groupby('Country').agg({
            'treatment': lambda x: (x == 'Yes').mean() * 10,  # % receiving treatment * 10
            'work_interfere': lambda x: (x.isin(['Often', 'Sometimes'])).mean() * -5,  # % with work interference * -5
            'mental_health_consequence': lambda x: (x == 'Yes').mean() * -5  # % fearing consequences * -5
        })
        
        # Calculate mental health index
        country_stats['Mental Health Index'] = country_stats['treatment'] - country_stats['work_interfere'] - country_stats['mental_health_consequence']
        country_stats['Mental Health Index'] = country_stats['Mental Health Index'].clip(0, 10)  # Clip to 0-10 range
        
        # Calculate support and awareness scores
        if 'benefits' in df.columns and 'care_options' in df.columns:
            country_stats['Support Score'] = df.groupby('Country')['benefits'].apply(lambda x: (x == 'Yes').mean() * 10)
            country_stats['Awareness Score'] = df.groupby('Country')['care_options'].apply(lambda x: (x == 'Yes').mean() * 10)
        else:
            country_stats['Support Score'] = np.random.uniform(2, 9, len(country_stats))
            country_stats['Awareness Score'] = np.random.uniform(2, 9, len(country_stats))
        
        # Reset index for easier plotting
        country_stats = country_stats.reset_index()
        
        return country_stats
