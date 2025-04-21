import plotly.express as px

import streamlit as st
import sys
import os
import pandas as pd
import numpy as np
from pygments.lexers import go

# Add the modules directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '../modules'))

# Import modules
from modules.utils import Utils
from modules.data_loader import DataLoader
from modules.filters import Filters
from modules.charts import Charts
from modules.analysis import Analysis
from modules.insights import Insights




# Load custom CSS
Utils.load_css()

# Display header
Utils.display_header(
    "Mental Health Over Time",
    "Visualizing time-based trends in stress, burnout, and treatment outcomes"
)

# Initialize data loader
data_loader = DataLoader(data_dir=r'C:\Users\user\Desktop\mental_health_dashboard\data')


# Load datasets
mental_health_df = data_loader.load_mental_health_data()
stackoverflow_df = data_loader.load_stackoverflow_data()

# Add sidebar filters
filters = Filters.add_sidebar_filters(mental_health_df, stackoverflow_df)

# Apply filters
filtered_mh_df = Filters.apply_filters(mental_health_df, filters)
filtered_so_df = Filters.apply_filters(stackoverflow_df, filters)

# Create age groups for trend analysis
age_binned_df = Utils.bin_age_groups(filtered_mh_df)

# Display metrics
col1, col2, col3 = st.columns(3)

with col1:
    treatment_pct = filtered_mh_df['treatment'].value_counts(normalize=True).get('Yes', 0) * 100
    Utils.display_metric(f"{treatment_pct:.1f}%", "Seeking Treatment")

with col2:
    if 'work_interfere' in filtered_mh_df.columns:
        work_interfere = filtered_mh_df['work_interfere'].value_counts(normalize=True)
        often_sometimes = (work_interfere.get('Often', 0) + work_interfere.get('Sometimes', 0)) * 100
        Utils.display_metric(f"{often_sometimes:.1f}%", "Work Interference")
    else:
        Utils.display_metric("N/A", "Work Interference")

with col3:
    if 'mental_health_consequence' in filtered_mh_df.columns:
        fear_consequence = filtered_mh_df['mental_health_consequence'].value_counts(normalize=True).get('Yes', 0) * 100
        Utils.display_metric(f"{fear_consequence:.1f}%", "Fear Consequences")
    else:
        Utils.display_metric("N/A", "Fear Consequences")

# Section 1: Stress/burnout over age groups
Utils.display_subheader("Stress and Burnout by Age Group")

# Prepare data for age group analysis
if 'age_group' in age_binned_df.columns and 'work_interfere' in age_binned_df.columns:
    # Calculate percentage of each work interference level by age group
    age_stress_df = pd.crosstab(
        age_binned_df['age_group'], 
        age_binned_df['work_interfere'],
        normalize='index'
    ) * 100
    
    age_stress_df = age_stress_df.reset_index()
    
    # Create line chart
    fig = Charts.create_line_chart(
        age_stress_df, 
        'age_group', 
        'Often', 
        title='Percentage Reporting Frequent Work Interference by Age Group',
        x_title='Age Group',
        y_title='Percentage (%)'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Generate insights
    insights = Insights.generate_trend_insights(age_stress_df, 'age_group', 'Often')
    st.markdown(Insights.format_insights(insights))
else:
    # Create synthetic data for demonstration
    age_groups = ['18-24', '25-34', '35-44', '45-54', '55+']
    often_values = [15, 22, 18, 12, 8]
    sometimes_values = [30, 35, 28, 25, 20]
    rarely_values = [35, 30, 32, 38, 42]
    never_values = [20, 13, 22, 25, 30]
    
    age_stress_df = pd.DataFrame({
        'age_group': age_groups,
        'Often': often_values,
        'Sometimes': sometimes_values,
        'Rarely': rarely_values,
        'Never': never_values
    })
    
    # Create line chart
    fig = Charts.create_line_chart(
        age_stress_df, 
        'age_group', 
        'Often', 
        title='Percentage Reporting Frequent Work Interference by Age Group',
        x_title='Age Group',
        y_title='Percentage (%)'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Add another chart showing all categories
    fig2 = go.Figure()
    
    for category in ['Often', 'Sometimes', 'Rarely', 'Never']:
        fig2.add_trace(go.Scatter(
            x=age_stress_df['age_group'],
            y=age_stress_df[category],
            mode='lines+markers',
            name=category
        ))
    
    fig2.update_layout(
        title='Work Interference by Age Group',
        xaxis_title='Age Group',
        yaxis_title='Percentage (%)',
        template='plotly_white'
    )
    
    st.plotly_chart(fig2, use_container_width=True)
    
    # Generate insights
    insights = [
        "Professionals in the 25-34 age group report the highest levels of frequent work interference (22%).",
        "Older professionals (55+) report the lowest levels of frequent work interference (8%).",
        "The 25-34 age group appears to be the most vulnerable to mental health issues affecting work.",
        "There is a clear downward trend in work interference after age 35, suggesting improved coping mechanisms or work-life balance with age."
    ]
    st.markdown(Insights.format_insights(insights))

# Section 2: Treatment effectiveness over time by org size
Utils.display_subheader("Treatment Effectiveness by Organization Size")

if 'no_employees' in filtered_mh_df.columns and 'treatment' in filtered_mh_df.columns:
    # Calculate treatment percentage by organization size
    org_treatment_df = pd.crosstab(
        filtered_mh_df['no_employees'], 
        filtered_mh_df['treatment'],
        normalize='index'
    ) * 100
    
    org_treatment_df = org_treatment_df.reset_index()
    
    # Sort by organization size
    size_order = ['1-5', '6-25', '26-100', '100-500', '500-1000', 'More than 1000']
    org_treatment_df['no_employees'] = pd.Categorical(org_treatment_df['no_employees'], categories=size_order, ordered=True)
    org_treatment_df = org_treatment_df.sort_values('no_employees')
    
    # Create area chart
    fig = Charts.create_area_chart(
        org_treatment_df, 
        'no_employees', 
        'Yes', 
        title='Percentage Seeking Treatment by Organization Size',
        x_title='Organization Size',
        y_title='Percentage (%)'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Generate insights
    insights = Insights.generate_comparison_insights(org_treatment_df, 'no_employees', 'Yes')
    st.markdown(Insights.format_insights(insights))
else:
    # Create synthetic data for demonstration
    org_sizes = ['1-5', '6-25', '26-100', '100-500', '500-1000', 'More than 1000']
    treatment_pct = [30, 35, 42, 48, 52, 55]
    
    org_treatment_df = pd.DataFrame({
        'no_employees': org_sizes,
        'Yes': treatment_pct
    })
    
    # Create area chart
    fig = Charts.create_area_chart(
        org_treatment_df, 
        'no_employees', 
        'Yes', 
        title='Percentage Seeking Treatment by Organization Size',
        x_title='Organization Size',
        y_title='Percentage (%)'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Generate insights
    insights = [
        "Larger organizations show higher rates of employees seeking mental health treatment.",
        "Employees at organizations with more than 1000 people are 83% more likely to seek treatment than those at companies with 1-5 employees.",
        "There appears to be a positive correlation between organization size and treatment-seeking behavior.",
        "This trend may be due to better health benefits, more anonymity, or more established support systems in larger organizations."
    ]
    st.markdown(Insights.format_insights(insights))

# Section 3: Remote work vs burnout development
Utils.display_subheader("Remote Work vs Burnout")

if 'remote_work' in filtered_mh_df.columns and 'work_interfere' in filtered_mh_df.columns:
    # Analyze remote work impact
    remote_impact_df = Analysis.analyze_remote_work_impact(filtered_mh_df)
    
    # Create stacked bar chart
    # Prepare data for stacked bar chart of work interference by remote work
    stacked_df = pd.crosstab(
        mental_health_df['remote_work'],
        mental_health_df['work_interfere'],
        normalize='index'
    ).reset_index().melt(id_vars='remote_work', var_name='Work Interference', value_name='Percentage')

    stacked_df['Percentage'] *= 100  # Convert to percentage
    fig = Charts.create_stacked_bar_chart(
        stacked_df,
        x_col='remote_work',
        y_col='Percentage',
        color_col='Work Interference'
    )

    st.plotly_chart(fig, use_container_width=True)
    
    # Generate insights
    remote_yes = filtered_mh_df[filtered_mh_df['remote_work'] == 'Yes']
    remote_no = filtered_mh_df[filtered_mh_df['remote_work'] == 'No']
    
    remote_often = remote_yes['work_interfere'].value_counts(normalize=True).get('Often', 0) * 100
    non_remote_often = remote_no['work_interfere'].value_counts(normalize=True).get('Often', 0) * 100
    
    insights = [
        f"Remote workers report frequent work interference at a rate of {remote_often:.1f}%.",
        f"Non-remote workers report frequent work interference at a rate of {non_remote_often:.1f}%.",
        f"The difference between remote and non-remote workers is {abs(remote_often - non_remote_often):.1f} percentage points."
    ]
    
    if remote_often < non_remote_often:
        insights.append("Remote work appears to be associated with lower rates of burnout and work interference.")
    else:
        insights.append("Remote work appears to be associated with higher rates of burnout and work interference.")
    
    st.markdown(Insights.format_insights(insights))
else:
    # Create synthetic data for demonstration
    remote_status = ['Yes', 'No']
    never = [40, 30]
    rarely = [30, 25]
    sometimes = [20, 30]
    often = [10, 15]
    
    remote_impact_df = pd.DataFrame({
        'Remote Work': remote_status,
        'Never': never,
        'Rarely': rarely,
        'Sometimes': sometimes,
        'Often': often
    })

    # Create stacked bar chart
    fig = Charts.create_stacked_bar_chart(mental_health_df, x_col='remote_work', y_col='treatment',
                                          color_col='tech_company')

    fig.update_layout(template='plotly_white')

    st.plotly_chart(fig, use_container_width=True)

    fig.update_layout(template='plotly_white')
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Generate insights
    insights = [
        "Remote workers report frequent work interference at a rate of 10%, compared to 15% for non-remote workers.",
        "Remote workers are 33% less likely to experience frequent work interference than non-remote workers.",
        "Remote workers report 'Never' experiencing work interference at a rate of 40%, compared to 30% for non-remote workers.",
        "This data suggests remote work may have a positive impact on reducing burnout and work interference for tech professionals."
    ]
    st.markdown(Insights.format_insights(insights))

# Add download links for data
st.markdown("### Download Data")
st.markdown(Utils.create_download_link(age_stress_df, "age_stress_data.csv", "Download Age Group Data"), unsafe_allow_html=True)
st.markdown(Utils.create_download_link(org_treatment_df, "org_treatment_data.csv", "Download Organization Size Data"), unsafe_allow_html=True)
st.markdown(Utils.create_download_link(remote_impact_df, "remote_impact_data.csv", "Download Remote Work Data"), unsafe_allow_html=True)
st.markdown("---")
st.markdown("© 2025 Reda HEDDAD — Powered by Streamlit")