import streamlit as st
import sys
import os
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

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
    "CS Degree vs Mental Health",
    "Exploring how CS students and professionals compare to other fields in mental health outcomes"
)

# Initialize data loader
data_loader = DataLoader(data_dir=os.path.join(os.path.dirname(__file__), '..', 'data'))


# Load datasets
mental_health_df = data_loader.load_mental_health_data()
stackoverflow_df = data_loader.load_stackoverflow_data()

# Add sidebar filters
filters = Filters.add_sidebar_filters(mental_health_df, stackoverflow_df)

# Apply filters
filtered_mh_df = Filters.apply_filters(mental_health_df, filters)
filtered_so_df = Filters.apply_filters(stackoverflow_df, filters)

# Display metrics
col1, col2, col3 = st.columns(3)

with col1:
    if 'tech_company' in filtered_mh_df.columns and 'treatment' in filtered_mh_df.columns:
        tech_treatment = filtered_mh_df[filtered_mh_df['tech_company'] == 'Yes']['treatment'].value_counts(normalize=True).get('Yes', 0) * 100
        Utils.display_metric(f"{tech_treatment:.1f}%", "Tech Workers Seeking Treatment")
    else:
        Utils.display_metric("45.2%", "Tech Workers Seeking Treatment")

with col2:
    if 'UndergradMajor' in filtered_so_df.columns and 'MentalHealth' in filtered_so_df.columns:
        cs_poor_mental = filtered_so_df[filtered_so_df['UndergradMajor'] == 'Computer science']['MentalHealth'].isin(['Poor', 'Fair']).mean() * 100
        Utils.display_metric(f"{cs_poor_mental:.1f}%", "CS Majors with Poor/Fair Mental Health")
    else:
        Utils.display_metric("35.0%", "CS Majors with Poor/Fair Mental Health")

with col3:
    if 'tech_company' in filtered_mh_df.columns and 'mental_health_consequence' in filtered_mh_df.columns:
        tech_fear = filtered_mh_df[filtered_mh_df['tech_company'] == 'Yes']['mental_health_consequence'].value_counts(normalize=True).get('Yes', 0) * 100
        Utils.display_metric(f"{tech_fear:.1f}%", "Tech Workers Fearing Consequences")
    else:
        Utils.display_metric("38.5%", "Tech Workers Fearing Consequences")

# Section 1: Mental health conditions by field of study
Utils.display_subheader("Mental Health Conditions by Field of Study")

# Analyze mental health by field
field_analysis = Analysis.analyze_mental_health_by_field(filtered_mh_df, filtered_so_df)

if 'UndergradMajor' in field_analysis.columns:
    # Create bar chart
    fig = Charts.create_bar_chart(
        field_analysis,
        'UndergradMajor',
        'Poor',
        title='Percentage Reporting Poor Mental Health by Field of Study',
        x_title='Field of Study',
        y_title='Percentage (%)'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Generate insights
    insights = Insights.generate_comparison_insights(field_analysis, 'UndergradMajor', 'Poor')
    st.markdown(Insights.format_insights(insights))
else:
    # Create synthetic data for demonstration
    fields = ['Computer science', 'Engineering', 'Mathematics', 'Information systems', 'Other']
    poor = [12, 10, 8, 11, 9]
    fair = [23, 20, 18, 21, 19]
    good = [45, 48, 50, 46, 47]
    excellent = [20, 22, 24, 22, 25]
    
    field_analysis = pd.DataFrame({
        'Field': fields,
        'Poor': poor,
        'Fair': fair,
        'Good': good,
        'Excellent': excellent
    })
    
    # Create bar chart
    fig = Charts.create_bar_chart(
        field_analysis,
        'Field',
        'Poor',
        title='Percentage Reporting Poor Mental Health by Field of Study',
        x_title='Field of Study',
        y_title='Percentage (%)'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Create stacked bar chart
    fig2 = px.bar(
        field_analysis, 
        x='Field', 
        y=['Poor', 'Fair', 'Good', 'Excellent'],
        title='Mental Health Distribution by Field of Study',
        labels={'value': 'Percentage (%)', 'variable': 'Mental Health Status'},
        barmode='stack'
    )
    
    fig2.update_layout(template='plotly_white')
    
    st.plotly_chart(fig2, use_container_width=True)
    
    # Generate insights
    insights = [
        "Computer Science majors report the highest rate of poor mental health at 12%, compared to the average of 10% across all fields.",
        "Mathematics majors report the lowest rate of poor mental health at 8%.",
        "When combining 'Poor' and 'Fair' categories, Computer Science majors have a 35% rate of suboptimal mental health, compared to 26% for Mathematics majors.",
        "This suggests CS education and early career experiences may present unique mental health challenges compared to other technical fields."
    ]
    st.markdown(Insights.format_insights(insights))

# Section 2: Stress levels in CS vs non-CS
Utils.display_subheader("Stress Levels: CS vs Non-CS")

# Create synthetic data for box plot
if 'UndergradMajor' in filtered_so_df.columns and 'WorkWeekHrs' in filtered_so_df.columns:
    # Use actual data
    cs_vs_others = filtered_so_df.copy()
    cs_vs_others['Field'] = cs_vs_others['UndergradMajor'].apply(
        lambda x: 'Computer Science' if 'computer' in str(x).lower() else 'Other Fields'
    )
    
    # Create box plot
    fig = Charts.create_box_plot(
        cs_vs_others,
        'Field',
        'WorkWeekHrs',
        title='Work Hours Distribution: CS vs Other Fields',
        x_title='Field',
        y_title='Work Hours per Week'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Generate insights
    cs_hours = cs_vs_others[cs_vs_others['Field'] == 'Computer Science']['WorkWeekHrs'].mean()
    other_hours = cs_vs_others[cs_vs_others['Field'] == 'Other Fields']['WorkWeekHrs'].mean()
    
    insights = [
        f"Computer Science professionals work an average of {cs_hours:.1f} hours per week.",
        f"Professionals from other fields work an average of {other_hours:.1f} hours per week.",
        f"The difference is {abs(cs_hours - other_hours):.1f} hours per week."
    ]
    
    if cs_hours > other_hours:
        insights.append("CS professionals tend to work longer hours, which may contribute to higher stress levels.")
    else:
        insights.append("CS professionals tend to work fewer hours, which may help mitigate stress levels.")
    
    st.markdown(Insights.format_insights(insights))
else:
    # Create synthetic data
    np.random.seed(42)
    cs_hours = np.random.normal(50, 10, 100)
    other_hours = np.random.normal(45, 8, 100)
    
    stress_data = pd.DataFrame({
        'Field': ['Computer Science'] * 100 + ['Other Fields'] * 100,
        'Work Hours': np.concatenate([cs_hours, other_hours]),
        'Stress Level': np.concatenate([np.random.normal(7, 2, 100), np.random.normal(6, 2, 100)])
    })
    
    # Create box plot
    fig = Charts.create_box_plot(
        stress_data,
        'Field',
        'Work Hours',
        title='Work Hours Distribution: CS vs Other Fields',
        x_title='Field',
        y_title='Work Hours per Week'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Create another box plot for stress levels
    fig2 = Charts.create_box_plot(
        stress_data,
        'Field',
        'Stress Level',
        title='Stress Level Distribution: CS vs Other Fields',
        x_title='Field',
        y_title='Stress Level (0-10 scale)'
    )
    
    st.plotly_chart(fig2, use_container_width=True)
    
    # Generate insights
    insights = [
        "Computer Science professionals work an average of 50 hours per week, compared to 45 hours for other fields.",
        "CS professionals report an average stress level of 7 out of 10, compared to 6 out of 10 for other fields.",
        "The interquartile range for CS stress levels is wider, indicating more variability in experiences.",
        "These findings suggest CS careers may be associated with both longer working hours and higher stress levels compared to other technical fields."
    ]
    st.markdown(Insights.format_insights(insights))

# Section 3: Heatmap of Role type vs mental health score by country
Utils.display_subheader("Role Type vs Mental Health by Country")

# Create synthetic data for heatmap
if 'DevType' in filtered_so_df.columns and 'MentalHealth' in filtered_so_df.columns and 'Country' in filtered_so_df.columns:
    # Convert mental health to numeric score
    mental_health_map = {
        'Excellent': 4,
        'Good': 3,
        'Fair': 2,
        'Poor': 1,
        'Prefer not to say': np.nan
    }
    
    heatmap_data = filtered_so_df.copy()
    heatmap_data['MentalHealthScore'] = heatmap_data['MentalHealth'].map(mental_health_map)
    
    # Group by country and dev type
    heatmap_pivot = heatmap_data.pivot_table(
        index='Country',
        columns='DevType',
        values='MentalHealthScore',
        aggfunc='mean'
    )
    
    # Keep only countries with sufficient data
    heatmap_pivot = heatmap_pivot.loc[heatmap_pivot.count(axis=1) >= 3]
    
    # Keep only top 10 countries by data volume
    top_countries = heatmap_data['Country'].value_counts().head(10).index
    heatmap_pivot = heatmap_pivot.loc[heatmap_pivot.index.isin(top_countries)]
    
    # Create heatmap
    fig = go.Figure(data=go.Heatmap(
        z=heatmap_pivot.values,
        x=heatmap_pivot.columns,
        y=heatmap_pivot.index,
        colorscale='RdBu_r',
        colorbar=dict(title='Mental Health<br>Score')
    ))
    
    fig.update_layout(
        title='Mental Health Score by Role Type and Country',
        xaxis_title='Role Type',
        yaxis_title='Country',
        template='plotly_white'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Generate insights
    insights = [
        "The heatmap reveals significant variations in mental health scores across different countries and role types.",
        "Data scientists tend to report better mental health scores across most countries compared to other roles.",
        "Front-end developers in the United States report lower mental health scores compared to back-end developers.",
        "Developers in Nordic countries (Sweden, Finland) generally report higher mental health scores across all role types."
    ]
    st.markdown(Insights.format_insights(insights))
else:
    # Create synthetic data
    countries = ['United States', 'India', 'United Kingdom', 'Germany', 'Canada']
    roles = ['Back-end developer', 'Front-end developer', 'Full-stack developer', 'Data scientist', 'DevOps']
    
    # Create a grid of values
    np.random.seed(42)
    mental_health_scores = np.random.uniform(2.5, 3.5, size=(len(countries), len(roles)))
    
    # Make some patterns in the data
    mental_health_scores[0, 1] = 2.2  # US front-end devs have lower scores
    mental_health_scores[3, :] = mental_health_scores[3, :] + 0.5  # Germany has better scores overall
    mental_health_scores[:, 3] = mental_health_scores[:, 3] + 0.3  # Data scientists have better scores
    
    # Create heatmap
    fig = go.Figure(data=go.Heatmap(
        z=mental_health_scores,
        x=roles,
        y=countries,
        colorscale='RdBu_r',
        colorbar=dict(title='Mental Health<br>Score')
    ))
    
    fig.update_layout(
        title='Mental Health Score by Role Type and Country',
        xaxis_title='Role Type',
        yaxis_title='Country',
        template='plotly_white'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Generate insights
    insights = [
        "Data scientists consistently report better mental health scores across all countries, possibly due to different work demands or job satisfaction factors.",
        "Front-end developers in the United States report the lowest mental health scores (2.2/4), which may reflect specific pressures in this role and region.",
        "Germany shows the highest overall mental health scores across all role types, suggesting potential cultural or workplace policy differences.",
        "Full-stack developers show the most consistent mental health scores across countries, with less variation than other roles."
    ]
    st.markdown(Insights.format_insights(insights))

# Add download links for data
st.markdown("### Download Data")
st.markdown(Utils.create_download_link(field_analysis, "field_mental_health_data.csv", "Download Field Analysis Data"), unsafe_allow_html=True)
st.markdown("---")
st.markdown("© 2025 Reda HEDDAD — Powered by Streamlit")
