import streamlit as st
import pandas as pd
import numpy as np

class Insights:
    """
    A class to generate insights from mental health data analysis
    """
    
    @staticmethod
    def generate_trend_insights(df, x_col, y_col, group_col=None):
        """
        Generate insights about trends in the data
        
        Parameters:
        -----------
        df : pandas.DataFrame
            The dataframe containing the data
        x_col : str
            Column name for x-axis (typically time or categories)
        y_col : str
            Column name for y-axis (metric of interest)
        group_col : str, optional
            Column name for grouping
            
        Returns:
        --------
        list
            List of insight strings
        """
        insights = []
        
        try:
            # Check if columns exist
            if x_col not in df.columns or y_col not in df.columns:
                return ["Insufficient data to generate insights."]
            
            # Basic statistics
            if df[y_col].dtype in [np.float64, np.int64]:
                mean_val = df[y_col].mean()
                max_val = df[y_col].max()
                min_val = df[y_col].min()
                
                insights.append(f"The average {y_col} is {mean_val:.2f}.")
                insights.append(f"The highest {y_col} is {max_val:.2f}, while the lowest is {min_val:.2f}.")
            
            # Group analysis if group_col is provided
            if group_col and group_col in df.columns:
                group_means = df.groupby(group_col)[y_col].mean().sort_values(ascending=False)
                top_group = group_means.index[0]
                bottom_group = group_means.index[-1]
                
                insights.append(f"{top_group} has the highest average {y_col} at {group_means.iloc[0]:.2f}.")
                insights.append(f"{bottom_group} has the lowest average {y_col} at {group_means.iloc[-1]:.2f}.")
                
                # Compare top and bottom groups
                diff_pct = ((group_means.iloc[0] - group_means.iloc[-1]) / group_means.iloc[-1]) * 100
                insights.append(f"The difference between the highest and lowest group is {diff_pct:.1f}%.")
            
            # Trend analysis if x_col is numeric or temporal
            if df[x_col].dtype in [np.float64, np.int64]:
                # Simple correlation to detect trend
                correlation = df[[x_col, y_col]].corr().iloc[0, 1]
                
                if correlation > 0.7:
                    insights.append(f"There is a strong positive trend between {x_col} and {y_col}.")
                elif correlation > 0.3:
                    insights.append(f"There is a moderate positive trend between {x_col} and {y_col}.")
                elif correlation < -0.7:
                    insights.append(f"There is a strong negative trend between {x_col} and {y_col}.")
                elif correlation < -0.3:
                    insights.append(f"There is a moderate negative trend between {x_col} and {y_col}.")
                else:
                    insights.append(f"There is no clear linear trend between {x_col} and {y_col}.")
        
        except Exception as e:
            insights.append(f"Error generating insights: {str(e)}")
        
        return insights
    
    @staticmethod
    def generate_comparison_insights(df, category_col, value_col):
        """
        Generate insights comparing different categories
        
        Parameters:
        -----------
        df : pandas.DataFrame
            The dataframe containing the data
        category_col : str
            Column name for categories to compare
        value_col : str
            Column name for the value to compare across categories
            
        Returns:
        --------
        list
            List of insight strings
        """
        insights = []
        
        try:
            # Check if columns exist
            if category_col not in df.columns or value_col not in df.columns:
                return ["Insufficient data to generate comparison insights."]
            
            # Calculate category statistics
            if df[value_col].dtype in [np.float64, np.int64]:
                category_stats = df.groupby(category_col)[value_col].agg(['mean', 'count']).reset_index()
                category_stats = category_stats.sort_values('mean', ascending=False)
                
                # Get top and bottom categories
                top_categories = category_stats.head(3)
                bottom_categories = category_stats.tail(3)
                
                # Generate insights for top categories
                insights.append("Top performing categories:")
                for _, row in top_categories.iterrows():
                    insights.append(f"- {row[category_col]}: {row['mean']:.2f} (based on {row['count']} data points)")
                
                # Generate insights for bottom categories
                insights.append("\nCategories with lowest performance:")
                for _, row in bottom_categories.iterrows():
                    insights.append(f"- {row[category_col]}: {row['mean']:.2f} (based on {row['count']} data points)")
                
                # Calculate overall statistics
                overall_mean = df[value_col].mean()
                insights.append(f"\nThe overall average across all categories is {overall_mean:.2f}.")
                
                # Calculate variance between categories
                category_variance = category_stats['mean'].var()
                if category_variance > 1:
                    insights.append("There is high variance between categories, suggesting significant differences.")
                else:
                    insights.append("There is relatively low variance between categories.")
        
        except Exception as e:
            insights.append(f"Error generating comparison insights: {str(e)}")
        
        return insights
    
    @staticmethod
    def generate_mental_health_insights(mental_health_df, stackoverflow_df):
        """
        Generate insights specific to mental health in tech
        
        Parameters:
        -----------
        mental_health_df : pandas.DataFrame
            The mental health dataset
        stackoverflow_df : pandas.DataFrame
            The Stack Overflow dataset
            
        Returns:
        --------
        list
            List of insight strings
        """
        insights = []
        
        try:
            # Mental health treatment insights
            if 'treatment' in mental_health_df.columns:
                treatment_pct = mental_health_df['treatment'].value_counts(normalize=True).get('Yes', 0) * 100
                insights.append(f"{treatment_pct:.1f}% of tech professionals have sought treatment for mental health issues.")
            
            # Work interference insights
            if 'work_interfere' in mental_health_df.columns:
                work_interfere = mental_health_df['work_interfere'].value_counts(normalize=True)
                often_sometimes = (work_interfere.get('Often', 0) + work_interfere.get('Sometimes', 0)) * 100
                insights.append(f"{often_sometimes:.1f}% report that mental health issues interfere with work sometimes or often.")
            
            # Company size insights
            if 'no_employees' in mental_health_df.columns and 'mental_health_consequence' in mental_health_df.columns:
                by_size = mental_health_df.groupby('no_employees')['mental_health_consequence'].apply(lambda x: (x == 'Yes').mean() * 100)
                by_size = by_size.sort_values()
                
                if not by_size.empty:
                    best_size = by_size.index[0]
                    worst_size = by_size.index[-1]
                    insights.append(f"Companies with {best_size} employees have the lowest rate of negative mental health consequences ({by_size.iloc[0]:.1f}%).")
                    insights.append(f"Companies with {worst_size} employees have the highest rate of negative mental health consequences ({by_size.iloc[-1]:.1f}%).")
            
            # Remote work insights
            if 'remote_work' in mental_health_df.columns and 'work_interfere' in mental_health_df.columns:
                remote_work = mental_health_df[mental_health_df['remote_work'] == 'Yes']
                non_remote = mental_health_df[mental_health_df['remote_work'] == 'No']
                
                if not remote_work.empty and not non_remote.empty:
                    remote_interfere = remote_work['work_interfere'].isin(['Often', 'Sometimes']).mean() * 100
                    non_remote_interfere = non_remote['work_interfere'].isin(['Often', 'Sometimes']).mean() * 100
                    
                    if remote_interfere < non_remote_interfere:
                        diff = non_remote_interfere - remote_interfere
                        insights.append(f"Remote workers report {diff:.1f}% less work interference from mental health issues compared to non-remote workers.")
                    else:
                        diff = remote_interfere - non_remote_interfere
                        insights.append(f"Remote workers report {diff:.1f}% more work interference from mental health issues compared to non-remote workers.")
            
            # Stack Overflow insights
            if 'MentalHealth' in stackoverflow_df.columns and 'DevType' in stackoverflow_df.columns:
                dev_mental_health = stackoverflow_df.groupby('DevType')['MentalHealth'].apply(
                    lambda x: (x.isin(['Poor', 'Fair'])).mean() * 100
                ).sort_values()
                
                if not dev_mental_health.empty:
                    best_role = dev_mental_health.index[0]
                    worst_role = dev_mental_health.index[-1]
                    insights.append(f"{best_role}s report the lowest rates of poor mental health ({dev_mental_health.iloc[0]:.1f}%).")
                    insights.append(f"{worst_role}s report the highest rates of poor mental health ({dev_mental_health.iloc[-1]:.1f}%).")
            
            # Job satisfaction insights
            if 'JobSatisfaction' in stackoverflow_df.columns and 'MentalHealth' in stackoverflow_df.columns:
                job_sat_mental = stackoverflow_df.pivot_table(
                    index='JobSatisfaction', 
                    columns='MentalHealth', 
                    aggfunc='size', 
                    fill_value=0
                )
                
                if not job_sat_mental.empty and 'Excellent' in job_sat_mental.columns and 'Poor' in job_sat_mental.columns:
                    job_sat_mental['Ratio'] = job_sat_mental['Excellent'] / job_sat_mental['Poor']
                    best_sat = job_sat_mental['Ratio'].idxmax()
                    insights.append(f"Professionals who are '{best_sat}' with their jobs report the highest ratio of excellent to poor mental health.")
        
        except Exception as e:
            insights.append(f"Error generating mental health insights: {str(e)}")
        
        return insights
    
    @staticmethod
    def format_insights(insights_list):
        """
        Format a list of insights for display
        
        Parameters:
        -----------
        insights_list : list
            List of insight strings
            
        Returns:
        --------
        str
            Formatted insights text
        """
        if not insights_list:
            return "No insights available."
        
        formatted_text = "## Key Insights\n\n"
        
        for i, insight in enumerate(insights_list, 1):
            if insight.startswith('-'):
                formatted_text += f"{insight}\n"
            elif insight.startswith('\n'):
                formatted_text += f"{insight}\n"
            else:
                formatted_text += f"{i}. {insight}\n\n"
        
        return formatted_text
