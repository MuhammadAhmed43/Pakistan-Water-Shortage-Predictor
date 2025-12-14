"""
Pakistan map generator using Folium
"""
import folium
from folium import plugins
import pandas as pd
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
import config

def create_pakistan_map(shortage_data=None):
    """
    Create interactive map of Pakistan with district markers
    
    Args:
        shortage_data: DataFrame with columns ['District', 'water_shortage_index', 'shortage_category']
    
    Returns:
        folium.Map object
    """
    # Create base map centered on Pakistan
    m = folium.Map(
        location=config.PAKISTAN_CENTER,
        zoom_start=config.MAP_ZOOM,
        tiles='OpenStreetMap'
    )
    
    # Add fullscreen button
    plugins.Fullscreen().add_to(m)
    
    # If shortage data provided, add markers for each district
    if shortage_data is not None and not shortage_data.empty:
        for _, row in shortage_data.iterrows():
            district = row['District']
            if district in config.DISTRICT_COORDS:
                coords = config.DISTRICT_COORDS[district]
                shortage_index = row.get('water_shortage_index', 0)
                category = row.get('shortage_category', 'No shortage')
                color = config.SEVERITY_COLORS.get(category, '#999999')
                
                # Create popup content
                popup_html = f"""
                <div style='width: 200px; font-family: Arial;'>
                    <h4 style='margin: 0; color: {color};'>{district}</h4>
                    <hr style='margin: 5px 0;'>
                    <p style='margin: 5px 0;'><b>WSI:</b> {shortage_index:.2f}</p>
                    <p style='margin: 5px 0;'><b>Category:</b> {category}</p>
                    <p style='margin: 5px 0;'><b>Crop:</b> {row.get('Crop', 'N/A')}</p>
                    <hr style='margin: 5px 0;'>
                    <p style='margin: 5px 0;'><b>Rainfall:</b> {row.get('rainfall_pred', 0):.1f} mm</p>
                    <p style='margin: 5px 0;'><b>Irrigation:</b> {row.get('irrigation_added', 0):.1f} mm</p>
                    <p style='margin: 5px 0;'><b>Effective Supply:</b> {row.get('effective_supply', 0):.1f} mm</p>
                    <p style='margin: 5px 0;'><b>Demand:</b> {row.get('crop_demand', 0):.1f} mm</p>
                </div>
                """
                
                # Detailed Tooltip (HTML)
                tooltip_html = f"""
                <div style="font-family: Arial; font-size: 12px;">
                    <b>{district}</b> ({category})<br>
                    WSI: {shortage_index:.2f}<br>
                    Rainfall: {row.get('rainfall_pred', 0):.1f} mm<br>
                    Irrigation: {row.get('irrigation_added', 0):.1f} mm<br>
                    Supply: {row.get('effective_supply', 0):.1f} mm<br>
                    Demand: {row.get('crop_demand', 0):.1f} mm<br>
                    Temp: {row.get('temperature', 0):.1f}°C
                </div>
                """
                
                # Add circle marker
                folium.CircleMarker(
                    location=coords,
                    radius=10 + (shortage_index / 20),  # Size based on shortage (scaled down for 0-100)
                    popup=folium.Popup(popup_html, max_width=250),
                    tooltip=folium.Tooltip(tooltip_html, sticky=True),
                    color=color,
                    fillColor=color,
                    fillOpacity=0.7,
                    weight=2
                ).add_to(m)
    else:
        # Just add markers for all districts
        for district, coords in config.DISTRICT_COORDS.items():
            folium.Marker(
                location=coords,
                popup=district,
                tooltip=district,
                icon=folium.Icon(color='blue', icon='info-sign')
            ).add_to(m)
    
    # Add legend
    legend_html = create_legend()
    m.get_root().html.add_child(folium.Element(legend_html))
    
    return m

def create_legend():
    """Create HTML legend for the map"""
    legend_html = '''
    <div style="position: fixed; 
                bottom: 50px; 
                right: 50px; 
                width: 200px; 
                background-color: white; 
                border:2px solid grey; 
                z-index:9999; 
                font-size:14px;
                padding: 10px;
                border-radius: 5px;
                box-shadow: 0 0 15px rgba(0,0,0,0.2);">
        <h4 style="margin:0 0 10px 0;">Water Shortage</h4>
        <div style="margin: 5px 0;">
            <span style="background:#28A745; padding: 2px 8px; border-radius: 3px; color: white;">●</span> No Shortage (>100)
        </div>
        <div style="margin: 5px 0;">
            <span style="background:#17A2B8; padding: 2px 8px; border-radius: 3px; color: white;">●</span> Mild (80-100)
        </div>
        <div style="margin: 5px 0;">
            <span style="background:#FFC107; padding: 2px 8px; border-radius: 3px; color: black;">●</span> Moderate (60-80)
        </div>
        <div style="margin: 5px 0;">
            <span style="background:#FD7E14; padding: 2px 8px; border-radius: 3px; color: white;">●</span> Severe (40-60)
        </div>
        <div style="margin: 5px 0;">
            <span style="background:#DC3545; padding: 2px 8px; border-radius: 3px; color: white;">●</span> Critical (0-40)
        </div>
    </div>
    '''
    return legend_html

def create_multi_district_map(predictions_df):
    """
    Create map with multiple district predictions
    
    Args:
        predictions_df: DataFrame with predictions for multiple districts
    
    Returns:
        folium.Map object
    """
    return create_pakistan_map(predictions_df)
