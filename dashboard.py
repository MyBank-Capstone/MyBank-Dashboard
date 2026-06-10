import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta
import random
import uuid
import os

# ============================================================
# KONFIGURASI
# ============================================================

EXCEL_FILE_NAME = 'Mybank Data.xlsx' 

# ============================================================
# SETUP PAGE
# ============================================================

st.set_page_config(
    page_title="MyBank Analytics Dashboard",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>
    .main { background-color: #f8f9fa; }
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border-left: 4px solid #c8102e;
        margin-bottom: 16px;
    }
    .metric-label {
        font-size: 13px;
        color: #6c757d;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .metric-value {
        font-size: 32px;
        font-weight: 700;
        color: #1a1a2e;
        margin: 4px 0;
    }
    .section-header {
        font-size: 18px;
        font-weight: 700;
        color: #1a1a2e;
        padding: 12px 0 8px 0;
        border-bottom: 2px solid #c8102e;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# LOAD & TRANSFORM DATA
# ============================================================

@st.cache_data
def load_and_transform_data():
    """Load data dari Excel dan transform untuk analytics"""
    
    # Validasi file ada
    if not os.path.exists(EXCEL_FILE_NAME):
        st.error(f"❌ File '{EXCEL_FILE_NAME}' tidak ditemukan!")
        st.info(f"Pastikan file '{EXCEL_FILE_NAME}' ada di folder yang sama dengan app.py")
        st.stop()
    
    try:
        # Load sheets dari Excel
        df_accounts = pd.read_excel(EXCEL_FILE_NAME, sheet_name='Accounts')
        df_transactions = pd.read_excel(EXCEL_FILE_NAME, sheet_name='Transactions')
        df_merchants = pd.read_excel(EXCEL_FILE_NAME, sheet_name='Merchants')
        
        # ===== CREATE USERS =====
        users_data = []
        for idx, row in df_accounts.iterrows():
            no_rek = str(row['no_rek'])
            user_id = str(uuid.uuid4())
            
            # Assign A/B group random 50-50
            ab_group = random.choice(['control', 'treatment'])
            
            # Map income range ke segment
            income_range = str(row['monthly_income_range']).lower()
            if 'tinggi' in income_range or '10' in income_range:
                segment_id = 4
                segment_label = 'Heavy User'
            elif 'menengah' in income_range or '5' in income_range:
                segment_id = 2
                segment_label = 'Transfer Rutin'
            elif 'rendah' in income_range or '1' in income_range:
                segment_id = 3
                segment_label = 'Penabung Pasif'
            else:
                segment_id = 1
                segment_label = 'QRIS Aktif'
            
            consent_status = random.random() < 0.7
            
            users_data.append({
                'no_rek': no_rek,
                'user_id': user_id,
                'segment_id': segment_id,
                'segment_label': segment_label,
                'ab_group': ab_group,
                'consent_status': consent_status,
                'nama': row['nama'],
                'pekerjaan': row['pekerjaan']
            })
        
        df_users = pd.DataFrame(users_data)
        
        # ===== CREATE EVENTS & SESSIONS =====
        events_data = []
        
        # Mapping
        user_map = dict(zip(df_users['no_rek'], df_users['user_id']))
        ab_map = dict(zip(df_users['user_id'], df_users['ab_group']))
        
        # Generate sessions
        sessions_dict = {}
        base_date = datetime.now() - timedelta(days=30)
        
        for idx, row in df_transactions.iterrows():
            no_rek = str(row['no_rek'])
            
            if no_rek not in user_map:
                continue
            
            user_id = user_map[no_rek]
            
            # Create sessions per user
            if user_id not in sessions_dict:
                num_sessions = random.randint(3, 5)
                sessions_dict[user_id] = []
                
                for _ in range(num_sessions):
                    session_id = str(uuid.uuid4())
                    session_date = base_date + timedelta(
                        days=random.randint(0, 30),
                        hours=random.randint(6, 22)
                    )
                    
                    # Treatment users: longer sessions (engagement)
                    if ab_map.get(user_id) == 'treatment':
                        duration = random.randint(120, 300)
                    else:
                        duration = random.randint(30, 120)
                    
                    session_end = session_date + timedelta(seconds=duration)
                    
                    sessions_dict[user_id].append({
                        'session_id': session_id,
                        'user_id': user_id,
                        'session_start': session_date,
                        'session_end': session_end,
                        'duration_sec': duration
                    })
            
            # Get random session
            if sessions_dict[user_id]:
                session = random.choice(sessions_dict[user_id])
                session_id = session['session_id']
            else:
                continue
            
            # Create recommendation
            rec_id = str(uuid.uuid4())
            
            # Map kategori ke item_type
            kategori = str(row['kategori']).lower()
            if 'promo' in kategori or 'diskon' in kategori:
                item_type = 'promo'
            elif 'fitur' in kategori:
                item_type = 'feature'
            else:
                item_type = 'product'
            
            # Map source sesuai A/B group
            source = 'ai_personalized' if ab_map.get(user_id) == 'treatment' else 'rule_based'
            
            # Map channel ke event_source
            channel = str(row['channel']).lower()
            if 'mobile' in channel:
                event_source = 'notification'
            elif 'atm' in channel:
                event_source = 'banner'
            else:
                event_source = 'homepage'
            
            event_timestamp = pd.to_datetime(row['tanggal_transaksi'])
            
            # Create VIEW event (always)
            events_data.append({
                'event_id': str(uuid.uuid4()),
                'user_id': user_id,
                'recommendation_id': rec_id,
                'event_type': 'view',
                'event_source': event_source,
                'session_id': session_id,
                'event_timestamp': event_timestamp,
                'item_type': item_type,
                'kategori': kategori,
                'merchant_id': row['merchant_id'],
                'nominal': row['nominal'],
                'source': source
            })
            
            # Create CLICK event (30% probability)
            if random.random() < 0.3:
                events_data.append({
                    'event_id': str(uuid.uuid4()),
                    'user_id': user_id,
                    'recommendation_id': rec_id,
                    'event_type': 'click',
                    'event_source': event_source,
                    'session_id': session_id,
                    'event_timestamp': event_timestamp + timedelta(seconds=random.randint(2, 30)),
                    'item_type': item_type,
                    'kategori': kategori,
                    'merchant_id': row['merchant_id'],
                    'nominal': row['nominal'],
                    'source': source
                })
        
        # Create dataframes
        all_sessions = []
        for user_id, sessions in sessions_dict.items():
            all_sessions.extend(sessions)
        
        df_sessions = pd.DataFrame(all_sessions)
        df_events = pd.DataFrame(events_data)
        
        # Add user info ke events & sessions
        df_events = df_events.merge(
            df_users[['user_id', 'ab_group', 'segment_label']],
            on='user_id',
            how='left'
        )
        
        df_sessions = df_sessions.merge(
            df_users[['user_id', 'ab_group', 'segment_label']],
            on='user_id',
            how='left'
        )
        
        return df_users, df_events, df_sessions, df_transactions, df_accounts, df_merchants
    
    except FileNotFoundError:
        st.error(f"❌ File '{EXCEL_FILE_NAME}' tidak ditemukan!")
        st.info(f"Pastikan file '{EXCEL_FILE_NAME}' ada di folder yang sama dengan app.py")
        st.stop()
    except Exception as e:
        st.error(f"❌ Error loading data: {e}")
        st.stop()


# Load data
df_users, df_events, df_sessions, df_transactions, df_accounts, df_merchants = load_and_transform_data()

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown("## 🏦 MyBank")
    st.markdown("**Analytics Dashboard**")
    st.markdown("---")
    
    st.markdown("### 📊 Filter")
    
    # Date range filter
    if not df_events.empty:
        min_date = df_events['event_timestamp'].min().date()
        max_date = df_events['event_timestamp'].max().date()
        
        date_range = st.date_input(
            "Rentang Tanggal",
            value=[min_date, max_date],
            min_value=min_date,
            max_value=max_date
        )
    else:
        date_range = None
    
    # Item type filter
    selected_item_types = st.multiselect(
        "Tipe Item Rekomendasi",
        options=["promo", "feature", "product"],
        default=["promo", "feature", "product"]
    )
    
    # Segment filter
    selected_segments = st.multiselect(
        "Segmen Nasabah",
        options=df_users['segment_label'].unique(),
        default=df_users['segment_label'].unique()
    )
    
    st.markdown("---")
    st.markdown("### 📈 Data Info")
    st.markdown(f"**👥 Total Users:** {len(df_users):,}")
    st.markdown(f"**📊 Total Events:** {len(df_events):,}")
    st.markdown(f"**🕐 Total Sessions:** {len(df_sessions):,}")
    
    st.markdown("---")
    st.markdown("### 📁 File Info")
    st.markdown(f"**File:** {EXCEL_FILE_NAME}")
    st.markdown(f"**Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")

# ============================================================
# APPLY FILTERS
# ============================================================

filtered_events = df_events.copy()

if date_range and len(date_range) == 2:
    filtered_events = filtered_events[
        (filtered_events['event_timestamp'].dt.date >= date_range[0]) &
        (filtered_events['event_timestamp'].dt.date <= date_range[1])
    ]

if selected_item_types:
    filtered_events = filtered_events[filtered_events['item_type'].isin(selected_item_types)]

if selected_segments:
    filtered_events = filtered_events[filtered_events['segment_label'].isin(selected_segments)]

filtered_sessions = df_sessions.copy()
if selected_segments:
    filtered_sessions = filtered_sessions[
        filtered_sessions['segment_label'].isin(selected_segments)
    ]

# ============================================================
# HELPER FUNCTIONS
# ============================================================

def calculate_ctr(events_df, group_by=None):
    """Calculate CTR dari events"""
    if events_df.empty:
        return pd.DataFrame()
    
    views = events_df[events_df['event_type'] == 'view']
    clicks = events_df[events_df['event_type'] == 'click']
    
    if group_by:
        views_count = views.groupby(group_by).size().reset_index(name='views')
        clicks_count = clicks.groupby(group_by).size().reset_index(name='clicks')
        merged = views_count.merge(clicks_count, on=group_by, how='left').fillna(0)
        merged['ctr_pct'] = (merged['clicks'] / merged['views'] * 100).round(2)
        return merged
    else:
        total_views = len(views)
        total_clicks = len(clicks)
        ctr_pct = (total_clicks / total_views * 100) if total_views > 0 else 0
        return pd.DataFrame({
            'views': [total_views],
            'clicks': [total_clicks],
            'ctr_pct': [round(ctr_pct, 2)]
        })

# ============================================================
# HEADER
# ============================================================

st.markdown("""
<div style='background: linear-gradient(135deg, #1a1a2e 0%, #c8102e 100%);
     padding: 28px 32px; border-radius: 16px; margin-bottom: 28px;'>
    <h1 style='color:white; margin:0; font-size:28px;'>🏦 MyBank Analytics Dashboard</h1>
    <p style='color:#f0f0f0; margin:6px 0 0 0; font-size:14px;'>
        Monitoring CTR, Engagement Rate & A/B Testing
    </p>
</div>
""", unsafe_allow_html=True)

# ============================================================
# TABS
# ============================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Overview",
    "🧪 A/B Testing",
    "👥 Segmen Nasabah",
    "📈 Trend Harian",
    "👨‍💼 Admin Data"
])

# ============================================================
# TAB 1: OVERVIEW
# ============================================================

with tab1:
    st.markdown('<div class="section-header">Metrik Utama</div>', unsafe_allow_html=True)
    
    if not filtered_events.empty:
        # Calculate metrics
        overall_ctr = calculate_ctr(filtered_events)
        ctr_by_group = calculate_ctr(filtered_events, group_by='ab_group')
        
        overall_ctr_pct = overall_ctr['ctr_pct'].values[0] if not overall_ctr.empty else 0
        
        if not ctr_by_group.empty:
            treatment_ctr = ctr_by_group[ctr_by_group['ab_group'] == 'treatment']['ctr_pct'].values
            control_ctr = ctr_by_group[ctr_by_group['ab_group'] == 'control']['ctr_pct'].values
            treatment_ctr = treatment_ctr[0] if len(treatment_ctr) > 0 else 0
            control_ctr = control_ctr[0] if len(control_ctr) > 0 else 0
            ctr_lift = treatment_ctr - control_ctr
        else:
            treatment_ctr = control_ctr = ctr_lift = 0
        
        # Engagement metrics
        if not filtered_sessions.empty:
            avg_dur_by_group = filtered_sessions.groupby('ab_group')['duration_sec'].mean()
            avg_session_treatment = avg_dur_by_group.get('treatment', 0)
            avg_session_control = avg_dur_by_group.get('control', 0)
            session_lift = avg_session_treatment - avg_session_control
        else:
            avg_session_treatment = avg_session_control = session_lift = 0
        
        consent_rate = df_users['consent_status'].mean() * 100
        
        # Display KPI cards
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Overall CTR</div>
                <div class="metric-value">{overall_ctr_pct:.2f}%</div>
                <div style="font-size:12px; color:#28a745;">↑ dari seluruh rekomendasi</div>
            </div>""", unsafe_allow_html=True)
        
        with col2:
            delta_color = "color:#28a745;" if ctr_lift > 0 else "color:#dc3545;"
            delta_icon = "↑" if ctr_lift > 0 else "↓"
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">CTR Lift (AI vs Rule)</div>
                <div class="metric-value">{ctr_lift:+.2f}%</div>
                <div style="font-size:12px; {delta_color}">{delta_icon} Treatment vs Control</div>
            </div>""", unsafe_allow_html=True)
        
        with col3:
            lift_sec = int(session_lift)
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Avg. Session Duration</div>
                <div class="metric-value">{int(avg_session_treatment)}s</div>
                <div style="font-size:12px; color:#28a745;">↑ {lift_sec}s vs kontrol</div>
            </div>""", unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Consent Rate</div>
                <div class="metric-value">{consent_rate:.1f}%</div>
                <div style="font-size:12px; color:#28a745;">↑ user setuju personalisasi</div>
            </div>""", unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Charts
        col_a, col_b = st.columns([3, 2])
        
        with col_a:
            st.markdown('<div class="section-header">CTR per Tipe Rekomendasi & Grup</div>',
                        unsafe_allow_html=True)
            ctr_item = calculate_ctr(filtered_events, group_by=['ab_group', 'item_type'])
            if not ctr_item.empty:
                fig_bar = px.bar(
                    ctr_item,
                    x='item_type', y='ctr_pct',
                    color='ab_group',
                    barmode='group',
                    color_discrete_map={'treatment': '#c8102e', 'control': '#6c757d'},
                    labels={'ctr_pct': 'CTR (%)', 'item_type': 'Tipe Item',
                            'ab_group': 'Grup'},
                    text_auto='.2f'
                )
                fig_bar.update_layout(
                    plot_bgcolor='white', paper_bgcolor='white',
                    height=350
                )
                st.plotly_chart(fig_bar, width="stretch")
        
        with col_b:
            st.markdown('<div class="section-header">Volume Event</div>',
                        unsafe_allow_html=True)
            event_counts = filtered_events.groupby('event_type').size().reset_index(name='count')
            if not event_counts.empty:
                fig_donut = px.pie(
                    event_counts,
                    names='event_type', values='count',
                    hole=0.55,
                    color_discrete_sequence=['#c8102e', '#1a1a2e', '#adb5bd']
                )
                fig_donut.update_layout(
                    height=350, paper_bgcolor='white'
                )
                st.plotly_chart(fig_donut, width="stretch")
    else:
        st.warning("Tidak ada data event untuk periode ini.")

# ============================================================
# TAB 2: A/B TESTING
# ============================================================

with tab2:
    st.markdown('<div class="section-header">A/B Testing: Rule-Based vs AI Personalisasi</div>',
                unsafe_allow_html=True)
    
    st.info(
        "**Grup Kontrol:** Rekomendasi berbasis rule sederhana  \n"
        "**Grup Treatment:** Rekomendasi berbasis AI personalisasi"
    )
    
    if not filtered_events.empty:
        ctr_group = calculate_ctr(filtered_events, group_by='ab_group')
        
        col1, col2 = st.columns(2)
        
        for i, row in ctr_group.iterrows():
            col = col1 if row['ab_group'] == 'control' else col2
            badge_label = "Control" if row['ab_group'] == 'control' else "Treatment"
            with col:
                st.markdown(f"""
                <div class="metric-card">
                    <span style="background:#{'6c757d' if row['ab_group']=='control' else '#c8102e'};
                                  color:white; padding:2px 10px; border-radius:12px;
                                  font-size:12px;">{badge_label}</span><br><br>
                    <div class="metric-label">Total Views</div>
                    <div class="metric-value" style="font-size:22px">{int(row['views']):,}</div>
                    <div class="metric-label" style="margin-top:10px">Total Clicks</div>
                    <div class="metric-value" style="font-size:22px">{int(row['clicks']):,}</div>
                    <div class="metric-label" style="margin-top:10px">CTR</div>
                    <div class="metric-value">{row['ctr_pct']:.2f}%</div>
                </div>""", unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.markdown('<div class="section-header">CTR per Segmen</div>',
                        unsafe_allow_html=True)
            ctr_seg = calculate_ctr(filtered_events, group_by=['ab_group', 'segment_label'])
            if not ctr_seg.empty:
                fig_seg = px.bar(
                    ctr_seg,
                    x='segment_label', y='ctr_pct',
                    color='ab_group',
                    barmode='group',
                    color_discrete_map={'treatment': '#c8102e', 'control': '#6c757d'},
                    labels={'ctr_pct': 'CTR (%)', 'segment_label': 'Segmen'}
                )
                fig_seg.update_layout(plot_bgcolor='white', height=380)
                st.plotly_chart(fig_seg, width="stretch")
        
        with col_right:
            st.markdown('<div class="section-header">Durasi Sesi per Grup</div>',
                        unsafe_allow_html=True)
            if not filtered_sessions.empty:
                avg_dur = filtered_sessions.groupby('ab_group')['duration_sec'].mean().reset_index()
                avg_dur['duration_min'] = (avg_dur['duration_sec'] / 60).round(2)
                avg_dur['label'] = avg_dur['ab_group'].map(
                    {'control': 'Control', 'treatment': 'Treatment'}
                )
                fig_eng = px.bar(
                    avg_dur,
                    x='label', y='duration_min',
                    color='ab_group',
                    color_discrete_map={'treatment': '#c8102e', 'control': '#6c757d'},
                    labels={'duration_min': 'Durasi (menit)'},
                    text_auto='.2f'
                )
                fig_eng.update_layout(plot_bgcolor='white', height=380, showlegend=False)
                st.plotly_chart(fig_eng, width="stretch")
    else:
        st.warning("Tidak ada data A/B testing untuk periode ini.")

# ============================================================
# TAB 3: SEGMEN NASABAH
# ============================================================

with tab3:
    st.markdown('<div class="section-header">Distribusi Segmen Nasabah</div>',
                unsafe_allow_html=True)
    
    if not df_users.empty:
        col1, col2 = st.columns([2, 3])
        
        with col1:
            seg_dist = df_users[df_users['segment_label'].isin(selected_segments)]\
                .groupby('segment_label').size().reset_index(name='count')
            if not seg_dist.empty:
                fig_pie = px.pie(
                    seg_dist,
                    names='segment_label', values='count',
                    color_discrete_sequence=['#c8102e', '#1a1a2e', '#6c757d', '#e63946']
                )
                fig_pie.update_layout(height=380, paper_bgcolor='white')
                st.plotly_chart(fig_pie, width="stretch")
        
        with col2:
            st.markdown('<div class="section-header">CTR per Segmen</div>',
                        unsafe_allow_html=True)
            ctr_by_seg = calculate_ctr(filtered_events, group_by='segment_label')
            if not ctr_by_seg.empty:
                fig_ctr_seg = px.bar(
                    ctr_by_seg.sort_values('ctr_pct', ascending=True),
                    x='ctr_pct', y='segment_label',
                    orientation='h',
                    color='ctr_pct',
                    color_continuous_scale=['#f0f0f0', '#c8102e'],
                    labels={'ctr_pct': 'CTR (%)'},
                    text_auto='.2f'
                )
                fig_ctr_seg.update_layout(plot_bgcolor='white', height=380, coloraxis_showscale=False)
                st.plotly_chart(fig_ctr_seg, width="stretch")
    else:
        st.warning("Tidak ada data user untuk ditampilkan.")

# ============================================================
# TAB 4: TREND HARIAN
# ============================================================

with tab4:
    st.markdown('<div class="section-header">Trend CTR Harian — Control vs Treatment</div>',
                unsafe_allow_html=True)
    
    if not filtered_events.empty:
        daily_views = filtered_events[filtered_events['event_type'] == 'view']\
            .groupby([filtered_events['event_timestamp'].dt.date, 'ab_group']).size().reset_index(name='views')
        daily_views.rename(columns={'event_timestamp': 'event_date'}, inplace=True)
        
        daily_clicks = filtered_events[filtered_events['event_type'] == 'click']\
            .groupby([filtered_events['event_timestamp'].dt.date, 'ab_group']).size().reset_index(name='clicks')
        daily_clicks.rename(columns={'event_timestamp': 'event_date'}, inplace=True)
        
        daily = daily_views.merge(daily_clicks, on=['event_date', 'ab_group'], how='left').fillna(0)
        daily['ctr_pct'] = (daily['clicks'] / daily['views'] * 100).round(2)
        daily['event_date'] = pd.to_datetime(daily['event_date'])
        
        if not daily.empty:
            fig_trend = px.line(
                daily,
                x='event_date', y='ctr_pct',
                color='ab_group',
                color_discrete_map={'treatment': '#c8102e', 'control': '#6c757d'},
                labels={'ctr_pct': 'CTR (%)', 'event_date': 'Tanggal'},
                markers=True
            )
            fig_trend.update_layout(plot_bgcolor='white', height=400, hovermode='x unified')
            st.plotly_chart(fig_trend, width="stretch")
    
    st.markdown('<div class="section-header">Trend Engagement — Durasi Sesi Harian</div>',
                unsafe_allow_html=True)
    
    if not filtered_sessions.empty:
        daily_dur = filtered_sessions.copy()
        daily_dur['session_date'] = daily_dur['session_start'].dt.date
        daily_dur = daily_dur.groupby(['session_date', 'ab_group'])['duration_sec']\
            .mean().reset_index()
        daily_dur['duration_min'] = (daily_dur['duration_sec'] / 60).round(2)
        daily_dur['session_date'] = pd.to_datetime(daily_dur['session_date'])
        
        fig_dur = px.area(
            daily_dur,
            x='session_date', y='duration_min',
            color='ab_group',
            color_discrete_map={'treatment': '#c8102e', 'control': '#6c757d'},
            labels={'duration_min': 'Durasi (menit)', 'session_date': 'Tanggal'}
        )
        fig_dur.update_layout(plot_bgcolor='white', height=380, hovermode='x unified')
        st.plotly_chart(fig_dur, width="stretch")

# ============================================================
# TAB 5: ADMIN DATA
# ============================================================

with tab5:
    st.markdown('<div class="section-header">📊 Raw Data dari Excel</div>', unsafe_allow_html=True)
    st.info("Section ini untuk admin - menampilkan data dummy dari file Excel")
    
    admin_tab1, admin_tab2, admin_tab3, admin_tab4 = st.tabs([
        "👥 Users",
        "📋 Transactions",
        "🏢 Merchants",
        "📈 Events"
    ])
    
    # TAB: USERS
    with admin_tab1:
        st.markdown("### Data Users (dari Accounts sheet)")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Users", len(df_users))
        with col2:
            control_count = len(df_users[df_users['ab_group'] == 'control'])
            st.metric("Control Group", control_count)
        with col3:
            treatment_count = len(df_users[df_users['ab_group'] == 'treatment'])
            st.metric("Treatment Group", treatment_count)
        with col4:
            consent_count = len(df_users[df_users['consent_status'] == True])
            st.metric("Consent Count", consent_count)
        
        st.markdown("---")
        
        search_user = st.text_input("🔍 Cari user (nama atau no_rek):", "")
        if search_user:
            display_users = df_users[
                (df_users['nama'].str.contains(search_user, case=False)) |
                (df_users['no_rek'].str.contains(search_user, case=False))
            ].copy()
        else:
            display_users = df_users.copy()
        
        rows_per_page = st.selectbox("Rows per page:", [10, 25, 50, 100], index=0)
        page_num = st.number_input("Page:", min_value=1, 
                                   max_value=max(1, len(display_users) // rows_per_page + 1))
        
        start_idx = (page_num - 1) * rows_per_page
        end_idx = start_idx + rows_per_page
        
        display_cols = ['no_rek', 'nama', 'segment_label', 'ab_group', 'consent_status']
        st.dataframe(
            display_users[display_cols].iloc[start_idx:end_idx],
            width="stretch",
            height=400
        )
        
        csv_users = display_users.to_csv(index=False)
        st.download_button(
            label="📥 Download Users Data (CSV)",
            data=csv_users,
            file_name="users_data.csv",
            mime="text/csv"
        )
    
    # TAB: TRANSACTIONS
    with admin_tab2:
        st.markdown("### Data Transactions (dari Transactions sheet)")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Transactions", len(df_transactions))
        with col2:
            total_nominal = df_transactions['nominal'].sum()
            st.metric("Total Nominal", f"Rp {total_nominal:,.0f}")
        with col3:
            avg_nominal = df_transactions['nominal'].mean()
            st.metric("Avg Nominal", f"Rp {avg_nominal:,.0f}")
        
        st.markdown("---")
        
        search_trx = st.text_input("🔍 Cari transaction (no_rek atau kategori):", "")
        if search_trx:
            display_trx = df_transactions[
                (df_transactions['no_rek'].astype(str).str.contains(search_trx, case=False)) |
                (df_transactions['kategori'].str.contains(search_trx, case=False))
            ].copy()
        else:
            display_trx = df_transactions.copy()
        
        rows_per_page_trx = st.selectbox("Rows per page:", [10, 25, 50, 100], index=1, key="trx_page")
        page_num_trx = st.number_input("Page:", min_value=1, 
                                       max_value=max(1, len(display_trx) // rows_per_page_trx + 1),
                                       key="trx_page_num")
        
        start_idx_trx = (page_num_trx - 1) * rows_per_page_trx
        end_idx_trx = start_idx_trx + rows_per_page_trx
        
        display_cols_trx = ['trx_id', 'no_rek', 'tanggal_transaksi', 'nominal', 'kategori', 'merchant_id', 'channel']
        st.dataframe(
            display_trx[display_cols_trx].iloc[start_idx_trx:end_idx_trx],
            width="stretch",
            height=400
        )
        
        csv_trx = display_trx.to_csv(index=False)
        st.download_button(
            label="📥 Download Transactions Data (CSV)",
            data=csv_trx,
            file_name="transactions_data.csv",
            mime="text/csv"
        )
    
    # TAB: MERCHANTS
    with admin_tab3:
        st.markdown("### Data Merchants (dari Merchants sheet)")
        st.metric("Total Merchants", len(df_merchants))
        st.markdown("---")
        st.dataframe(df_merchants, width="stretch", height=400)
        
        csv_merchants = df_merchants.to_csv(index=False)
        st.download_button(
            label="📥 Download Merchants Data (CSV)",
            data=csv_merchants,
            file_name="merchants_data.csv",
            mime="text/csv"
        )
    
    # TAB: EVENTS
    with admin_tab4:
        st.markdown("### Data Events (Generated)")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Events", len(df_events))
        with col2:
            views_count = len(df_events[df_events['event_type'] == 'view'])
            st.metric("Views", views_count)
        with col3:
            clicks_count = len(df_events[df_events['event_type'] == 'click'])
            st.metric("Clicks", clicks_count)
        
        st.markdown("---")
        
        event_type_filter = st.selectbox("Filter by event type:", ["All", "view", "click"], key="event_type")
        if event_type_filter == "All":
            display_events = df_events.copy()
        else:
            display_events = df_events[df_events['event_type'] == event_type_filter].copy()
        
        rows_per_page_evt = st.selectbox("Rows per page:", [10, 25, 50, 100], index=1, key="evt_page")
        page_num_evt = st.number_input("Page:", min_value=1,
                                       max_value=max(1, len(display_events) // rows_per_page_evt + 1),
                                       key="evt_page_num")
        
        start_idx_evt = (page_num_evt - 1) * rows_per_page_evt
        end_idx_evt = start_idx_evt + rows_per_page_evt
        
        display_cols_evt = ['event_id', 'user_id', 'event_type', 'event_timestamp', 'item_type', 'ab_group', 'source']
        st.dataframe(
            display_events[display_cols_evt].iloc[start_idx_evt:end_idx_evt],
            width="stretch",
            height=400
        )
        
        csv_events = display_events.to_csv(index=False)
        st.download_button(
            label="📥 Download Events Data (CSV)",
            data=csv_events,
            file_name="events_data.csv",
            mime="text/csv"
        )

# ============================================================
# FOOTER
# ============================================================

st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🔄 Refresh Data", width="stretch"):
        st.cache_data.clear()
        st.success("Data refreshed!")
        st.rerun()

with col2:
    st.markdown(f"<p style='text-align:center; font-size:12px; color:#666;'>Data dari {EXCEL_FILE_NAME}</p>", 
                unsafe_allow_html=True)

with col3:
    st.markdown(
        "<p style='text-align:right; font-size:11px; color:#666;'>MyBank Capstone 2026</p>",
        unsafe_allow_html=True
    )