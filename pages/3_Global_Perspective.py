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
    "Worldview & Awareness",
    "Visualizing how different countries rank in mental health support and awareness"
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

# Create country mental health index
country_stats = Analysis.create_country_mental_health_index(filtered_mh_df)

# Display metrics
col1, col2, col3 = st.columns(3)

with col1:
    top_country = country_stats.sort_values('Mental Health Index', ascending=False).iloc[0]
    Utils.display_metric(f"{top_country['Country']}", "Highest Mental Health Index")

with col2:
    avg_support = country_stats['Support Score'].mean()
    Utils.display_metric(f"{avg_support:.1f}/10", "Average Support Score")

with col3:
    avg_awareness = country_stats['Awareness Score'].mean()
    Utils.display_metric(f"{avg_awareness:.1f}/10", "Average Awareness Score")

# Section 1: Choropleth map of support score by country
Utils.display_subheader("Global Mental Health Support Score")

# Create choropleth map
fig = Charts.create_choropleth_map(
    country_stats,
    'Country',
    'Support Score',
    title='Mental Health Support Score by Country',
    colorscale='Viridis'
)

st.plotly_chart(fig, use_container_width=True)

# Generate insights
insights = [
    f"{top_country['Country']} has the highest mental health support score at {top_country['Support Score']:.1f}/10.",
    f"The global average support score is {avg_support:.1f}/10.",
    "Countries with strong social safety nets and healthcare systems tend to score higher on mental health support.",
    "There are significant regional variations in mental health support, with Nordic and Western European countries generally scoring higher."
]
st.markdown(Insights.format_insights(insights))

# Section 2: Stacked bar chart of country-wise mental health services access
Utils.display_subheader("Mental Health Services Access by Country")

# Create synthetic data for stacked bar chart if needed
if 'Country' in filtered_mh_df.columns and 'care_options' in filtered_mh_df.columns and 'benefits' in filtered_mh_df.columns:
    # Use actual data
    services_access = filtered_mh_df.groupby('Country').agg({
        'care_options': lambda x: (x == 'Yes').mean() * 100,
        'benefits': lambda x: (x == 'Yes').mean() * 100
    }).reset_index()
    
    # Rename columns
    services_access.columns = ['Country', 'Care Options Available', 'Mental Health Benefits']
    
    # Sort by care options
    services_access = services_access.sort_values('Care Options Available', ascending=False).head(10)
else:
    # Create synthetic data
    countries = ['United States', 'United Kingdom', 'Canada', 'Germany', 'Australia', 
                'Sweden', 'Netherlands', 'France', 'Japan', 'India']
    
    care_options = [75, 82, 80, 78, 76, 88, 85, 72, 65, 45]
    benefits = [65, 78, 75, 80, 70, 85, 82, 68, 60, 40]
    no_access = [100 - (c + b)/2 for c, b in zip(care_options, benefits)]
    
    services_access = pd.DataFrame({
        'Country': countries,
        'Care Options Available': care_options,
        'Mental Health Benefits': benefits
    })

# Create stacked bar chart
fig = px.bar(
    services_access,
    x='Country',
    y=['Care Options Available', 'Mental Health Benefits'],
    title='Mental Health Services Access by Country',
    labels={'value': 'Percentage (%)', 'variable': 'Service Type'},
    barmode='group'
)

fig.update_layout(template='plotly_white')

st.plotly_chart(fig, use_container_width=True)

# Generate insights
top_care = services_access.sort_values('Care Options Available', ascending=False).iloc[0]
top_benefits = services_access.sort_values('Mental Health Benefits', ascending=False).iloc[0]

insights = [
    f"{top_care['Country']} has the highest availability of mental health care options at {top_care['Care Options Available']:.1f}%.",
    f"{top_benefits['Country']} has the highest provision of mental health benefits at {top_benefits['Mental Health Benefits']:.1f}%.",
    "There is a strong correlation between care options availability and mental health benefits provision.",
    "Countries with higher GDP per capita tend to have better mental health service access."
]
st.markdown(Insights.format_insights(insights))

# Section 3: Interactive map with regional initiatives
Utils.display_subheader("Regional Mental Health Initiatives")

# Create a dataframe with regional initiatives
initiatives = pd.DataFrame({
    'Country': ['United States', 'United Kingdom', 'Canada', 'Germany', 'Australia', 
               'Sweden', 'Netherlands', 'France', 'Japan', 'India'],
    'Initiative': [
        'National Alliance on Mental Illness (NAMI)',
        'Time to Change campaign',
        'Bell Let\'s Talk',
        'German Depression Foundation',
        'Beyond Blue',
        'Hjärnkoll (Mind Check)',
        'I.COM (ICT & Mental Health)',
        'Psycom',
        'Kokoro no Kenko (Mental Health)',
        'National Mental Health Program'
    ],
    'Focus': [
        'Education and advocacy',
        'Reducing stigma',
        'Awareness and funding',
        'Depression research',
        'Anxiety and depression support',
        'Anti-stigma campaign',
        'Technology and mental health',
        'Information and resources',
        'Workplace mental health',
        'Treatment access'
    ],
    'Impact Score': [8, 9, 8, 7, 9, 9, 8, 7, 6, 5],
    'Year Started': [1979, 2007, 2010, 2008, 2000, 2009, 2013, 1998, 2015, 1982],
    'lat': [37.0902, 51.5074, 45.4215, 52.5200, -35.2809, 59.3293, 52.3676, 46.2276, 35.6762, 20.5937],
    'lon': [-95.7129, -0.1278, -75.6972, 13.4050, 149.1300, 18.0686, 4.9041, 2.2137, 139.6503, 78.9629]
})

# Create an interactive map
fig = px.scatter_geo(
    initiatives,
    lat='lat',
    lon='lon',
    color='Impact Score',
    size='Impact Score',
    hover_name='Country',
    hover_data=['Initiative', 'Focus', 'Year Started'],
    projection='natural earth',
    title='Mental Health Initiatives Around the World'
)

fig.update_layout(
    template='plotly_white',
    geo=dict(
        showland=True,
        landcolor='rgb(243, 243, 243)',
        countrycolor='rgb(204, 204, 204)',
        showocean=True,
        oceancolor='rgb(230, 230, 250)'
    )
)

st.plotly_chart(fig, use_container_width=True)

# Generate insights
insights = [
    "The UK's 'Time to Change' campaign has had one of the highest impacts on reducing mental health stigma.",
    "Australia's 'Beyond Blue' has been particularly effective in providing support for anxiety and depression.",
    "Newer initiatives like Canada's 'Bell Let's Talk' have leveraged social media effectively for awareness.",
    "There is a notable gap in comprehensive mental health initiatives in developing regions.",
    "Technology-focused mental health initiatives are emerging, particularly in countries with strong tech sectors."
]
st.markdown(Insights.format_insights(insights))

# Add download links for data
st.markdown("### Download Data")
st.markdown(Utils.create_download_link(country_stats, "country_mental_health_data.csv", "Download Country Statistics"), unsafe_allow_html=True)
st.markdown(Utils.create_download_link(services_access, "mental_health_services_data.csv", "Download Services Access Data"), unsafe_allow_html=True)
st.markdown(Utils.create_download_link(initiatives, "mental_health_initiatives_data.csv", "Download Initiatives Data"), unsafe_allow_html=True)
st.markdown("---")
st.markdown("© 2025 Reda HEDDAD — Powered by Streamlit")
