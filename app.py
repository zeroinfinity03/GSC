import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime

# Set page config with larger initial size
st.set_page_config(
    page_title="Graduate Studies Center Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better scrolling and layout
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stPlotlyChart {
        background-color: #ffffff;
        border-radius: 5px;
        padding: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
        min-height: 400px;  /* Minimum height for plots */
    }
    [data-testid="stVerticalBlock"] {
        gap: 2rem;
    }
    .plot-container {
        overflow-x: auto;
        overflow-y: auto;
        max-height: 600px;  /* Maximum height before scrolling */
    }
    </style>
""", unsafe_allow_html=True)

# Load and prepare data
@st.cache_data
def load_data():
    df = pd.read_csv("GSC cleaned.csv")
    df['Date Time'] = pd.to_datetime(df['Date Time'])
    return df

df = load_data()

# Header with better spacing
st.title("📊 Graduate Studies Center Analytics Dashboard")
st.markdown("---")

# Sidebar filters with more options
st.sidebar.header("Filters")

# Date range filter
date_range = st.sidebar.date_input(
    "Select Date Range",
    [df['Date Time'].min().date(), df['Date Time'].max().date()]
)

# Staff filter with select all option
all_staff = sorted(df['Staff Name'].unique())
staff_container = st.sidebar.container()
select_all = st.sidebar.checkbox("Select All Staff", True)
if select_all:
    selected_staff = all_staff
else:
    selected_staff = st.sidebar.multiselect(
        "Select Staff Members",
        options=all_staff,
        default=all_staff
    )

# Filter data
mask = (
    (df['Date Time'].dt.date >= date_range[0]) & 
    (df['Date Time'].dt.date <= date_range[1]) &
    (df['Staff Name'].isin(selected_staff))
)
filtered_df = df[mask]

# Create scrollable containers for plots
st.markdown('<div class="plot-container">', unsafe_allow_html=True)

# Layout with better spacing
col1, col2 = st.columns(2)

with col1:
    # Appointments by Staff
    st.subheader("📋 Appointments by Staff")
    staff_counts = filtered_df['Staff Name'].value_counts()
    fig_staff = px.bar(
        x=staff_counts.index,
        y=staff_counts.values,
        labels={'x': 'Staff Member', 'y': 'Number of Appointments'},
        color=staff_counts.values,
        color_continuous_scale='Viridis',
        height=500  # Increased height
    )
    fig_staff.update_layout(
        margin=dict(l=20, r=20, t=40, b=20),
        showlegend=False,
        xaxis={'tickangle': 45}
    )
    st.plotly_chart(fig_staff, use_container_width=True)

with col2:
    # DSS Distribution
    st.subheader("🎯 DSS Students Distribution")
    dss_counts = filtered_df['DSS_Response'].value_counts()
    fig_dss = px.pie(
        values=dss_counts.values,
        names=dss_counts.index,
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Set3,
        height=500  # Increased height
    )
    fig_dss.update_layout(margin=dict(l=20, r=20, t=40, b=20))
    st.plotly_chart(fig_dss, use_container_width=True)

# Appointments Over Time - Full width
st.subheader("📈 Appointments Timeline")
appointments_by_date = filtered_df.groupby(filtered_df['Date Time'].dt.date).size().reset_index()
appointments_by_date.columns = ['Date', 'Count']

fig_timeline = px.line(
    appointments_by_date,
    x='Date',
    y='Count',
    labels={'Count': 'Number of Appointments', 'Date': 'Date'},
    height=400
)
fig_timeline.update_traces(line_color='#2E86C1')
fig_timeline.update_layout(margin=dict(l=20, r=20, t=40, b=20))
st.plotly_chart(fig_timeline, use_container_width=True)

# Project Types Analysis - Full width
st.subheader("📝 Common Project Types")
def get_keywords(text):
    common_words = ['thesis', 'paper', 'research', 'proposal', 'draft', 'review', 'msw', 'writing']
    if isinstance(text, str):
        return [word for word in common_words if word in text.lower()]
    return []

project_keywords = filtered_df['Statement_of_Purpose'].apply(get_keywords)
keyword_counts = {}
for keywords in project_keywords:
    for keyword in keywords:
        keyword_counts[keyword] = keyword_counts.get(keyword, 0) + 1

if keyword_counts:
    fig_keywords = px.bar(
        x=list(keyword_counts.keys()),
        y=list(keyword_counts.values()),
        labels={'x': 'Project Type', 'y': 'Frequency'},
        color=list(keyword_counts.values()),
        color_continuous_scale='Viridis',
        height=400
    )
    fig_keywords.update_layout(margin=dict(l=20, r=20, t=40, b=20))
    st.plotly_chart(fig_keywords, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# Show raw data in an expandable section
with st.expander("Show Raw Data"):
    st.dataframe(filtered_df, height=400)
