import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# ── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="EV Site Optimizer",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS (Modern Light Theme) ──────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Prompt:wght@300;400;600;700&family=Space+Mono:wght@400;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Prompt', sans-serif;
}

/* Light background */
.stApp {
    background-color: #F8FAFC; /* Slate 50 */
    color: #1E293B; /* Slate 800 */
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #FFFFFF;
    border-right: 1px solid #E2E8F0;
}

/* Metric Cards */
.metric-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 16px;
    padding: 24px;
    text-align: center;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
    transition: transform 0.2s, box-shadow 0.2s, border-color 0.2s;
}
.metric-card:hover { 
    transform: translateY(-2px);
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    border-color: #0EA5E9; /* Sky 500 */
}
.metric-value {
    font-family: 'Space Mono', monospace;
    font-size: 2.5rem;
    font-weight: 700;
    color: #0EA5E9; 
    line-height: 1;
}
.metric-label {
    font-size: 0.85rem;
    color: #64748B; /* Slate 500 */
    margin-top: 8px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
.metric-sub {
    font-size: 0.9rem;
    color: #10B981; /* Emerald 500 */
    margin-top: 6px;
    font-weight: 600;
}

/* Header */
.header-title {
    font-family: 'Space Mono', monospace;
    font-size: 2.2rem;
    font-weight: 700;
    color: #0F172A; /* Slate 900 */
    letter-spacing: -0.02em;
}
.header-sub {
    color: #64748B;
    font-size: 1.1rem;
    margin-top: 4px;
    font-weight: 300;
}

/* Tags (Pastel Style) */
.tag-green { background:#DCFCE7; color:#16A34A; padding:4px 12px; border-radius:20px; font-size:0.8rem; font-weight:700; border: 1px solid #BBF7D0; }
.tag-orange { background:#FEF3C7; color:#D97706; padding:4px 12px; border-radius:20px; font-size:0.8rem; font-weight:700; border: 1px solid #FDE68A; }
.tag-red { background:#FEE2E2; color:#DC2626; padding:4px 12px; border-radius:20px; font-size:0.8rem; font-weight:700; border: 1px solid #FECACA; }

/* Table styling override */
.dataframe { font-size: 0.9rem !important; }

/* Divider */
hr { border-color: #E2E8F0; }
</style>
""", unsafe_allow_html=True)

# ── Load Data ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("gold_data.csv")
    return df

df = load_data()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚡ EV Site Optimizer")
    st.markdown("<hr>", unsafe_allow_html=True)

    st.markdown("**🎛️ ตัวกรองผลลัพธ์ (Filters)**")

    payback_max = st.slider(
        "Payback Period สูงสุด (ปี)",
        min_value=1.0, max_value=4.0,
        value=4.0, step=0.1
    )

    zone_options = ["ทั้งหมด", "CBD", "URBAN"]
    zone_filter = st.selectbox("โซนพื้นที่ (Zoning)", zone_options)

    flood_only = st.toggle("🛡️ ปลอดภัยจากน้ำท่วม 100%", value=True)

    score_min = st.slider(
        "Total Score ขั้นต่ำ",
        min_value=0.0, max_value=1.0,
        value=0.0, step=0.05
    )

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("**🗺️ การแสดงผล (Display)**")
    show_top = st.slider("แสดง Top N ทำเล", 5, 50, 20)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("""
    <div style='font-size:0.85rem; color:#64748B; background:#F1F5F9; padding:15px; border-radius:10px; border:1px solid #E2E8F0;'>
    <b>📊 แผนผังสี (Legend)</b><br><br>
    🟢 <b>คืนทุน < 2 ปี</b><br><span style='font-size:0.75rem'>แนะนำลงทุนทันที</span><br><br>
    🟡 <b>คืนทุน 2–3.5 ปี</b><br><span style='font-size:0.75rem'>มีศักยภาพ พิจารณาได้</span><br><br>
    🔴 <b>คืนทุน > 3.5 ปี</b><br><span style='font-size:0.75rem'>ความเสี่ยงระยะยาว</span>
    </div>
    """, unsafe_allow_html=True)

# ── Filter Data ───────────────────────────────────────────────────────────────
df_filtered = df[df["payback_years"] <= payback_max].copy()
if zone_filter != "ทั้งหมด":
    df_filtered = df_filtered[df_filtered["zone_type"] == zone_filter]
if flood_only:
    df_filtered = df_filtered[df_filtered["is_flood_safe"] == True]
df_filtered = df_filtered[df_filtered["total_score"] >= score_min]
df_filtered = df_filtered.sort_values("payback_years").head(show_top)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="header-title">⚡ EV Site Optimizer</div>
<div class="header-sub">ระบบอัจฉริยะจำลองกลยุทธ์และคัดกรองทำเลสถานีชาร์จรถยนต์ไฟฟ้า — กรุงเทพมหานครและปริมณฑล</div>
""", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# ── Metric Cards ──────────────────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)

total_golden  = len(df)
best_payback  = df["payback_years"].min()
avg_payback   = df["payback_years"].mean()
filtered_count = len(df_filtered)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{total_golden:,}</div>
        <div class="metric-label">Golden Gap Locations</div>
        <div class="metric-sub">✓ ทำเลผ่านเกณฑ์ทั้งหมด</div>
    </div>""", unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{best_payback:.2f}Y</div>
        <div class="metric-label">Fastest Payback</div>
        <div class="metric-sub">🚀 คืนทุนเร็วที่สุด</div>
    </div>""", unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{avg_payback:.2f}Y</div>
        <div class="metric-label">Average Payback</div>
        <div class="metric-sub">📈 ค่าเฉลี่ยทั้งระบบ</div>
    </div>""", unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value" style="color: #8B5CF6;">{filtered_count}</div>
        <div class="metric-label">Filtered Results</div>
        <div class="metric-sub" style="color: #8B5CF6;">🎯 ตรงตามเงื่อนไขที่เลือก</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# ── Map + Table ───────────────────────────────────────────────────────────────
map_col, table_col = st.columns([1.2, 1])

with map_col:
    st.markdown(f"**🗺️ แผนที่พิกัด Top {show_top} ทำเลศักยภาพ**")

    # เปลี่ยน Map Style เป็นแบบสว่าง สะอาดตา
    m = folium.Map(
        location=[13.7563, 100.5018],
        zoom_start=11,
        tiles="CartoDB positron"
    )

    for rank, (_, row) in enumerate(df_filtered.iterrows(), 1):
        p = row["payback_years"]
        if p < 2:
            color, hex_color = "green", "#10B981"
        elif p <= 3.5:
            color, hex_color = "orange", "#F59E0B"
        else:
            color, hex_color = "red", "#EF4444"

        flood_text = "ปลอดภัย ✅" if row["is_flood_safe"] else "เสี่ยง ❌"

        # ปรับ Popup ให้ดูสว่างและมินิมอล
        popup_html = f"""
        <div style='font-family:"Prompt", sans-serif; font-size:13px;
                    background:#FFFFFF; color:#1E293B;
                    padding:12px; border-radius:12px; width:220px;
                    border:1px solid #E2E8F0; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
            <div style='font-size:16px; font-weight:700; color:{hex_color}; text-align:center; margin-bottom:8px;'>
                🏆 อันดับ #{rank} <br> คืนทุนใน {p:.2f} ปี
            </div>
            <hr style='border-color:#F1F5F9; margin:8px 0'>
            <b>🏙️ โซนพื้นที่:</b> {row['zone_type']}<br>
            <b>🌊 ความเสี่ยงน้ำท่วม:</b> {flood_text}<br>
            <b>📊 ศักยภาพรวม:</b> {row['total_score']:.3f}<br>
            <b>🚗 รถที่คาดการณ์:</b> {int(row['est_cars_per_day'])} คัน/วัน<br>
            <b>💰 รายได้ปีแรก:</b> ฿{int(row['year_1_revenue']):,}
        </div>
        """

        folium.Marker(
            location=[row["grid_lat"], row["grid_lon"]],
            popup=folium.Popup(popup_html, max_width=250),
            tooltip=f"Rank #{rank} | Payback {p:.2f}Y",
            icon=folium.Icon(color=color, icon="bolt", prefix="fa")
        ).add_to(m)

    st_folium(m, width=None, height=520)

with table_col:
    st.markdown(f"**📋 รายละเอียดเจาะลึก (Top {show_top} Locations)**")

    def payback_tag(p):
        if p < 2:
            return f'<span class="tag-green">🟢 {p:.2f}Y</span>'
        elif p <= 3.5:
            return f'<span class="tag-orange">🟡 {p:.2f}Y</span>'
        else:
            return f'<span class="tag-red">🔴 {p:.2f}Y</span>'

    df_display = df_filtered[["payback_years", "zone_type",
                               "total_score", "est_cars_per_day",
                               "year_1_revenue", "is_flood_safe"]].copy()
    df_display.insert(0, "Rank", range(1, len(df_display)+1))
    
    # ใส่ Emoji ให้ตารางดูมีชีวิตชีวา
    df_display["Payback"] = df_display["payback_years"].apply(
        lambda p: f"{'🟢' if p < 2 else '🟡' if p <= 3.5 else '🔴'} {p:.2f} Y"
    )
    df_display["Flood Safe"] = df_display["is_flood_safe"].apply(
        lambda x: "✅" if x else "❌"
    )
    df_display["Revenue/Year"] = df_display["year_1_revenue"].apply(
        lambda x: f"฿ {int(x):,}"
    )
    df_display["Cars/Day"] = df_display["est_cars_per_day"].apply(int)
    df_display["Total Score"] = df_display["total_score"].apply(lambda x: f"{x:.3f}")

    df_show = df_display[["Rank", "Payback", "zone_type",
                           "Total Score", "Cars/Day", "Revenue/Year", "Flood Safe"]]
    df_show.columns = ["#", "Payback", "Zone", "Score",
                        "Cars/Day", "Revenue/Y", "Flood"]

    st.dataframe(df_show, use_container_width=True, hide_index=True, height=520)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align:center; color:#94A3B8; font-size:0.85rem; padding-bottom: 20px;'>
    <div style='margin-bottom: 10px;'>
        <b>EV Site Optimizer v2.0</b> &nbsp;|&nbsp; 
        Powered by <b>Databricks</b>, <b>PySpark</b> & <b>MLflow</b>
    </div>
    <div style='margin-bottom: 15px;'>
        Open Data Sources: OSM · WorldPop · World Bank
    </div>
    <a href='https://github.com/PlamGG/smart-ev-site-selection' target='_blank' 
       style='text-decoration: none; color: #0EA5E9; border: 1px solid #0EA5E9; 
              padding: 4px 12px; border-radius: 20px; font-weight: 600; transition: 0.3s;'>
        <i class='fa-brands fa-github'></i> View Project on GitHub
    </a>
</div>
""", unsafe_allow_html=True)