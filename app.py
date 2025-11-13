import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Page config
st.set_page_config(page_title="Environmental Pollution Dashboard", page_icon="🌍", layout="wide")

# Compact CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    * { font-family: 'Inter', sans-serif; }
    .stApp { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
    .block-container { background: rgba(255,255,255,0.95); border-radius: 20px; 
                       box-shadow: 0 20px 60px rgba(0,0,0,0.3); padding: 2rem; }
    .stMetric { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 20px; border-radius: 15px; transition: transform 0.3s; }
    .stMetric:hover { transform: translateY(-5px); }
    .stMetric label, .stMetric [data-testid="stMetricValue"] { color: white !important; }
    h1 { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
         -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800; }
    [data-testid="stSidebar"] { background: linear-gradient(180deg, #667eea 0%, #764ba2 100%); }
    [data-testid="stSidebar"] label { color: white !important; }
    .stButton>button { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                       color: white; border: none; border-radius: 10px; padding: 0.6rem 2rem; }
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    try:
        url = "https://raw.githubusercontent.com/KAVYA-29-ai/dv-assigment/main/city_day.csv"
        df = pd.read_csv(url)
        df['Date'] = pd.to_datetime(df['Date'])
        return df
    except:
        try:
            df = pd.read_csv("city_day.csv")
            df['Date'] = pd.to_datetime(df['Date'])
            return df
        except Exception as e:
            st.error(f"Error loading data: {str(e)}")
            return None

def get_aqi_level(aqi):
    if aqi <= 50: return "Good", "🟢"
    elif aqi <= 100: return "Moderate", "🟡"
    elif aqi <= 150: return "Unhealthy for Sensitive", "🟠"
    elif aqi <= 200: return "Unhealthy", "🔴"
    elif aqi <= 300: return "Very Unhealthy", "🟣"
    else: return "Hazardous", "🟤"

df = load_data()

if df is not None:
    # Header
    st.markdown("# 🌍 Environmental Pollution Dashboard")
    st.markdown("### Track and analyze air quality trends across cities")
    
    # Sidebar
    st.sidebar.markdown("### 🔍 Filters")
    cities = st.sidebar.multiselect("🏙️ Cities", sorted(df['City'].unique()), 
                                    default=sorted(df['City'].unique())[:3])
    date_range = st.sidebar.date_input("📅 Date Range", 
                                       [df['Date'].min().date(), df['Date'].max().date()])
    aqi_range = st.sidebar.slider("🎯 AQI Range", int(df['AQI'].min()), 
                                   int(df['AQI'].max()), (int(df['AQI'].min()), int(df['AQI'].max())))
    
    # Filter data
    filtered = df[df['City'].isin(cities)] if cities else df
    if len(date_range) == 2:
        filtered = filtered[(filtered['Date'].dt.date >= date_range[0]) & 
                          (filtered['Date'].dt.date <= date_range[1])]
    filtered = filtered[(filtered['AQI'] >= aqi_range[0]) & (filtered['AQI'] <= aqi_range[1])]
    
    if filtered.empty:
        st.warning("⚠️ No data for selected filters")
    else:
        # KPIs
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            avg_aqi = filtered['AQI'].mean()
            st.metric("Average AQI", f"{avg_aqi:.0f}")
            level, icon = get_aqi_level(avg_aqi)
            st.caption(f"{icon} {level}")
        
        with col2:
            max_aqi = filtered['AQI'].max()
            max_city = filtered[filtered['AQI'] == max_aqi]['City'].iloc[0]
            st.metric("Peak AQI", f"{max_aqi:.0f}")
            st.caption(f"📍 {max_city}")
        
        with col3:
            min_aqi = filtered['AQI'].min()
            min_city = filtered[filtered['AQI'] == min_aqi]['City'].iloc[0]
            st.metric("Min AQI", f"{min_aqi:.0f}")
            st.caption(f"📍 {min_city}")
        
        with col4:
            st.metric("Total Records", f"{len(filtered):,}")
            st.caption(f"🏙️ {len(filtered['City'].unique())} cities")
        
        st.divider()
        
        # Charts
        st.markdown("### 📈 Visualizations")
        
        # Trend line
        metric = st.selectbox("Metric", ['AQI', 'PM2.5', 'PM10'] if 'PM2.5' in df.columns else ['AQI'])
        trend = filtered.groupby(['Date', 'City'])[metric].mean().reset_index()
        fig_line = px.line(trend, x='Date', y=metric, color='City', markers=True)
        fig_line.update_layout(height=400, hovermode='x unified')
        st.plotly_chart(fig_line, use_container_width=True)
        
        # Bar and scatter
        col1, col2 = st.columns(2)
        with col1:
            city_aqi = filtered.groupby('City')['AQI'].mean().sort_values(ascending=False).reset_index()
            fig_bar = px.bar(city_aqi, x='City', y='AQI', color='AQI', color_continuous_scale='Sunset')
            fig_bar.update_layout(height=350, showlegend=False)
            st.plotly_chart(fig_bar, use_container_width=True)
        
        with col2:
            fig_box = px.box(filtered, x='City', y='AQI', color='City')
            fig_box.update_layout(height=350, showlegend=False)
            st.plotly_chart(fig_box, use_container_width=True)
        
        st.divider()
        
        # Insights
        st.markdown("### 💡 Key Insights")
        col1, col2 = st.columns(2)
        
        with col1:
            most_polluted = filtered.groupby('City')['AQI'].mean().idxmax()
            least_polluted = filtered.groupby('City')['AQI'].mean().idxmin()
            st.info(f"""
            🏭 **Most Polluted**: {most_polluted}  
            🌿 **Least Polluted**: {least_polluted}  
            📊 **Records**: {len(filtered):,}
            """)
        
        with col2:
            high_aqi = len(filtered[filtered['AQI'] > 150])
            hazardous = len(filtered[filtered['AQI'] > 300])
            st.warning(f"""
            ⚠️ **Unhealthy Days**: {high_aqi}  
            🚨 **Hazardous Days**: {hazardous}  
            😷 Wear masks when AQI >150
            """)
        
        # Data table
        st.divider()
        st.markdown("### 📋 Data View")
        display_df = filtered.sort_values('Date', ascending=False)
        st.dataframe(display_df, use_container_width=True, height=300)
        
        # Download
        csv = display_df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download CSV", csv, 
                          f"pollution_data_{datetime.now().strftime('%Y%m%d')}.csv",
                          "text/csv", use_container_width=True)
        
        # Refresh
        if st.button("🔄 Refresh", use_container_width=True):
            st.rerun()

else:
    st.error("❌ Failed to load data. Check file path and permissions.")
