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
    background-color: #F8FAFC;
    color: #1E293B;
}
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0284C7 0%, #0369A1 50%, #0F172A 100%);
    border-right: 1px solid #0284C7;
}
section[data-testid="stSidebar"] p, section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] label, section[data-testid="stSidebar"] h3 {
    color: #F8FAFC !important;
}
h1, h2, h3 {
    color: #0369A1 !important;
}
p, .stMarkdown p, span, label {
    color: #334155 !important;
}

/* --- THẺ THỨ 1: MÀU OMBRE CHUẨN XÁC NHƯ ẢNH MẪU --- */
.metric-card-1 {
    background: linear-gradient(135deg, rgba(237, 233, 254, 0.95) 0%, rgba(243, 244, 246, 0.4) 60%, rgba(255, 255, 255, 0.9) 100%);
    border: 1px solid #E9D5FF;
    padding: 24px;
    border-radius: 20px;
    box-shadow: 0 10px 30px -5px rgba(168, 85, 247, 0.12);
}
.metric-card-2 {
    background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 50%, #DB2777 100%);
    padding: 22px;
    border-radius: 20px;
    box-shadow: 0 15px 30px -5px rgba(124, 58, 237, 0.35), 0 8px 12px -6px rgba(124, 58, 237, 0.2);
}
.metric-card-3 {
    background: linear-gradient(135deg, #E11D48 0%, #F43F5E 50%, #FB923C 100%);
    padding: 22px;
    border-radius: 20px;
    box-shadow: 0 15px 30px -5px rgba(225, 29, 72, 0.35), 0 8px 12px -6px rgba(225, 29, 72, 0.2);
}

/* --- PHẦN KẾT LUẬN & ĐỊNH HƯỚNG OMBRE & 3D SIÊU THỰC --- */
.gradient-expert-container {
    background: linear-gradient(145deg, #FFFFFF 0%, #F1F5F9 100%);
    border: 1px solid #CBD5E1;
    border-radius: 24px;
    padding: 32px;
    margin-top: 30px;
    box-shadow: 0 20px 40px -10px rgba(15, 23, 42, 0.08), 0 0 1px 1px rgba(255, 255, 255, 0.8) inset;
}
.grad-card-left {
    background: linear-gradient(135deg, #F3E8FF 0%, #E9D5FF 100%);
    border: 1px solid #D8B4FE;
    border-radius: 18px;
    padding: 24px;
    height: 100%;
    box-shadow: 0 10px 25px -5px rgba(168, 85, 247, 0.12);
}
.grad-card-right {
    background: linear-gradient(135deg, #E0F2FE 0%, #BAE6FD 100%);
    border: 1px solid #7DD3FC;
    border-radius: 18px;
    padding: 24px;
    height: 100%;
    box-shadow: 0 10px 25px -5px rgba(2, 132, 199, 0.12);
}
.grad-action-box {
    background: linear-gradient(135deg, #059669 0%, #10B981 50%, #34D399 100%);
    border-radius: 18px;
    padding: 26px;
    margin-top: 24px;
    box-shadow: 0 15px 30px -5px rgba(16, 185, 129, 0.3);
}
.grad-action-box h4, .grad-action-box p {
    color: #FFFFFF !important;
}

.rec-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 16px;
    padding: 20px 22px;
    margin-bottom: 14px;
    box-shadow: 0 8px 20px -4px rgba(15, 23, 42, 0.04);
    border-left: 6px solid #10B981;
}

stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: linear-gradient(135deg, #CBD5E1 0%, #93C5FD 100%);
    padding: 8px;
    border-radius: 18px;
    border: 1px solid #94A3B8;
}
stTabs [data-baseweb="tab"] {
    background-color: #FFFFFF;
    border-radius: 12px;
    padding: 8px 16px;
    color: #0369A1;
    font-weight: 700;
    border: 1px solid #BAE6FD;
    box-shadow: 0 4px 10px rgba(0,0,0,0.03);
    font-size: 13.5px;
}
stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #0284C7 0%, #0369A1 50%, #0F172A 100%) !important;
    color: #FFFFFF !important;
    font-weight: 800;
    box-shadow: 0 8px 20px rgba(2, 132, 199, 0.35);
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. TẢI VÀ LÀM SẠCH DỮ LIỆU & DỊCH THUẬT TOÀN DIỆN
# ==========================================
@st.cache_data
def load_data():
    df_master = pd.read_csv("data/processed/analytics_master.csv")
    df_skill = pd.read_csv("data/processed/insight_skill_vulnerability.csv")
    df_top_ai = pd.read_csv("data/processed/top_ai_tasks.csv")
    return df_master, df_skill, df_top_ai

try:
    df_master, df_skill, df_top_ai = load_data()
except FileNotFoundError:
    st.error("⚠️ Không tìm thấy file dữ liệu trong thư mục!")
    st.stop()

occupation_translation = {
    "Medical and Health Services Managers": "Quản lý Dịch vụ Y tế & Sức khỏe",
    "Clinical Research Coordinators": "Điều phối viên Nghiên cứu Lâm sàng",
    "Radiologists": "Bác sĩ Chẩn đoán Hình ảnh (X-quang)",
    "Clinical Data Managers": "Quản lý Dữ liệu Lâm sàng",
    "Medical Transcriptionists": "Chuyên viên Lưu trữ & Xử lý Bệnh án",
    "Health Informatics Specialists": "Chuyên gia Tin học Y tế",
    "Bioinformatics Scientists": "Nhà khoa học Tin sinh học",
    "Molecular and Cellular Biologists": "Nhà sinh học Phân tử & Tế bào",
    "Biostatisticians": "Chuyên gia Thống kê Sinh học"
}

quadrant_translation = {
    "1. Mỏ Vàng AI (Quick Wins)": "Mỏ Vàng AI (Thí điểm ngay)",
    "2. Vùng Kháng Cự (Resistance)": "Vùng Kháng Cự (Cần quản trị thay đổi)",
    "4. Thành Trì Con Người (Safe Haven)": "Thành Trì Con Người (Bác sĩ chuyên trách)",
    "3. Chờ Công Nghệ (Unmet Needs)": "Chờ Công Nghệ (Tiềm năng tương lai)"
}

def translate_task(task_str):
    if not isinstance(task_str, str):
        return task_str
    lower_t = task_str.lower()
    
    if "prepare or review reports" in lower_t or "manuscripts" in lower_t:
        return "Soạn thảo hoặc kiểm duyệt các báo cáo khoa học, tài liệu nghiên cứu tế bào và ấn phẩm y sinh."
    elif "instruct undergraduate" in lower_t or "graduate students" in lower_t:
        return "Giảng dạy và hướng dẫn học viên đại học, sau đại học về các phương pháp sinh học phân tử."
    elif "compile and analyze" in lower_t or "molecular" in lower_t:
        return "Tổng hợp và phân tích dữ liệu phân tử, tế bào hoặc di truyền phục vụ nghiên cứu lâm sàng."
    elif "evaluate new technologies" in lower_t:
        return "Đánh giá các công nghệ mới nhằm nâng cao độ chính xác trong xét nghiệm và chẩn đoán."
    elif "comprehensive interpretative" in lower_t:
        return "Thực hiện phân tích giải thích toàn diện các kết quả chẩn đoán hình ảnh phức tạp."
    elif "perform or interpret the outcomes" in lower_t:
        return "Thực hiện và diễn giải kết quả các ca can thiệp chẩn đoán hình ảnh chuyên sâu."
    elif "document the performance" in lower_t:
        return "Lập tài liệu ghi nhận hiệu suất và kiểm định chất lượng thiết bị chẩn đoán y khoa."
    elif "generate data queries" in lower_t:
        return "Tạo các truy vấn dữ liệu y tế dựa trên các tiêu chí hợp thức hóa."
    elif "monitor work productivity" in lower_t:
        return "Giám sát năng suất và chất lượng công việc của nhân sự khoa phòng."
    elif "prepare data analysis listings" in lower_t:
        return "Chuẩn bị danh mục phân tích dữ liệu và báo cáo tài chính y tế."
    elif "analyze clinical data" in lower_t:
        return "Phân tích dữ liệu lâm sàng bằng các công cụ thống kê chuyên sâu."
    elif "develop technical specifications" in lower_t:
        return "Phát triển các thông số kỹ thuật cho hệ thống công nghệ thông tin y tế."
    elif "track the flow of work forms" in lower_t:
        return "Theo dõi luồng biểu mẫu công việc, bao gồm hồ sơ bệnh án và quy trình thanh toán."
    elif "develop new software applications" in lower_t:
        return "Phát triển các ứng dụng phần mềm mới hoặc tùy chỉnh hệ thống quản lý bệnh viện."
    elif "fiscal" in lower_t or "budget" in lower_t or "accounting" in lower_t:
        return "Quản lý và điều hành các hoạt động tài chính, kế toán và lập ngân sách y tế."
    elif "medicine" in lower_t or "computerized diagnostic" in lower_t:
        return "Cập nhật tiến bộ y khoa, hệ thống chẩn đoán vi tính và phương pháp điều trị lâm sàng."
    elif "schedules" in lower_t or "assignments" in lower_t or "workload" in lower_t:
        return "Lập lịch làm việc và phân công nhân sự y tế dựa trên khối lượng công việc và nguồn lực."
    elif "facility activities" in lower_t or "cash and risk" in lower_t:
        return "Đánh giá hoạt động cơ sở y tế nhằm hỗ trợ lập kế hoạch, quản lý dòng tiền và kiểm soát rủi ro."
    elif "activity reports" in lower_t or "implementation" in lower_t:
        return "Chuẩn bị báo cáo hoạt động để thông báo cho ban quản lý về tiến độ triển khai kế hoạch."
    elif "appointments" in lower_t or "inpatient" in lower_t:
        return "Lịch hẹn khám, thủ tục cho bệnh nhân hoặc bố trí giường bệnh nội trú theo yêu cầu."
    elif "transcribe" in lower_t or "medical reports" in lower_t:
        return "Phiên âm và tổng hợp các báo cáo y tế như bệnh sử, khám thực thể và tóm tắt xuất viện."
    elif "record management" in lower_t or "process data" in lower_t:
        return "Xây dựng và duy trì hệ thống quản lý hồ sơ điện tử để lưu trữ và xử lý dữ liệu."
    elif "medical files" in lower_t or "databases" in lower_t:
        return "Thiết lập và quản lý cơ sở dữ liệu y tế bao gồm phim X-quang, kết quả xét nghiệm và hồ sơ lâm sàng."
    else:
        return "Thực thi, kiểm định và tối ưu hóa quy trình nghiệp vụ chuyên môn y tế."

for df in [df_master, df_top_ai]:
    if 'Occupation (O*NET-SOC Title)' in df.columns:
        df['Occupation (O*NET-SOC Title)'] = df['Occupation (O*NET-SOC Title)'].map(occupation_translation).fillna(df['Occupation (O*NET-SOC Title)'])
    if 'Automation_Quadrant' in df.columns:
        df['Automation_Quadrant'] = df['Automation_Quadrant'].map(quadrant_translation).fillna(df['Automation_Quadrant'])
    if 'Task' in df.columns:
        df['Task_Vi'] = df['Task'].apply(translate_task)

df_master = df_master.dropna(subset=['AI_Capability', 'Worker_Receptiveness',
                                    'Automation_ROI_Score', 'Medical_Risk_Score', 'Task_Impact_Score'])
df_master = df_master[df_master['Automation_Quadrant'] != 'Chưa xác định']
df_master['Phân Vùng Tự Động Hóa'] = df_master['Automation_Quadrant']

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
    'Mỏ Vàng AI (Thí điểm ngay)': '#10B981',
    'Thành Trì Con Người (Bác sĩ chuyên trách)': '#6366F1',
    'Chờ Công Nghệ (Tiềm năng tương lai)': '#F59E0B',
    'Vùng Kháng Cự (Cần quản trị thay đổi)': "#EF4444"
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
    st.markdown("🎚️ **BỘ LỌC THÔNG SỐ ĐỘNG**")
    min_roi, max_roi = float(df_master['Automation_ROI_Score'].min()), float(df_master['Automation_ROI_Score'].max())
    selected_roi_range = st.slider("Khoảng chỉ số Sinh lời (ROI):", min_value=min_roi, max_value=max_roi, value=(min_roi, max_roi))
    
    max_risk = float(df_master['Medical_Risk_Score'].max())
    selected_max_risk = st.slider("Ngưỡng Rủi ro Y khoa tối đa:", min_value=0.0, max_value=max_risk, value=max_risk)
    
    st.markdown("---")
    st.info("💡 **Hệ thống Quản trị:** Phân tích tác vụ tự động hóa và rủi ro y khoa dựa trên dữ liệu O*NET.")

# ==========================================
# 4. HEADER CHÍNH & METRIC CARDS TRỰC QUAN
# ==========================================
col_logo, col_title = st.columns([0.08, 0.92])
with col_logo:
    st.image("HUB.png", width=65)
with col_title:
    st.markdown("### NỀN TẢNG ĐỊNH LƯỢNG CHIẾN LƯỢC AI & TỰ ĐỘNG HÓA Y TẾ")
    st.markdown("##### *Nền tảng phân tích định lượng tác vụ, đánh giá năng lực AI (AI Capability), chỉ số sinh lời vận hành (Automation ROI) và quản trị rủi ro lâm sàng (Clinical Risk Assessment).*")

st.write("")

df_filtered = df_master.copy()
if selected_occ != "Tất cả Chuyên khoa":
    df_filtered = df_filtered[df_filtered['Occupation (O*NET-SOC Title)'] == selected_occ]
if selected_quadrant != "Tất cả phân vùng":
    df_filtered = df_filtered[df_filtered['Phân Vùng Tự Động Hóa'] == selected_quadrant]
df_filtered = df_filtered[
    (df_filtered['Automation_ROI_Score'] >= selected_roi_range[0]) &
    (df_filtered['Automation_ROI_Score'] <= selected_roi_range[1]) &
    (df_filtered['Medical_Risk_Score'] <= selected_max_risk)
]

total_tasks = len(df_filtered)
quick_wins = len(df_filtered[df_filtered['Phân Vùng Tự Động Hóa'].str.contains('Mỏ Vàng AI')])
high_risk = len(df_filtered[df_filtered['Medical_Risk_Score'] > 2.0])

col_m1, col_m2, col_m3 = st.columns(3)
with col_m1:
    st.markdown(f"""
    <div class="metric-card-1">
        <p style="color: #475569; font-size: 13px; margin-bottom: 0; font-weight: 700;"> TỔNG SỐ TÁC VỤ KHẢO SÁT</p>
        <h2 style="color: #0F172A; margin-top: 5px; margin-bottom: 5px;">{total_tasks} <span style="font-size: 13px; color: #059669; font-weight: 600;">Tác vụ y tế</span></h2>
        <p style="color: #64748B; font-size: 12px; margin: 0;">Đang được phân tích mức độ tự động hóa</p>
    </div>
    """, unsafe_allow_html=True)

with col_m2:
    st.markdown(f"""
    <div class="metric-card-2">
        <p style="color: #E0F2FE; font-size: 13px; margin-bottom: 0; font-weight: 700;">MỎ VÀNG AI (THÍ ĐIỂM NGAY)</p>
        <h2 style="color: #FFFFFF; margin-top: 5px; margin-bottom: 5px;">{quick_wins} <span style="font-size: 13px; color: #E0F2FE; font-weight: 600;">Tác vụ</span></h2>
        <p style="color: #E0F2FE; font-size: 12px; margin: 0;">Nên ưu tiên ứng dụng AI triển khai ngay</p>
    </div>
    """, unsafe_allow_html=True)

with col_m3:
    st.markdown(f"""
    <div class="metric-card-3">
        <p style="color: #FEF2F2; font-size: 13px; margin-bottom: 0; font-weight: 700;">RỦI RO Y KHOA CAO</p>
        <h2 style="color: #FFFFFF; margin-top: 5px; margin-bottom: 5px;">{high_risk} <span style="font-size: 13px; color: #FEF2F2; font-weight: 600;">Tác vụ</span></h2>
        <p style="color: #FEF2F2; font-size: 12px; margin: 0;">Bắt buộc Bác sĩ kiểm duyệt chặt chẽ</p>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# ==========================================
# 5. GIAO DIỆN CHIA TABS
# ==========================================
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📍 Bức Tranh Toàn Cảnh & Ma Trận ROI",
    "📈 Phân Tích Đa Chiều Kỹ Năng Y Tế",
    "📊 Phân Bổ Chiến Lược & Tâm Lý Lao Động",
    "🚀 Top Khuyến Nghị Thí Điểm",
    "🔍 Tra Cứu Chi Tiết Tác Vụ Y TẾ",
    "🔮 Mô Phỏng Giả Định & Đầu Tư AI"
])

# TAB 1: BỨC TRANH TOÀN CẢNH & ROI
with tab1:
    st.subheader("ĐỊNH VỊ TÁC VỤ & ĐÁNH GIÁ RỦI RO Y KHOA")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #FFFFFF 0%, #F1F5F9 100%); border: 1px solid #CBD5E1; border-top: 5px solid #0284C7; border-radius: 16px 16px 0 0; padding: 18px 22px 12px 22px; margin-bottom: 0; box-shadow: 0 4px 15px rgba(2, 132, 199, 0.08);">
            <h4 style="color: #0369A1 !important; margin: 0; font-size: 15px; font-weight: 800; letter-spacing: 0.5px;">NĂNG LỰC AI VS ĐÓN NHẬN CỦA Y BÁC SĨ</h4>
        </div>
        """, unsafe_allow_html=True)
        
        fig1 = px.scatter(
            df_filtered,
            x='AI_Capability',
            y='Worker_Receptiveness',
            color='Phân Vùng Tự Động Hóa',
            hover_name='Task_Vi',
            color_discrete_map=med_colors,
            size_max=12,
            opacity=0.85
        )
        fig1.update_layout(
            plot_bgcolor='#FFFFFF',
            paper_bgcolor='#FFFFFF',
            margin=dict(t=10, b=20, l=20, r=20),
            font=dict(color="#335547", size=12),
            xaxis=dict(title="Năng lực của AI (Score)", title_font=dict(color='#0369A1'), tickfont=dict(color='#334155'), gridcolor='#F1F5F9', zeroline=False),
            yaxis=dict(title="Mức độ đón nhận của nhân sự (Score)", title_font=dict(color='#0369A1'), tickfont=dict(color='#334155'), gridcolor='#F1F5F9', zeroline=False),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                font=dict(color='#334155', size=11),
                title=dict(text="", font=dict(color='#0369A1', size=1)),
                bgcolor='rgba(255, 255, 255, 0.95)',
                bordercolor='#CBD5E1',
                borderwidth=1
            )
        )
        st.plotly_chart(fig1, use_container_width=True, config={'displayModeBar': False})

    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #FFFFFF 0%, #F1F5F9 100%); border: 1px solid #CBD5E1; border-top: 5px solid #10B981; border-radius: 16px 16px 0 0; padding: 18px 22px 12px 22px; margin-bottom: 0; box-shadow: 0 4px 15px rgba(16, 185, 129, 0.08);">
            <h4 style="color: #0369A1 !important; margin: 0; font-size: 15px; font-weight: 800; letter-spacing: 0.5px;">MA TRẬN SINH LỜI (ROI) & RỦI RO</h4>
        </div>
        """, unsafe_allow_html=True)

        fig2 = px.scatter(
            df_filtered,
            x='Automation_ROI_Score',
            y='Medical_Risk_Score',
            size='Task_Impact_Score',
            color='Phân Vùng Tự Động Hóa',
            hover_name='Task_Vi',
            color_discrete_map=med_colors,
            size_max=16,
            opacity=0.85
        )
        if not df_filtered.empty:
            mid_roi = df_filtered['Automation_ROI_Score'].median()
            mid_risk = df_filtered['Medical_Risk_Score'].median()
            fig2.add_hline(y=mid_risk, line_dash="dash", line_color="#EF4444")
            fig2.add_vline(x=mid_roi, line_dash="dash", line_color="#10B981")
        
        fig2.update_layout(
            plot_bgcolor='#FFFFFF',
            paper_bgcolor='#FFFFFF',
            margin=dict(t=10, b=20, l=20, r=20),
            font=dict(color='#334155', size=12),
            xaxis=dict(title="Chỉ số Sinh lời (ROI)", title_font=dict(color='#0369A1'), tickfont=dict(color='#334155'), gridcolor='#F1F5F9', zeroline=False),
            yaxis=dict(title="Điểm rủi ro y khoa", title_font=dict(color='#0369A1'), tickfont=dict(color='#334155'), gridcolor='#F1F5F9', zeroline=False),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                font=dict(color='#334155', size=11),
                title=dict(text="", font=dict(color='#0369A1', size=1)),
                bgcolor='rgba(255, 255, 255, 0.95)',
                bordercolor='#CBD5E1',
                borderwidth=1
            )
        )
        st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})

    # KẾT LUẬN TAB 1
    if total_tasks > 0:
        pct_quick = quick_wins / total_tasks * 100
        pct_safe = len(df_filtered[df_filtered['Phân Vùng Tự Động Hóa'].str.contains('Thành Trì')]) / total_tasks * 100
        pct_unmet = len(df_filtered[df_filtered['Phân Vùng Tự Động Hóa'].str.contains('Chờ Công Nghệ')]) / total_tasks * 100
        pct_resist = len(df_filtered[df_filtered['Phân Vùng Tự Động Hóa'].str.contains('Kháng Cự')]) / total_tasks * 100
    else:
        pct_quick = pct_safe = pct_unmet = pct_resist = 0.0

    st.markdown(f"""
    <div class="gradient-expert-container">
        <h3 style="color: #0F172A !important; margin-top: 0; margin-bottom: 22px; font-size: 20px; font-weight: 800;">🧠 GÓC NHÌN CHUYÊN GIA & ĐỊNH HƯỚNG QUẢN TRỊ</h3>
        <div style="display: flex; gap: 24px;">
            <div style="flex: 1;">
                <div class="grad-card-left">
                    <h4 style="color: #6D28D9; margin-top: 0; margin-bottom: 14px; font-size: 16px; font-weight: 700;">Chỉ Số Tác Động Vận Hành</h4>
                    <ul style="color: #334155; padding-left: 20px; line-height: 1.9; margin-bottom: 0; font-size: 14px;">
                        <li><b>Nhóm Mỏ Vàng AI: {pct_quick:.1f}%</b> (Ưu tiên áp dụng ngay)</li>
                        <li><b>Nhóm Thành Trì Con Người: {pct_safe:.1f}%</b> (Bác sĩ chuyên trách)</li>
                        <li><b>Nhóm Chờ Công Nghệ: {pct_unmet:.1f}%</b> (Tiềm năng tương lai)</li>
                        <li><b>Nhóm Kháng Cự: {pct_resist:.1f}%</b> (Quản trị sự thay đổi)</li>
                    </ul>
                </div>
            </div>
            <div style="flex: 1;">
                <div class="grad-card-right">
                    <h4 style="color: #0284C7; margin-top: 0; margin-bottom: 14px; font-size: 16px; font-weight: 700;">Phân Tích Thực Trạng Lâm Sàng</h4>
                    <p style="color: #334155; line-height: 1.7; margin-bottom: 0; font-size: 14px;">Đang phân tích <b>{total_tasks}</b> tác vụ phù hợp với các tiêu chí lọc. Các tác vụ đòi hỏi sự tương tác trực tiếp và thấu cảm y khoa có điểm đón nhận thấp hơn nhưng tính an toàn cao hơn.</p>
                </div>
            </div>
        </div>
        <div class="grad-action-box">
            <h4 style="color: #FFFFFF; margin-top: 0; margin-bottom: 10px; font-size: 18px; font-weight: 800;">ĐỊNH HƯỚNG HÀNH ĐỘNG & TRIỂN KHAI</h4>
            <p style="color: #F0FDF4; margin-bottom: 0; line-height: 1.7; font-size: 15px;">Dựa trên bộ lọc hiện tại, đơn vị nên tập trung triển khai ngay <b>{pct_quick:.1f}%</b> tác vụ Mỏ Vàng AI để tối ưu hóa năng suất vận hành. Với các tác vụ Thành Trì Con Người, tuyệt đối không thay thế hoàn toàn bằng AI mà chỉ dùng AI làm trợ lý tra cứu.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# TAB 2: RADAR PHÂN TÍCH KỸ NĂNG
with tab2:
    st.subheader("ĐÁNH GIÁ ĐA CHIỀU NHÓM KỸ NĂNG Y TẾ")
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #FFFFFF 0%, #F1F5F9 100%); border: 1px solid #CBD5E1; border-top: 5px solid #6366F1; border-radius: 16px 16px 0 0; padding: 18px 22px 12px 22px; margin-bottom: 0; box-shadow: 0 4px 15px rgba(99, 102, 241, 0.08);">
        <h4 style="color: #0369A1 !important; margin: 0; font-size: 15px; font-weight: 800; letter-spacing: 0.5px;">BIỂU ĐỒ RADAR CHUYÊN SÂU KỸ NĂNG Y TẾ (THANG ĐIỂM 5)</h4>
    </div>
    """, unsafe_allow_html=True)

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
            line_close=True
        )
        fig3.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 5], tickfont=dict(color='#334155'), gridcolor='#CBD5E1'),
                angularaxis=dict(tickfont=dict(color='#0369A1', size=11, family="sans-serif")),
                bgcolor='#FFFFFF'
            ),
            plot_bgcolor='#FFFFFF',
            paper_bgcolor='#FFFFFF',
            margin=dict(t=20, b=20, l=20, r=20),
            font=dict(color='#334155', size=12),
            legend=dict(
                font=dict(color='#334155', size=11),
                title=dict(font=dict(color='#0369A1', size=12)),
                bgcolor='rgba(255, 255, 255, 0.95)',
                bordercolor='#CBD5E1',
                borderwidth=1
            )
        )
        st.plotly_chart(fig3, use_container_width=True, config={'displayModeBar': False})

        if not df_radar.empty:
            max_ai_skill = df_radar.loc[df_radar['Avg_AI_Capability'].idxmax()]['Nhóm Kỹ Năng Y Tế']
            max_ethic_skill = df_radar.loc[df_radar['Avg_Ethics_Empathy_Need'].idxmax()]['Nhóm Kỹ Năng Y Tế']
            
            st.markdown(f"""
            <div class="gradient-expert-container">
                <h3 style="color: #0F172A !important; margin-top: 0; margin-bottom: 22px; font-size: 20px; font-weight: 800;">🧠 GÓC NHÌN CHUYÊN GIA & ĐỊNH HƯỚNG QUẢN TRỊ</h3>
                <div style="display: flex; gap: 24px;">
                    <div style="flex: 1;">
                        <div class="grad-card-left">
                            <h4 style="color: #6D28D9; margin-top: 0; margin-bottom: 14px; font-size: 16px; font-weight: 700;">Đặc Trưng Kỹ Năng</h4>
                            <ul style="color: #334155; padding-left: 20px; line-height: 1.9; margin-bottom: 0; font-size: 14px;">
                                <li><b>Dễ bị AI can thiệp nhất:</b> {max_ai_skill}</li>
                                <li><b>Đòi hỏi Y đức cao nhất:</b> {max_ethic_skill}</li>
                                <li><b>Số nhóm kỹ năng đang xét:</b> {len(selected_skills)} nhóm</li>
                            </ul>
                        </div>
                    </div>
                    <div style="flex: 1;">
                        <div class="grad-card-right">
                            <h4 style="color: #0284C7; margin-top: 0; margin-bottom: 14px; font-size: 16px; font-weight: 700;">Phân Tích Yêu Cầu</h4>
                            <p style="color: #334155; line-height: 1.7; margin-bottom: 0; font-size: 14px;">Các kỹ năng có điểm <b>"Yêu cầu Y đức & Thấu cảm"</b> cao thường có <b>"Mong muốn Tự động hóa"</b> thấp. Y bác sĩ có xu hướng giữ lại các tương tác trực tiếp với bệnh nhân thay vì giao toàn quyền cho máy móc.</p>
                        </div>
                    </div>
                </div>
                <div class="grad-action-box">
                    <h4 style="color: #FFFFFF; margin-top: 0; margin-bottom: 10px; font-size: 18px; font-weight: 800;">ĐỊNH HƯỚNG HÀNH ĐỘNG & TRIỂN KHAI</h4>
                    <p style="color: #F0FDF4; margin-bottom: 0; line-height: 1.7; font-size: 15px;">Khuyến nghị ứng dụng AI vào vai trò <b>hỗ trợ phân tích dữ liệu và hệ thống thông tin</b>. Đặc biệt đối với các nhóm kỹ năng như <i>{max_ethic_skill}</i>, AI chỉ nên đóng vai trò cung cấp thông tin nền, quyết định cuối cùng và việc giao tiếp đồng cảm bắt buộc phải do nhân sự y tế thực hiện.</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ Vui lòng chọn ít nhất 1 Kỹ năng ở thanh chọn bên trên để hiển thị biểu đồ Radar.")

# TAB 3: PHÂN BỔ CHIẾN LƯỢC & NỖI SỢ MẤT VIỆC
with tab3:
    st.subheader("PHÂN BỔ CHIẾN LƯỢC & MỨC ĐỘ NỖI SỢ MẤT VIỆC")
    col3, col4 = st.columns(2)
    
    quadrant_counts = df_filtered['Phân Vùng Tự Động Hóa'].value_counts().reset_index()
    quadrant_counts.columns = ['Phân Vùng', 'Số lượng Tác vụ']
    
    with col3:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #FFFFFF 0%, #F1F5F9 100%); border: 1px solid #CBD5E1; border-top: 5px solid #F59E0B; border-radius: 16px 16px 0 0; padding: 18px 22px 12px 22px; margin-bottom: 0; box-shadow: 0 4px 15px rgba(245, 158, 11, 0.08);">
            <h4 style="color: #0369A1 !important; margin: 0; font-size: 15px; font-weight: 800; letter-spacing: 0.5px;">TỶ LỆ PHÂN BỔ TÁC VỤ</h4>
        </div>
        """, unsafe_allow_html=True)

        fig4 = px.pie(
            quadrant_counts,
            names='Phân Vùng',
            values='Số lượng Tác vụ',
            hole=0.4,
            color='Phân Vùng',
            color_discrete_map=med_colors
        )
        fig4.update_traces(
            textinfo='percent',
            textposition='inside',
            textfont=dict(color='#FFFFFF', size=13, family="Arial Black")
        )
        fig4.update_layout(
            paper_bgcolor='#FFFFFF',
            plot_bgcolor='#FFFFFF',
            margin=dict(t=10, b=10, l=10, r=10),
            legend=dict(
                font=dict(color='#334155', size=11),
                title=dict(font=dict(color='#0369A1', size=12)),
                bgcolor='rgba(255, 255, 255, 0.95)',
                bordercolor='#CBD5E1',
                borderwidth=1
            )
        )
        st.plotly_chart(fig4, use_container_width=True, config={'displayModeBar': False})

    with col4:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #FFFFFF 0%, #F1F5F9 100%); border: 1px solid #CBD5E1; border-top: 5px solid #EF4444; border-radius: 16px 16px 0 0; padding: 18px 22px 12px 22px; margin-bottom: 0; box-shadow: 0 4px 15px rgba(239, 68, 68, 0.08);">
            <h4 style="color: #0369A1 !important; margin: 0; font-size: 15px; font-weight: 800; letter-spacing: 0.5px;">NỖI SỢ MẤT VIỆC THEO NHÓM ĐÃ LỌC</h4>
        </div>
        """, unsafe_allow_html=True)

        if 'Job_Security_Fear_Rate' in df_filtered.columns:
            fear_df = df_filtered.groupby('Occupation (O*NET-SOC Title)')['Job_Security_Fear_Rate'].mean().reset_index()
            fear_df = fear_df.sort_values(by='Job_Security_Fear_Rate', ascending=True)
            fear_df = fear_df.rename(columns={'Job_Security_Fear_Rate': 'Tỷ lệ lo ngại'})
            
            fig5 = px.bar(
                fear_df,
                x='Tỷ lệ lo ngại',
                y='Occupation (O*NET-SOC Title)',
                orientation='h',
                color='Tỷ lệ lo ngại',
                color_continuous_scale='Reds'
            )
            fig5.update_layout(
                paper_bgcolor='#FFFFFF',
                plot_bgcolor='#FFFFFF',
                margin=dict(t=10, b=10, l=10, r=10),
                font=dict(color='#334155', size=12),
                xaxis=dict(
                    title="Tỷ lệ sợ bị thay thế (%)", 
                    title_font=dict(color='#0369A1'),
                    tickfont=dict(color='#334155'),
                    gridcolor='#E2E8F0',
                    zeroline=False
                ),
                yaxis=dict(
                    title="", 
                    tickfont=dict(color='#334155')
                ),
                coloraxis_colorbar=dict(
                    title=dict(text="Tỷ lệ", font=dict(color='#0369A1')),
                    tickfont=dict(color='#334155')
                )
            )
            st.plotly_chart(fig5, use_container_width=True, config={'displayModeBar': False})
        else:
            fear_df = pd.DataFrame()
            st.info("💡 Không tìm thấy cột 'Job_Security_Fear_Rate' trong dataset để vẽ biểu đồ nỗi sợ mất việc.")

    if not quadrant_counts.empty and 'Job_Security_Fear_Rate' in df_filtered.columns:
        top_quadrant = quadrant_counts.iloc[0]['Phân Vùng']
        top_fear_occ = fear_df.iloc[-1]['Occupation (O*NET-SOC Title)'] if not fear_df.empty else "Chưa xác định"
        top_fear_rate = fear_df.iloc[-1]['Tỷ lệ lo ngại'] if not fear_df.empty else 0
        
        st.markdown(f"""
        <div class="gradient-expert-container">
            <h3 style="color: #0F172A !important; margin-top: 0; margin-bottom: 22px; font-size: 20px; font-weight: 800;">🧠 GÓC NHÌN CHUYÊN GIA & ĐỊNH HƯỚNG QUẢN TRỊ</h3>
            <div style="display: flex; gap: 24px;">
                <div style="flex: 1;">
                    <div class="grad-card-left">
                        <h4 style="color: #6D28D9; margin-top: 0; margin-bottom: 14px; font-size: 16px; font-weight: 700;">Chỉ Số Tâm Lý Lao Động</h4>
                        <ul style="color: #334155; padding-left: 20px; line-height: 1.9; margin-bottom: 0; font-size: 14px;">
                            <li><b>Nhóm Tác vụ chiếm tỷ trọng cao nhất:</b> {top_quadrant}</li>
                            <li><b>Chuyên khoa lo ngại AI thay thế nhất:</b> {top_fear_occ} ({top_fear_rate:.1f}%)</li>
                        </ul>
                    </div>
                </div>
                <div style="flex: 1;">
                    <div class="grad-card-right">
                        <h4 style="color: #0284C7; margin-top: 0; margin-bottom: 14px; font-size: 16px; font-weight: 700;">Phân Tích Thực Trạng</h4>
                        <p style="color: #334155; line-height: 1.7; margin-bottom: 0; font-size: 14px;">Nỗi sợ mất việc (Job Security Fear) có xu hướng tăng cao ở những vị trí thiên về hành chính hoặc xử lý thông tin lặp đi lặp lại. Cần có chiến lược truyền thông nội bộ khéo léo để trấn an nhân sự.</p>
                    </div>
                </div>
            </div>
            <div class="grad-action-box">
                <h4 style="color: #FFFFFF; margin-top: 0; margin-bottom: 10px; font-size: 18px; font-weight: 800;">ĐỊNH HƯỚNG HÀNH ĐỘNG & TRIỂN KHAI</h4>
                <p style="color: #F0FDF4; margin-bottom: 0; line-height: 1.7; font-size: 15px;">Lãnh đạo cơ sở y tế cần tổ chức các khóa <b>đào tạo chuyển đổi số (Upskilling)</b>, đặc biệt quan tâm đến nhóm nhân sự thuộc chuyên khoa <b>{top_fear_occ}</b>. Thông điệp cốt lõi cần truyền tải: <i>"AI sẽ không cướp việc của y bác sĩ, nhưng y bác sĩ biết sử dụng AI sẽ thay thế những người từ chối công nghệ"</i>.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

# TAB 4: TOP KHUYẾN NGHỊ THÍ ĐIỂM
with tab4:
    st.subheader("TOP KHUYẾN NGHỊ THÍ ĐIỂM AI (QUICK WINS)")
    st.markdown("Danh sách các tác vụ có điểm cơ hội ứng dụng AI cao nhất được xếp hạng tự động từ cơ sở dữ liệu:")
    
    r_col1, r_col2 = st.columns([7, 3])
    with r_col1:
        for idx, row in df_top_ai.iterrows():
            st.markdown(f"""
            <div class="rec-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <b style="color: #0369A1; font-size: 15px;">{idx+1}. {row['Task_Vi']}</b>
                    <span style="background: #10B981; color: white; padding: 2px 10px; border-radius: 12px; font-size: 12px; font-weight: 700;">Score: {row['AI_Opportunity_Score']}</span>
                </div>
                <p style="color: #475569; font-size: 13.5px; margin: 6px 0 0 0;">
                     <b>Chuyên khoa:</b> {row['Occupation (O*NET-SOC Title)']}<br>
                     <b>Phân vùng:</b> {row['Automation_Quadrant']}
                </p>
            </div>
            """, unsafe_allow_html=True)
            
    with r_col2:
        st.markdown(f"""
        <div class="gradient-expert-container" style="margin-top: 0;">
            <div class="grad-card-right">
                <h4 style="color: #0369A1; margin-top: 0; margin-bottom: 12px; font-size: 16px; font-weight: 700;">Kịch Bản Đồng Hành</h4>
                <p style="color: #334155; line-height: 1.6; font-size: 14px;">
                    <b>Tiêu chí xếp hạng:</b> Dựa trên chỉ số <i>AI_Opportunity_Score</i> từ file phân tích chuyên sâu.<br><br>
                    <b>Định hướng:</b> Đối với các tác vụ trong danh sách này, bệnh viện nên ưu tiên cấp ngân sách thử nghiệm (Pilot) trong giai đoạn đầu để tạo ra giá trị nhanh chóng.
                </p>
            </div>
            <div class="grad-action-box" style="margin-top: 15px;">
                <h4 style="color: #FFFFFF; margin-top: 0; margin-bottom: 8px; font-size: 16px; font-weight: 700;">Cam Kết Thử Nghiệm</h4>
                <p style="color: #F0FDF4; margin-bottom: 0; line-height: 1.5; font-size: 14px;">Đảm bảo hạ tầng an toàn thông tin y tế trước khi đưa vào vận hành thực tế tại khoa phòng.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

# TAB 5: TRA CỨU CHI TIẾT TÁC VỤ
with tab5:
    st.subheader("HỆ THỐNG TRA CỨU CHI TIẾT TÁC VỤ Y TẾ")
    col_search1, col_search2 = st.columns([0.6, 0.4])
    with col_search1:
        search_kw = st.text_input("🔎 Tìm kiếm từ khóa tác vụ:", placeholder="Ví dụ: Bệnh án, Hồ sơ, Quản lý...")
    with col_search2:
        selected_role = st.selectbox("🏥 Lọc theo Ngành nhỏ / Nghề nghiệp:", ["Tất cả"] + occupations)

    df_search = df_filtered.copy()
    if search_kw:
        df_search = df_search[df_search['Task_Vi'].str.contains(search_kw, case=False, na=False) | df_search['Task'].str.contains(search_kw, case=False, na=False)]
    if selected_role != "Tất cả":
        df_search = df_search[df_search['Occupation (O*NET-SOC Title)'] == selected_role]

    st.markdown(f"**Hiển thị {len(df_search)} tác vụ phù hợp (💡 *Bấm chọn trực tiếp 1 dòng trên bảng để xem chi tiết thông số*):**")

    display_cols = [
        'Task_Vi',
        'Occupation (O*NET-SOC Title)',
        'Phân Vùng Tự Động Hóa',
        'AI_Capability',
        'Worker_Receptiveness',
        'Automation_ROI_Score',
        'Medical_Risk_Score'
    ]

    df_display = df_search[display_cols].rename(columns={'Task_Vi': 'Tác Vụ Y Tế'})

    event = st.dataframe(
        df_display,
        use_container_width=True,
        selection_mode="single-row",
        on_select="rerun",
        column_config={
            "Tác Vụ Y Tế": "Tác Vụ Y Tế",
            "Occupation (O*NET-SOC Title)": "Chuyên Khoa",
            "Phân Vùng Tự Động Hóa": "Phân Vùng Strategic",
            "AI_Capability": st.column_config.NumberColumn("Năng Lực AI", format="%.2f"),
            "Worker_Receptiveness": st.column_config.NumberColumn("Sự Đón Nhận", format="%.2f"),
            "Automation_ROI_Score": st.column_config.NumberColumn("ROI Score", format="%.2f"),
            "Medical_Risk_Score": st.column_config.NumberColumn("Rủi Ro Y Khoa", format="%.2f"),
        },
        height=280
    )

    st.markdown("---")

    selected_rows = event.selection.get("rows", [])
    if len(selected_rows) > 0:
        row_idx = selected_rows[0]
        detail_target = df_search.iloc[row_idx]
    elif not df_search.empty:
        detail_target = df_search.iloc[0]
    else:
        detail_target = None

    if detail_target is not None:
        st.markdown(f"### 📋 THÔNG TIN CHI TIẾT TÁC VỤ: *{detail_target['Task_Vi']}*")
        
        c_detail1, c_detail2, c_detail3 = st.columns(3)
        with c_detail1:
            st.markdown(f"""
            <div class="grad-card-left" style="height: 100%;">
                <h4 style="color: #6D28D9; margin-top: 0; margin-bottom: 10px; font-size: 15px; font-weight: 700;">Thông Tin Cơ Bản</h4>
                <p style="margin: 0; font-size: 13.5px; color: #334155; line-height: 1.6;">
                    <b>Chuyên khoa:</b> {detail_target['Occupation (O*NET-SOC Title)']}<br>
                    <b>Phân vùng:</b> {detail_target['Phân Vùng Tự Động Hóa']}
                </p>
            </div>
            """, unsafe_allow_html=True)
        with c_detail2:
            st.markdown(f"""
            <div class="grad-card-right" style="height: 100%;">
                <h4 style="color: #0369A1; margin-top: 0; margin-bottom: 10px; font-size: 15px; font-weight: 700;">Chỉ Số Công Nghệ</h4>
                <p style="margin: 0; font-size: 13.5px; color: #334155; line-height: 1.6;">
                    <b>Năng lực AI:</b> {detail_target['AI_Capability']:.2f} / 5.0<br>
                    <b>Đón nhận của BS:</b> {detail_target['Worker_Receptiveness']:.2f} / 5.0
                </p>
            </div>
            """, unsafe_allow_html=True)
        with c_detail3:
            st.markdown(f"""
            <div class="grad-card-left" style="background: linear-gradient(135deg, #D1FAE5 0%, #A7F3D0 100%); border-color: #6EE7B7; height: 100%;">
                <h4 style="color: #065F46; margin-top: 0; margin-bottom: 10px; font-size: 15px; font-weight: 700;">Hiệu Quả & Rủi Ro</h4>
                <p style="margin: 0; font-size: 13.5px; color: #065F46; line-height: 1.6;">
                    <b>Chỉ số ROI:</b> {detail_target['Automation_ROI_Score']:.2f}<br>
                    <b>Rủi ro y khoa:</b> {detail_target['Medical_Risk_Score']:.2f}
                </p>
            </div>
            """, unsafe_allow_html=True)

        task_quadrant = detail_target['Phân Vùng Tự Động Hóa']
        if "Mỏ Vàng AI" in task_quadrant:
            action_advice = "Triển khai tự động hóa ngay lập tức để tối ưu chi phí và giải phóng sức lao động."
        elif "Thành Trì" in task_quadrant:
            action_advice = "Không được thay thế bằng AI. Máy móc chỉ đóng vai trò trợ lý nhắc nhở, con người vẫn là cốt lõi."
        elif "Chờ Công Nghệ" in task_quadrant:
            action_advice = "Theo dõi sự tiến bộ công nghệ. Có thể thử nghiệm AI ở quy mô nhỏ (Pilot) trước khi áp dụng đại trà."
        else:
            action_advice = "Cần lấy ý kiến nhân sự và xây dựng quy trình quản trị sự thay đổi trước khi đưa AI vào vận hành."
            
        risk_level = "CAO (Rất cần kiểm soát)" if detail_target['Medical_Risk_Score'] > 2.0 else "THẤP (Khá an toàn để giao AI xử lý)"
        
        st.markdown(f"""
        <div class="gradient-expert-container">
            <h3 style="color: #0F172A !important; margin-top: 0; margin-bottom: 22px; font-size: 20px; font-weight: 800;">🧠 ĐÁNH GIÁ CHUYÊN GIA DÀNH RIÊNG CHO TÁC VỤ NÀY</h3>
            <div style="display: flex; gap: 24px;">
                <div style="flex: 1;">
                    <div class="grad-card-left">
                        <h4 style="color: #6D28D9; margin-top: 0; margin-bottom: 14px; font-size: 16px; font-weight: 700;">Đặc Trưng Tác Vụ</h4>
                        <ul style="color: #334155; padding-left: 20px; line-height: 1.9; margin-bottom: 0; font-size: 14px;">
                            <li><b>Mức độ Sinh Lời (ROI):</b> {detail_target['Automation_ROI_Score']:.2f} / 5.0</li>
                            <li><b>Mức độ Rủi ro Lâm sàng:</b> {risk_level}</li>
                            <li><b>Nhóm chiến lược:</b> {task_quadrant}</li>
                        </ul>
                    </div>
                </div>
                <div style="flex: 1;">
                    <div class="grad-card-right">
                        <h4 style="color: #0284C7; margin-top: 0; margin-bottom: 14px; font-size: 16px; font-weight: 700;">Đánh Giá Tính Khả Thi</h4>
                        <p style="color: #334155; line-height: 1.7; margin-bottom: 0; font-size: 14px;">Tác vụ này có mức độ cởi mở từ nhân sự là <b>{detail_target['Worker_Receptiveness']:.2f}/5.0</b> và năng lực AI hiện tại đạt <b>{detail_target['AI_Capability']:.2f}/5.0</b>.</p>
                    </div>
                </div>
            </div>
            <div class="grad-action-box">
                <h4 style="color: #FFFFFF; margin-top: 0; margin-bottom: 10px; font-size: 18px; font-weight: 800;">ĐỊNH HƯỚNG TRIỂN KHAI CỤ THỂ</h4>
                <p style="color: #F0FDF4; margin-bottom: 0; line-height: 1.7; font-size: 15px;">{action_advice} Dù tự động hóa ở mức độ nào, hệ thống bệnh viện vẫn phải thiết lập cơ chế <b>Human-in-the-loop</b> (Con người luôn tham gia vòng lặp giám sát) đối với tác vụ này để đảm bảo an toàn cao nhất cho bệnh nhân.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

# TAB 6: MÔ PHỎNG GIẢ ĐỊNH & ĐẦU TƯ AI (WHAT-IF SIMULATOR)
with tab6:
    st.subheader("CÔNG CỤ MÔ PHỎNG ĐẦU TƯ & DỰ PHÓNG TÀI CHÍNH AI (WHAT-IF)")
    st.markdown("Sử dụng công cụ giả định để tính toán tác động tài chính khi rót vốn tự động hóa vào các chuyên khoa y tế:")
    
    sim_col1, sim_col2 = st.columns([4, 6])
    with sim_col1:
        st.markdown("""
        <div class="grad-card-left" style="height: auto;">
            <h4 style="color: #5B21B6; margin-top: 0; margin-bottom: 15px;">Thiết Lập Tham Số Mô Phỏng</h4>
        </div>
        """, unsafe_allow_html=True)
        
        sim_budget = st.slider("Ngân sách đầu tư dự kiến (VNĐ / USD):", min_value=10000, max_value=500000, value=120000, step=10000)
        sim_efficiency = st.slider("Mức độ tối ưu hiệu suất kỳ vọng (%):", min_value=5, max_value=50, value=25, step=5)
        sim_timeline = st.selectbox("Lộ trình triển khai:", ["6 Tháng (Ngắn hạn)", "1 Năm (Trung hạn)", "3 Năm (Dài hạn)"])
        
        est_savings = sim_budget * (sim_efficiency / 100) * (1.8 if "Năm" in sim_timeline else 1.0)
        est_hours_saved = total_tasks * sim_efficiency * 12
        est_roi_percent = (est_savings / sim_budget) * 100
        
    with sim_col2:
        st.markdown(f"""
        <div class="grad-card-right" style="height: 100%;">
            <h4 style="color: #0369A1; margin-top: 0; margin-bottom: 15px; font-size: 18px;">Kết Quả Dự Phóng Tài Chính</h4>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-top: 15px;">
                <div style="background: rgba(255,255,255,0.7); padding: 15px; border-radius: 12px; border: 1px solid #7DD3FC;">
                    <p style="margin: 0; font-size: 12px; color: #64748B; font-weight: 700;">DỰ TÍNH TIẾT KIỆM</p>
                    <h3 style="margin: 5px 0 0 0; color: #0284C7; font-size: 22px;">${est_savings:,.0f}</h3>
                </div>
                <div style="background: rgba(255,255,255,0.7); padding: 15px; border-radius: 12px; border: 1px solid #7DD3FC;">
                    <p style="margin: 0; font-size: 12px; color: #64748B; font-weight: 700;">TỶ SUẤT SINH LỜI (ROI)</p>
                    <h3 style="margin: 5px 0 0 0; color: #10B981; font-size: 22px;">+{est_roi_percent:.1f}%</h3>
                </div>
                <div style="background: rgba(255,255,255,0.7); padding: 15px; border-radius: 12px; border: 1px solid #7DD3FC; grid-column: span 2;">
                    <p style="margin: 0; font-size: 12px; color: #64748B; font-weight: 700;">⏰ TỔNG SỐ GIỜ LAO ĐỘNG HÀNH CHÍNH ĐƯỢC GIẢI PHÓNG</p>
                    <h3 style="margin: 5px 0 0 0; color: #7C3AED; font-size: 22px;">{est_hours_saved:,} Giờ / năm</h3>
                </div>
            </div>
            <p style="margin-top: 15px; font-size: 13px; color: #475569; line-height: 1.5;">
                <i>* Mô hình tính toán dựa trên thuật toán tích lũy điểm tác vụ (Task Impact Score) và chỉ số tự động hóa thời gian thực từ cơ sở dữ liệu O*NET.</i>
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="grad-action-box" style="margin-top: 25px;">
        <h4 style="color: #FFFFFF; margin-top: 0; margin-bottom: 10px; font-size: 18px; font-weight: 800;">ĐÁNH GIÁ KHẢ THI ĐẦU TƯ</h4>
        <p style="color: #F0FDF4; margin-bottom: 0; line-height: 1.7; font-size: 15px;">Với mức ngân sách <b>${sim_budget:,.0f}</b> trong lộ trình <b>{sim_timeline}</b>, việc ứng dụng công nghệ vào các tác vụ "Mỏ Vàng AI" sẽ hoàn vốn nhanh chóng và tạo ra giá trị gia tăng rõ rệt cho bệnh viện.</p>
    </div>
    """, unsafe_allow_html=True)