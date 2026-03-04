---
name: PDF Paper Translator
description: This skill should be used when the user asks to "translate a paper", "extract paper summary", "analyze an English paper", "convert PDF paper to CSV", or "translate English PDF".
version: 0.1.0
---

# PDF Paper Translator

This skill processes an English academic paper (PDF), translates it with academic precision into Traditional Chinese, extracts structured key points, and saves the output as a CSV file.

## Execution Workflow

To use this skill, write and execute a Python script that completes the entire process. Follow these steps exactly:


### 1. Pre-Execution Checks

Before beginning file processing or making any API calls, you must check the environment:
- **Verify File Existence:** Ensure the user-provided PDF file path actually exists. If it does not, abort and inform the user.
- **Check Dependencies:** Verify that a PDF parsing library like `PyMuPDF` (imported as `fitz`) or `PyPDF2` is installed. Check for any required API clients if you are querying an LLM in the script. If they are missing, run pip install to install them before continuing.

### 2. Read the PDF

Use the checked PDF parsing library to read all text from the PDF file. Extract the text carefully to maintain as much structural integrity as possible.

### 3. Structured Extraction and Translation

Pass the extracted text to an LLM to generate the translated summary. You must ensure the following rules are met in the LLM prompt:
- **Academic Precision Translation:** The translation must completely align with the Traditional Chinese academic context and terminology. Strictly avoid stiff or literal word-for-word translation.
- **Structured Extraction Fields:** You must explicitly extract exactly the following five fields:
  1. `論文標題` (Paper Title)
  2. `研究背景` (Background)
  3. `核心方法` (Core Methods)
  4. `實驗結果` (Experimental Results)
  5. `結論` (Conclusion)



## Output Requirements
- **CSV 垂直佈局**：產出的 `paper_analysis.csv` 必須採用「兩欄式垂直佈局」（第一欄為項目名稱，第二欄為內容），避免在編輯器中產生長距離的橫向捲動。
- **長文本處理**：寫入 CSV 時，必須保留內容內部的換行符號 (`\n`)，並確保所有欄位內容都使用雙引號 (`""`) 包覆，防止檔案解析跑版。
- **新增 Markdown 報告**：除了 CSV，必須額外生成一個 `report.md`，使用 Markdown 的層級標題（#、##）與清單，將論文重點整理成易於閱讀的報告。







### 4. Save as CSV

Write the structured output into a CSV file.
- **Output Filename:** Must be exactly `paper_analysis.csv`.
- **CSV Formatting:** Always include a header row containing exactly: `論文標題,研究背景,核心方法,實驗結果,結論`.
- **Prevent Formatting Breakage (防止跑版):** Use Python's built-in `csv` module (e.g., `csv.DictWriter`) with `encoding="utf-8-sig"` (to ensure Excel compatibility). The `csv` module guarantees that fields containing internal commas, quotes, or newlines are properly wrapped in double quotes, preventing structure breakage.

### Example Script Outline

```python
import os
import csv
import sys
# import fitz  # PyMuPDF

def check_environment(pdf_path):
    # 1. Verify input file exists
    if not os.path.exists(pdf_path):
        print(f"Error: File '{pdf_path}' not found.")
        sys.exit(1)
        
    # 2. Check dependencies
    try:
        import fitz
    except ImportError:
        print("Required library not found. Please install: pip install PyMuPDF")
        sys.exit(1)

def save_to_csv(extracted_data, output_file="paper_analysis.csv"):
    headers = ["論文標題", "研究背景", "核心方法", "實驗結果", "結論"]
    file_exists = os.path.exists(output_file)
    
    with open(output_file, mode='a' if file_exists else 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        if not file_exists:
            writer.writeheader()
        writer.writerow(extracted_data)

# Main Execution Flow
# 1. check_environment(pdf_path)
# 2. text = read_pdf(pdf_path)
# 3. extracted_data = analyze_and_translate_with_llm(text)
# 4. save_to_csv(extracted_data)
```
