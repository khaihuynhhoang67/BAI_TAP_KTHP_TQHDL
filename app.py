import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================================
# 1. CẤU HÌNH TRANG & GIAO DIỆN LIGHT MEDICAL DASHBOARD
# ==========================================
st.set_page_config(
    page_title="Hệ Thống Quản Trị & Tự Động Hóa Y Tế", 
    page_icon="🩺", 
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .stApp { 
        background-color: #F0F4F8;
        color: #1E293B;
    }
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0284C7 0%, #0369A1 50%, #0F172A 100%);
        border-right: 1px solid #0284C7;
    }
    section[data-testid="stSidebar"] p, section[data-testid="stSidebar"] span, section[data-testid="stSidebar"] label, section[data-testid="stSidebar"] h3 {
        color: #F8FAFC !important;
    }
    
    h1, h2, h3 { 
        color: #0369A1 !important; 
    }
    p, .stMarkdown p, span, label { 
        color: #334155 !important; 
    }
    .metric-card-1 {
        background: linear-gradient(135deg, #FFFFFF 0%, #D8B4FE 100%);
        border: 1px solid #E9D5FF;
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0 4px 15px rgba(168, 85, 247, 0.15);
    }
    .metric-card-2 {
        background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 50%, #EC4899 100%);
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(139, 92, 246, 0.35);
    }
    .metric-card-3 {
        background: linear-gradient(135deg, #EC4899 0%, #F43F5E 50%, #FB923C 100%);
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(244, 63, 94, 0.35);
    }
    .stTabs [data-baseweb="tab-list"] { 
        gap: 12px; 
        background: linear-gradient(135deg, #E2E8F0 0%, #BAE6FD 100%);
        padding: 10px;
        border-radius: 16px;
        border: 1px solid #94A3B8;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #FFFFFF;
        border-radius: 10px;
        padding: 10px 24px;
        color: #0369A1;
        font-weight: 700;
        border: 1px solid #BAE6FD;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #0284C7 0%, #0369A1 50%, #0F172A 100%) !important;
        color: #FFFFFF !important;
        font-weight: 800;
        box-shadow: 0 4px 12px rgba(2, 132, 199, 0.3);
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. TẢI VÀ LÀM SẠCH DỮ LIỆU
# ==========================================
@st.cache_data
def load_data():
    df_master = pd.read_csv("data/processed/analytics_master.csv")
    df_skill = pd.read_csv("data/processed/insight_skill_vulnerability.csv")
    return df_master, df_skill

try:
    df_master, df_skill = load_data()
except FileNotFoundError:
    st.error("⚠️ Không tìm thấy file dữ liệu trong thư mục data/processed/!")
    st.stop()

df_master = df_master.dropna(subset=['AI_Capability', 'Worker_Receptiveness', 'Automation_ROI_Score', 'Medical_Risk_Score', 'Task_Impact_Score'])
df_master = df_master[df_master['Automation_Quadrant'] != 'Chưa xác định']

df_master['Phân Vùng Tự Động Hóa'] = df_master['Automation_Quadrant'].str.replace(r"^\d+\.\s*", "", regex=True)

skill_translation = {
    "Documenting/Recording Information": "Ghi chép & Lưu trữ Hồ sơ Y tế",
    "Making Decisions and Solving Problems": "Ra quyết định & Giải quyết Vấn đề",
    "Guiding, Directing, and Motivating Subordinates": "Hướng dẫn & Động viên Nhân sự",
    "Assisting and Caring for Others": "Hỗ trợ & Chăm sóc Người bệnh",
    "Analyzing Data or Information": "Phân tích Dữ liệu Y khoa",
    "Communicating with Persons Outside Organization": "Giao tiếp với Bệnh nhân & Cộng đồng",
    "Processing Information": "Xử lý Thông tin Lâm sàng",
    "Updating and Using Relevant Knowledge": "Cập nhật Kiến thức Y khoa Mới",
    "Getting Information": "Thu thập Thông tin & Dữ liệu",
    "Thinking Creatively": "Tư duy Sáng tạo & Cải tiến",
    "Communicating with Supervisors, Peers, or Subordinates": "Giao tiếp với Đồng nghiệp & Cấp quản lý",
    "Training and Teaching Others": "Đào tạo & Hướng dẫn Chuyên môn",
    "Judging the Qualities of Objects, Services, or People": "Đánh giá Chất lượng Dịch vụ & Y tế",
    "Evaluating Information to Determine Compliance with Standards": "Kiểm định Tiêu chuẩn & Quy chuẩn Y tế"
}

df_skill['Nhóm Kỹ Năng Y Tế'] = df_skill['Skill (O*NET Work Activity)'].astype(str).str.replace(r"[\[\]'\"]", "", regex=True)
df_skill['Nhóm Kỹ Năng Y Tế'] = df_skill['Nhóm Kỹ Năng Y Tế'].map(skill_translation).fillna(df_skill['Nhóm Kỹ Năng Y Tế'])

med_colors = {
    'Mỏ Vàng AI (Quick Wins)': '#059669',       
    'Thành Trì Con Người (Safe Haven)': '#E11D48', 
    'Chờ Công Nghệ (Unmet Needs)': '#D97706',    
    'Vùng Kháng Cự (Resistance)': "#4F0CEA"      
}

# ==========================================
# 3. THANH SIDEBAR
# ==========================================
with st.sidebar:
    st.markdown("### 🏥 AI Medical Analytics")
    st.markdown("---")
    st.markdown("👨‍⚕️ **BỘ LỌC CHUYÊN KHOA**")
    occupations = df_master['Occupation (O*NET-SOC Title)'].unique().tolist()
    selected_occ = st.selectbox("Chọn chuyên khoa y tế:", ["Tất cả Chuyên khoa"] + occupations)
    
    st.markdown("---")
    st.markdown("📊 **BỘ LỌC TỰ ĐỘNG HÓA**")
    quadrants = ["Tất cả phân vùng"] + df_master['Phân Vùng Tự Động Hóa'].unique().tolist()
    selected_quadrant = st.selectbox("Chọn nhóm tự động hóa:", quadrants)
    
    st.markdown("---")
    st.info("💡 **Hệ thống Quản trị:** Phân tích tác vụ tự động hóa và rủi ro y khoa dựa trên dữ liệu O*NET.")

# ==========================================
# 4. HEADER CHÍNH & METRIC CARDS TRỰC QUAN
# ==========================================
col_logo, col_title = st.columns([0.08, 0.92])
with col_logo:
    # Hiển thị ảnh logo (dùng đường dẫn tương đối để đồng đội clone về không bị lỗi)
    st.image("HUB.png", width=65)
with col_title:
    st.markdown("### HỆ THỐNG QUẢN TRỊ & TỰ ĐỘNG HÓA Y TẾ THÔNG MINH")   
    st.markdown("##### *Nền tảng phân tích chiến lược tác vụ, đánh giá năng lực AI, chỉ số sinh lời (ROI) và rủi ro lâm sàng.*")
st.write("")

total_tasks = len(df_master)
quick_wins = len(df_master[df_master['Phân Vùng Tự Động Hóa'] == 'Mỏ Vàng AI (Quick Wins)'])
high_risk = len(df_master[df_master['Medical_Risk_Score'] > 2.0])

col_m1, col_m2, col_m3 = st.columns(3)

with col_m1:
    st.markdown(f"""
        <div class="metric-card-1">
            <p style="color: #64748B; font-size: 13px; margin-bottom: 0; font-weight: 700;"> TỔNG SỐ TÁC VỤ KHẢO SÁT</p>
            <h2 style="color: #0F172A; margin-top: 5px; margin-bottom: 5px;">{total_tasks} <span style="font-size: 13px; color: #059669; font-weight: 600;">Tác vụ y tế</span></h2>
            <p style="color: #475569; font-size: 12px; margin: 0;">Đang được phân tích mức độ tự động hóa</p>
        </div>
    """, unsafe_allow_html=True)

with col_m2:
    st.markdown(f"""
        <div class="metric-card-2">
            <p style="color: #E0F2FE; font-size: 13px; margin-bottom: 0; font-weight: 700;">⚡ MỎ VÀNG AI (QUICK WINS)</p>
            <h2 style="color: #FFFFFF; margin-top: 5px; margin-bottom: 5px;">{quick_wins} <span style="font-size: 13px; color: #E0F2FE; font-weight: 600;">Tác vụ</span></h2>
            <p style="color: #E0F2FE; font-size: 12px; margin: 0;">Nên ưu tiên ứng dụng AI triển khai ngay</p>
        </div>
    """, unsafe_allow_html=True)

with col_m3:
    st.markdown(f"""
        <div class="metric-card-3">
            <p style="color: #D1FAE5; font-size: 13px; margin-bottom: 0; font-weight: 700;">⚠️ RỦI RO Y KHOA CAO</p>
            <h2 style="color: #FFFFFF; margin-top: 5px; margin-bottom: 5px;">{high_risk} <span style="font-size: 13px; color: #D1FAE5; font-weight: 600;">Tác vụ</span></h2>
            <p style="color: #D1FAE5; font-size: 12px; margin: 0;">Bắt buộc Bác sĩ kiểm duyệt chặt chẽ</p>
        </div>
    """, unsafe_allow_html=True)

st.write("")

df_filtered = df_master.copy()
if selected_occ != "Tất cả Chuyên khoa":
    df_filtered = df_filtered[df_filtered['Occupation (O*NET-SOC Title)'] == selected_occ]
if selected_quadrant != "Tất cả phân vùng":
    df_filtered = df_filtered[df_filtered['Phân Vùng Tự Động Hóa'] == selected_quadrant]

# ==========================================
# 5. GIAO DIỆN CHIA TABS
# ==========================================
tab1, tab2 = st.tabs([
    "📍 Bức Tranh Toàn Cảnh & Ma Trận ROI", 
    "📈 Phân Tích Đa Chiều Kỹ Năng Y Tế"
])

# TAB 1: BỨC TRANH TOÀN CẢNH & ROI
with tab1:
    st.subheader("🌐 ĐỊNH VỊ TÁC VỤ & ĐÁNH GIÁ RỦI RO Y KHOA")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig1 = px.scatter(
            df_filtered, 
            x='AI_Capability', 
            y='Worker_Receptiveness', 
            color='Phân Vùng Tự Động Hóa', 
            hover_name='Task', 
            color_discrete_map=med_colors,
            size_max=15,
            title="1. NĂNG LỰC AI VS ĐÓN NHẬN CỦA Y BÁC SĨ"
        )
        fig1.update_layout(
            plot_bgcolor='#FFFFFF', 
            paper_bgcolor='#FFFFFF',
            title_font_color='#0369A1',
            title_x=0.0,
            font=dict(color="#335547", size=12),
            xaxis=dict(title="Năng lực của AI", title_font=dict(color='#0369A1'), tickfont=dict(color='#334155'), gridcolor='#E2E8F0'),
            yaxis=dict(title="Mức độ đón nhận của nhân sự", title_font=dict(color='#0369A1'), tickfont=dict(color='#334155'), gridcolor='#E2E8F0'),
            legend=dict(
                font=dict(color='#334155', size=11),
                title=dict(font=dict(color='#0369A1', size=12)),
                bgcolor='rgba(255, 255, 255, 0.9)'
            )
        )
        st.plotly_chart(fig1, use_container_width=True)
        
    with col2:
        fig2 = px.scatter(
            df_filtered, 
            x='Automation_ROI_Score', 
            y='Medical_Risk_Score',
            size='Task_Impact_Score', 
            color='Phân Vùng Tự Động Hóa', 
            hover_name='Task', 
            color_discrete_map=med_colors, 
            size_max=40, 
            title="2. MA TRẬN SINH LỜI (ROI) & RỦI RO"
        )
        if not df_filtered.empty:
            mid_roi = df_filtered['Automation_ROI_Score'].median()
            mid_risk = df_filtered['Medical_Risk_Score'].median()
            fig2.add_hline(y=mid_risk, line_dash="dash", line_color="#E11D48")
            fig2.add_vline(x=mid_roi, line_dash="dash", line_color="#059669")
        
        fig2.update_layout(
            plot_bgcolor='#FFFFFF', 
            paper_bgcolor='#FFFFFF',
            title_font_color='#0369A1',
            title_x=0.0,
            font=dict(color='#334155', size=12),
            xaxis=dict(title="Chỉ số Sinh lời (ROI)", title_font=dict(color='#0369A1'), tickfont=dict(color='#334155'), gridcolor='#E2E8F0'),
            yaxis=dict(title="Điểm rủi ro y khoa", title_font=dict(color='#0369A1'), tickfont=dict(color='#334155'), gridcolor='#E2E8F0'),
            legend=dict(
                font=dict(color='#334155', size=11),
                title=dict(font=dict(color='#0369A1', size=12)),
                bgcolor='rgba(255, 255, 255, 0.9)'
            )
        )
        st.plotly_chart(fig2, use_container_width=True)

# TAB 2: RADAR PHÂN TÍCH KỸ NĂNG 
with tab2:
    st.subheader("🎯 ĐÁNH GIÁ ĐA CHIỀU NHÓM KỸ NĂNG Y TẾ")
    
    skill_list = df_skill['Nhóm Kỹ Năng Y Tế'].unique().tolist()
    selected_skills = st.multiselect("🔍 Lọc chọn nhóm Kỹ năng y tế để so sánh chi tiết:", skill_list, default=skill_list[:min(3, len(skill_list))])
    
    if selected_skills:
        df_radar = df_skill[df_skill['Nhóm Kỹ Năng Y Tế'].isin(selected_skills)]
        
        df_melted = df_radar.melt(
            id_vars=['Nhóm Kỹ Năng Y Tế'], 
            value_vars=['Avg_AI_Capability', 'Avg_Worker_Desire', 'Avg_Ethics_Empathy_Need'], 
            var_name='Tiêu chí', 
            value_name='Điểm số'
        )
        
        df_melted['Tiêu chí'] = df_melted['Tiêu chí'].replace({
            'Avg_AI_Capability': 'Năng lực của AI',
            'Avg_Worker_Desire': 'Mong muốn Tự động hóa',
            'Avg_Ethics_Empathy_Need': 'Yêu cầu Y đức & Thấu cảm'
        })
        
        fig3 = px.line_polar(
            df_melted, 
            r='Điểm số', 
            theta='Tiêu chí', 
            color='Nhóm Kỹ Năng Y Tế', 
            line_close=True,
            title="3. BIỂU ĐỒ RADAR CHUYÊN SÂU KỸ NĂNG Y TẾ (THANG ĐIỂM 5)"
        )
        fig3.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 5], tickfont=dict(color='#334155'), gridcolor='#CBD5E1'),
                angularaxis=dict(tickfont=dict(color='#0369A1', size=11, family="sans-serif")),
                bgcolor='#FFFFFF'
            ), 
            plot_bgcolor='#FFFFFF',
            paper_bgcolor='#FFFFFF',
            title_font_color='#0369A1',
            title_x=0.0,
            font=dict(color='#334155', size=12),
            legend=dict(
                font=dict(color='#334155', size=11),
                title=dict(font=dict(color='#0369A1', size=12)),
                bgcolor='rgba(255, 255, 255, 0.9)'
            )
        )
        st.plotly_chart(fig3, use_container_width=True)
    else:
        st.warning("⚠️ Vui lòng chọn ít nhất 1 Kỹ năng ở thanh chọn bên trên để hiển thị biểu đồ Radar.")