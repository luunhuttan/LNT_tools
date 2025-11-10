import pandas as pd #Triệu hồi" thư viện Pandas. Tưởng tượng nó là một chuyên gia làm việc với file Excel/CSV. Đọc, xóa, sửa file CSV là nhờ nó hết.
import re 
import json
import os #Giúp script của mình "nhìn" được cây thư mục, tìm file, lấy đường dẫn.
import argparse
from tqdm import tqdm #tạo ra thanh loading %
import spacy

#TẢI MODEL AI (spaCy)
try:
    nlp = spacy.load("en_core_web_sm") #Tải model AI nhỏ gọn của spaCy để xử lý ngôn ngữ tự nhiên (NLP)
    print("[INFO] Đã tải xong model AI (spaCy). Bắt đầu xử lý...") 
except OSError:
    print("[LỖI] Không tìm thấy model 'en_core_web_sm' của spaCy.") #Cái try...except là để phòng hờ: Nếu mày chưa tải bộ não này (lỗi OSError), thì báo lỗi và chỉ cách tải.
    print("Vui lòng chạy 2 lệnh sau trong terminal:")
    print("1. pip install spacy")
    print("2. python -m spacy download en_core_web_sm")
    exit(1)


# Các từ khóa để phân biệt Trường học và Công ty
# Chúng ta dùng danh sách này để phân loại
EDUCATION_KEYWORDS = [
    'university', 'college', 'institute', 'academy', 'school',
    'đại học', 'học viện', 'trường', 'cử nhân', 'thạc sĩ',
    'bachelor', 'master'
]

def extract_education(about_text): #nhận 1 đoạn văn bản "about_text"
    """
    Trích xuất HỌC VẤN bằng AI (spaCy).   
    Chúng ta tìm các 'Tổ chức' (ORG) có chứa từ khóa giáo dục.
    """
    if not isinstance(about_text, str):
        return None
    
    doc = nlp(about_text)
    matches = []
    
    # 1. Tìm bằng cấp (Bachelor, Master)
    # Dùng regex đơn giản cho các bằng cấp phổ biến
    try:
        degrees = re.findall(
            r'(Bachelor of [^\n\.|,]+|Master of [^\n\.|,]+|Cử nhân [^\n\.|,]+|Thạc sĩ [^\n\.|,]+)', 
            about_text, 
            re.IGNORECASE
        )
        if degrees:
            matches.extend([d.strip() for d in degrees])
    except Exception:
        pass # Bỏ qua nếu regex lỗi
        
    # 2. Tìm tên trường bằng AI
    for ent in doc.ents:
        # Nếu AI tìm thấy một 'Tổ chức' (ORG)
        if ent.label_ == 'ORG':
            # Kiểm tra xem tên tổ chức đó có chứa từ khóa giáo dục không
            text_lower = ent.text.lower()
            if any(keyword in text_lower for keyword in EDUCATION_KEYWORDS):
                matches.append(ent.text.strip())
                
    if not matches:
        return None
        
    # Trả về kết quả duy nhất, không trùng lặp
    return "; ".join(sorted(list(set(matches)), key=matches.index))

def extract_experience(about_text):
    """
    Trích xuất KINH NGHIỆM bằng AI (spaCy).
    Chúng ta tìm các 'Tổ chức' (ORG) KHÔNG chứa từ khóa giáo dục.
    """
    if not isinstance(about_text, str):
        return None

    doc = nlp(about_text)
    matches = []
    
    # 1. Tìm (Title @ Company) hoặc (Title tại Company) - Regex cũ vẫn tốt
    try:
        # Tìm "Title" @ "Company"
        matches_at = re.findall(r'([^\n\|@]{5,70})\s*@\s*([^\n\|@\.]{3,70})', about_text)
        if matches_at:
            matches.extend([f"{title.strip()} @ {company.strip()}" for title, company in matches_at if '.' not in company])
            
        # Tìm (Title tại Company)
        matches_tai = re.findall(
            r'([a-zA-Z\s]+(?:Engineer|Developer|Analyst|Manager|Scientist))\s+tại\s+([^\n\.]+)',
            about_text, re.IGNORECASE
        )
        if matches_tai:
            matches.extend([f"{title.strip()} tại {company.strip()}" for title, company in matches_tai])
    except Exception:
        pass
        
    # 2. Tìm tên Công ty bằng AI
    for ent in doc.ents:
        # Nếu AI tìm thấy một 'Tổ chức' (ORG)
        if ent.label_ == 'ORG':
            # Kiểm tra xem nó KHÔNG PHẢI là trường học
            text_lower = ent.text.lower()
            if not any(keyword in text_lower for keyword in EDUCATION_KEYWORDS):
                # Và loại bỏ các tên quá ngắn (có thể là rác)
                if len(ent.text.strip()) > 3:
                    matches.append(ent.text.strip())

    if not matches:
        return None
        
    # Trả về kết quả duy nhất, không trùng lặp
    return "; ".join(sorted(list(set(matches)), key=matches.index))


# --- HÀM XỬ LÝ (MỖI FILE) ---
# (Hàm này giữ nguyên như cũ, chỉ thay đổi tên cột)
def process_single_file(input_csv_path, output_json_path):
    """
    Quy trình: Load CSV -> Clean -> Extract -> Save JSON
    """
    try:
        if not os.path.exists(input_csv_path):
            return False
            
        df = pd.read_csv(input_csv_path)
    except Exception as e:
        print(f"  [LỖI] Không thể đọc file CSV: {e}")
        return False

    # --- Bước 1: Làm sạch cơ bản ---
    # Tên cột đã được cập nhật theo file Excel của bạn
    url_column = 'URL'     
    name_column = 'Name'   
    about_column = 'About' 
    
    if url_column not in df.columns or name_column not in df.columns or about_column not in df.columns:
        print(f"  [LỖI] Thiếu các cột (URL, Name, About) trong file: {input_csv_path}")
        return False

    df = df.drop_duplicates(subset=[url_column], keep='first')
    df = df.dropna(subset=[url_column, name_column])

    # --- Bước 2: Trích xuất thông tin ---
    # Áp dụng các hàm trích xuất AI MỚI
    df['education_extracted'] = df[about_column].apply(extract_education)
    df['experience_extracted'] = df[about_column].apply(extract_experience)
    
    # --- Bước 3: Lưu sang JSON ---
    try:
        data_json = df.to_json(orient='records', indent=4, force_ascii=False)
        with open(output_json_path, 'w', encoding='utf-8') as f:
            f.write(data_json)
        return True
    except Exception as e:
        print(f"  [LỖI] Không thể lưu file JSON: {e}")
        return False

# --- HÀM CHÍNH (QUÉT THƯ MỤC) ---
# (Hàm này giữ nguyên như cũ)
def batch_process_all(base_directory):
    print(f"🚀 Bắt đầu quét hàng loạt từ thư mục: {base_directory}")
    print("=" * 60)
    
    try:
        all_industries = [d for d in os.listdir(base_directory) if os.path.isdir(os.path.join(base_directory, d))]
    except FileNotFoundError:
        print(f"[LỖI] Không tìm thấy thư mục: {base_directory}")
        return
        
    if not all_industries:
        print("[LỖI] Không tìm thấy thư mục ngành nghề nào trong 'data_collected'.")
        return

    success_count = 0
    fail_count = 0

    for industry_name in tqdm(all_industries, desc="Xử lý các ngành", unit="folder"):
        industry_path = os.path.join(base_directory, industry_name)
        input_csv = os.path.join(industry_path, "profiles.csv")
        output_json = os.path.join(industry_path, f"cleaned_profiles.json")
        
        if process_single_file(input_csv, output_json):
            success_count += 1
        else:
            fail_count += 1
            
    print("\n" + "=" * 60)
    print("✅ Xử lý hàng loạt hoàn tất!")
    print(f"  - {success_count} thư mục đã được xử lý thành công.")
    print(f"  - {fail_count} thư mục bị bỏ qua (lỗi hoặc thiếu file 'profiles.csv').")
    print("=" * 60)

# --- ĐIỂM VÀO SCRIPT ---
# (Giữ nguyên như cũ)
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Làm sạch HÀNG LOẠT và chuyển đổi CSV sang JSON (Phiên bản AI).")
    parser.add_argument('--dir', type=str, default='data_collected', help="Thư mục cơ sở (mặc định: 'data_collected')")
    args = parser.parse_args()
    
    try:
        import pandas as pd
        from tqdm import tqdm
    except ImportError:
        print("[LỖI] Thiếu thư viện. Vui lòng chạy: pip install pandas tqdm")
        exit(1)
        
    batch_process_all(args.dir)