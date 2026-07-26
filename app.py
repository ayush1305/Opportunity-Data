import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os
import base64

# Set Streamlit Page Configuration
st.set_page_config(
    page_title="Excelerate Opportunity Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Brand Color Palette
PRIMARY_COLOR = "#f94c44"
SECONDARY_COLOR = "#f14159"
ACCENT_COLOR = "#e7306b"
DARK_TEXT_COLOR = "#1e293b"
LIGHT_BG_COLOR = "#f8fafc"

# Embedded Base64 Logo (automatically populated from logo_b64.txt)
LOGO_B64 = "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"

# Custom CSS for Premium UI Styling (Segoe UI, transparent elements, pill navigation)
def inject_custom_css():
    st.markdown(
        f"""
        <style>
        /* Set Global Font to Segoe UI */
        html, body, [class*="css"], .stApp {{
            font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, Helvetica, Arial, sans-serif;
            color: {DARK_TEXT_COLOR};
        }}

        /* Completely hide Streamlit sidebar and collapsed sidebar controls */
        [data-testid="stSidebar"], [data-testid="collapsedControl"] {{
            display: none !important;
        }}

        /* Content Area Adjustments - start right at the top */
        header[data-testid="stHeader"] {{
            display: none !important;
        }}
        .stAppHeader {{
            display: none !important;
        }}
        .block-container {{
            padding-top: 0.5rem !important;
            padding-bottom: 2rem !important;
            padding-left: 2rem !important;
            padding-right: 2rem !important;
        }}

        /* Styled headers */
        h1, h2, h3, h4, h5, h6 {{
            color: {PRIMARY_COLOR};
            font-family: 'Segoe UI', sans-serif;
            font-weight: 700;
        }}

        /* Hide Streamlit default styling elements */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}

        /* Custom Header Navigation buttons styling (Pill shaped, NO square borders at all) */
        .stButton > button, div[data-testid="column"] button {{
            background-color: transparent !important;
            border: none !important;
            background: none !important;
            box-shadow: none !important;
            outline: none !important;
            color: #475569 !important;
            font-family: 'Segoe UI', sans-serif !important;
            font-size: 1.15rem !important;
            font-weight: 700 !important;
            padding: 8px 24px !important;
            border-radius: 24px !important;
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
            height: auto !important;
            width: 100% !important;
            cursor: pointer !important;
            display: inline-block !important;
        }}
        
        .stButton > button:hover, div[data-testid="column"] button:hover {{
            background: linear-gradient(90deg, {PRIMARY_COLOR} 0%, {ACCENT_COLOR} 100%) !important;
            color: white !important;
            transform: scale(1.05) !important;
            box-shadow: 0 4px 12px rgba(231, 48, 107, 0.25) !important;
            border: none !important;
        }}

        /* Custom styling for selectbox/multiselect inputs to be transparent with rounded corners */
        div[data-baseweb="select"] {{
            background-color: transparent !important;
            border-radius: 10px !important;
            border: 1px solid rgba(249, 76, 68, 0.3) !important;
            box-shadow: none !important;
        }}
        div[data-baseweb="select"] > div {{
            background-color: transparent !important;
            border-radius: 10px !important;
        }}
        div[data-baseweb="select"] span {{
            color: #1e293b !important;
        }}
        div[role="listbox"] {{
            background-color: white !important;
            border-radius: 10px !important;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1) !important;
        }}
        div[data-testid="stExpander"] {{
            border-radius: 12px !important;
            background-color: transparent !important;
            border: 1px solid rgba(249, 76, 68, 0.2) !important;
        }}

        /* KPI Card styling with Segoe UI */
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

# Helper function to format big numbers
def format_kpi_value(val):
    if val >= 1000000:
        return f"{val/1000000:.1f}M".replace(".0", "")
    elif val >= 1000:
        return f"{val/1000:.1f}K".replace(".0", "")
    return str(val)

# Custom KPI Card Renderer
def render_kpi_card(value, label, icon_svg):
    html_card = f'<div class="kpi-card"><div class="kpi-icon">{icon_svg}</div><div><div class="kpi-value">{value}</div><div class="kpi-label">{label}</div></div></div>'
    st.markdown(html_card, unsafe_allow_html=True)

# Inline SVG icons colored with PRIMARY_COLOR
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

# Standardize Columns of the Dataframe and dynamically extract Deadline/Expiry dates
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
            
    if 'currency_type' not in df.columns:
        df['currency_type'] = 'USD'
    if 'is_auto_approve' not in df.columns:
        df['is_auto_approve'] = True

    # Search for applying/deadline date first to establish the time axis
    date_col = None
    for c in df.columns:
        if c.lower().strip() in ['last_date_to_apply_date', 'last_date_to_apply date', 'expiry_date', 'deadline']:
            date_col = c
            break
            
    # Fallback to created_date if applying date not found
    if date_col is None:
        for c in df.columns:
            if c.lower().strip() in ['created_date', 'created date', 'date', 'created_at_date']:
                date_col = c
                break
            
    if date_col is not None:
        try:
            parsed_dates = pd.to_datetime(df[date_col], errors='coerce', dayfirst=True)
            df['Year'] = parsed_dates.dt.year.fillna(2025).astype(int)
            month_names = {
                1: 'January', 2: 'February', 3: 'March', 4: 'April',
                5: 'May', 6: 'June', 7: 'July', 8: 'August',
                9: 'September', 10: 'October', 11: 'November', 12: 'December'
            }
            df['Month'] = parsed_dates.dt.month.map(month_names).fillna('February')
            df['Day'] = parsed_dates.dt.day.fillna(1).astype(int)
        except Exception:
            df['Year'] = 2025
            df['Month'] = 'February'
            df['Day'] = 1
    else:
        df['Year'] = 2025
        df['Month'] = 'February'
        df['Day'] = 1
        
    return df

# Main logic
def main():
    inject_custom_css()
    
    # Initialize session state for navigation and filter toggle
    if 'page' not in st.session_state:
        st.session_state.page = 'Overview'
    if 'show_filters' not in st.session_state:
        st.session_state.show_filters = False

    # Load raw data directly from local opportunityData.csv
    local_csv_path = os.path.join(os.path.dirname(__file__), "opportunityData.csv")
    if os.path.exists(local_csv_path):
        try:
            df_raw = pd.read_csv(local_csv_path)
        except Exception as e:
            st.error(f"Error loading opportunityData.csv: {e}")
            st.stop()
    else:
        st.error("Error: 'opportunityData.csv' not found. Please place your file in the directory.")
        st.stop()
        
    # Standardize columns
    df = standardize_columns(df_raw.copy())
    
    # ---------------------------------------------------------
    # HORIZONTAL PREMIUM WEBSITE NAVIGATION HEADER (Logo & Page title on the same row)
    # ---------------------------------------------------------
    # Layout Ratios: Brand info (4.2), Spacer (0.6), Overview link (1.2), Insight link (1.2), Filters toggle (1.2)
    col_brand, col_space, col_overview, col_insight, col_filter = st.columns([4.2, 0.6, 1.2, 1.2, 1.2])
    
    with col_brand:
        # Show embedded base64 logo with subtitle directly below it (no duplicate title text)
        if LOGO_B64:
            st.markdown(
                f"""
                <div style="display: flex; flex-direction: column; align-items: flex-start; justify-content: center; height: 42px;">
                    <img src="data:image/png;base64,{LOGO_B64}" style="max-height: 25px; width: auto;" alt="Excelerate Logo">
                    <span style="font-size: 0.65rem; color: #64748b; font-weight: 800; margin-top: 3px; letter-spacing: 0.5px;">OPPORTUNITY CATALOG & STRATEGIC OPERATIONS</span>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"""
                <div style="display: flex; flex-direction: column; align-items: flex-start; justify-content: center; height: 42px;">
                    <h3 style="color:{PRIMARY_COLOR}; margin:0; font-weight:800; line-height:1.1;">Excelerate</h3>
                    <span style="font-size: 0.65rem; color: #64748b; font-weight: 800; margin-top: 3px; letter-spacing: 0.5px;">OPPORTUNITY CATALOG & STRATEGIC OPERATIONS</span>
                </div>
                """, 
                unsafe_allow_html=True
            )

    with col_space:
        st.markdown("<div style='height: 42px;'></div>", unsafe_allow_html=True)

    with col_overview:
        if st.button("Overview", key="nav_overview"):
            st.session_state.page = "Overview"
            st.rerun()

    with col_insight:
        if st.button("Insight", key="nav_insight"):
            st.session_state.page = "Insight"
            st.rerun()

    with col_filter:
        filter_text = "Filters ▾" if st.session_state.show_filters else "Filters"
        if st.button(filter_text, key="nav_filters"):
            st.session_state.show_filters = not st.session_state.show_filters
            st.rerun()

    # Active Tab Highlight Styling: Pill-shaped with gradient background, white text, and NO borders
    if st.session_state.page == 'Overview':
        st.markdown(
            """
            <style>
            div[data-testid="column"]:nth-of-type(3) button {
                background: linear-gradient(90deg, #f94c44 0%, #e7306b 100%) !important;
                color: white !important;
                box-shadow: 0 4px 12px rgba(231, 48, 107, 0.25) !important;
                border: none !important;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            """
            <style>
            div[data-testid="column"]:nth-of-type(4) button {
                background: linear-gradient(90deg, #f94c44 0%, #e7306b 100%) !important;
                color: white !important;
                box-shadow: 0 4px 12px rgba(231, 48, 107, 0.25) !important;
                border: none !important;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

    if st.session_state.show_filters:
        st.markdown(
            """
            <style>
            div[data-testid="column"]:nth-of-type(5) button {
                background: linear-gradient(90deg, #f94c44 0%, #e7306b 100%) !important;
                color: white !important;
                box-shadow: 0 4px 12px rgba(231, 48, 107, 0.25) !important;
                border: none !important;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

    # Tight Divider Line shifted upwards
    st.markdown("<hr style='margin: 2px 0 18px 0; border: 0; border-top: 1px solid #e2e8f0;'>", unsafe_allow_html=True)
    
    # ---------------------------------------------------------
    # FILTER SLICER PANEL (Horizontal container toggleable right below the header)
    # ---------------------------------------------------------
    if st.session_state.show_filters:
        with st.container():
            col_f1, col_f2, col_f3, col_f4, col_f5 = st.columns(5)
            
            with col_f1:
                op_type_filter = st.selectbox(
                    "Opportunity Type",
                    options=["All", "Free Only", "Paid Only"],
                    key="op_type_filter"
                )
                
            with col_f2:
                categories_available = sorted(df['category'].dropna().unique())
                selected_categories = st.multiselect(
                    "Categories",
                    options=categories_available,
                    key="selected_categories",
                    placeholder="All"
                )
                
            with col_f3:
                locations_available = sorted(df['location'].dropna().unique())
                selected_locations = st.multiselect(
                    "Locations",
                    options=locations_available,
                    key="selected_locations",
                    placeholder="All"
                )
                
            with col_f4:
                durations_available = sorted(df['duration_category'].dropna().unique())
                selected_durations = st.multiselect(
                    "Duration Category",
                    options=durations_available,
                    key="selected_durations",
                    placeholder="All"
                )
                
            with col_f5:
                auto_approve_filter = st.selectbox(
                    "Auto Approval Status",
                    options=["All", "Auto-Approved Only", "Manual Approval Only"],
                    key="auto_approve_filter"
                )
            st.markdown("<div style='margin-bottom: 25px;'></div>", unsafe_allow_html=True)
            
    # Retrieve active filter values
    op_type_filter = st.session_state.get("op_type_filter", "All")
    selected_categories = st.session_state.get("selected_categories", [])
    selected_locations = st.session_state.get("selected_locations", [])
    selected_durations = st.session_state.get("selected_durations", [])
    auto_approve_filter = st.session_state.get("auto_approve_filter", "All")
    
    # Apply Filters to DataFrame
    filtered_df = df.copy()
    
    if op_type_filter == "Free Only":
        filtered_df = filtered_df[filtered_df['Sum of fee'] == 0]
    elif op_type_filter == "Paid Only":
        filtered_df = filtered_df[filtered_df['Sum of fee'] > 0]
        
    if selected_categories:
        filtered_df = filtered_df[filtered_df['category'].isin(selected_categories)]
        
    if selected_locations:
        filtered_df = filtered_df[filtered_df['location'].isin(selected_locations)]
        
    if selected_durations:
        filtered_df = filtered_df[filtered_df['duration_category'].isin(selected_durations)]
        
    if auto_approve_filter == "Auto-Approved Only":
        filtered_df = filtered_df[filtered_df['is_auto_approve'] == True]
    elif auto_approve_filter == "Manual Approval Only":
        filtered_df = filtered_df[filtered_df['is_auto_approve'] == False]
        
    if filtered_df.empty:
        st.warning("⚠️ No opportunities match the selected filter criteria. Please open the Filters panel and adjust your selections.")
        st.stop()
        
    # Page Routing
    if st.session_state.page == "Overview":
        # ---------------------------------------------------------
        # PAGE 1: OVERVIEW
        # ---------------------------------------------------------
        col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)
        
        tot_opps = len(filtered_df)
        tot_cats = filtered_df['category'].nunique()
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
        
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            st.markdown(f"<h3 style='font-size:1.15rem; color:{PRIMARY_COLOR}; margin-bottom: 10px;'>Count of opportunity_id by Duration Category</h3>", unsafe_allow_html=True)
            dur_counts = filtered_df['duration_category'].value_counts().reset_index()
            dur_counts.columns = ['Duration Category', 'Count']
            
            sort_order = ["Less than 1 Day", "1 Week", "1 Month", "1 Year", "Long Term"]
            dur_counts['Duration Category'] = pd.Categorical(dur_counts['Duration Category'], categories=sort_order, ordered=True)
            dur_counts = dur_counts.sort_values('Duration Category')
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
                textfont=dict(size=11, color='#1e293b', family='Segoe UI'),
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
                xaxis=dict(showgrid=False, linecolor='#e2e8f0', tickfont=dict(size=11, family='Segoe UI')),
                yaxis=dict(showgrid=True, gridcolor='#f1f5f9', linecolor='rgba(0,0,0,0)', showticklabels=False),
                showlegend=False
            )
            st.plotly_chart(fig1, use_container_width=True, config={'displayModeBar': False})
            
        with col_chart2:
            st.markdown(f"<h3 style='font-size:1.15rem; color:{PRIMARY_COLOR}; margin-bottom: 10px;'>Count of opportunity_id by location</h3>", unsafe_allow_html=True)
            loc_counts = filtered_df['location'].value_counts().reset_index()
            loc_counts.columns = ['location', 'Count']
            loc_counts = loc_counts.sort_values('Count', ascending=True)
            
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
                textfont=dict(size=11, color='#1e293b', family='Segoe UI'),
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
                yaxis=dict(showgrid=False, linecolor='#e2e8f0', tickfont=dict(size=11, family='Segoe UI')),
                xaxis=dict(showgrid=True, gridcolor='#f1f5f9', linecolor='rgba(0,0,0,0)', showticklabels=False),
                showlegend=False
            )
            st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})
            
        col_chart3, col_chart4 = st.columns(2)
        
        with col_chart3:
            st.markdown(f"<h3 style='font-size:1.15rem; color:{PRIMARY_COLOR}; margin-bottom: 10px;'>Count of opportunity_id by Opportunity Type</h3>", unsafe_allow_html=True)
            free_count = len(filtered_df[filtered_df['Sum of fee'] == 0])
            paid_count = len(filtered_df[filtered_df['Sum of fee'] > 0])
            
            type_df = pd.DataFrame({
                'Opportunity Type': ['Free', 'Paid'],
                'Count': [free_count, paid_count]
            })
            type_df = type_df[type_df['Count'] > 0]
            donut_colors = [PRIMARY_COLOR, '#fca5a5']
            
            fig3 = go.Figure(data=[go.Pie(
                labels=type_df['Opportunity Type'],
                values=type_df['Count'],
                hole=0.55,
                marker=dict(colors=donut_colors),
                textinfo='percent+value',
                textposition='outside',
                textfont=dict(size=11, family='Segoe UI', color='#1e293b'),
                direction='clockwise',
                sort=False
            )])
            fig3.update_layout(
                showlegend=True,
                legend=dict(
                    orientation="v",
                    yanchor="middle",
                    y=0.5,
                    xanchor="left",
                    x=1.02,
                    font=dict(size=11, family='Segoe UI', color='#1e293b')
                ),
                margin=dict(l=10, r=80, t=10, b=10),
                height=260,
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig3, use_container_width=True, config={'displayModeBar': False})
            
        with col_chart4:
            st.markdown(f"<h3 style='font-size:1.15rem; color:{PRIMARY_COLOR}; margin-bottom: 10px;'>Count of opportunities by category</h3>", unsafe_allow_html=True)
            cat_counts = filtered_df['category'].value_counts().reset_index()
            cat_counts.columns = ['category', 'Count']
            cat_counts = cat_counts.sort_values('Count', ascending=True)
            
            # Show every category individually - no "Other Categories" grouping
            cat_counts['Label'] = cat_counts['Count'].apply(format_kpi_value)
            
            fig4 = px.bar(
                cat_counts,
                x='Count',
                y='category',
                orientation='h',
                text='Count',
                color_discrete_sequence=[PRIMARY_COLOR]
            )
            fig4.update_traces(
                textposition='outside',
                textfont=dict(size=11, color='#1e293b', family='Segoe UI'),
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
                yaxis=dict(showgrid=False, linecolor='#e2e8f0', tickfont=dict(size=11, family='Segoe UI')),
                xaxis=dict(showgrid=True, gridcolor='#f1f5f9', linecolor='rgba(0,0,0,0)', showticklabels=False),
                showlegend=False
            )
            st.plotly_chart(fig4, use_container_width=True, config={'displayModeBar': False})
            
        st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
        with st.expander("📝 View Filtered Opportunity Raw Data Table", expanded=False):
            disp_cols = [
                'name', 'category', 'Sum of fee', 'currency_type', 
                'Sum of microscholarship', 'Sum of duration', 'duration_type', 
                'location', 'Year', 'Month', 'Day', 'is_auto_approve'
            ]
            table_cols = [c for c in disp_cols if c in filtered_df.columns]
            st.dataframe(
                filtered_df[table_cols],
                use_container_width=True,
                height=300
            )
            
    elif st.session_state.page == "Insight":
        # ---------------------------------------------------------
        # PAGE 2: OPERATIONAL INSIGHTS
        # ---------------------------------------------------------
        col_insight1, col_insight2 = st.columns(2)
        
        with col_insight1:
            st.markdown(f"<h3 style='font-size:1.15rem; color:{PRIMARY_COLOR}; margin-bottom: 10px;'>Sum of microscholarship by category</h3>", unsafe_allow_html=True)
            sch_sum = filtered_df.groupby('category')['Sum of microscholarship'].sum().reset_index()
            sch_sum.columns = ['category', 'Total Funding']
            sch_sum = sch_sum[sch_sum['Total Funding'] > 0]
            
            if sch_sum.empty:
                st.info("No microscholarship funding in the filtered data.")
            else:
                sch_sum = sch_sum.sort_values('Total Funding', ascending=False)
                total_funding_sum = sch_sum['Total Funding'].sum()
                sch_sum['percentage'] = (sch_sum['Total Funding'] / total_funding_sum * 100)
                sch_sum['Label'] = sch_sum.apply(lambda r: f"{r['category']} ({r['percentage']:.2f}%)", axis=1)
                
                pie_colors = [PRIMARY_COLOR, '#fca5a5', '#f87171', '#ef4444', '#dc2626', '#b91c1c', '#991b1b', '#7f1d1d', '#475569', '#64748b']
                
                fig5 = go.Figure(data=[go.Pie(
                    labels=sch_sum['category'],
                    values=sch_sum['Total Funding'],
                    marker=dict(colors=pie_colors),
                    textinfo='percent+value',
                    texttemplate='%{percent:.1%}<br>$%{value:.3s}',
                    textposition='inside',
                    textfont=dict(size=10, family='Segoe UI', color='white'),
                    direction='clockwise',
                    sort=True
                )])
                fig5.update_layout(
                    showlegend=True,
                    legend=dict(
                        orientation="v",
                        yanchor="middle",
                        y=0.5,
                        xanchor="left",
                        x=1.02,
                        font=dict(size=11, family='Segoe UI', color='#1e293b')
                    ),
                    margin=dict(l=10, r=80, t=10, b=10),
                    height=280,
                    paper_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig5, use_container_width=True, config={'displayModeBar': False})
                
        with col_insight2:
            st.markdown(f"<h3 style='font-size:1.15rem; color:{PRIMARY_COLOR}; margin-bottom: 10px;'>Monthly Trend of Opportunities over Time (by Apply Deadline)</h3>", unsafe_allow_html=True)
            
            # Extract a chronological timeline based on Expiry Year and Month
            timeline_df = filtered_df.copy()
            month_map = {
                'January': 1, 'February': 2, 'March': 3, 'April': 4,
                'May': 5, 'June': 6, 'July': 7, 'August': 8,
                'September': 9, 'October': 10, 'November': 11, 'December': 12
            }
            timeline_df['Month_Num'] = timeline_df['Month'].map(month_map)
            
            # Group by year and month
            grouped_time = timeline_df.groupby(['Year', 'Month', 'Month_Num']).size().reset_index(name='Count')
            grouped_time = grouped_time.sort_values(['Year', 'Month_Num'])
            
            # Format labels as YYYY-Mon (e.g. 2025-Feb)
            grouped_time['Year_Month_Label'] = grouped_time.apply(lambda r: f"{r['Year']} {r['Month'][:3]}", axis=1)
            
            # Plot chronological area time series chart
            fig6 = px.line(
                grouped_time,
                x='Year_Month_Label',
                y='Count',
                markers=True,
                color_discrete_sequence=[PRIMARY_COLOR]
            )
            fig6.update_traces(
                line=dict(width=3, shape='spline'),
                marker=dict(size=7, color='#1e293b', line=dict(width=1.5, color='white')),
                fill='tozeroy',
                fillcolor='rgba(249, 76, 68, 0.08)',
                mode="lines+markers+text",
                text=grouped_time['Count'].apply(format_kpi_value),
                textposition="top center",
                textfont=dict(size=10, family='Segoe UI', color='#1e293b')
            )
            fig6.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=10, r=10, t=10, b=10),
                height=280,
                xaxis_title="",
                yaxis_title="",
                xaxis=dict(showgrid=False, linecolor='#e2e8f0', tickfont=dict(size=11, family='Segoe UI')),
                yaxis=dict(showgrid=True, gridcolor='#f1f5f9', linecolor='rgba(0,0,0,0)', showticklabels=False),
                showlegend=False
            )
            st.plotly_chart(fig6, use_container_width=True, config={'displayModeBar': False})
            
        st.markdown("<div style='margin-top: 25px;'></div>", unsafe_allow_html=True)
        st.markdown(
            f"""
            <div style="background-color: white; border: 2px solid {PRIMARY_COLOR}; border-radius: 16px; padding: 25px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); margin-bottom: 20px;">
                <div style="display: inline-block; background: linear-gradient(90deg, {PRIMARY_COLOR} 0%, {ACCENT_COLOR} 100%); color: white; font-weight: 800; font-size: 1.1rem; padding: 6px 20px; border-radius: 20px; margin-bottom: 18px; letter-spacing: 0.5px;">
                    CONCLUSIONS
                </div>
                <ul style="list-style-type: none; padding-left: 0; margin: 0; font-family: 'Segoe UI', sans-serif;">
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
