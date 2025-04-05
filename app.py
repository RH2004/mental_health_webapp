import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from plotly.subplots import make_subplots

# Set page configuration
st.set_page_config(
    page_title="Mental Health & Tech Careers Insight",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Cache the data loading to improve performance
@st.cache_data
def load_data():
    mental_health_df = pd.read_csv("data/mental_health_selected.csv")
    stackoverflow_df = pd.read_csv("data/stackoverflow_selected.csv")
    return mental_health_df, stackoverflow_df


# Helper functions for data processing
def get_age_group(age):
    if pd.isna(age):
        return "Unknown"
    age = int(age)
    if age < 25:
        return "Under 25"
    elif age < 35:
        return "25-34"
    elif age < 45:
        return "35-44"
    elif age < 55:
        return "45-54"
    else:
        return "55+"


def add_sidebar_filters(mental_health_df, stackoverflow_df):
    st.sidebar.title("Data Source")
    data_source = st.sidebar.radio(
        "Select data source:",
        ["Mental Health", "Stack Overflow", "Both"]
    )

    # Get list of countries from both datasets
    mh_countries = mental_health_df['country'].dropna().unique().tolist()
    so_countries = stackoverflow_df['country'].dropna().unique().tolist()
    all_countries = sorted(list(set(mh_countries + so_countries)))

    st.sidebar.title("Filters")

    # Country filter
    selected_countries = st.sidebar.multiselect(
        "Select Countries:",
        all_countries,
        default=["United States", "United Kingdom", "Canada", "Germany", "India"][:3]
    )

    # Age group filter
    age_groups = ["Under 25", "25-34", "35-44", "45-54", "55+"]
    selected_age_groups = st.sidebar.multiselect(
        "Select Age Groups:",
        age_groups,
        default=age_groups
    )

    # Gender filter (only for mental health dataset)
    if data_source in ["Mental Health", "Both"]:
        genders = mental_health_df['gender'].dropna().unique().tolist()
        selected_genders = st.sidebar.multiselect(
            "Select Genders:",
            genders,
            default=genders[:3] if len(genders) > 3 else genders
        )
    else:
        selected_genders = None

    # Employment type (only for Stack Overflow dataset)
    if data_source in ["Stack Overflow", "Both"]:
        employment_types = stackoverflow_df['employment'].dropna().unique().tolist()
        selected_employment = st.sidebar.multiselect(
            "Select Employment Types:",
            employment_types,
            default=employment_types[:3] if len(employment_types) > 3 else employment_types
        )

        # Remote work filter
        remote_options = stackoverflow_df['remotework'].dropna().unique().tolist()
        selected_remote = st.sidebar.multiselect(
            "Remote Work:",
            remote_options,
            default=remote_options
        )
    else:
        selected_employment = None
        selected_remote = None

    return {
        'data_source': data_source,
        'countries': selected_countries,
        'age_groups': selected_age_groups,
        'genders': selected_genders,
        'employment': selected_employment,
        'remote': selected_remote
    }


def filter_data(df, filters, dataset_type):
    filtered_df = df.copy()

    # Filter by country if selected
    if filters['countries'] and len(filters['countries']) > 0:
        filtered_df = filtered_df[filtered_df['country'].isin(filters['countries'])]

    # Apply age group filter
    if 'age' in filtered_df.columns:
        filtered_df['age_group'] = filtered_df['age'].apply(get_age_group)
        if filters['age_groups'] and len(filters['age_groups']) > 0:
            filtered_df = filtered_df[filtered_df['age_group'].isin(filters['age_groups'])]

    # Apply dataset-specific filters
    if dataset_type == 'mental_health' and filters['genders'] and len(filters['genders']) > 0:
        filtered_df = filtered_df[filtered_df['gender'].isin(filters['genders'])]

    if dataset_type == 'stackoverflow':
        if filters['employment'] and len(filters['employment']) > 0:
            filtered_df = filtered_df[filtered_df['employment'].isin(filters['employment'])]

        if filters['remote'] and len(filters['remote']) > 0:
            filtered_df = filtered_df[filtered_df['remotework'].isin(filters['remote'])]

    return filtered_df


def create_dashboard_overview(mental_health_df, stackoverflow_df, filters):
    st.header("🧠💼 Mental Health & Tech Careers Insight")

    # Introduction
    st.markdown("""
    This dashboard provides insights into mental health in the tech industry alongside career metrics.
    Data is sourced from the OSMI Mental Health in Tech survey and the Stack Overflow Developer Survey.

    Use the sidebar filters to explore different segments of the data.
    """)

    # Dataset summaries
    col1, col2, col3 = st.columns(3)

    # Display different metrics based on selected data source
    if filters['data_source'] in ["Mental Health", "Both"]:
        filtered_mh = filter_data(mental_health_df, filters, 'mental_health')
        col1.metric("Mental Health Survey Respondents", f"{len(filtered_mh):,}")
        col2.metric("Countries Represented (MH)", f"{filtered_mh['country'].nunique():,}")
        col3.metric("Received Treatment", f"{filtered_mh['treatment'].value_counts().get('Yes', 0):,}")

    if filters['data_source'] in ["Stack Overflow", "Both"]:
        filtered_so = filter_data(stackoverflow_df, filters, 'stackoverflow')
        if filters['data_source'] == "Stack Overflow":
            col1.metric("Stack Overflow Survey Respondents", f"{len(filtered_so):,}")
            col2.metric("Countries Represented (SO)", f"{filtered_so['country'].nunique():,}")
            avg_comp = filtered_so['convertedcompyearly'].dropna().mean()
            col3.metric("Avg. Annual Compensation", f"${avg_comp:,.2f}")
        else:  # Both datasets
            st.markdown("---")
            st.subheader("Stack Overflow Survey Statistics")
            col4, col5, col6 = st.columns(3)
            col4.metric("Stack Overflow Survey Respondents", f"{len(filtered_so):,}")
            col5.metric("Countries Represented (SO)", f"{filtered_so['country'].nunique():,}")
            avg_comp = filtered_so['convertedcompyearly'].dropna().mean()
            col6.metric("Avg. Annual Compensation", f"${avg_comp:,.2f}")


def create_mh_visualizations(mental_health_df, filters):
    filtered_df = filter_data(mental_health_df, filters, 'mental_health')

    st.subheader("Mental Health in Tech Insights")

    col1, col2 = st.columns(2)

    # Pie chart: Treatment vs. No Treatment
    with col1:
        treatment_counts = filtered_df['treatment'].value_counts().reset_index()
        treatment_counts.columns = ['Treatment', 'Count']

        fig_pie = px.pie(
            treatment_counts,
            values='Count',
            names='Treatment',
            title='Mental Health Treatment Distribution',
            color_discrete_sequence=px.colors.sequential.Viridis,
            hole=0.4
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)

    # Bar chart: Work Interference vs. Mental Health Treatment
    with col2:
        work_interfere_treatment = filtered_df.groupby(['work_interfere', 'treatment']).size().reset_index()
        work_interfere_treatment.columns = ['Work Interference', 'Treatment', 'Count']

        fig_bar = px.bar(
            work_interfere_treatment,
            x='Work Interference',
            y='Count',
            color='Treatment',
            title='Work Interference by Treatment Status',
            color_discrete_sequence=px.colors.sequential.Viridis
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    col3, col4 = st.columns(2)

    # Grouped bar chart: Family History vs. Treatment
    with col3:
        family_treatment = filtered_df.groupby(['family_history', 'treatment']).size().reset_index()
        family_treatment.columns = ['Family History', 'Treatment', 'Count']

        fig_grouped = px.bar(
            family_treatment,
            x='Family History',
            y='Count',
            color='Treatment',
            barmode='group',
            title='Family History of Mental Health vs. Treatment',
            color_discrete_sequence=px.colors.sequential.Viridis
        )
        st.plotly_chart(fig_grouped, use_container_width=True)

    # Map chart: Country-wise mental health response statistics
    with col4:
        country_treatment = filtered_df.groupby('country')['treatment'].apply(
            lambda x: (x == 'Yes').sum() / len(x)
        ).reset_index()
        country_treatment.columns = ['country', 'treatment_rate']
        country_treatment['treatment_rate'] = country_treatment['treatment_rate'] * 100

        fig_map = px.choropleth(
            country_treatment,
            locations='country',
            locationmode='country names',
            color='treatment_rate',
            title='Mental Health Treatment Rate by Country (%)',
            color_continuous_scale='Viridis',
            range_color=[0, 100]
        )
        fig_map.update_layout(geo=dict(showframe=False, showcoastlines=True))
        st.plotly_chart(fig_map, use_container_width=True)


def create_so_visualizations(stackoverflow_df, filters):
    filtered_df = filter_data(stackoverflow_df, filters, 'stackoverflow')

    st.subheader("Tech Career Insights")

    col1, col2 = st.columns(2)

    # Boxplot: Age vs. Compensation
    with col1:
        # Add age group to filtered df if not already there
        if 'age_group' not in filtered_df.columns:
            filtered_df['age_group'] = filtered_df['age'].apply(get_age_group)

        # Filter out outliers for visualization
        q1 = filtered_df['convertedcompyearly'].quantile(0.05)
        q3 = filtered_df['convertedcompyearly'].quantile(0.95)
        iqr = q3 - q1
        df_no_outliers = filtered_df[(filtered_df['convertedcompyearly'] >= q1 - 1.5 * iqr) &
                                     (filtered_df['convertedcompyearly'] <= q3 + 1.5 * iqr)]

        fig_box = px.box(
            df_no_outliers,
            x='age_group',
            y='convertedcompyearly',
            title='Compensation Distribution by Age Group',
            color='age_group',
            labels={'convertedcompyearly': 'Annual Compensation (USD)', 'age_group': 'Age Group'},
            color_discrete_sequence=px.colors.sequential.Viridis
        )
        st.plotly_chart(fig_box, use_container_width=True)

    # Bar chart: Job Satisfaction by Employment Type
    with col2:
        job_sat_employment = filtered_df.groupby(['employment', 'jobsat']).size().reset_index()
        job_sat_employment.columns = ['Employment Type', 'Job Satisfaction', 'Count']

        fig_bar = px.bar(
            job_sat_employment,
            x='Employment Type',
            y='Count',
            color='Job Satisfaction',
            title='Job Satisfaction by Employment Type',
            color_discrete_sequence=px.colors.sequential.Viridis
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    col3, col4 = st.columns(2)

    # Map chart: Country-wise compensation distribution
    with col3:
        country_comp = filtered_df.groupby('country')['convertedcompyearly'].mean().reset_index()

        fig_map = px.choropleth(
            country_comp,
            locations='country',
            locationmode='country names',
            color='convertedcompyearly',
            title='Average Annual Compensation by Country (USD)',
            color_continuous_scale='Viridis'
        )
        fig_map.update_layout(geo=dict(showframe=False, showcoastlines=True))
        st.plotly_chart(fig_map, use_container_width=True)

    # Remote work vs Job Satisfaction
    with col4:
        remote_jobsat = filtered_df.groupby(['remotework', 'jobsat']).size().reset_index()
        remote_jobsat.columns = ['Remote Work', 'Job Satisfaction', 'Count']

        fig_remote = px.bar(
            remote_jobsat,
            x='Remote Work',
            y='Count',
            color='Job Satisfaction',
            title='Job Satisfaction by Remote Work Status',
            color_discrete_sequence=px.colors.sequential.Viridis
        )
        st.plotly_chart(fig_remote, use_container_width=True)


def create_comparison_panel(mental_health_df, stackoverflow_df, filters):
    if filters['data_source'] != "Both":
        return

    st.header("Comparison Panel")
    st.markdown("Compare mental health metrics with career and compensation data.")

    # Filter datasets
    mh_filtered = filter_data(mental_health_df, filters, 'mental_health')
    so_filtered = filter_data(stackoverflow_df, filters, 'stackoverflow')

    # Add age group if not already added
    if 'age_group' not in mh_filtered.columns:
        mh_filtered['age_group'] = mh_filtered['age'].apply(get_age_group)

    if 'age_group' not in so_filtered.columns:
        so_filtered['age_group'] = so_filtered['age'].apply(get_age_group)

    # Get common countries for comparison
    common_countries = set(mh_filtered['country'].unique()).intersection(set(so_filtered['country'].unique()))

    # Only show comparison if there are common countries
    if len(common_countries) == 0:
        st.warning("No common countries in the filtered datasets to show comparison.")
        return

    selected_comparison = st.selectbox(
        "Select comparison type:",
        ["Country", "Age Group"]
    )

    if selected_comparison == "Country":
        selected_entity = st.selectbox("Select Country:", sorted(list(common_countries)))

        # Filter for selected country
        mh_country = mh_filtered[mh_filtered['country'] == selected_entity]
        so_country = so_filtered[so_filtered['country'] == selected_entity]

        col1, col2 = st.columns(2)

        # Mental health metrics
        with col1:
            st.subheader(f"Mental Health Metrics - {selected_entity}")

            # Treatment distribution
            treatment_counts = mh_country['treatment'].value_counts().reset_index()
            treatment_counts.columns = ['Treatment', 'Count']

            fig_treatment = px.pie(
                treatment_counts,
                values='Count',
                names='Treatment',
                title=f'Treatment Distribution in {selected_entity}',
                color_discrete_sequence=px.colors.sequential.Viridis
            )
            st.plotly_chart(fig_treatment, use_container_width=True)

        # Career metrics
        with col2:
            st.subheader(f"Career Metrics - {selected_entity}")

            # Job satisfaction distribution
            if 'jobsat' in so_country.columns:
                jobsat_counts = so_country['jobsat'].value_counts().reset_index()
                jobsat_counts.columns = ['Job Satisfaction', 'Count']

                fig_jobsat = px.pie(
                    jobsat_counts,
                    values='Count',
                    names='Job Satisfaction',
                    title=f'Job Satisfaction in {selected_entity}',
                    color_discrete_sequence=px.colors.sequential.Viridis
                )
                st.plotly_chart(fig_jobsat, use_container_width=True)

    elif selected_comparison == "Age Group":
        age_groups = sorted(
            list(set(mh_filtered['age_group'].unique()).intersection(set(so_filtered['age_group'].unique()))))

        if not age_groups:
            st.warning("No common age groups in the filtered datasets.")
            return

        selected_entity = st.selectbox("Select Age Group:", age_groups)

        # Filter for selected age group
        mh_age = mh_filtered[mh_filtered['age_group'] == selected_entity]
        so_age = so_filtered[so_filtered['age_group'] == selected_entity]

        col1, col2 = st.columns(2)

        # Mental health metrics
        with col1:
            st.subheader(f"Mental Health Metrics - {selected_entity}")

            # Work interference distribution
            if 'work_interfere' in mh_age.columns:
                work_counts = mh_age['work_interfere'].value_counts().reset_index()
                work_counts.columns = ['Work Interference', 'Count']

                fig_work = px.bar(
                    work_counts,
                    x='Work Interference',
                    y='Count',
                    title=f'Work Interference in {selected_entity} Age Group',
                    color_discrete_sequence=px.colors.sequential.Viridis
                )
                st.plotly_chart(fig_work, use_container_width=True)

        # Career metrics
        with col2:
            st.subheader(f"Career Metrics - {selected_entity}")

            # Average compensation
            if 'convertedcompyearly' in so_age.columns:
                avg_comp = so_age['convertedcompyearly'].mean()
                median_comp = so_age['convertedcompyearly'].median()

                fig = go.Figure()
                fig.add_trace(go.Indicator(
                    mode="number+delta",
                    value=avg_comp,
                    number={'prefix': "$", "valueformat": ",.2f"},
                    title={
                        "text": f"Average Compensation<br><span style='font-size:0.8em;'>Age Group: {selected_entity}</span>"},
                    delta={'reference': median_comp, 'relative': True},
                    domain={'x': [0, 1], 'y': [0, 1]}
                ))
                st.plotly_chart(fig, use_container_width=True)


def main():
    # Load data
    try:
        mental_health_df, stackoverflow_df = load_data()
    except Exception as e:
        st.error(f"Error loading data: {e}")
        st.warning("Please ensure the data files are in the 'data' directory.")
        return

    # Create sidebar filters
    filters = add_sidebar_filters(mental_health_df, stackoverflow_df)

    # Create dashboard sections based on selected data source
    create_dashboard_overview(mental_health_df, stackoverflow_df, filters)

    st.markdown("---")

    # Create visualizations based on selected data source
    if filters['data_source'] in ["Mental Health", "Both"]:
        create_mh_visualizations(mental_health_df, filters)

    if filters['data_source'] in ["Stack Overflow", "Both"]:
        create_so_visualizations(stackoverflow_df, filters)

    # Create comparison panel if both datasets are selected
    if filters['data_source'] == "Both":
        st.markdown("---")
        create_comparison_panel(mental_health_df, stackoverflow_df, filters)

    # Footer
    st.markdown("---")
    st.markdown("""
    **About this project:**
    This dashboard was created to help understand the relationship between mental health and career metrics in the tech industry.
    Data is sourced from the OSMI Mental Health in Tech survey and the Stack Overflow Developer Survey.
    """)


if __name__ == "__main__":
    main()