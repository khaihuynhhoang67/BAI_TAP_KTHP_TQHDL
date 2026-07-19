"""
=========================================================
ANALYTICS & STRATEGY (TASK 2)
Chủ đề 5: Healthcare, Pharmaceuticals & Life Sciences
=========================================================
"""
import pandas as pd

def run_full_analytics_pipeline():
    print("Đang xử lý phân tích dữ liệu chuyên sâu...")
    
    # 1. Đọc dữ liệu sạch (Kết quả từ data_processing.py)
    worker = pd.read_csv("data/processed/worker_medical.csv")
    expert = pd.read_csv("data/processed/expert_medical.csv")
    task = pd.read_csv("data/processed/task_medical.csv")

    # 2. FEATURE ENGINEERING: Bóc tách Insight Y tế
    worker_agg = worker.groupby('Task ID').agg(
        Worker_Receptiveness=('Automation Desire Rating', 'mean'),
        Job_Security_Fear_Rate=('Job Security Rating', lambda x: (x <= 2).mean()),
        Desire_Reduce_Stress=('Reasons for Automation Desire - Stress', 'mean'),
        Desire_Reduce_Error=('Reasons for Automation Desire - Human Error', 'mean'),
        Desire_Repetitive=('Reasons for Automation Desire - Repetitive', 'mean'),
        Need_Empathy=('Reasons for Human Agency - Empathy', 'mean'),
        Need_Ethics=('Reasons for Human Agency - Ethical', 'mean'),
        Need_Oversight=('Reasons for Human Agency - Quality Oversight', 'mean')
    ).reset_index()

    expert_agg = expert.groupby('Task ID').agg(
        AI_Capability=('Automation Capacity Rating', 'mean')
    ).reset_index()

    # 3. MERGE & TẠO MA TRẬN GÓC PHẦN TƯ (QUADRANT)
    master_df = task.merge(worker_agg, on='Task ID', how='left').merge(expert_agg, on='Task ID', how='left')

    # Tính điểm Cơ hội và Khoảng trống kháng cự
    master_df['AI_Opportunity_Score'] = (master_df['Worker_Receptiveness'] + master_df['AI_Capability']) / 2
    master_df['AI_Resistance_Gap'] = master_df['AI_Capability'] - master_df['Worker_Receptiveness']
    master_df['Ethics_Empathy_Need'] = (master_df['Need_Ethics'] + master_df['Need_Empathy']) / 2

    # Phân loại 4 Chiến lược (Dựa trên thang điểm 5)
    master_df['Automation_Quadrant'] = 'Chưa xác định'
    master_df.loc[(master_df['AI_Capability'] >= 3.0) & (master_df['Worker_Receptiveness'] >= 3.0), 'Automation_Quadrant'] = '1. Mỏ Vàng AI (Quick Wins)'
    master_df.loc[(master_df['AI_Capability'] >= 3.0) & (master_df['Worker_Receptiveness'] < 3.0), 'Automation_Quadrant'] = '2. Vùng Kháng Cự (Resistance)'
    master_df.loc[(master_df['AI_Capability'] < 3.0) & (master_df['Worker_Receptiveness'] >= 3.0), 'Automation_Quadrant'] = '3. Chờ Công Nghệ (Unmet Needs)'
    master_df.loc[(master_df['AI_Capability'] < 3.0) & (master_df['Worker_Receptiveness'] < 3.0), 'Automation_Quadrant'] = '4. Thành Trì Con Người (Safe Haven)'

    # 4. TÍNH TOÁN ROI & RỦI RO 
    master_df['Task_Impact_Score'] = master_df['Frequency'] * master_df['Importance']
    master_df['Automation_ROI_Score'] = master_df['AI_Capability'] * master_df['Task_Impact_Score']
    master_df['Medical_Risk_Score'] = master_df['Importance'] * master_df['Ethics_Empathy_Need']

    # ========================================================
    # 5. XUẤT CÁC TẬP DATA MART 
    # ========================================================
    
    # 5.1. Master Data (Phục vụ Dashboard tổng và Tra cứu chi tiết)
    master_df.to_csv("data/processed/analytics_master.csv", index=False)

    # 5.2. Insight rủi ro theo Kỹ năng cốt lõi
    skill_summary = master_df.groupby('Skill (O*NET Work Activity)').agg(
        Total_Tasks=('Task ID', 'count'),
        Avg_AI_Capability=('AI_Capability', 'mean'),
        Avg_Worker_Desire=('Worker_Receptiveness', 'mean'),
        Avg_Ethics_Empathy_Need=('Ethics_Empathy_Need', 'mean')
    ).reset_index().sort_values(by='Avg_AI_Capability', ascending=False)
    
    skill_summary = skill_summary[skill_summary['Total_Tasks'] >= 2]
    skill_summary.to_csv("data/processed/insight_skill_vulnerability.csv", index=False)

    # 5.3. Top 10 Tác vụ dễ áp dụng AI nhất
    top_tasks = master_df.sort_values(by='AI_Opportunity_Score', ascending=False).head(10)
    top_tasks[['Task ID', 'Task', 'Occupation (O*NET-SOC Title)', 'Automation_Quadrant', 'AI_Opportunity_Score']].to_csv("data/processed/top_ai_tasks.csv", index=False)
    
    # 5.4. Ma trận Chiến lược Đầu tư & Rủi ro
    roi_risk_df = master_df.sort_values(by='Automation_ROI_Score', ascending=False)
    roi_risk_df[['Task ID', 'Occupation (O*NET-SOC Title)', 'Task', 'Automation_Quadrant', 'Task_Impact_Score', 'Automation_ROI_Score', 'Medical_Risk_Score']].to_csv("data/processed/insight_roi_risk.csv", index=False)

    print("Hoàn tất! Đã xuất toàn bộ Data Mart vào data/processed/")

if __name__ == "__main__":
    run_full_analytics_pipeline()