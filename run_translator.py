import os
import sys
import csv
import json

def check_environment(pdf_path):
    if not os.path.exists(pdf_path):
        print(f"Error: File '{pdf_path}' not found.")
        sys.exit(1)
        
    try:
        import fitz
    except ImportError:
        print("Required library not found. Please install: pip install PyMuPDF")
        sys.exit(1)

def read_pdf(pdf_path):
    import fitz
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def analyze_and_translate_with_llm(text):
    from dotenv import load_dotenv
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
         print("Error: GEMINI_API_KEY environment variable not set.")
         sys.exit(1)
         
    import urllib.request
    import json
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    
    prompt = """
You are an expert academic translator and summarizer.
Please read the following English academic paper text and perform a structured extraction and translation into Traditional Chinese with academic precision.

Extract exactly the following five fields:
1. "論文標題" (Paper Title)
2. "研究背景" (Background)
3. "核心方法" (Core Methods)
4. "實驗結果" (Experimental Results)
5. "結論" (Conclusion)

Translation Instructions:
- The translation must completely align with the Traditional Chinese academic context and terminology. 
- Strictly avoid stiff or literal word-for-word translation.

Output Instructions:
Return the output ONLY as a valid JSON object. 
The keys MUST EXACTLY match these Traditional Chinese strings: "論文標題", "研究背景", "核心方法", "實驗結果", "結論".
Do not include any other markdown formatting or outside text.

Paper Text:
""" + text

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseMimeType": "application/json"
        }
    }
    
    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"})
    
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode("utf-8"))
            content_text = result["candidates"][0]["content"]["parts"][0]["text"]
            
            # Clean JSON markup just in case
            cleaned_text = content_text.strip()
            if cleaned_text.startswith('```json'):
                cleaned_text = cleaned_text[7:]
            if cleaned_text.startswith('```'):
                cleaned_text = cleaned_text[3:]
            if cleaned_text.endswith('```'):
                cleaned_text = cleaned_text[:-3]
                
            data = json.loads(cleaned_text.strip())
            return data
    except Exception as e:
        print("Failed to call API or parse JSON:", e)
        if hasattr(e, "read"):
            print("API Error Response:", e.read().decode("utf-8"))
        return {"論文標題": "錯誤", "研究背景": "錯誤", "核心方法": "錯誤", "實驗結果": "錯誤", "結論": "錯誤"}

def save_output(extracted_data, csv_file="paper_analysis.csv", md_file="report.md"):
    # 兩欄式垂直佈局 (CSV)
    with open(csv_file, mode='w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["項目名稱", "內容"])
        for key in ["論文標題", "研究背景", "核心方法", "實驗結果", "結論"]:
            writer.writerow([key, extracted_data.get(key, "")])
            
    # Markdown 報告
    with open(md_file, mode='w', encoding='utf-8') as f:
        f.write(f"# {extracted_data.get('論文標題', '無標題')}\n\n")
        f.write("## 研究背景\n")
        f.write(f"{extracted_data.get('研究背景', '')}\n\n")
        f.write("## 核心方法\n")
        f.write(f"{extracted_data.get('核心方法', '')}\n\n")
        f.write("## 實驗結果\n")
        f.write(f"{extracted_data.get('實驗結果', '')}\n\n")
        f.write("## 結論\n")
        f.write(f"{extracted_data.get('結論', '')}\n\n")

def main():
    pdf_path = r"c:\Users\user\Downloads\新增資料夾\s123.pdf"
    
    print("Checking environment...")
    check_environment(pdf_path)
    
    print(f"Reading PDF '{pdf_path}'...")
    text = read_pdf(pdf_path)
    print(f"Read {len(text)} characters.")
    
    print("Calling LLM for extraction and translation...")
    extracted_data = analyze_and_translate_with_llm(text)
    
    output_csv = "paper_analysis.csv"
    output_md = "report.md"
    print(f"Saving to Cvs ({output_csv}) and Markdown ({output_md})...")
    save_output(extracted_data, output_csv, output_md)
    print("Done!")

if __name__ == "__main__":
    main()
