"""
=========================================================
DATA PROCESSING (TASK 2)
Chủ đề 5: Healthcare, Pharmaceuticals & Life Sciences
=========================================================
"""
import pandas as pd
from datasets import load_dataset

def run_etl_pipeline():
    # 1. EXTRACT: Tải dữ liệu
    print("Downloading datasets...")
    worker_df = pd.DataFrame(load_dataset("SALT-NLP/WORKBank", data_files="worker_data/domain_worker_desires.csv")["train"])
    expert_df = pd.DataFrame(load_dataset("SALT-NLP/WORKBank", data_files="expert_ratings/expert_rated_technological_capability.csv")["train"])
    task_df = pd.DataFrame(load_dataset("SALT-NLP/WORKBank", data_files="task_data/task_statement_with_metadata.csv")["train"])

    # 2. TRANSFORM: Lọc theo danh sách O*NET-SOC Codes chuẩn của nhóm Healthcare & Life Sciences
    target_soc_codes = [
        "11-9111.00", "11-9121.01", "15-1211.01", "15-2041.01", 
        "15-2051.02", "19-1029.01", "19-1029.02", "29-1224.00", "31-9094.00"
    ]
    
    # Lọc Task Data trước
    task_medical = task_df[task_df['O*NET-SOC Code'].isin(target_soc_codes)].copy()
    valid_task_ids = task_medical['Task ID'].unique()
    
    # Lọc Worker và Expert dựa trên danh sách Task ID hợp lệ
    worker_medical = worker_df[worker_df['Task ID'].isin(valid_task_ids)].copy()
    expert_medical = expert_df[expert_df['Task ID'].isin(valid_task_ids)].copy()
    
    # Xử lý Missing Values an toàn với đúng tên cột trong file gốc
    task_medical.dropna(subset=['Task ID', 'O*NET-SOC Code'], inplace=True)
    worker_medical.dropna(subset=['Task ID', 'Automation Desire Rating'], inplace=True)
    expert_medical.dropna(subset=['Task ID', 'Automation Capacity Rating'], inplace=True)

    # 3. LOAD: Xuất dữ liệu
    worker_medical.to_csv("data/processed/worker_medical.csv", index=False)
    expert_medical.to_csv("data/processed/expert_medical.csv", index=False)
    task_medical.to_csv("data/processed/task_medical.csv", index=False)
    
    print(f"ETL Hoàn tất! Số nghề y tế lấy được: {task_medical['Occupation (O*NET-SOC Title)'].nunique()}")

if __name__ == "__main__":
    run_etl_pipeline()