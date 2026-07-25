import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os
import base64
from PIL import Image

# Set Streamlit Page Configuration
st.set_page_config(
    page_title="Excelerate Opportunity Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Brand Color Palette
PRIMARY_COLOR = "#f94c44"
SECONDARY_COLOR = "#f14159"
ACCENT_COLOR = "#e7306b"
DARK_TEXT_COLOR = "#1e293b"
LIGHT_BG_COLOR = "#f8fafc"

# Custom CSS for Premium UI Styling
def inject_custom_css():
    # Convert local logo image to base64 for sidebar rendering
    logo_b64 = ""
    logo_path = os.path.join(os.path.dirname(__file__), "assets", "logo.png")
    if os.path.exists(logo_path):
        try:
            with open(logo_path, "rb") as f:
                logo_b64 = base64.b64encode(f.read()).decode()
        except Exception as e:
            pass

    st.markdown(
        f"""
        <style>
        /* Import Google Font */
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');
        
        html, body, [class*="css"], .stApp {{
            font-family: 'Outfit', sans-serif;
            color: {DARK_TEXT_COLOR};
        }}

        /* Sidebar Styling with Gradient */
        [data-testid="stSidebar"] {{
            background: linear-gradient(180deg, {PRIMARY_COLOR} 0%, {SECONDARY_COLOR} 50%, {ACCENT_COLOR} 100%);
            color: white !important;
            border-right: none;
        }}

        /* Make sidebar text and labels white */
        [data-testid="stSidebar"] label, 
        [data-testid="stSidebar"] p, 
        [data-testid="stSidebar"] span,
        [data-testid="stSidebar"] .stRadio div {{
            color: white !important;
        }}

        /* Sidebar Uploader text custom style */
        [data-testid="stSidebar"] .stMarkdown h3, 
        [data-testid="stSidebar"] .stMarkdown p {{
            color: white !important;
        }}
        
        /* Stylized Sidebar Radio Buttons */
        div[data-testid="stSidebarUserContent"] .stRadio div[role="radiogroup"] {{
            gap: 10px;
        }}
        
        div[data-testid="stSidebarUserContent"] .stRadio div[role="radiogroup"] label {{
            background-color: rgba(255, 255, 255, 0.1);
            padding: 10px 16px;
            border-radius: 8px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            transition: all 0.3s ease;
            cursor: pointer;
            width: 100%;
        }}
        
        div[data-testid="stSidebarUserContent"] .stRadio div[role="radiogroup"] label:hover {{
            background-color: rgba(255, 255, 255, 0.2);
            transform: translateX(5px);
        }}
        
        div[data-testid="stSidebarUserContent"] .stRadio div[role="radiogroup"] label[data-checked="true"] {{
            background-color: white !important;
            color: {PRIMARY_COLOR} !important;
            font-weight: 700 !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }}
        
        div[data-testid="stSidebarUserContent"] .stRadio div[role="radiogroup"] label[data-checked="true"] p {{
            color: {PRIMARY_COLOR} !important;
            font-weight: 700 !important;
        }}

        /* Content Area Adjustments */
        .block-container {{
            padding-top: 1.5rem;
            padding-bottom: 2rem;
            padding-left: 2rem;
            padding-right: 2rem;
        }}

        /* Styled headers */
        h1, h2, h3, h4, h5, h6 {{
            color: {PRIMARY_COLOR};
            font-weight: 700;
        }}

        /* Hide Streamlit default styling elements */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        header {{visibility: hidden;}}

        /* White rounded box for Logo */
        .logo-container {{
            background-color: white;
            padding: 15px;
            border-radius: 12px;
            margin-bottom: 25px;
            display: flex;
            justify-content: center;
            align-items: center;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        }}
        .logo-img {{
            max-width: 90%;
            height: auto;
        }}

        /* Filter headers in Sidebar */
        .sidebar-section-title {{
            font-size: 1.1rem;
            font-weight: 700;
            margin-top: 20px;
            margin-bottom: 10px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.3);
            padding-bottom: 5px;
            color: white;
        }}

        /* KPI Card styling */
        .kpi-card {{
            background-color: white;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.05);
            display: flex;
            align-items: center;
            border-left: 5px solid {PRIMARY_COLOR};
            margin-bottom: 15px;
            transition: transform 0.2s ease;
        }}
        .kpi-card:hover {{
            transform: translateY(-3px);
            box-shadow: 0 6px 20px rgba(0,0,0,0.08);
        }}
        .kpi-icon {{
            font-size: 2.2rem;
            margin-right: 20px;
            color: {PRIMARY_COLOR};
            display: flex;
            align-items: center;
        }}
        .kpi-value {{
            font-size: 1.8rem;
            font-weight: 800;
            color: {PRIMARY_COLOR};
            line-height: 1.1;
        }}
        .kpi-label {{
            font-size: 0.85rem;
            color: #64748b;
            font-weight: 600;
            margin-top: 3px;
        }}

        /* Table Styling */
        div[data-testid="stDataFrame"] {{
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

    # Render Sidebar Logo Container
    if logo_b64:
        st.sidebar.markdown(
            f"""
            <div class="logo-container">
                <img src="data:image/png;base64,{logo_b64}" class="logo-img" alt="Excelerate Logo">
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        # Fallback text logo if file doesn't exist
        st.sidebar.markdown(
            f"""
            <div class="logo-container">
                <h2 style="color:{PRIMARY_COLOR}; margin:0; font-weight:800; letter-spacing:-1px;">Excelerate</h2>
            </div>
            """,
            unsafe_allow_html=True
        )

# Helper function to format big numbers (e.g. 6000 -> 6K)
def format_kpi_value(val):
    if val >= 1000000:
        return f"{val/1000000:.1f}M".replace(".0", "")
    elif val >= 1000:
        return f"{val/1000:.1f}K".replace(".0", "")
    return str(val)

# Custom KPI Card Renderer
def render_kpi_card(value, label, icon_svg):
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-icon">
                {icon_svg}
            </div>
            <div>
                <div class="kpi-value">{value}</div>
                <div class="kpi-label">{label}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# Inline SVG icons colored with PRIMARY_COLOR (#f94c44)
ICONS = {
    "opportunities": """
        <svg xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="m8 3 4 8 5-5 5 15H2L8 3z"/>
        </svg>
    """,
    "categories": """
        <svg xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M21.21 15.89A10 10 0 1 1 8 2.83"/>
            <path d="M22 12A10 10 0 0 0 12 2v10z"/>
        </svg>
    """,
    "scholarships": """
        <svg xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M21.42 10.922a1 1 0 0 0-.019-1.838L12.83 5.18a2 2 0 0 0-1.66 0L2.6 9.08a1 1 0 0 0 0 1.832l8.57 3.908a2 2 0 0 0 1.66 0z"/>
            <path d="M6 12v5c0 2 2 3 6 3s6-1 6-3v-5"/>
            <circle cx="12" cy="17" r="2" fill="currentColor"/>
        </svg>
    """,
    "locations": """
        <svg xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/>
            <circle cx="12" cy="10" r="3"/>
        </svg>
    """
}

# Standardize Columns of the Dataframe
def standardize_columns(df):
    col_mapping = {}
    for col in df.columns:
        col_lower = col.lower().strip()
        if col_lower == 'opportunity_id' or col_lower == 'opportunity id' or col_lower == 'opp_id':
            col_mapping[col] = 'opportunity_id'
        elif col_lower == 'name' or col_lower == 'opportunity_name' or col_lower == 'title':
            col_mapping[col] = 'name'
        elif col_lower == 'category' or col_lower == 'opportunity_category':
            col_mapping[col] = 'category'
        elif col_lower in ['fee', 'sum of fee', 'opportunity_fee', 'cost']:
            col_mapping[col] = 'Sum of fee'
        elif col_lower in ['currency', 'currency_type', 'currency type']:
            col_mapping[col] = 'currency_type'
        elif col_lower in ['microscholarship', 'sum of microscholarship', 'scholarship', 'scholarship_amount']:
            col_mapping[col] = 'Sum of microscholarship'
        elif col_lower in ['duration', 'sum of duration', 'duration_value']:
            col_mapping[col] = 'Sum of duration'
        elif col_lower in ['duration_type', 'duration type']:
            col_mapping[col] = 'duration_type'
        elif col_lower in ['duration_category', 'duration category']:
            col_mapping[col] = 'duration_category'
        elif col_lower == 'location':
            col_mapping[col] = 'location'
        elif col_lower == 'year':
            col_mapping[col] = 'Year'
        elif col_lower == 'month':
            col_mapping[col] = 'Month'
        elif col_lower == 'day':
            col_mapping[col] = 'Day'
        elif col_lower in ['is_auto_approve', 'auto_approve', 'auto approve', 'is auto approve', 'auto-approve']:
            col_mapping[col] = 'is_auto_approve'
            
    df = df.rename(columns=col_mapping)
    
    # Ensure critical columns exist
    if 'opportunity_id' not in df.columns:
        df['opportunity_id'] = [f"OPP-{i}" for i in range(1, len(df)+1)]
    if 'category' not in df.columns:
        df['category'] = 'Uncategorized'
    if 'Sum of fee' not in df.columns:
        df['Sum of fee'] = 0
    if 'Sum of microscholarship' not in df.columns:
        df['Sum of microscholarship'] = 0
    if 'location' not in df.columns:
        df['location'] = 'Virtual'
    if 'duration_category' not in df.columns:
        # Infer duration category from duration value if possible
        if 'Sum of duration' in df.columns and 'duration_type' in df.columns:
            def infer_duration_cat(row):
                val = row['Sum of duration']
                t = str(row['duration_type']).lower()
                if 'hour' in t:
                    return 'Less than 1 Day'
                elif 'day' in t:
                    return 'Less than 1 Day' if val <= 1 else '1 Week'
                elif 'week' in t:
                    return '1 Week' if val <= 1 else '1 Month'
                elif 'month' in t:
                    return '1 Month' if val < 12 else '1 Year'
                elif 'year' in t:
                    return '1 Year' if val <= 1 else 'Long Term'
                return 'Less than 1 Day'
            df['duration_category'] = df.apply(infer_duration_cat, axis=1)
        else:
            df['duration_category'] = 'Less than 1 Day'
            
    # Set default values for other missing columns
    if 'currency_type' not in df.columns:
        df['currency_type'] = 'USD'
    if 'is_auto_approve' not in df.columns:
        df['is_auto_approve'] = True
    if 'Year' not in df.columns:
        df['Year'] = 2026
    if 'Month' not in df.columns:
        df['Month'] = 'July'
    if 'Day' not in df.columns:
        df['Day'] = 1
        
    return df

# Main logic
def main():
    # Inject styling
    inject_custom_css()
    
    # ---------------------------------------------------------
    # SIDEBAR NAVIGATION
    # ---------------------------------------------------------
    st.sidebar.markdown('<div class="sidebar-section-title">Navigation</div>', unsafe_allow_html=True)
    page = st.sidebar.radio(
        label="Select Dashboard Page",
        options=["Overview", "Insight"],
        label_visibility="collapsed"
    )
    
    # ---------------------------------------------------------
    # SIDEBAR DATA LOADER
    # ---------------------------------------------------------
    st.sidebar.markdown('<div class="sidebar-section-title">Data Source</div>', unsafe_allow_html=True)
    
    # File Uploader
    uploaded_file = st.sidebar.file_uploader(
        "Upload custom opportunity data (.csv or .xlsx)",
        type=["csv", "xlsx"]
    )
    
    # Load raw data
    data_loaded_msg = ""
    df_raw = None
    
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith(".xlsx"):
                df_raw = pd.read_excel(uploaded_file)
            else:
                df_raw = pd.read_csv(uploaded_file)
            data_loaded_msg = "✅ Using uploaded dataset"
        except Exception as e:
            st.sidebar.error(f"Error loading file: {e}")
            
    if df_raw is None:
        # Fallback to local file or auto-generated mock file
        local_csv_path = os.path.join(os.path.dirname(__file__), "opportunityData.csv")
        if os.path.exists(local_csv_path):
            try:
                df_raw = pd.read_csv(local_csv_path)
                data_loaded_msg = "ℹ️ Using default opportunityData.csv"
            except Exception as e:
                st.sidebar.error(f"Error loading default CSV: {e}")
        else:
            st.sidebar.warning("No data file found. Place opportunityData.csv in this directory or upload one.")
            st.stop()
            
    # Display loading status
    st.sidebar.markdown(f"<small style='color:white;'>{data_loaded_msg}</small>", unsafe_allow_html=True)
    
    # Standardize columns
    df = standardize_columns(df_raw.copy())
    
    # ---------------------------------------------------------
    # SIDEBAR FILTERS
    # ---------------------------------------------------------
    st.sidebar.markdown('<div class="sidebar-section-title">Interactive Filters</div>', unsafe_allow_html=True)
    
    # Filter 1: Opportunity Type (Free vs Paid)
    op_type_filter = st.sidebar.radio(
        "Opportunity Type",
        options=["All", "Free Only", "Paid Only"],
        index=0
    )
    
    # Filter 2: Category
    categories_available = sorted(df['category'].dropna().unique())
    selected_categories = st.sidebar.multiselect(
        "Categories",
        options=categories_available,
        default=categories_available
    )
    
    # Filter 3: Location
    locations_available = sorted(df['location'].dropna().unique())
    selected_locations = st.sidebar.multiselect(
        "Locations",
        options=locations_available,
        default=locations_available
    )
    
    # Filter 4: Duration Category
    durations_available = sorted(df['duration_category'].dropna().unique())
    selected_durations = st.sidebar.multiselect(
        "Duration Category",
        options=durations_available,
        default=durations_available
    )
    
    # Filter 5: Auto-Approve Status
    auto_approve_filter = st.sidebar.radio(
        "Auto Approval Status",
        options=["All", "Auto-Approved Only", "Manual Approval Only"],
        index=0
    )
    
    # Apply Filters to DataFrame
    filtered_df = df.copy()
    
    # Filter by Opportunity Type
    if op_type_filter == "Free Only":
        filtered_df = filtered_df[filtered_df['Sum of fee'] == 0]
    elif op_type_filter == "Paid Only":
        filtered_df = filtered_df[filtered_df['Sum of fee'] > 0]
        
    # Filter by Categories
    if selected_categories:
        filtered_df = filtered_df[filtered_df['category'].isin(selected_categories)]
    else:
        filtered_df = filtered_df.iloc[0:0] # empty if nothing selected
        
    # Filter by Locations
    if selected_locations:
        filtered_df = filtered_df[filtered_df['location'].isin(selected_locations)]
    else:
        filtered_df = filtered_df.iloc[0:0]
        
    # Filter by Duration Category
    if selected_durations:
        filtered_df = filtered_df[filtered_df['duration_category'].isin(selected_durations)]
    else:
        filtered_df = filtered_df.iloc[0:0]
        
    # Filter by Auto Approval Status
    if auto_approve_filter == "Auto-Approved Only":
        filtered_df = filtered_df[filtered_df['is_auto_approve'] == True]
    elif auto_approve_filter == "Manual Approval Only":
        filtered_df = filtered_df[filtered_df['is_auto_approve'] == False]
        
    # ---------------------------------------------------------
    # MAIN CONTENT PANEL
    # ---------------------------------------------------------
    
    # Header Banner Area
    st.markdown(
        f"""
        <div style="margin-bottom: 25px;">
            <h1 style="margin: 0; font-size: 2.2rem; font-weight: 800; letter-spacing: -0.5px; background: linear-gradient(90deg, {PRIMARY_COLOR}, {ACCENT_COLOR}); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                Excelerate Learning Platform
            </h1>
            <p style="margin: 5px 0 0 0; color: #64748b; font-size: 1rem; font-weight: 500;">
                Opportunity Catalog Analysis & Strategic Operations Dashboard
            </p>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    if filtered_df.empty:
        st.warning("⚠️ No opportunities match the selected filter criteria. Please adjust your filters in the sidebar.")
        st.stop()
        
    # Page Routing
    if page == "Overview":
        # ---------------------------------------------------------
        # PAGE 1: OVERVIEW
        # ---------------------------------------------------------
        
        # 1. Row of KPI Cards
        col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)
        
        # Aggregate KPI figures
        tot_opps = len(filtered_df)
        tot_cats = filtered_df['category'].nunique()
        # Scholarship counts (microscholarship > 0)
        tot_scholarships = len(filtered_df[filtered_df['Sum of microscholarship'] > 0])
        tot_locations = filtered_df['location'].nunique()
        
        with col_kpi1:
            render_kpi_card(
                value=format_kpi_value(tot_opps),
                label="Total Opportunities",
                icon_svg=ICONS["opportunities"]
            )
        with col_kpi2:
            render_kpi_card(
                value=format_kpi_value(tot_cats),
                label="Total Categories",
                icon_svg=ICONS["categories"]
            )
        with col_kpi3:
            render_kpi_card(
                value=format_kpi_value(tot_scholarships),
                label="Scholarship Opportunities",
                icon_svg=ICONS["scholarships"]
            )
        with col_kpi4:
            render_kpi_card(
                value=format_kpi_value(tot_locations),
                label="Total Locations",
                icon_svg=ICONS["locations"]
            )
            
        st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
        
        # 2. Charts Row 1
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            st.markdown(f"<h3 style='font-size:1.15rem; color:{PRIMARY_COLOR}; margin-bottom: 10px;'>Count of opportunity_id by Duration Category</h3>", unsafe_allow_html=True)
            
            # Group by duration category and count
            dur_counts = filtered_df['duration_category'].value_counts().reset_index()
            dur_counts.columns = ['Duration Category', 'Count']
            
            # Sort categories properly
            sort_order = ["Less than 1 Day", "1 Week", "1 Month", "1 Year", "Long Term"]
            dur_counts['Duration Category'] = pd.Categorical(dur_counts['Duration Category'], categories=sort_order, ordered=True)
            dur_counts = dur_counts.sort_values('Duration Category')
            
            # Convert counts to K formatting labels
            dur_counts['Label'] = dur_counts['Count'].apply(format_kpi_value)
            
            fig1 = px.bar(
                dur_counts,
                x='Duration Category',
                y='Count',
                text='Label',
                color_discrete_sequence=[PRIMARY_COLOR]
            )
            fig1.update_traces(
                textposition='outside', 
                textfont=dict(size=11, color='#1e293b', family='Outfit'),
                cliponaxis=False,
                marker=dict(line=dict(width=0))
            )
            fig1.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=10, r=10, t=10, b=10),
                height=260,
                xaxis_title="",
                yaxis_title="",
                xaxis=dict(showgrid=False, linecolor='#e2e8f0', tickfont=dict(size=11, family='Outfit')),
                yaxis=dict(showgrid=True, gridcolor='#f1f5f9', linecolor='rgba(0,0,0,0)', showticklabels=False),
                showlegend=False
            )
            st.plotly_chart(fig1, use_container_width=True, config={'displayModeBar': False})
            
        with col_chart2:
            st.markdown(f"<h3 style='font-size:1.15rem; color:{PRIMARY_COLOR}; margin-bottom: 10px;'>Count of opportunity_id by location</h3>", unsafe_allow_html=True)
            
            # Group by location and count (top 8)
            loc_counts = filtered_df['location'].value_counts().reset_index()
            loc_counts.columns = ['location', 'Count']
            loc_counts = loc_counts.sort_values('Count', ascending=True)
            
            # Use top 10 locations to keep it clean, group the rest
            if len(loc_counts) > 10:
                others_sum = loc_counts.iloc[:-9]['Count'].sum()
                top_locs = loc_counts.iloc[-9:].copy()
                others_df = pd.DataFrame([{'location': 'Other Locations', 'Count': others_sum}])
                loc_counts = pd.concat([others_df, top_locs], ignore_index=True)
                
            loc_counts['Label'] = loc_counts['Count'].apply(format_kpi_value)
            
            fig2 = px.bar(
                loc_counts,
                x='Count',
                y='location',
                orientation='h',
                text='Label',
                color_discrete_sequence=[PRIMARY_COLOR]
            )
            fig2.update_traces(
                textposition='outside',
                textfont=dict(size=11, color='#1e293b', family='Outfit'),
                cliponaxis=False,
                marker=dict(line=dict(width=0))
            )
            fig2.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=10, r=40, t=10, b=10),
                height=260,
                xaxis_title="",
                yaxis_title="",
                yaxis=dict(showgrid=False, linecolor='#e2e8f0', tickfont=dict(size=11, family='Outfit')),
                xaxis=dict(showgrid=True, gridcolor='#f1f5f9', linecolor='rgba(0,0,0,0)', showticklabels=False),
                showlegend=False
            )
            st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})
            
        # 3. Charts Row 2
        col_chart3, col_chart4 = st.columns(2)
        
        with col_chart3:
            st.markdown(f"<h3 style='font-size:1.15rem; color:{PRIMARY_COLOR}; margin-bottom: 10px;'>Count of opportunity_id by Opportunity Type</h3>", unsafe_allow_html=True)
            
            # Determine Free vs Paid counts
            free_count = len(filtered_df[filtered_df['Sum of fee'] == 0])
            paid_count = len(filtered_df[filtered_df['Sum of fee'] > 0])
            total_type_count = free_count + paid_count
            
            type_df = pd.DataFrame({
                'Opportunity Type': ['Free', 'Paid'],
                'Count': [free_count, paid_count]
            })
            type_df = type_df[type_df['Count'] > 0]
            
            # Define colors
            donut_colors = [PRIMARY_COLOR, '#fca5a5']
            
            fig3 = go.Figure(data=[go.Pie(
                labels=type_df['Opportunity Type'],
                values=type_df['Count'],
                hole=0.55,
                marker=dict(colors=donut_colors),
                textinfo='percent+value',
                textposition='outside',
                textfont=dict(size=11, family='Outfit', color='#1e293b'),
                direction='clockwise',
                sort=False
            )])
            fig3.update_layout(
                showlegend=True,
                legend=dict(
                    orientation="v",
                    yanchor="center",
                    y=0.5,
                    xanchor="left",
                    x=1.02,
                    font=dict(size=11, family='Outfit', color='#1e293b')
                ),
                margin=dict(l=10, r=80, t=10, b=10),
                height=260,
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig3, use_container_width=True, config={'displayModeBar': False})
            
        with col_chart4:
            st.markdown(f"<h3 style='font-size:1.15rem; color:{PRIMARY_COLOR}; margin-bottom: 10px;'>Count of opportunities by category</h3>", unsafe_allow_html=True)
            
            # Group by category
            cat_counts = filtered_df['category'].value_counts().reset_index()
            cat_counts.columns = ['category', 'Count']
            cat_counts = cat_counts.sort_values('Count', ascending=True)
            
            # Keep top 8 categories, group others if many
            if len(cat_counts) > 8:
                others_sum = cat_counts.iloc[:-7]['Count'].sum()
                top_cats = cat_counts.iloc[-7:].copy()
                others_df = pd.DataFrame([{'category': 'Other Categories', 'Count': others_sum}])
                cat_counts = pd.concat([others_df, top_cats], ignore_index=True)
                
            cat_counts['Label'] = cat_counts['Count'].apply(format_kpi_value)
            
            fig4 = px.bar(
                cat_counts,
                x='Count',
                y='category',
                orientation='h',
                text='Count', # show exact count as requested in category horizontal bar chart
                color_discrete_sequence=[PRIMARY_COLOR]
            )
            fig4.update_traces(
                textposition='outside',
                textfont=dict(size=11, color='#1e293b', family='Outfit'),
                cliponaxis=False,
                marker=dict(line=dict(width=0))
            )
            fig4.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=10, r=40, t=10, b=10),
                height=260,
                xaxis_title="",
                yaxis_title="",
                yaxis=dict(showgrid=False, linecolor='#e2e8f0', tickfont=dict(size=11, family='Outfit')),
                xaxis=dict(showgrid=True, gridcolor='#f1f5f9', linecolor='rgba(0,0,0,0)', showticklabels=False),
                showlegend=False
            )
            st.plotly_chart(fig4, use_container_width=True, config={'displayModeBar': False})
            
        # 4. Data Table Row
        st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
        with st.expander("📝 View Filtered Opportunity Raw Data Table", expanded=False):
            # Display Table with standardized columns from the screenshot
            disp_cols = [
                'name', 'category', 'Sum of fee', 'currency_type', 
                'Sum of microscholarship', 'Sum of duration', 'duration_type', 
                'location', 'Year', 'Month', 'Day', 'is_auto_approve'
            ]
            # Verify which columns exist, select them
            table_cols = [c for c in disp_cols if c in filtered_df.columns]
            
            # Standardize column displays
            st.dataframe(
                filtered_df[table_cols],
                use_container_width=True,
                height=300
            )
            
    elif page == "Insight":
        # ---------------------------------------------------------
        # PAGE 2: OPERATIONAL INSIGHTS
        # ---------------------------------------------------------
        
        # 1. Charts Row 1
        col_insight1, col_insight2 = st.columns(2)
        
        with col_insight1:
            st.markdown(f"<h3 style='font-size:1.15rem; color:{PRIMARY_COLOR}; margin-bottom: 10px;'>Sum of microscholarship by category</h3>", unsafe_allow_html=True)
            
            # Group by category and sum microscholarships
            sch_sum = filtered_df.groupby('category')['Sum of microscholarship'].sum().reset_index()
            sch_sum.columns = ['category', 'Total Funding']
            sch_sum = sch_sum[sch_sum['Total Funding'] > 0]
            
            if sch_sum.empty:
                st.info("No microscholarship funding in the filtered data.")
            else:
                sch_sum = sch_sum.sort_values('Total Funding', ascending=False)
                
                # Format legend/label strings
                total_funding_sum = sch_sum['Total Funding'].sum()
                sch_sum['percentage'] = (sch_sum['Total Funding'] / total_funding_sum * 100)
                
                # Standardize pie labels
                sch_sum['Label'] = sch_sum.apply(lambda r: f"{r['category']} ({r['percentage']:.2f}%)", axis=1)
                
                # Use a sequential brand colors
                pie_colors = [PRIMARY_COLOR, '#fca5a5', '#f87171', '#ef4444', '#dc2626', '#b91c1c', '#991b1b', '#7f1d1d', '#475569', '#64748b']
                
                fig5 = go.Figure(data=[go.Pie(
                    labels=sch_sum['category'],
                    values=sch_sum['Total Funding'],
                    marker=dict(colors=pie_colors),
                    textinfo='percent+value',
                    texttemplate='%{percent:.1%}<br>$%{value:.3s}',
                    textposition='inside',
                    textfont=dict(size=10, family='Outfit', color='white'),
                    direction='clockwise',
                    sort=True
                )])
                fig5.update_layout(
                    showlegend=True,
                    legend=dict(
                        orientation="v",
                        yanchor="center",
                        y=0.5,
                        xanchor="left",
                        x=1.02,
                        font=dict(size=11, family='Outfit', color='#1e293b')
                    ),
                    margin=dict(l=10, r=80, t=10, b=10),
                    height=280,
                    paper_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig5, use_container_width=True, config={'displayModeBar': False})
                
        with col_insight2:
            st.markdown(f"<h3 style='font-size:1.15rem; color:{PRIMARY_COLOR}; margin-bottom: 10px;'>Count of opportunity_id by Month(Expiry)</h3>", unsafe_allow_html=True)
            
            # Monthly counts
            months_order = [
                'January', 'February', 'March', 'April', 'May', 'June', 
                'July', 'August', 'September', 'October', 'November', 'December'
            ]
            month_counts = filtered_df['Month'].value_counts().reset_index()
            month_counts.columns = ['Month', 'Count']
            
            # Sort by calendar months
            month_counts['Month'] = pd.Categorical(month_counts['Month'], categories=months_order, ordered=True)
            month_counts = month_counts.sort_values('Month')
            # Drop months with 0 to keep the line continuous like in reference image, 
            # but standardizing: let's keep only months that have data
            month_counts = month_counts[month_counts['Count'] > 0]
            
            fig6 = px.line(
                month_counts,
                x='Month',
                y='Count',
                markers=True,
                color_discrete_sequence=[PRIMARY_COLOR]
            )
            fig6.update_traces(
                line=dict(width=3),
                marker=dict(size=8, color='#1e293b', line=dict(width=1, color='white')),
                text=month_counts['Count'],
                textposition="top center",
                mode="lines+markers+text",
                textfont=dict(size=10, family='Outfit', color='#1e293b')
            )
            fig6.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=10, r=10, t=10, b=10),
                height=280,
                xaxis_title="",
                yaxis_title="",
                xaxis=dict(showgrid=False, linecolor='#e2e8f0', tickfont=dict(size=11, family='Outfit')),
                yaxis=dict(showgrid=True, gridcolor='#f1f5f9', linecolor='rgba(0,0,0,0)', showticklabels=False),
                showlegend=False
            )
            st.plotly_chart(fig6, use_container_width=True, config={'displayModeBar': False})
            
        # 2. Row 2: Styled Conclusions Panel
        st.markdown("<div style='margin-top: 25px;'></div>", unsafe_allow_html=True)
        
        st.markdown(
            f"""
            <div style="background-color: white; border: 2px solid {PRIMARY_COLOR}; border-radius: 16px; padding: 25px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); margin-bottom: 20px;">
                <div style="display: inline-block; background-color: {PRIMARY_COLOR}; color: white; font-weight: 800; font-size: 1.1rem; padding: 6px 20px; border-radius: 8px; margin-bottom: 18px; letter-spacing: 0.5px;">
                    CONCLUSIONS
                </div>
                <ul style="list-style-type: none; padding-left: 0; margin: 0;">
                    <li style="margin-bottom: 12px; font-size: 1rem; line-height: 1.5; display: flex; align-items: flex-start;">
                        <span style="color: {PRIMARY_COLOR}; margin-right: 10px; font-size: 1.1rem;">•</span>
                        <span><strong>Internships</strong> represent the largest share of opportunities, indicating strong demand for practical, career-focused programs.</span>
                    </li>
                    <li style="margin-bottom: 12px; font-size: 1rem; line-height: 1.5; display: flex; align-items: flex-start;">
                        <span style="color: {PRIMARY_COLOR}; margin-right: 10px; font-size: 1.1rem;">•</span>
                        <span>A significant percentage of opportunities are <strong>free</strong>, making the platform accessible to a broad audience.</span>
                    </li>
                    <li style="margin-bottom: 12px; font-size: 1rem; line-height: 1.5; display: flex; align-items: flex-start;">
                        <span style="color: {PRIMARY_COLOR}; margin-right: 10px; font-size: 1.1rem;">•</span>
                        <span>Most opportunities fall within a limited number of categories, suggesting that users primarily engage with a few popular domains.</span>
                    </li>
                    <li style="margin-bottom: 12px; font-size: 1rem; line-height: 1.5; display: flex; align-items: flex-start;">
                        <span style="color: {PRIMARY_COLOR}; margin-right: 10px; font-size: 1.1rem;">•</span>
                        <span>The majority of opportunities have <strong>short to medium durations</strong>, making them suitable for students and working professionals.</span>
                    </li>
                    <li style="margin-bottom: 12px; font-size: 1rem; line-height: 1.5; display: flex; align-items: flex-start;">
                        <span style="color: {PRIMARY_COLOR}; margin-right: 10px; font-size: 1.1rem;">•</span>
                        <span>Scholarship availability varies across categories, with some categories offering more financial support than others.</span>
                    </li>
                    <li style="margin-bottom: 0px; font-size: 1rem; line-height: 1.5; display: flex; align-items: flex-start;">
                        <span style="color: {PRIMARY_COLOR}; margin-right: 10px; font-size: 1.1rem;">•</span>
                        <span>Most opportunities are <strong>auto-approved</strong>, resulting in a faster application process.</span>
                    </li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )

if __name__ == "__main__":
    main()
