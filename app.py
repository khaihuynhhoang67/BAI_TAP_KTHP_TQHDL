import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================================
# 1. CẤU HÌNH TRANG & CẤU TRÚC MÀU SẮC ĐỒNG BỘ (EXECUTIVE COLOR PALETTE)
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
    background-color: #F8FAFC;
    color: #1E293B;
}

/* 1. Sidebar Style */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0284C7 0%, #0369A1 50%, #0F172A 100%);
    border-right: 1px solid #0284C7;
}
section[data-testid="stSidebar"] p, section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] label, section[data-testid="stSidebar"] h3 {
    color: #F8FAFC !important;
}

/* 2. Style Metric Cards */
.metric-card-1 {
    background: linear-gradient(135deg, #FFFFFF 0%, #F3E8FF 100%);
    border: 1px solid #E9D5FF;
    padding: 20px;
    border-radius: 16px;
    box-shadow: 0 4px 15px rgba(168, 85, 247, 0.12);
}
.metric-card-2 {
    background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 50%, #EC4899 100%);
    padding: 20px;
    border-radius: 16px;
    box-shadow: 0 4px 20px rgba(139, 92, 246, 0.25);
}
.metric-card-3 {
    background: linear-gradient(135deg, #F43F5E 0%, #FB923C 100%);
    padding: 20px;
    border-radius: 16px;
    box-shadow: 0 4px 20px rgba(244, 63, 94, 0.25);
}

/* 3. MÀU TÙY CHỈNH CHO CÁC KHỐI ĐÁNH GIÁ (CUSTOM COLORED CARDS) */
.card-left-eval {
    background: linear-gradient(135deg, #EEF2FF 0%, #E0E7FF 100%);
    border-left: 5px solid #6366F1;
    border-radius: 12px;
    padding: 18px;
    height: 100%;
}
.card-right-eval {
    background: linear-gradient(135deg, #F0F9FF 0%, #E0F2FE 100%);
    border-left: 5px solid #0284C7;
    border-radius: 12px;
    padding: 18px;
    height: 100%;
}

/* 4. Khung Kết Luận Màu Xanh Lá Y Tế (Executive Green Box) */
.conclusion-box-colorful {
    background: linear-gradient(135deg, #ECFDF5 0%, #D1FAE5 100%);
    border: 1px solid #6EE7B7;
    border-left: 6px solid #059669;
    border-radius: 14px;
    padding: 20px;
    margin-top: 15px;
    box-shadow: 0 4px 12px rgba(5, 150, 105, 0.08);
}

/* 5. Custom Tabs Styling */
stTabs [data-baseweb="tab-list"] {
    gap: 12px;
    background: #E2E8F0;
    padding: 8px;
    border-radius: 16px;
}
stTabs [data-baseweb="tab"] {
    background-color: #FFFFFF;
    border-radius: 10px;
    padding: 8px 20px;
    color: #0369A1;
    font-weight: 700;
}
stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #0284C7 0%, #0369A1 100%) !important;
    color: #FFFFFF !important;
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
    st.error("⚠ Không tìm thấy file dữ liệu trong thư mục data/processed/!")
    st.stop()

df_master = df_master.dropna(subset=['AI_Capability', 'Worker_Receptiveness',
                                    'Automation_ROI_Score', 'Medical_Risk_Score', 'Task_Impact_Score'])
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
        <p style="color: #D1FAE5; font-size: 13px; margin-bottom: 0; font-weight: 700;">⚠ RỦI RO Y KHOA CAO</p>
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
# 5. GIAO DIỆN CHIA TABS VỚI MÀU SẮC ĐỒNG BỘ
# ==========================================
tab1, tab2, tab3, tab4 = st.tabs([
    "📍 Bức Tranh Toàn Cảnh & Ma Trận ROI",
    "📈 Phân Tích Đa Chiều Kỹ Năng Y Tế",
    "📊 Phân Bổ Chiến Lược & Tâm Lý Lao Động",
    "🔍 Tra Cứu Chi Tiết Tác Vụ Y TẾ"
])

# ------------------------------------------
# TAB 1: BỨC TRANH TOÀN CẢNH & MA TRẬN ROI
# ------------------------------------------
with tab1:
    st.subheader("🌐 ĐỊNH VỊ TÁC VỤ & ĐÁNH GIÁ RỦI RO Y KHOA")
    
    fig1 = px.scatter(
        df_filtered,
        x='AI_Capability',
        y='Worker_Receptiveness',
        color='Phân Vùng Tự Động Hóa',
        hover_name='Task',
        color_discrete_map=med_colors,
        size_max=15,
        title="NĂNG LỰC AI VS MỨC ĐỘ ĐÓN NHẬN"
    )
    fig1.update_layout(
        plot_bgcolor='#FFFFFF', paper_bgcolor='#FFFFFF',
        title_font_color='#0369A1', title_x=0.0, height=420,
        xaxis=dict(title="Năng lực AI", gridcolor='#E2E8F0'),
        yaxis=dict(title="Mức độ đón nhận", gridcolor='#E2E8F0')
    )
    st.plotly_chart(fig1, use_container_width=True)

    with st.container(border=True):
        st.markdown("### 🧠 GÓC NHÌN CHUYÊN GIA & ĐỊNH HƯỚNG QUẢN TRỊ")
        n_total = len(df_filtered)
        if n_total > 0:
            qw_pct = (len(df_filtered[df_filtered['Phân Vùng Tự Động Hóa'].str.contains('Quick Wins|Mỏ Vàng', na=False)]) / n_total) * 100
            sh_pct = (len(df_filtered[df_filtered['Phân Vùng Tự Động Hóa'].str.contains('Safe Haven|Thành Trì', na=False)]) / n_total) * 100
            um_pct = (len(df_filtered[df_filtered['Phân Vùng Tự Động Hóa'].str.contains('Unmet Needs|Chờ Công Nghệ', na=False)]) / n_total) * 100
            rs_pct = (len(df_filtered[df_filtered['Phân Vùng Tự Động Hóa'].str.contains('Resistance|Kháng Cự', na=False)]) / n_total) * 100

            c1, c2 = st.columns(2)
            with c1:
                st.markdown(f"""
                <div class="card-left-eval">
                    <h4 style="color: #4338CA; margin-top:0;">📊 Chỉ Số Tác Động Vận Hành</h4>
                    <ul style="margin-bottom:0; color: #1E1B4B;">
                        <li><b>Nhóm Mỏ Vàng AI (Quick Wins):</b> <span style="color:#059669; font-weight:bold;">{qw_pct:.1f}%</span> (Ưu tiên áp dụng ngay)</li>
                        <li><b>Nhóm Thành Trì (Safe Haven):</b> <span style="color:#E11D48; font-weight:bold;">{sh_pct:.1f}%</span> (Bác sĩ trực tiếp làm)</li>
                        <li><b>Nhóm Chờ Công Nghệ (Unmet Needs):</b> <span style="color:#D97706; font-weight:bold;">{um_pct:.1f}%</span> (Cần cải tiến AI)</li>
                        <li><b>Nhóm Kháng Cự (Resistance):</b> <span style="color:#4F0CEA; font-weight:bold;">{rs_pct:.1f}%</span> (Quản trị sự thay đổi)</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            with c2:
                st.markdown(f"""
                <div class="card-right-eval">
                    <h4 style="color: #0369A1; margin-top:0;">🔬 Phân Tích Thực Trạng Lâm Sàng</h4>
                    <p style="color: #0C4A6E; margin-bottom:0;">
                        Đang phân tích <b>{n_total} tác vụ</b> thuộc chuyên khoa <b>{selected_occ}</b>. 
                        Các tác vụ đòi hỏi sự tương tác trực tiếp và thấu cảm y khoa có điểm đón nhận thấp hơn nhưng tính an toàn cao hơn.
                    </p>
                </div>
                """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="conclusion-box-colorful">
                <h4 style="color: #065F46; margin-top:0;">🎯 ĐỊNH HƯỚNG HÀNH ĐỘNG & TRIỂN KHAI</h4>
                <p style="color: #064E3B; margin-bottom:0; font-size: 14.5px; line-line: 1.6;">
                    Dựa trên ma trận phân bổ <b>{selected_occ}</b>, đơn vị nên tập trung triển khai ngay <b>{qw_pct:.1f}% tác vụ Mỏ Vàng AI</b> để tối ưu hóa năng suất vận hành. Với <b>{sh_pct:.1f}% tác vụ Thành Trì Con Người</b>, tuyệt đối không thay thế hoàn toàn bằng AI mà chỉ dùng AI làm trợ lý tra cứu.
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("Không có dữ liệu phù hợp với bộ lọc hiện tại.")

# ------------------------------------------
# TAB 2: PHÂN TÍCH ĐA CHIỀU KỸ NĂNG Y TẾ
# ------------------------------------------
with tab2:
    st.subheader("🎯 ĐÁNH GIÁ ĐA CHIỀU NHÓM KỸ NĂNG Y TẾ")
    
    skill_list = df_skill['Nhóm Kỹ Năng Y Tế'].unique().tolist()
    selected_skills = st.multiselect("🔍 Lọc chọn nhóm Kỹ năng y tế để so sánh:", skill_list, default=skill_list[:min(3, len(skill_list))])
    
    if selected_skills:
        df_radar = df_skill[df_skill['Nhóm Kỹ Năng Y Tế'].isin(selected_skills)]
        df_melted = df_radar.melt(
            id_vars=['Nhóm Kỹ Năng Y Tế'],
            value_vars=['Avg_AI_Capability', 'Avg_Worker_Desire', 'Avg_Ethics_Empathy_Need'],
            var_name='Tiêu chí', value_name='Điểm số'
        )
        df_melted['Tiêu chí'] = df_melted['Tiêu chí'].replace({
            'Avg_AI_Capability': 'Năng lực AI',
            'Avg_Worker_Desire': 'Mong muốn TĐH',
            'Avg_Ethics_Empathy_Need': 'Yêu cầu Thấu cảm'
        })
        fig3 = px.line_polar(
            df_melted, r='Điểm số', theta='Tiêu chí', color='Nhóm Kỹ Năng Y Tế', line_close=True
        )
        fig3.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 5])),
            paper_bgcolor='#FFFFFF',
            margin=dict(t=20, b=20, l=0, r=0),
            height=380
        )
        st.plotly_chart(fig3, use_container_width=True)

        # Cụm Thẻ Khuyên Dùng dưới chân
        with st.container(border=True):
            col_t2_a, col_t2_b = st.columns(2)
            
            avg_ai = df_radar['Avg_AI_Capability'].mean()
            avg_desire = df_radar['Avg_Worker_Desire'].mean()
            avg_ethics = df_radar['Avg_Ethics_Empathy_Need'].mean()
            
            with col_t2_a:
                st.markdown(f"""
                <div class="card-left-eval">
                    <h4 style="color: #4338CA; margin-top:0;">📈 Đánh Giá Năng Lực Kỹ Năng</h4>
                    <ul style="margin-bottom:0; color: #1E1B4B;">
                        <li><b>Năng lực AI trung bình:</b> <span style="color:#6366F1; font-weight:bold;">{avg_ai:.2f} / 5.0</span></li>
                        <li><b>Nhu cầu Tự động hóa:</b> <span style="color:#6366F1; font-weight:bold;">{avg_desire:.2f} / 5.0</span></li>
                        <li><b>Yêu cầu Y đức & Thấu cảm:</b> <span style="color:#6366F1; font-weight:bold;">{avg_ethics:.2f} / 5.0</span></li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
                
            with col_t2_b:
                st.markdown(f"""
                <div class="card-right-eval">
                    <h4 style="color: #0369A1; margin-top:0;">🔍 Phân Tích Chuyên Sâu</h4>
                    <p style="color: #0C4A6E; margin-bottom:0;">
                        Các nhóm kỹ năng có yêu cầu <b>Y đức & Thấu cảm cao</b> thường đi kèm rủi ro lớn khi giao cho AI độc lập xử lý. Cần cơ chế kiểm soát kép giữa AI và Bác sĩ chuyên khoa.
                    </p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="conclusion-box-colorful">
                <h4 style="color: #065F46; margin-top:0;">💡 KẾT LUẬN & ĐỀ XUẤT ĐÀO TẠO KỸ NĂNG</h4>
                <p style="color: #064E3B; margin-bottom:0; font-size: 14.5px; line-height: 1.6;">
                    Khuyến nghị đơn vị đào tạo nhân sự tập trung vào các kỹ năng có điểm <b>Thấu cảm > 3.5</b>. 
                    Đối với các nhóm kỹ năng có điểm <b>Năng lực AI cao ({avg_ai:.1f})</b>, có thể tích hợp ngay vào quy trình đào tạo phần mềm tự động hóa cho nhân sự mới để giảm tải vận hành.
                </p>
            </div>
            """, unsafe_allow_html=True)

# ------------------------------------------
# TAB 3: PHÂN BỔ CHIẾN LƯỢC & TÂM LÝ LAO ĐỘNG
# ------------------------------------------
with tab3:
    st.subheader("📊 PHÂN BỔ CHIẾN LƯỢC & MỨC ĐỘ NỖI SỢ MẤT VIỆC")
    
    df_donut = df_filtered.copy()
    quadrant_counts = df_donut['Phân Vùng Tự Động Hóa'].value_counts().reset_index()
    quadrant_counts.columns = ['Phân Vùng', 'Số lượng Tác vụ']
    
    fig4 = px.pie(
        quadrant_counts, names='Phân Vùng', values='Số lượng Tác vụ', hole=0.45,
        color='Phân Vùng', color_discrete_map=med_colors, title="TỶ LỆ PHÂN BỔ TÁC VỤ KHẢO SÁT"
    )
    fig4.update_layout(margin=dict(t=30, b=10, l=0, r=0), paper_bgcolor='#FFFFFF', height=360)
    st.plotly_chart(fig4, use_container_width=True)

    with st.container(border=True):
        st.markdown("### 📊 Phân Tích Tâm Lý Nhân Sự & Đề Xuất Management")
        
        if 'Job_Security_Fear_Rate' in df_filtered.columns and not df_filtered.empty:
            avg_fear = df_filtered['Job_Security_Fear_Rate'].mean()
            max_fear_occ = df_filtered.groupby('Occupation (O*NET-SOC Title)')['Job_Security_Fear_Rate'].mean().idxmax()
            
            col_t3_a, col_t3_b = st.columns(2)
            with col_t3_a:
                st.markdown(f"""
                <div class="card-left-eval">
                    <h4 style="color: #4338CA; margin-top:0;">📉 Chỉ Số Tâm Lý Lao Động</h4>
                    <ul style="margin-bottom:0; color: #1E1B4B;">
                        <li><b>Mức lo ngại mất việc TB:</b> <span style="color:#E11D48; font-weight:bold;">{avg_fear:.1f}%</span></li>
                        <li><b>Chuyên khoa lo ngại nhất:</b> <span style="color:#4338CA; font-weight:bold;">{max_fear_occ}</span></li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            with col_t3_b:
                st.markdown(f"""
                <div class="card-right-eval">
                    <h4 style="color: #0369A1; margin-top:0;">💬 Nhận Định Quản Trị</h4>
                    <p style="color: #0C4A6E; margin-bottom:0;">
                        Mức độ e ngại của nhân sự tập trung chủ yếu ở nhóm tác vụ phân tích dữ liệu tự động, nơi AI có tốc độ xử lý vượt trội so với thao tác thủ công.
                    </p>
                </div>
                """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="conclusion-box-colorful">
                <h4 style="color: #065F46; margin-top:0;">💡 ĐỀ XUẤT TRUYỀN THÔNG NỘI BỘ</h4>
                <p style="color: #064E3B; margin-bottom:0; font-size: 14.5px; line-height: 1.6;">
                    Tỷ lệ lo ngại mất việc ở mức <b>{avg_fear:.1f}%</b>. Ban quản lý cần truyền thông rõ ràng rằng AI đóng vai trò <b>Trợ lý (Copilot)</b> nâng cao năng suất chứ không thay thế hoàn toàn vị trí chuyên môn của Y Bác sĩ.
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("💡 Chọn chuyên khoa cụ thể để xem phân tích tâm lý nhân sự.")

# ------------------------------------------
# TAB 4: TRA CỨU CHI TIẾT TÁC VỤ
# ------------------------------------------
with tab4:
    st.subheader("🔍 HỆ THỐNG TRA CỨU CHI TIẾT TÁC VỤ Y TẾ")
    
    col_sel1, col_sel2 = st.columns(2)
    with col_sel1:
        selected_role = st.selectbox("🏥 Lọc theo Ngành nhỏ / Nghề nghiệp:", ["Tất cả"] + occupations, key="t4_role")
        df_role_filtered = df_filtered.copy()
        if selected_role != "Tất cả":
            df_role_filtered = df_role_filtered[df_role_filtered['Occupation (O*NET-SOC Title)'] == selected_role]
        available_tasks = df_role_filtered['Task'].unique().tolist()
    
    with col_sel2:
        selected_task_option = st.selectbox("📋 Chọn Tác vụ Y tế cần tra cứu:", available_tasks if available_tasks else ["Không có dữ liệu"], key="t4_task")

    if available_tasks and selected_task_option in available_tasks:
        target_row = df_role_filtered[df_role_filtered['Task'] == selected_task_option].iloc[0]
    else:
        target_row = None

    if target_row is not None:
        st.markdown("#### 📊 Bảng Chỉ Số Tác Vụ Dữ Liệu")
        st.dataframe(
            pd.DataFrame([target_row[['AI_Capability', 'Worker_Receptiveness', 'Automation_ROI_Score', 'Medical_Risk_Score']]]),
            use_container_width=True
        )

        with st.container(border=True):
            col_t4_a, col_t4_b = st.columns(2)
            
            with col_t4_a:
                st.markdown(f"""
                <div class="card-left-eval">
                    <h4 style="color: #4338CA; margin-top:0;">📋 Tổng Quan Tác Vụ</h4>
                    <p style="color: #1E1B4B; margin-bottom: 5px;"><b>Tác vụ:</b> <i>{target_row['Task']}</i></p>
                    <p style="color: #1E1B4B; margin-bottom: 5px;"><b>Chuyên khoa:</b> <code>{target_row['Occupation (O*NET-SOC Title)']}</code></p>
                    <p style="color: #1E1B4B; margin-bottom: 0;"><b>Phân vùng:</b> <span style="color:#059669; font-weight:bold;">{target_row['Phân Vùng Tự Động Hóa']}</span></p>
                </div>
                """, unsafe_allow_html=True)
                
            with col_t4_b:
                st.markdown(f"""
                <div class="card-right-eval">
                    <h4 style="color: #0369A1; margin-top:0;">📈 Chi Tiết Điểm Số</h4>
                    <ul style="margin-bottom:0; color: #0C4A6E;">
                        <li><b>Năng lực AI:</b> <code>{target_row['AI_Capability']}/5.0</code> | <b>Mức đón nhận:</b> <code>{target_row['Worker_Receptiveness']}/5.0</code></li>
                        <li><b>Điểm ROI:</b> <code>{target_row['Automation_ROI_Score']}</code> | <b>Rủi ro Y khoa:</b> <code>{target_row['Medical_Risk_Score']}/5.0</code></li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            
            q = target_row['Phân Vùng Tự Động Hóa']
            if 'Mỏ Vàng' in q or 'Quick Wins' in q:
                rec_text = "<b>Ưu tiên triển khai ngay.</b> Tác vụ có hiệu quả ROI cao, rủi ro thấp và được nhân sự đón nhận tích cực."
            elif 'Thành Trì' in q or 'Safe Haven' in q:
                rec_text = "<b>Không tự động hóa hoàn toàn.</b> Yêu cầu Bác sĩ chuyên khoa trực tiếp xử lý để đảm bảo an toàn lâm sàng."
            elif 'Chờ Công Nghệ' in q or 'Unmet Needs' in q:
                rec_text = "<b>Chạy thử nghiệm (Pilot).</b> Nhân sự rất mong muốn tự động hóa nhưng cần theo dõi độ chính xác của AI."
            else:
                rec_text = "<b>Đào tạo & Truyền thông.</b> Cần tập huấn để nhân sự tin tưởng hơn vào độ chính xác của công cụ AI."

            st.markdown(f"""
            <div class="conclusion-box-colorful">
                <h4 style="color: #065F46; margin-top:0;">💡 ĐỀ XUẤT CHIẾN LƯỢC TRIỂN KHAI</h4>
                <p style="color: #064E3B; margin-bottom:0; font-size: 14.5px; line-height: 1.6;">{rec_text}</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Vui lòng chọn 1 tác vụ để tra cứu thông tin chi tiết.")