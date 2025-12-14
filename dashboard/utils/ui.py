"""
UI Utilities for consistent styling across the dashboard
"""
import streamlit as st

def apply_styling():
    """Apply global CSS styling"""
    st.markdown("""
    <style>
        /* Global Styles */
        .stApp {
            background-color: #f8f9fa;
            background-image: linear-gradient(#e5e5e5 1px, transparent 1px),
            linear-gradient(90deg, #e5e5e5 1px, transparent 1px);
            background-size: 20px 20px;
        }

        /* Hide Streamlit Elements */
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
        .stDeployButton {display:none;}
        
        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: #ffffff;
            border-right: 1px solid #e0e0e0;
        }
        
        [data-testid="stSidebarNav"] {
            padding-top: 1rem;
        }
        
        /* Sidebar Links */
        [data-testid="stSidebarNav"] a {
            font-size: 1.2rem !important;
            padding: 1rem 1.5rem !important;
            margin-bottom: 0.5rem;
            border-radius: 8px;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
        }
        
        [data-testid="stSidebarNav"] a:hover {
            background-color: #f0f2f6;
            transform: translateX(5px);
        }
        
        /* Active Link */
        [data-testid="stSidebarNav"] a[aria-current="page"] {
            background-color: #e8f5e9;
            color: #01411C;
            font-weight: 600;
            border-left: 5px solid #28A745;
        }
        
        /* Sidebar Header/Title if any */
        .sidebar-title {
            font-size: 1.5rem;
            font-weight: 700;
            color: #01411C;
            padding: 1rem 0;
            text-align: center;
        }

        /* Recommendation Cards */
        .recommendation-card {
            background-color: white;
            padding: 1.5rem;
            border-radius: 10px;
            border-left: 5px solid #28A745;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            height: 100%;
            transition: transform 0.2s;
        }
        
        .recommendation-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(0,0,0,0.1);
        }
        
        /* Hero Section */
        .hero-container {
            background: linear-gradient(rgba(1, 65, 28, 0.9), rgba(10, 102, 56, 0.9)), url('https://images.unsplash.com/photo-1625246333195-78d9c38ad449?q=80&w=1740&auto=format&fit=crop');
            background-size: cover;
            background-position: center;
            padding: 3rem 2rem;
            border-radius: 15px;
            color: white;
            text-align: center;
            margin-bottom: 2rem;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }
        
        .hero-title {
            font-size: 3rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .hero-subtitle {
            font-size: 1.2rem;
            font-weight: 300;
            margin-bottom: 0;
            opacity: 0.9;
        }
        
        /* Vision Section */
        .vision-container {
            background-color: white;
            padding: 2rem;
            border-radius: 10px;
            border-left: 5px solid #01411C;
            margin: 2rem 0;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }
        
        .vision-title {
            color: #01411C;
            font-size: 1.8rem;
            font-weight: 600;
            margin-bottom: 1rem;
        }
        
        /* Metric Cards */
        .metric-card {
            background: white;
            padding: 1.5rem;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
            border-top: 4px solid #28A745;
        }
        
        .metric-card:hover {
            transform: translateY(-5px);
        }
        
        .metric-value {
            font-size: 2.5rem;
            font-weight: 700;
            color: #01411C;
            margin: 0.5rem 0;
        }
        
        .metric-label {
            color: #666;
            font-size: 1rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        /* Section Headers */
        .section-header {
            color: #01411C;
            font-size: 1.8rem;
            font-weight: 600;
            margin: 2rem 0 1rem 0;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid #28A745;
        }

        /* Interactive Section Headers */
        .interactive-header {
            color: #01411C;
            font-size: 2rem;
            font-weight: 700;
            margin: 2.5rem 0 1.5rem 0;
            padding-bottom: 0.5rem;
            border-bottom: 3px solid transparent;
            transition: all 0.3s ease;
            display: inline-block;
            cursor: default;
            position: relative;
        }
        
        .interactive-header:after {
            content: '';
            position: absolute;
            width: 0;
            height: 3px;
            bottom: 0;
            left: 0;
            background-color: #28A745;
            transition: width 0.3s ease;
        }

        .interactive-header:hover {
            color: #28A745;
            transform: translateX(10px);
        }
        
        .interactive-header:hover:after {
            width: 100%;
        }

        .interactive-subheader {
            color: #0A6638;
            font-size: 1.4rem;
            font-weight: 600;
            margin: 1.5rem 0 1rem 0;
            transition: all 0.3s ease;
            display: inline-block;
            border-left: 4px solid transparent;
            padding-left: 0;
        }
        
        .interactive-subheader:hover {
            color: #28A745;
            border-left: 4px solid #28A745;
            padding-left: 10px;
        }
        
        /* Card Styling */
        .custom-card {
            background: white;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            border-top: 3px solid #28A745;
            margin-bottom: 1rem;
        }
        
        /* Filter/Input Section */
        .filter-container {
            background-color: white;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            margin-bottom: 2rem;
            border-left: 5px solid #01411C;
        }
        
        /* Metrics */
        .stMetric {
            background-color: white;
            padding: 1rem;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
            border: 1px solid #eee;
        }
        
        /* Buttons */
        .stButton button {
            background-color: #01411C;
            color: white;
            font-weight: 600;
            border-radius: 5px;
            padding: 0.5rem 2rem;
            border: none;
            transition: all 0.3s ease;
        }
        
        .stButton button:hover {
            background-color: #0A6638;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }
        
        /* Footer */
        .footer {
            text-align: center;
            color: #666;
            padding: 3rem 0;
            margin-top: 3rem;
            border-top: 1px solid #eee;
        }
    </style>
    """, unsafe_allow_html=True)

def create_page_header(title, subtitle):
    """Create a consistent page header"""
    st.markdown(f"""
    <div class="hero-container">
        <h1 class="hero-title">{title}</h1>
        <p class="hero-subtitle">{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)

def create_interactive_header(text, level=2):
    """Create an interactive section header"""
    if level == 2:
        st.markdown(f'<h2 class="interactive-header">{text}</h2>', unsafe_allow_html=True)
    else:
        st.markdown(f'<h3 class="interactive-subheader">{text}</h3>', unsafe_allow_html=True)
