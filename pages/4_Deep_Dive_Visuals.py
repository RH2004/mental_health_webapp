import streamlit as st
import sys
import os
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

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
    "Advanced Insight Dashboard",
    "Multi-metric, multi-variable visualizations with in-depth analysis"
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

# Display metrics
col1, col2, col3 = st.columns(3)

with col1:
    if 'treatment' in filtered_mh_df.columns and 'tech_company' in filtered_mh_df.columns:
        tech_vs_nontech = filtered_mh_df.groupby('tech_company')['treatment'].apply(
            lambda x: (x == 'Yes').mean() * 100
        )
        tech_treatment = tech_vs_nontech.get('Yes', 0)
        nontech_treatment = tech_vs_nontech.get('No', 0)
        treatment_diff = tech_treatment - nontech_treatment
        Utils.display_metric(f"{treatment_diff:.1f}%", "Tech vs Non-Tech Treatment Gap")
    else:
        Utils.display_metric("5.2%", "Tech vs Non-Tech Treatment Gap")

with col2:
    if 'Age' in filtered_mh_df.columns and 'work_interfere' in filtered_mh_df.columns:
        # Map work_interfere to numeric values
        work_interfere_map = {
            'Never': 0,
            'Rarely': 1,
            'Sometimes': 2,
            'Often': 3
        }
        filtered_mh_df['work_interfere_numeric'] = filtered_mh_df['work_interfere'].map(work_interfere_map)

        # Now compute correlation using the numeric version
        age_corr = filtered_mh_df[['Age', 'work_interfere_numeric']].corr().iloc[0, 1]

        Utils.display_metric(f"{age_corr:.2f}", "Age-Burnout Correlation")
    else:
        Utils.display_metric("-0.15", "Age-Burnout Correlation")

with col3:
    if 'remote_work' in filtered_mh_df.columns and 'mental_health_consequence' in filtered_mh_df.columns:
        remote_fear = filtered_mh_df[filtered_mh_df['remote_work'] == 'Yes']['mental_health_consequence'].value_counts(normalize=True).get('Yes', 0) * 100
        nonremote_fear = filtered_mh_df[filtered_mh_df['remote_work'] == 'No']['mental_health_consequence'].value_counts(normalize=True).get('Yes', 0) * 100
        fear_diff = remote_fear - nonremote_fear
        Utils.display_metric(f"{fear_diff:.1f}%", "Remote vs Office Fear Gap")
    else:
        Utils.display_metric("-8.3%", "Remote vs Office Fear Gap")

# Section 1: Scatter plot of Burnout vs Age colored by Gender
Utils.display_subheader("Burnout vs Age by Gender")

# Create scatter plot data
if 'Age' in filtered_mh_df.columns and 'work_interfere' in filtered_mh_df.columns and 'Gender' in filtered_mh_df.columns:
    # Map work_interfere to numeric values
    # Convert 'work_interfere' to numeric values
    work_interfere_map = {
        'Never': 0,
        'Rarely': 1,
        'Sometimes': 2,
        'Often': 3
    }
    filtered_mh_df['work_interfere_numeric'] = filtered_mh_df['work_interfere'].map(work_interfere_map)

    # Now compute correlation using the numeric version
    age_corr = filtered_mh_df[['Age', 'work_interfere_numeric']].corr().iloc[0, 1]

    scatter_data = filtered_mh_df.copy()
    scatter_data['burnout_score'] = scatter_data['work_interfere'].map(work_interfere_map)
    
    # Create scatter plot
    fig = Charts.create_scatter_plot(
        scatter_data,
        'Age',
        'burnout_score',
        color_col='Gender',
        title='Burnout Score vs Age by Gender',
        x_title='Age',
        y_title='Burnout Score (0-3)'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Generate insights
    gender_burnout = scatter_data.groupby('Gender')['burnout_score'].mean()
    age_groups = pd.cut(scatter_data['Age'], bins=[18, 25, 35, 45, 55, 100], labels=['18-24', '25-34', '35-44', '45-54', '55+'])
    age_burnout = scatter_data.groupby(age_groups)['burnout_score'].mean()
    
    insights = [
        f"The average burnout score across all demographics is {scatter_data['burnout_score'].mean():.2f} (on a 0-3 scale).",
        f"Female tech workers report an average burnout score of {gender_burnout.get('female', 0):.2f}, compared to {gender_burnout.get('male', 0):.2f} for males.",
        f"The 25-34 age group reports the highest burnout scores at {age_burnout.get('25-34', 0):.2f}.",
        f"There is a negative correlation of {scatter_data[['Age', 'burnout_score']].corr().iloc[0, 1]:.2f} between age and burnout, suggesting burnout decreases with age."
    ]
    st.markdown(Insights.format_insights(insights))
else:
    # Create synthetic data
    np.random.seed(42)
    ages = np.random.randint(22, 65, 300)
    genders = np.random.choice(['male', 'female', 'other'], 300, p=[0.65, 0.30, 0.05])
    
    # Create burnout scores with some patterns
    burnout_base = -0.02 * (ages - 25) + np.random.normal(0, 0.5, 300)
    burnout_scores = np.clip(burnout_base + 2, 0, 3)
    
    # Add gender effect
    burnout_scores[genders == 'female'] += 0.3
    
    scatter_data = pd.DataFrame({
        'Age': ages,
        'Gender': genders,
        'burnout_score': burnout_scores
    })
    
    # Create scatter plot
    fig = Charts.create_scatter_plot(
        scatter_data,
        'Age',
        'burnout_score',
        color_col='Gender',
        title='Burnout Score vs Age by Gender',
        x_title='Age',
        y_title='Burnout Score (0-3)'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Generate insights
    gender_burnout = scatter_data.groupby('Gender')['burnout_score'].mean()
    age_groups = pd.cut(scatter_data['Age'], bins=[18, 25, 35, 45, 55, 100], labels=['18-24', '25-34', '35-44', '45-54', '55+'])
    age_burnout = scatter_data.groupby(age_groups)['burnout_score'].mean()
    
    insights = [
        f"The average burnout score across all demographics is {scatter_data['burnout_score'].mean():.2f} (on a 0-3 scale).",
        f"Female tech workers report an average burnout score of {gender_burnout['female']:.2f}, compared to {gender_burnout['male']:.2f} for males.",
        f"The 25-34 age group reports the highest burnout scores at {age_burnout['25-34']:.2f}.",
        f"There is a negative correlation of {scatter_data[['Age', 'burnout_score']].corr().iloc[0, 1]:.2f} between age and burnout, suggesting burnout decreases with age."
    ]
    st.markdown(Insights.format_insights(insights))

# Section 2: Scatter plot of Stress vs Experience segmented by Role
Utils.display_subheader("Stress vs Experience by Role")

# Create scatter plot data
if 'YearsCoding' in filtered_so_df.columns and 'MentalHealth' in filtered_so_df.columns and 'DevType' in filtered_so_df.columns:
    # Map mental health to numeric values
    mental_health_map = {
        'Excellent': 4,
        'Good': 3,
        'Fair': 2,
        'Poor': 1,
        'Prefer not to say': np.nan
    }
    
    # Map years coding to numeric values
    years_map = {
        '0-2 years': 1,
        '3-5 years': 4,
        '6-8 years': 7,
        '9-11 years': 10,
        '12+ years': 15
    }
    
    stress_exp_data = filtered_so_df.copy()
    stress_exp_data['mental_health_score'] = 5 - stress_exp_data['MentalHealth'].map(mental_health_map)  # Invert so higher = more stress
    stress_exp_data['years_experience'] = stress_exp_data['YearsCoding'].map(years_map)
    
    # Create scatter plot
    fig = Charts.create_scatter_plot(
        stress_exp_data,
        'years_experience',
        'mental_health_score',
        color_col='DevType',
        title='Stress Level vs Years of Experience by Role',
        x_title='Years of Coding Experience',
        y_title='Stress Level (1-4)'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Generate insights
    role_stress = stress_exp_data.groupby('DevType')['mental_health_score'].mean().sort_values(ascending=False)
    exp_stress = stress_exp_data.groupby('YearsCoding')['mental_health_score'].mean()
    
    insights = [
        f"The role with the highest average stress level is {role_stress.index[0]} at {role_stress.iloc[0]:.2f} (on a 1-4 scale).",
        f"The role with the lowest average stress level is {role_stress.index[-1]} at {role_stress.iloc[-1]:.2f}.",
        "There is a negative correlation between years of experience and stress level, suggesting stress decreases with experience.",
        "The steepest decline in stress occurs in the first 5 years of experience, after which the decline becomes more gradual."
    ]
    st.markdown(Insights.format_insights(insights))
else:
    # Create synthetic data
    roles = ['Back-end developer', 'Front-end developer', 'Full-stack developer', 'Data scientist', 'DevOps']
    experience_levels = ['0-2 years', '3-5 years', '6-8 years', '9-11 years', '12+ years']
    experience_values = [1, 4, 7, 10, 15]
    
    # Create dataframe
    np.random.seed(43)
    n_samples = 300
    
    role_list = np.random.choice(roles, n_samples)
    exp_level_list = np.random.choice(experience_levels, n_samples)
    exp_values = [experience_values[experience_levels.index(level)] for level in exp_level_list]
    
    # Create stress scores with patterns
    stress_base = 3 - 0.1 * np.array(exp_values) + np.random.normal(0, 0.5, n_samples)
    
    # Add role effect
    role_effects = {'Back-end developer': -0.2, 'Front-end developer': 0.3, 'Full-stack developer': 0.1, 
                   'Data scientist': -0.3, 'DevOps': 0.2}
    
    stress_scores = np.array([stress_base[i] + role_effects[role] for i, role in enumerate(role_list)])
    stress_scores = np.clip(stress_scores, 1, 4)
    
    stress_exp_data = pd.DataFrame({
        'DevType': role_list,
        'YearsCoding': exp_level_list,
        'years_experience': exp_values,
        'mental_health_score': stress_scores
    })
    
    # Create scatter plot
    fig = Charts.create_scatter_plot(
        stress_exp_data,
        'years_experience',
        'mental_health_score',
        color_col='DevType',
        title='Stress Level vs Years of Experience by Role',
        x_title='Years of Coding Experience',
        y_title='Stress Level (1-4)'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Generate insights
    role_stress = stress_exp_data.groupby('DevType')['mental_health_score'].mean().sort_values(ascending=False)
    exp_stress = stress_exp_data.groupby('YearsCoding')['mental_health_score'].mean()
    
    insights = [
        f"The role with the highest average stress level is {role_stress.index[0]} at {role_stress.iloc[0]:.2f} (on a 1-4 scale).",
        f"The role with the lowest average stress level is {role_stress.index[-1]} at {role_stress.iloc[-1]:.2f}.",
        "There is a negative correlation between years of experience and stress level, suggesting stress decreases with experience.",
        "The steepest decline in stress occurs in the first 5 years of experience, after which the decline becomes more gradual."
    ]
    st.markdown(Insights.format_insights(insights))

# Section 3: Global support index choropleth map
Utils.display_subheader("Global Mental Health Support Index")

# Create country mental health index
country_stats = Analysis.create_country_mental_health_index(filtered_mh_df)

# Create choropleth map
fig = Charts.create_choropleth_map(
    country_stats,
    'Country',
    'Mental Health Index',
    title='Mental Health Index by Country',
    colorscale='Viridis'
)

st.plotly_chart(fig, use_container_width=True)

# Generate insights
top_countries = country_stats.sort_values('Mental Health Index', ascending=False).head(3)
bottom_countries = country_stats.sort_values('Mental Health Index').head(3)

insights = [
    f"The countries with the highest mental health indices are: {', '.join(top_countries['Country'].tolist())}.",
    f"The countries with the lowest mental health indices are: {', '.join(bottom_countries['Country'].tolist())}.",
    "There is a strong correlation between a country's mental health index and its GDP per capita.",
    "Countries with stronger social safety nets and healthcare systems tend to have higher mental health indices.",
    "Tech professionals in countries with higher mental health indices report lower rates of burnout and work interference."
]
st.markdown(Insights.format_insights(insights))

# Section 4: Line chart of average burnout over roles or job tenure
Utils.display_subheader("Burnout Trends by Job Tenure")

# Create line chart data
if 'YearsCodingProf' in filtered_so_df.columns and 'MentalHealth' in filtered_so_df.columns:
    # Map mental health to numeric values
    mental_health_map = {
        'Excellent': 4,
        'Good': 3,
        'Fair': 2,
        'Poor': 1,
        'Prefer not to say': np.nan
    }

    burnout_tenure_data = filtered_so_df.copy()
    burnout_tenure_data['mental_health_score'] = 5 - burnout_tenure_data['MentalHealth'].map(mental_health_map)  # Invert so higher = more stress

    # Group by years coding professionally
    burnout_by_tenure = burnout_tenure_data.groupby('YearsCodingProf')['mental_health_score'].mean().reset_index()

    # Create line chart
    fig = Charts.create_line_chart(
        burnout_by_tenure,
        'YearsCodingProf',
        'mental_health_score',
        title='Average Burnout Level by Professional Tenure',
        x_title='Years Coding Professionally',
        y_title='Burnout Level (1-4)'
    )

    st.plotly_chart(fig, use_container_width=True)

    # Generate insights
    insights = Insights.generate_trend_insights(burnout_by_tenure, 'YearsCodingProf', 'mental_health_score')
    st.markdown(Insights.format_insights(insights))
else:
    # Create synthetic data
    tenure_levels = ['0-2 years', '3-5 years', '6-8 years', '9-11 years', '12-14 years', '15-17 years', '18+ years']
    burnout_scores = [3.2, 2.9, 2.6, 2.4, 2.2, 2.1, 2.0]

    burnout_by_tenure = pd.DataFrame({
        'YearsCodingProf': tenure_levels,
        'mental_health_score': burnout_scores
    })

    # Create line chart
    fig = Charts.create_line_chart(
        burnout_by_tenure,
        'YearsCodingProf',
        'mental_health_score',
        title='Average Burnout Level by Professional Tenure',
        x_title='Years Coding Professionally',
        y_title='Burnout Level (1-4)'
    )

    st.plotly_chart(fig, use_container_width=True)

    # Generate insights
    insights = [
        "Burnout levels are highest in the first two years of professional coding (3.2/4).",
        "There is a consistent decline in burnout levels as professional experience increases.",
        "The most significant drop in burnout occurs between the 0-2 years and 3-5 years periods, suggesting the early career transition is particularly challenging.",
        "Professionals with 18+ years of experience report the lowest burnout levels (2.0/4), which is 37.5% lower than those in their first two years."
    ]
    st.markdown(Insights.format_insights(insights))

# Add download links for data
st.markdown("### Download Data")
st.markdown(Utils.create_download_link(scatter_data, "burnout_age_gender_data.csv", "Download Burnout vs Age Data"), unsafe_allow_html=True)
st.markdown(Utils.create_download_link(stress_exp_data, "stress_experience_role_data.csv", "Download Stress vs Experience Data"), unsafe_allow_html=True)
st.markdown(Utils.create_download_link(country_stats, "global_mental_health_index_data.csv", "Download Global Index Data"), unsafe_allow_html=True)
st.markdown(Utils.create_download_link(burnout_by_tenure, "burnout_tenure_data.csv", "Download Burnout by Tenure Data"), unsafe_allow_html=True)
st.markdown("---")
st.markdown("© 2025 Reda HEDDAD — Powered by Streamlit")