import fitz
import sys

def main():
    pdf_path = r'C:\Users\user\Downloads\s123.pdf'
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        with open('extracted_text.txt', 'w', encoding='utf-8') as f:
            f.write(text)
        print("Text extraction complete.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()
