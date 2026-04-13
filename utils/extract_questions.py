from docx import Document
 
def docx_to_txt(input_path, output_path):
    doc = Document(input_path)
    
    with open(output_path, "w", encoding="utf-8") as f:
        for para in doc.paragraphs:
            text = para.text.strip()
            if text:  # avoid empty lines if you want
                f.write(text + "\n")
 
# Example usage
docx_to_txt("benchmark_questions.docx", "benchmark_questions.txt")