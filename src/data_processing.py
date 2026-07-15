## File chứa các hàm tính toán insight, chỉ số AI Agent của TV2

#TẢI DỮ LIỆU VỀ MÁY
import pandas as pd
from datasets import load_dataset

print("Đang tải dữ liệu từ HuggingFace... Vui lòng đợi trong giây lát.")

# 1. Tải các tập dữ liệu từ WORKBank dưới dạng HuggingFace Dataset
worker_desire_hf = load_dataset("SALT-NLP/WORKBank", data_files="worker_data/domain_worker_desires.csv")["train"]
expert_ratings_hf = load_dataset("SALT-NLP/WORKBank", data_files="expert_ratings/expert_rated_technological_capability.csv")["train"]
task_meta_data_hf = load_dataset("SALT-NLP/WORKBank", data_files="task_data/task_statement_with_metadata.csv")["train"]

# 2. CHUYỂN ĐỔI SANG PANDAS DATAFRAME (Để xử lý dữ liệu liền mạch)
df_worker_desire = pd.DataFrame(worker_desire_hf)
df_expert_ratings = pd.DataFrame(expert_ratings_hf)
df_task_meta_data = pd.DataFrame(task_meta_data_hf)

# 3. LƯU THẲNG VÀO THƯ MỤC data/raw MÀ BẠN VỪA TẠO
df_worker_desire.to_csv("data/raw/domain_worker_desires.csv", index=False)
df_expert_ratings.to_csv("data/raw/expert_rated_technological_capability.csv", index=False)
df_task_meta_data.to_csv("data/raw/task_statement_with_metadata.csv", index=False)

print("Đã tải thành công và lưu 3 file dữ liệu thô vào thư mục 'data/raw'!")