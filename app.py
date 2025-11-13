import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="Environmental Pollution Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern aesthetic
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        padding: 0rem 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    [data-testid="stHeader"] {
        background: rgba(0,0,0,0);
    }
    
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        backdrop-filter: blur(10px);
    }
    
    .stMetric {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .stMetric:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.6);
    }
    
    .stMetric label {
        color: rgba(255, 255, 255, 0.9) !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
    }
    
    .stMetric [data-testid="stMetricValue"] {
        color: white !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
    }
    
    .metric-caption {
        color: rgba(255, 255, 255, 0.8);
        font-size: 0.85rem;
        margin-top: 5px;
    }
    
    h1 {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 800;
        font-size: 3rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    h2, h3, h4 {
        color: #2d3748;
        font-weight: 700;
    }
    
    .subtitle {
        color: #718096;
        font-size: 1.1rem;
        margin-bottom: 2rem;
        font-weight: 400;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.6rem 2rem;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    .stDownloadButton>button {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.6rem 2rem;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(245, 87, 108, 0.4);
        transition: all 0.3s ease;
    }
    
    .stDownloadButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(245, 87, 108, 0.6);
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
        padding: 2rem 1rem;
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: white;
    }
    
    [data-testid="stSidebar"] label {
        color: white !important;
        font-weight: 600 !important;
    }
    
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stMultiSelect label,
    [data-testid="stSidebar"] .stSlider label {
        color: white !important;
    }
    
    .insight-card {
        background: linear-gradient(135deg, #f6f8fb 0%, #ffffff 100%);
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.08);
        border-left: 4px solid #667eea;
        margin: 10px 0;
    }
    
    .section-divider {
        height: 3px;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border: none;
        border-radius: 2px;
        margin: 2rem 0;
    }
    
    .stExpander {
        background: white;
        border-radius: 10px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    
    div[data-testid="stDataFrame"] {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 5px 20px rgba(0,0,0,0.08);
    }
    
    .aqi-badge {
        display: inline-block;
        padding: 5px 15px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
        margin-top: 5px;
    }
    
    .badge-good {
        background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
        color: #065f46;
    }
    
    .badge-moderate {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        color: #92400e;
    }
    
    .badge-unhealthy {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        color: #7c2d12;
    }
    
    .badge-hazardous {
        background: linear-gradient(135deg, #d4145a 0%, #fbb034 100%);
        color: white;
    }
    
    .stAlert {
        border-radius: 10px;
        border-left: 4px solid;
    }
    
    .js-plotly-plot {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 5px 20px rgba(0,0,0,0.08);
    }
    
    .chart-container {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.08);
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Load data function with caching
@st.cache_data
def load_data():
    try:
        # Try GitHub raw URL first - CORRECT FILENAME: city_day.csv
        url = "https://raw.githubusercontent.com/KAVYA-29-ai/dv-assigment/main/city_day.csv"
        df = pd.read_csv(url)
        
        # Convert Date column to datetime
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'])
        
        # Handle column name variations
        column_mapping = {
            'PM2_5': 'PM2.5',
            'pm2.5': 'PM2.5',
            'pm2_5': 'PM2.5'
        }
        
        for old_col, new_col in column_mapping.items():
            if old_col in df.columns and new_col not in df.columns:
                df.rename(columns={old_col: new_col}, inplace=True)
        
        return df
    except Exception as e:
        # Try local file
        try:
            df = pd.read_csv("city_day.csv")
            if 'Date' in df.columns:
                df['Date'] = pd.to_datetime(df['Date'])
            
            column_mapping = {
                'PM2_5': 'PM2.5',
                'pm2.5': 'PM2.5',
                'pm2_5': 'PM2.5'
            }
            
            for old_col, new_col in column_mapping.items():
                if old_col in df.columns and new_col not in df.columns:
                    df.rename(columns={old_col: new_col}, inplace=True)
            
            return df
        except Exception as e2:
            st.error(f"Error loading data: {str(e2)}")
            return None

# Function to determine AQI level
def get_aqi_level(aqi):
    if aqi <= 50:
        return "Good", "🟢", "badge-good"
    elif aqi <= 100:
        return "Moderate", "🟡", "badge-moderate"
    elif aqi <= 150:
        return "Unhealthy for Sensitive", "🟠", "badge-unhealthy"
    elif aqi <= 200:
        return "Unhealthy", "🔴", "badge-unhealthy"
    elif aqi <= 300:
        return "Very Unhealthy", "🟣", "badge-hazardous"
    else:
        return "Hazardous", "🟤", "badge-hazardous"

# Load data
df = load_data()

if df is not None:
    # Check if required columns exist
    required_columns = ['City', 'Date', 'AQI']
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        st.error(f"Missing required columns: {', '.join(missing_columns)}")
        st.info(f"Available columns: {', '.join(df.columns.tolist())}")
        st.stop()
    
    # Fill missing values with defaults
    numeric_columns = ['PM2.5', 'PM10', 'NO2', 'SO2', 'AQI', 'Temperature', 'Humidity']
    for col in numeric_columns:
        if col in df.columns:
            df[col] = df[col].fillna(df[col].mean())
    
    # Header with gradient
    st.markdown("<h1>🌍 Environmental Pollution Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>✨ Track and analyze air quality trends across cities with real-time insights</p>", unsafe_allow_html=True)
    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

    # Sidebar Filters with enhanced styling
    st.sidebar.markdown("### 🔍 Filter Controls")
    st.sidebar.markdown("---")
    
    # City selection
    all_cities = sorted(df['City'].unique().tolist())
    selected_cities = st.sidebar.multiselect(
        "🏙️ Select Cities",
        options=all_cities,
        default=all_cities[:3] if len(all_cities) >= 3 else all_cities
    )
    
    st.sidebar.markdown("")
    
    # Date range
    min_date = df['Date'].min().date()
    max_date = df['Date'].max().date()
    
    date_range = st.sidebar.date_input(
        "📅 Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    st.sidebar.markdown("")
    
    # AQI Range slider
    aqi_range = st.sidebar.slider(
        "🎯 AQI Range",
        min_value=int(df['AQI'].min()),
        max_value=int(df['AQI'].max()),
        value=(int(df['AQI'].min()), int(df['AQI'].max()))
    )
    
    # PM2.5 Range slider (if column exists)
    if 'PM2.5' in df.columns:
        pm25_range = st.sidebar.slider(
            "💨 PM2.5 Range (µg/m³)",
            min_value=int(df['PM2.5'].min()),
            max_value=int(df['PM2.5'].max()),
            value=(int(df['PM2.5'].min()), int(df['PM2.5'].max()))
        )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🎨 Dashboard Info")
    st.sidebar.info("This dashboard provides real-time air quality analysis with interactive visualizations.")
    
    # Filter data
    filtered_df = df.copy()
    
    if selected_cities:
        filtered_df = filtered_df[filtered_df['City'].isin(selected_cities)]
    
    if len(date_range) == 2:
        start_date, end_date = date_range
        filtered_df = filtered_df[
            (filtered_df['Date'].dt.date >= start_date) & 
            (filtered_df['Date'].dt.date <= end_date)
        ]
    
    filtered_df = filtered_df[
        (filtered_df['AQI'] >= aqi_range[0]) & 
        (filtered_df['AQI'] <= aqi_range[1])
    ]
    
    if 'PM2.5' in df.columns:
        filtered_df = filtered_df[
            (filtered_df['PM2.5'] >= pm25_range[0]) & 
            (filtered_df['PM2.5'] <= pm25_range[1])
        ]
    
    # Display dataset overview
    with st.expander("📊 Dataset Overview & Statistics", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 📋 Sample Data")
            st.dataframe(df.head(10), use_container_width=True)
        with col2:
            st.markdown("#### 📈 Statistical Summary")
            st.dataframe(df.describe(), use_container_width=True)
    
    # Check if filtered data is empty
    if filtered_df.empty:
        st.warning("⚠️ No data available for the selected filters. Please adjust your selection.")
    else:
        # KPIs Section with enhanced cards
        st.markdown("### 📊 Key Metrics Overview")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            avg_aqi = filtered_df['AQI'].mean()
            st.metric("Average AQI", f"{avg_aqi:.0f}")
            level, icon, badge_class = get_aqi_level(avg_aqi)
            st.markdown(f"<div class='metric-caption'>{icon} {level}</div>", unsafe_allow_html=True)
        
        with col2:
            if 'PM2.5' in filtered_df.columns:
                max_pm25 = filtered_df['PM2.5'].max()
                max_pm25_city = filtered_df[filtered_df['PM2.5'] == max_pm25]['City'].iloc[0]
                st.metric("Peak PM2.5", f"{max_pm25:.0f}")
                st.markdown(f"<div class='metric-caption'>📍 {max_pm25_city}</div>", unsafe_allow_html=True)
            else:
                max_aqi = filtered_df['AQI'].max()
                st.metric("Peak AQI", f"{max_aqi:.0f}")
        
        with col3:
            if 'Humidity' in filtered_df.columns:
                min_humidity = filtered_df['Humidity'].min()
                min_hum_city = filtered_df[filtered_df['Humidity'] == min_humidity]['City'].iloc[0]
                st.metric("Min Humidity", f"{min_humidity:.0f}%")
                st.markdown(f"<div class='metric-caption'>📍 {min_hum_city}</div>", unsafe_allow_html=True)
            else:
                min_aqi = filtered_df['AQI'].min()
                st.metric("Min AQI", f"{min_aqi:.0f}")
        
        with col4:
            if 'Temperature' in filtered_df.columns:
                avg_temp = filtered_df['Temperature'].mean()
                st.metric("Avg Temperature", f"{avg_temp:.1f}°C")
                st.markdown(f"<div class='metric-caption'>🌡️ Overall</div>", unsafe_allow_html=True)
            else:
                total_records = len(filtered_df)
                st.metric("Total Records", f"{total_records:,}")
        
        st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
        
        # Charts Section
        st.markdown("### 📈 Interactive Visualizations")
        
        # Line Chart - Pollution Trend
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown("#### 📉 Pollution Trend Over Time")
        with col2:
            available_metrics = ['AQI']
            if 'PM2.5' in filtered_df.columns:
                available_metrics.append('PM2.5')
            if 'PM10' in filtered_df.columns:
                available_metrics.append('PM10')
            if 'NO2' in filtered_df.columns:
                available_metrics.append('NO2')
            if 'SO2' in filtered_df.columns:
                available_metrics.append('SO2')
            
            metric_choice = st.selectbox("Metric", available_metrics, label_visibility="collapsed")
        
        trend_data = filtered_df.groupby(['Date', 'City'])[metric_choice].mean().reset_index()
        fig_line = px.line(
            trend_data,
            x='Date',
            y=metric_choice,
            color='City',
            labels={metric_choice: f"{metric_choice} Level", 'Date': 'Date'},
            markers=True,
            color_discrete_sequence=px.colors.qualitative.Vivid
        )
        fig_line.update_layout(
            height=450,
            hovermode='x unified',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter, sans-serif"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        fig_line.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.1)')
        fig_line.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.1)')
        st.plotly_chart(fig_line, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("")
        
        # Bar Chart and Scatter Plot
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
            st.markdown("#### 🏆 Average AQI by City")
            city_aqi = filtered_df.groupby('City')['AQI'].mean().sort_values(ascending=False).reset_index()
            fig_bar = px.bar(
                city_aqi,
                x='City',
                y='AQI',
                color='AQI',
                color_continuous_scale='Sunset',
            )
            fig_bar.update_layout(
                height=400,
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Inter, sans-serif")
            )
            fig_bar.update_xaxes(showgrid=False)
            fig_bar.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.1)')
            st.plotly_chart(fig_bar, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
            if 'PM2.5' in filtered_df.columns and 'Temperature' in filtered_df.columns:
                st.markdown("#### 🌡️ PM2.5 vs Temperature")
                hover_cols = ['Date']
                if 'Humidity' in filtered_df.columns:
                    hover_cols.append('Humidity')
                
                fig_scatter = px.scatter(
                    filtered_df,
                    x='Temperature',
                    y='PM2.5',
                    color='City',
                    size='AQI',
                    hover_data=hover_cols,
                    labels={'Temperature': 'Temperature (°C)', 'PM2.5': 'PM2.5 (µg/m³)'},
                    color_discrete_sequence=px.colors.qualitative.Vivid
                )
            else:
                st.markdown("#### 📊 AQI Distribution by City")
                fig_scatter = px.box(
                    filtered_df,
                    x='City',
                    y='AQI',
                    color='City',
                    color_discrete_sequence=px.colors.qualitative.Vivid
                )
            
            fig_scatter.update_layout(
                height=400,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Inter, sans-serif"),
                showlegend=False
            )
            fig_scatter.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.1)')
            fig_scatter.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.1)')
            st.plotly_chart(fig_scatter, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("")
        
        # Additional Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
            st.markdown("#### 🔥 Pollutants Correlation")
            corr_columns = ['AQI']
            for col in ['PM2.5', 'PM10', 'NO2', 'SO2', 'Temperature', 'Humidity']:
                if col in filtered_df.columns:
                    corr_columns.append(col)
            
            if len(corr_columns) > 1:
                corr_data = filtered_df[corr_columns].corr()
                fig_heatmap = px.imshow(
                    corr_data,
                    text_auto='.2f',
                    color_continuous_scale='RdBu_r',
                    aspect="auto"
                )
                fig_heatmap.update_layout(
                    height=400,
                    font=dict(family="Inter, sans-serif")
                )
                st.plotly_chart(fig_heatmap, use_container_width=True)
            else:
                st.info("Not enough numeric columns for correlation analysis")
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
            st.markdown("#### 📊 AQI Distribution")
            fig_hist = px.histogram(
                filtered_df,
                x='AQI',
                color='City',
                marginal='box',
                nbins=30,
                color_discrete_sequence=px.colors.qualitative.Vivid
            )
            fig_hist.update_layout(
                height=400,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Inter, sans-serif"),
                showlegend=True
            )
            fig_hist.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.1)')
            fig_hist.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.1)')
            st.plotly_chart(fig_hist, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Filtered Data Table
        st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
        st.markdown("### 📋 Detailed Data View")
        
        display_df = filtered_df.copy()
        display_df['AQI_Level'] = display_df['AQI'].apply(lambda x: get_aqi_level(x)[0])
        
        st.dataframe(
            display_df.sort_values('Date', ascending=False),
            use_container_width=True,
            height=350
        )
        
        # Download button
        csv = display_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Data as CSV",
            data=csv,
            file_name=f"pollution_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )
        
        # Insights Section
        st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
        st.markdown("### 💡 Key Insights & Recommendations")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("<div class='insight-card'>", unsafe_allow_html=True)
            st.markdown("#### 🔍 Analysis Summary")
            
            most_polluted = filtered_df.groupby('City')['AQI'].mean().idxmax()
            most_polluted_aqi = filtered_df.groupby('City')['AQI'].mean().max()
            least_polluted = filtered_df.groupby('City')['AQI'].mean().idxmin()
            least_polluted_aqi = filtered_df.groupby('City')['AQI'].mean().min()
            
            insights_text = f"""
            - 🏭 **Most Polluted**: {most_polluted} (AQI: {most_polluted_aqi:.1f})
            - 🌿 **Least Polluted**: {least_polluted} (AQI: {least_polluted_aqi:.1f})
            """
            
            if 'PM2.5' in filtered_df.columns and 'Temperature' in filtered_df.columns:
                temp_pm_corr = filtered_df['Temperature'].corr(filtered_df['PM2.5'])
                insights_text += f"\n- 🌡️ **Temp-PM2.5 Correlation**: {temp_pm_corr:.2f}"
            
            if 'PM2.5' in filtered_df.columns and 'Humidity' in filtered_df.columns:
                humidity_pm_corr = filtered_df['Humidity'].corr(filtered_df['PM2.5'])
                insights_text += f"\n- 💧 **Humidity-PM2.5 Correlation**: {humidity_pm_corr:.2f}"
            
            insights_text += f"\n- 📊 **Records Analyzed**: {len(filtered_df):,}"
            
            st.markdown(insights_text)
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown("<div class='insight-card'>", unsafe_allow_html=True)
            st.markdown("#### 🎯 Health Advisory")
            
            high_aqi_days = len(filtered_df[filtered_df['AQI'] > 150])
            hazardous_days = len(filtered_df[filtered_df['AQI'] > 300])
            
            st.markdown(f"""
            - ⚠️ **Unhealthy Days (AQI >150)**: {high_aqi_days}
            - 🚨 **Hazardous Days (AQI >300)**: {hazardous_days}
            
            **Recommendations**:
            - 😷 Wear masks during high AQI periods
            - 🏠 Use air purifiers indoors
            - 🚶 Limit outdoor activities when AQI >150
            - 💧 Stay hydrated and monitor air quality
            """)
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Control buttons
        st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            if st.button("🔄 Refresh Dashboard", use_container_width=True):
                st.rerun()
        
        with col2:
            auto_refresh = st.checkbox("⏱️ Auto-refresh (1 min)")
        
        if auto_refresh:
            st.info("⏱️ Dashboard will auto-refresh every minute")
            import time
            time.sleep(60)
            st.rerun()

else:
    st.error("❌ Failed to load data. Please check if the dataset is available.")
    st.info("""
    **Trying to load from**: 
    - GitHub: `https://raw.githubusercontent.com/KAVYA-29-ai/dv-assigment/main/city_day.csv`
    - Local file: `city_day.csv`
    
    **Troubleshooting Steps**:
    1. ✅ Make sure the file `city_day.csv` exists in your repository
    2. ✅ Check that your repository is **public**
    3. ✅ Verify the file is accessible at: https://raw.githubusercontent.com/KAVYA-29-ai/dv-assigment/main/city_day.csv
    4. ✅ Ensure the CSV has these columns: `City`, `Date`, `AQI`
    
    **Your GitHub Repository**: 
    `https://github.com/KAVYA-29-ai/dv-assigment`
    
    **Alternative**: Place `city_day.csv` in the same directory as this script.
    """)
