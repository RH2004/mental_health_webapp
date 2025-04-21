import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

class Charts:
    """
    A class to create various charts for the dashboard
    """
    
    @staticmethod
    def create_line_chart(df, x_col, y_col, color_col=None, title=None, x_title=None, y_title=None):
        """
        Create a line chart using Plotly
        
        Parameters:
        -----------
        df : pandas.DataFrame
            The dataframe containing the data
        x_col : str
            Column name for x-axis
        y_col : str
            Column name for y-axis
        color_col : str, optional
            Column name for color differentiation
        title : str, optional
            Chart title
        x_title : str, optional
            X-axis title
        y_title : str, optional
            Y-axis title
            
        Returns:
        --------
        plotly.graph_objects.Figure
            The created line chart
        """
        if color_col:
            fig = px.line(df, x=x_col, y=y_col, color=color_col, 
                         title=title, labels={x_col: x_title or x_col, y_col: y_title or y_col})
        else:
            fig = px.line(df, x=x_col, y=y_col, 
                         title=title, labels={x_col: x_title or x_col, y_col: y_title or y_col})
        
        fig.update_layout(
            template="plotly_white",
            xaxis_title=x_title or x_col,
            yaxis_title=y_title or y_col,
            legend_title_text=color_col,
            title={
                'text': title or f"{y_col} by {x_col}",
                'y':0.95,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            }
        )
        
        return fig
    
    @staticmethod
    def create_bar_chart(df, x_col, y_col, color_col=None, title=None, x_title=None, y_title=None, orientation='v'):
        """
        Create a bar chart using Plotly
        
        Parameters:
        -----------
        df : pandas.DataFrame
            The dataframe containing the data
        x_col : str
            Column name for x-axis
        y_col : str
            Column name for y-axis
        color_col : str, optional
            Column name for color differentiation
        title : str, optional
            Chart title
        x_title : str, optional
            X-axis title
        y_title : str, optional
            Y-axis title
        orientation : str, optional
            Bar orientation ('v' for vertical, 'h' for horizontal)
            
        Returns:
        --------
        plotly.graph_objects.Figure
            The created bar chart
        """
        if orientation == 'h':
            # Swap x and y for horizontal orientation
            x_col, y_col = y_col, x_col
            x_title, y_title = y_title, x_title
        
        if color_col:
            fig = px.bar(df, x=x_col, y=y_col, color=color_col, 
                        title=title, labels={x_col: x_title or x_col, y_col: y_title or y_col},
                        orientation=orientation)
        else:
            fig = px.bar(df, x=x_col, y=y_col, 
                        title=title, labels={x_col: x_title or x_col, y_col: y_title or y_col},
                        orientation=orientation)
        
        fig.update_layout(
            template="plotly_white",
            xaxis_title=x_title or x_col,
            yaxis_title=y_title or y_col,
            legend_title_text=color_col,
            title={
                'text': title or f"{y_col} by {x_col}",
                'y':0.95,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            }
        )
        
        return fig
    
    @staticmethod
    def create_stacked_bar_chart(df, x_col, y_col, color_col, title=None, x_title=None, y_title=None):
        """
        Create a stacked bar chart using Plotly
        
        Parameters:
        -----------
        df : pandas.DataFrame
            The dataframe containing the data
        x_col : str
            Column name for x-axis
        y_col : str
            Column name for y-axis
        color_col : str
            Column name for stacking
        title : str, optional
            Chart title
        x_title : str, optional
            X-axis title
        y_title : str, optional
            Y-axis title
            
        Returns:
        --------
        plotly.graph_objects.Figure
            The created stacked bar chart
        """
        fig = px.bar(df, x=x_col, y=y_col, color=color_col, 
                    title=title, labels={x_col: x_title or x_col, y_col: y_title or y_col},
                    barmode='stack')
        
        fig.update_layout(
            template="plotly_white",
            xaxis_title=x_title or x_col,
            yaxis_title=y_title or y_col,
            legend_title_text=color_col,
            title={
                'text': title or f"{y_col} by {x_col} (Stacked by {color_col})",
                'y':0.95,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            }
        )
        
        return fig
    
    @staticmethod
    def create_area_chart(df, x_col, y_col, color_col=None, title=None, x_title=None, y_title=None):
        """
        Create an area chart using Plotly
        
        Parameters:
        -----------
        df : pandas.DataFrame
            The dataframe containing the data
        x_col : str
            Column name for x-axis
        y_col : str
            Column name for y-axis
        color_col : str, optional
            Column name for color differentiation
        title : str, optional
            Chart title
        x_title : str, optional
            X-axis title
        y_title : str, optional
            Y-axis title
            
        Returns:
        --------
        plotly.graph_objects.Figure
            The created area chart
        """
        if color_col:
            fig = px.area(df, x=x_col, y=y_col, color=color_col, 
                         title=title, labels={x_col: x_title or x_col, y_col: y_title or y_col})
        else:
            fig = px.area(df, x=x_col, y=y_col, 
                         title=title, labels={x_col: x_title or x_col, y_col: y_title or y_col})
        
        fig.update_layout(
            template="plotly_white",
            xaxis_title=x_title or x_col,
            yaxis_title=y_title or y_col,
            legend_title_text=color_col,
            title={
                'text': title or f"{y_col} by {x_col}",
                'y':0.95,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            }
        )
        
        return fig
    
    @staticmethod
    def create_scatter_plot(df, x_col, y_col, color_col=None, size_col=None, title=None, x_title=None, y_title=None):
        """
        Create a scatter plot using Plotly
        
        Parameters:
        -----------
        df : pandas.DataFrame
            The dataframe containing the data
        x_col : str
            Column name for x-axis
        y_col : str
            Column name for y-axis
        color_col : str, optional
            Column name for color differentiation
        size_col : str, optional
            Column name for point size
        title : str, optional
            Chart title
        x_title : str, optional
            X-axis title
        y_title : str, optional
            Y-axis title
            
        Returns:
        --------
        plotly.graph_objects.Figure
            The created scatter plot
        """
        fig = px.scatter(df, x=x_col, y=y_col, color=color_col, size=size_col,
                        title=title, labels={x_col: x_title or x_col, y_col: y_title or y_col})
        
        fig.update_layout(
            template="plotly_white",
            xaxis_title=x_title or x_col,
            yaxis_title=y_title or y_col,
            legend_title_text=color_col,
            title={
                'text': title or f"{y_col} vs {x_col}",
                'y':0.95,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            }
        )
        
        return fig
    
    @staticmethod
    def create_box_plot(df, x_col, y_col, color_col=None, title=None, x_title=None, y_title=None):
        """
        Create a box plot using Plotly
        
        Parameters:
        -----------
        df : pandas.DataFrame
            The dataframe containing the data
        x_col : str
            Column name for x-axis categories
        y_col : str
            Column name for y-axis values
        color_col : str, optional
            Column name for color differentiation
        title : str, optional
            Chart title
        x_title : str, optional
            X-axis title
        y_title : str, optional
            Y-axis title
            
        Returns:
        --------
        plotly.graph_objects.Figure
            The created box plot
        """
        fig = px.box(df, x=x_col, y=y_col, color=color_col,
                    title=title, labels={x_col: x_title or x_col, y_col: y_title or y_col})
        
        fig.update_layout(
            template="plotly_white",
            xaxis_title=x_title or x_col,
            yaxis_title=y_title or y_col,
            legend_title_text=color_col,
            title={
                'text': title or f"Distribution of {y_col} by {x_col}",
                'y':0.95,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            }
        )
        
        return fig
    
    @staticmethod
    def create_heatmap(df, x_col, y_col, value_col, title=None, x_title=None, y_title=None, colorscale='Viridis'):
        """
        Create a heatmap using Plotly
        
        Parameters:
        -----------
        df : pandas.DataFrame
            The dataframe containing the data
        x_col : str
            Column name for x-axis
        y_col : str
            Column name for y-axis
        value_col : str
            Column name for values (color intensity)
        title : str, optional
            Chart title
        x_title : str, optional
            X-axis title
        y_title : str, optional
            Y-axis title
        colorscale : str, optional
            Colorscale for the heatmap
            
        Returns:
        --------
        plotly.graph_objects.Figure
            The created heatmap
        """
        # Pivot the dataframe to create a matrix suitable for heatmap
        pivot_df = df.pivot_table(index=y_col, columns=x_col, values=value_col, aggfunc='mean')
        
        fig = go.Figure(data=go.Heatmap(
            z=pivot_df.values,
            x=pivot_df.columns,
            y=pivot_df.index,
            colorscale=colorscale
        ))
        
        fig.update_layout(
            template="plotly_white",
            xaxis_title=x_title or x_col,
            yaxis_title=y_title or y_col,
            title={
                'text': title or f"Heatmap of {value_col} by {x_col} and {y_col}",
                'y':0.95,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            }
        )
        
        return fig
    
    @staticmethod
    def create_choropleth_map(df, locations_col, color_col, title=None, location_mode='country names', colorscale='Viridis'):
        """
        Create a choropleth map using Plotly
        
        Parameters:
        -----------
        df : pandas.DataFrame
            The dataframe containing the data
        locations_col : str
            Column name for locations (countries, states, etc.)
        color_col : str
            Column name for color values
        title : str, optional
            Chart title
        location_mode : str, optional
            Mode for interpreting locations ('country names', 'ISO-3', 'USA-states', etc.)
        colorscale : str, optional
            Colorscale for the map
            
        Returns:
        --------
        plotly.graph_objects.Figure
            The created choropleth map
        """
        fig = px.choropleth(df, locations=locations_col, color=color_col,
                           locationmode=location_mode, color_continuous_scale=colorscale)
        
        fig.update_layout(
            template="plotly_white",
            title={
                'text': title or f"Geographic Distribution of {color_col}",
                'y':0.95,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            geo=dict(
                showframe=False,
                showcoastlines=True,
                projection_type='equirectangular'
            )
        )
        
        return fig
