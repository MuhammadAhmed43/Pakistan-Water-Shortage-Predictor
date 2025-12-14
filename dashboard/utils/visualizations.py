"""
Visualization utilities for charts and graphs
"""
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
import config

def create_water_balance_chart(rainfall, crop_water_demand, crop_name):
    """Create bar chart comparing rainfall vs crop water demand"""
    fig = go.Figure(data=[
        go.Bar(name='Rainfall', x=['Water Sources'], y=[rainfall], marker_color='#1f77b4'),
        go.Bar(name='Crop Water Demand', x=['Water Sources'], y=[crop_water_demand], marker_color='#ff7f0e')
    ])
    
    fig.update_layout(
        title=f'Water Balance for {crop_name}',
        yaxis_title='Water (mm)',
        barmode='group',
        height=400,
        showlegend=True
    )
    
    return fig

def create_shortage_gauge(wsi_value):
    """Create gauge chart for Water Sufficiency Index (WSI)"""
    # Determine color based on WSI (Higher is Better)
    if wsi_value >= 100:
        color = config.SEVERITY_COLORS["No Shortage"]
    elif wsi_value >= 80:
        color = config.SEVERITY_COLORS["Mild"]
    elif wsi_value >= 60:
        color = config.SEVERITY_COLORS["Moderate"]
    elif wsi_value >= 40:
        color = config.SEVERITY_COLORS["Severe"]
    else:
        color = config.SEVERITY_COLORS["Critical"]
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = wsi_value,
        title = {'text': "Water Sufficiency Index (WSI)"},
        gauge = {
            'axis': {'range': [None, 120]}, # Go a bit above 100
            'bar': {'color': color},
            'steps': [
                {'range': [0, 40], 'color': "#ffcdd2"},   # Red (Critical)
                {'range': [40, 60], 'color': "#ffccbc"},  # Orange (Severe)
                {'range': [60, 80], 'color': "#ffe0b2"},  # Yellow (Moderate)
                {'range': [80, 100], 'color': "#fff3cd"}, # Light Green/Yellow (Mild)
                {'range': [100, 120], 'color': "#e8f5e9"} # Green (No Shortage)
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 40 # Critical threshold
            }
        }
    ))
    
    fig.update_layout(height=300)
    return fig

def create_district_comparison_chart(data_df):
    """Create bar chart comparing shortage across districts"""
    fig = px.bar(
        data_df.sort_values('water_shortage_index', ascending=False).head(15),
        x='District',
        y='water_shortage_index',
        color='shortage_category',
        title='Top 15 Districts by Water Shortage',
        labels={'water_shortage_index': 'Shortage Index', 'District': 'District'},
        color_discrete_map=config.SEVERITY_COLORS,
        height=500
    )
    
    fig.update_layout(xaxis_tickangle=-45)
    return fig

def create_crop_comparison_chart(data_df):
    """Create bar chart comparing water demand by crop"""
    crop_avg = data_df.groupby('Crop')['Crop_Water_Demand_mm'].mean().sort_values(ascending=False)
    
    fig = px.bar(
        x=crop_avg.index,
        y=crop_avg.values,
        title='Average Crop Water Demand by Crop Type',
        labels={'x': 'Crop', 'y': 'Water Demand (mm)'},
        color=crop_avg.values,
        color_continuous_scale='Blues',
        height=500
    )
    
    fig.update_layout(xaxis_tickangle=-45, showlegend=False)
    return fig

def create_seasonal_trend_chart(monthly_stats, monthly_demand, current_month, district_name, crop_name):
    """Create line chart comparing Rainfall vs Crop Demand over the year"""
    import calendar
    
    # Merge data
    merged = pd.merge(monthly_stats, monthly_demand, on='Month', how='outer')
    # Sort by month to ensure line is drawn correctly
    merged = merged.sort_values('Month')
    
    # Create month names for ticks
    month_names = [calendar.month_abbr[i] for i in range(1, 13)]
    
    fig = go.Figure()
    
    # Rainfall Line
    fig.add_trace(go.Scatter(
        x=merged['Month'], 
        y=merged['Rainfall'],
        mode='lines+markers',
        name='Avg Rainfall',
        line=dict(color='#1f77b4', width=3),
        fill='tozeroy',
        fillcolor='rgba(31, 119, 180, 0.1)'
    ))
    
    # Demand Line
    fig.add_trace(go.Scatter(
        x=merged['Month'], 
        y=merged['Crop_Water_Demand_mm'],
        mode='lines+markers',
        name=f'{crop_name} Demand',
        line=dict(color='#ff7f0e', width=3, dash='dot')
    ))
    
    # Highlight current month
    # Use integer x-axis to avoid Plotly categorical axis issues with add_vline
    fig.add_vline(x=current_month, line_width=2, line_dash="dash", line_color="green", annotation_text="Current")
    
    fig.update_layout(
        title=f'Seasonal Water Profile: {district_name} vs {crop_name}',
        xaxis_title='Month',
        yaxis_title='Water (mm)',
        height=400,
        hovermode="x unified",
        xaxis=dict(
            tickmode='array',
            tickvals=list(range(1, 13)),
            ticktext=month_names
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig

def create_water_source_pie_chart(effective_supply, deficit, irrigation=0):
    """Create pie chart showing water supply vs deficit"""
    
    if irrigation > 0:
        rainfall_supply = max(0, effective_supply - irrigation)
        labels = ['Rainfall Supply', 'Irrigation', 'Water Deficit']
        values = [rainfall_supply, irrigation, max(0, deficit)]
        colors = ['#2ca02c', '#1f77b4', '#d62728'] # Green, Blue, Red
    else:
        labels = ['Effective Water Supply', 'Water Deficit']
        values = [effective_supply, max(0, deficit)]
        colors = ['#2ca02c', '#d62728'] # Green, Red
    
    fig = go.Figure(data=[go.Pie(
        labels=labels, 
        values=values,
        marker_colors=colors,
        hole=.4,
        textinfo='label+percent'
    )])
    
    fig.update_layout(
        title='Water Balance Composition',
        height=300,
        margin=dict(t=40, b=20, l=20, r=20),
        showlegend=False
    )
    
    return fig

def create_time_series_chart(data_df, district=None):
    """Create time series chart of water shortage over time"""
    if district:
        filtered_df = data_df[data_df['District'] == district]
        title = f'Water Shortage Trend - {district}'
    else:
        filtered_df = data_df
        title = 'Water Shortage Trend - All Districts'
    
    # Group by date if available
    if 'Date' in filtered_df.columns:
        time_col = 'Date'
    elif 'Year' in filtered_df.columns and 'Month' in filtered_df.columns:
        filtered_df['Date'] = pd.to_datetime(
            filtered_df['Year'].astype(str) + '-' + 
            filtered_df['Month'].astype(str).str.zfill(2) + '-01'
        )
        time_col = 'Date'
    else:
        return None
    
    fig = px.line(
        filtered_df.groupby(time_col)['water_shortage_index'].mean().reset_index(),
        x=time_col,
        y='water_shortage_index',
        title=title,
        labels={'water_shortage_index': 'Shortage Index', time_col: 'Date'},
        height=400
    )
    
    # Add horizontal lines for thresholds
    fig.add_hline(y=20, line_dash="dash", line_color="green", annotation_text="Mild")
    fig.add_hline(y=40, line_dash="dash", line_color="orange", annotation_text="Moderate")
    fig.add_hline(y=60, line_dash="dash", line_color="red", annotation_text="Severe")
    
    return fig

def create_monthly_heatmap(data_df):
    """Create heatmap of shortage by month"""
    if 'Month' not in data_df.columns or 'District' not in data_df.columns:
        return None
    
    pivot_df = data_df.pivot_table(
        values='water_shortage_index',
        index='District',
        columns='Month',
        aggfunc='mean'
    )
    
    fig = px.imshow(
        pivot_df,
        labels=dict(x="Month", y="District", color="Shortage Index"),
        title='Water Shortage by District and Month',
        color_continuous_scale='RdYlGn_r',
        height=600
    )
    
    return fig
