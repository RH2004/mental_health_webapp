import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


# Data loading and preprocessing functions
def load_and_preprocess_mental_health_data(file_path):
    """
    Load and preprocess the mental health dataset

    Parameters:
    file_path (str): Path to the mental health CSV file

    Returns:
    pd.DataFrame: Preprocessed mental health dataframe
    """
    try:
        df = pd.read_csv(file_path)

        # Clean country names
        if 'country' in df.columns:
            df['country'] = df['country'].str.strip()
            # Replace common country name variations
            country_map = {
                'United States of America': 'United States',
                'USA': 'United States',
                'US': 'United States',
                'U.S.': 'United States',
                'UK': 'United Kingdom',
                'U.K.': 'United Kingdom',
                'The United Kingdom': 'United Kingdom'
            }
            df['country'] = df['country'].replace(country_map)

        # Clean gender data if it exists
        if 'gender' in df.columns:
            # Standardize gender terms (this is a simplified approach)
            df['gender'] = df['gender'].str.lower().str.strip()
            gender_map = {
                'male': 'Male',
                'female': 'Female',
                'm': 'Male',
                'f': 'Female',
                'non-binary': 'Non-binary',
                'non binary': 'Non-binary',
                'nonbinary': 'Non-binary'
            }
            df['gender'] = df['gender'].replace(gender_map)

        # Convert yes/no columns to standardized format
        yes_no_columns = ['treatment', 'family_history']
        for col in yes_no_columns:
            if col in df.columns:
                df[col] = df[col].str.lower().str.strip() if df[col].dtype == 'object' else df[col]
                df[col] = df[col].replace({'yes': 'Yes', 'no': 'No', 1: 'Yes', 0: 'No'})

        # Clean work_interfere column if it exists
        if 'work_interfere' in df.columns:
            df['work_interfere'] = df['work_interfere'].str.capitalize() if df['work_interfere'].dtype == 'object' else \
            df['work_interfere']
            # Replace NaN with "Not specified"
            df['work_interfere'] = df['work_interfere'].fillna('Not specified')

        return df

    except Exception as e:
        st.error(f"Error preprocessing mental health data: {e}")
        return pd.DataFrame()


def load_and_preprocess_stackoverflow_data(file_path):
    """
    Load and preprocess the Stack Overflow dataset

    Parameters:
    file_path (str): Path to the Stack Overflow CSV file

    Returns:
    pd.DataFrame: Preprocessed Stack Overflow dataframe
    """
    try:
        df = pd.read_csv(file_path)

        # Clean country names for consistency with the mental health dataset
        if 'country' in df.columns:
            df['country'] = df['country'].str.strip()
            # Replace common country name variations
            country_map = {
                'United States of America': 'United States',
                'USA': 'United States',
                'US': 'United States',
                'U.S.': 'United States',
                'UK': 'United Kingdom',
                'U.K.': 'United Kingdom',
                'The United Kingdom': 'United Kingdom'
            }
            df['country'] = df['country'].replace(country_map)

        # Convert compensation to numeric if needed
        if 'convertedcompyearly' in df.columns:
            if df['convertedcompyearly'].dtype == 'object':
                df['convertedcompyearly'] = pd.to_numeric(
                    df['convertedcompyearly'].str.replace(',', '').str.replace('$', ''), errors='coerce')

        # Handle remote work status if exists
        if 'remotework' in df.columns:
            df['remotework'] = df['remotework'].str.strip() if df['remotework'].dtype == 'object' else df['remotework']

        # Clean job satisfaction column if it exists
        if 'jobsat' in df.columns:
            if df['jobsat'].dtype == 'object':
                # Standardize job satisfaction responses
                jobsat_map = {
                    'very satisfied': 'Very Satisfied',
                    'somewhat satisfied': 'Somewhat Satisfied',
                    'neither satisfied nor dissatisfied': 'Neutral',
                    'somewhat dissatisfied': 'Somewhat Dissatisfied',
                    'very dissatisfied': 'Very Dissatisfied'
                }
                df['jobsat'] = df['jobsat'].str.lower().str.strip().replace(jobsat_map)

        return df

    except Exception as e:
        st.error(f"Error preprocessing Stack Overflow data: {e}")
        return pd.DataFrame()


# Analytics functions
def calculate_treatment_rates_by_attribute(df, attribute):
    """
    Calculate treatment rates grouped by a specific attribute

    Parameters:
    df (pd.DataFrame): Mental health dataframe
    attribute (str): Column name to group by

    Returns:
    pd.DataFrame: DataFrame with treatment rates by attribute
    """
    if attribute not in df.columns or 'treatment' not in df.columns:
        return pd.DataFrame()

    treatment_by_attr = df.groupby(attribute)['treatment'].apply(
        lambda x: (x == 'Yes').sum() / len(x) * 100
    ).reset_index()
    treatment_by_attr.columns = [attribute, 'treatment_rate']
    return treatment_by_attr


def calculate_compensation_stats_by_attribute(df, attribute):
    """
    Calculate compensation statistics grouped by a specific attribute

    Parameters:
    df (pd.DataFrame): Stack Overflow dataframe
    attribute (str): Column name to group by

    Returns:
    pd.DataFrame: DataFrame with compensation statistics by attribute
    """
    if attribute not in df.columns or 'convertedcompyearly' not in df.columns:
        return pd.DataFrame()

    comp_stats = df.groupby(attribute)['convertedcompyearly'].agg([
        ('mean', 'mean'),
        ('median', 'median'),
        ('count', 'count')
    ]).reset_index()

    return comp_stats


# Visualization helper functions
def create_color_blind_friendly_palette(n_colors):
    """
    Create a color-blind friendly color palette

    Parameters:
    n_colors (int): Number of colors needed

    Returns:
    list: List of hex color codes
    """
    # Color-blind friendly palette from ColorBrewer
    palette = [
        '#1b9e77', '#d95f02', '#7570b3', '#e7298a',
        '#66a61e', '#e6ab02', '#a6761d', '#666666'
    ]

    # If we need more colors than are in our palette, cycle through them
    if n_colors <= len(palette):
        return palette[:n_colors]
    else:
        return palette * (n_colors // len(palette) + 1)


def create_choropleth_map(df, location_col, value_col, title, color_scale='Viridis'):
    """
    Create a choropleth map

    Parameters:
    df (pd.DataFrame): DataFrame with location and value columns
    location_col (str): Column name for location
    value_col (str): Column name for values to plot
    title (str): Map title
    color_scale (str): Plotly color scale name

    Returns:
    plotly.graph_objects.Figure: Choropleth map figure
    """
    fig = px.choropleth(
        df,
        locations=location_col,
        locationmode='country names',
        color=value_col,
        title=title,
        color_continuous_scale=color_scale
    )
    fig.update_layout(
        geo=dict(
            showframe=False,
            showcoastlines=True,
            projection_type='natural earth'
        ),
        margin={"r": 0, "t": 50, "l": 0, "b": 0}
    )
    return fig


def create_accessible_bar_chart(df, x_col, y_col, color_col=None, title='', orientation='v'):
    """
    Create an accessible bar chart with color-blind friendly colors

    Parameters:
    df (pd.DataFrame): DataFrame with data
    x_col (str): Column name for x-axis
    y_col (str): Column name for y-axis
    color_col (str, optional): Column name for color grouping
    title (str): Chart title
    orientation (str): 'v' for vertical bars, 'h' for horizontal bars

    Returns:
    plotly.graph_objects.Figure: Bar chart figure
    """
    if color_col:
        n_colors = df[color_col].nunique()
        color_sequence = create_color_blind_friendly_palette(n_colors)

        fig = px.bar(
            df,
            x=x_col if orientation == 'v' else y_col,
            y=y_col if orientation == 'v' else x_col,
            color=color_col,
            title=title,
            color_discrete_sequence=color_sequence,
            orientation=orientation
        )
    else:
        fig = px.bar(
            df,
            x=x_col if orientation == 'v' else y_col,
            y=y_col if orientation == 'v' else x_col,
            title=title,
            orientation=orientation
        )

    # Add value labels on the bars
    fig.update_traces(texttemplate='%{value}', textposition='auto')

    return fig