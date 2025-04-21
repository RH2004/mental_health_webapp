import streamlit as st
import sys
import os

# Add the modules directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))

# Import modules
from modules.utils import Utils
from modules.data_loader import DataLoader

# Set page configuration
Utils.set_page_config()

# Load custom CSS
Utils.load_css()

def main():
    """
    Main function to run the Streamlit app
    """
    # Display header
    Utils.display_header(
        "Mental Health in Tech Dashboard",
        "Visualizing the correlation between mental health outcomes and CS degrees/tech careers"
    )
    
    # Initialize data loader
    data_loader = DataLoader()
    
    # Load datasets
    mental_health_df = data_loader.load_mental_health_data()
    stackoverflow_df = data_loader.load_stackoverflow_data()
    
    # Display welcome message
    st.markdown("""
    ## Welcome to the Mental Health in Tech Dashboard
    
    This dashboard visualizes the correlation between mental health outcomes and the pursuit of a Computer Science (CS) degree or tech career, using data from OSMI and Stack Overflow surveys.
    
    ### Navigation
    
    Use the sidebar to navigate between different pages:
    
    1. **Mental Health Trends** - Time series of stress, burnout, and treatment outcomes
    2. **CS vs Mental Health** - Comparison of mental health conditions by field of study
    3. **Global Perspective** - Worldwide view of mental health support and awareness
    4. **Deep Dive Visuals** - Advanced visualizations and correlations
    
    ### Data Sources
    
    - OSMI Mental Health in Tech Survey
    - Stack Overflow Developer Survey
    - Additional data from WHO and OECD
    
    ### About
    
    This dashboard was created to help understand the unique mental health challenges faced by tech professionals and CS students, and to identify potential areas for improvement in support and awareness.
    """)
    
    # Display dataset information
    st.sidebar.markdown("### Dataset Information")
    st.sidebar.markdown(f"OSMI Survey: {len(mental_health_df)} records")
    st.sidebar.markdown(f"Stack Overflow Survey: {len(stackoverflow_df)} records")
    
    # Add footer
    st.markdown("""
    ---
    
    Created with Streamlit, Plotly, and Pandas | Data from OSMI and Stack Overflow
    """)

if __name__ == "__main__":
    main()
