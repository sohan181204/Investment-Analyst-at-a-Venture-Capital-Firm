import fitz  # PyMuPDF for PDF processing
import os
import json

def extract_text_from_pdf(pdf_path):
    """
    Extracts text from each page of a PDF file using PyMuPDF (fitz).
    """
    doc = fitz.open(pdf_path)
    text_pages = []

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text = page.get_text("text").strip()
        if text:
            text_pages.append({
                "page_number": page_num + 1,
                "text": text
            })

    return text_pages

def process_all_pdfs(input_folder):
    """
    Processes all PDF files in a given folder, extracting text from each.
    Returns:
        - all_data: list of dicts with document, page_number, and text
        - input_documents: list of filenames processed
    """
    all_data = []
    input_documents = []

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(input_folder, filename)
            print(f"📄 Extracting: {filename}")
            pages = extract_text_from_pdf(pdf_path)
            for page in pages:
                all_data.append({
                    "document": filename,
                    "page_number": page["page_number"],
                    "text": page["text"]
                })
            input_documents.append(filename)

    return all_data, input_documents

if __name__ == "__main__":
    input_folder = "input_pdfs"
    output_file = "extracted_text.json"

    # Run extraction
    extracted_data, input_documents = process_all_pdfs(input_folder)

    # Save to JSON for ranking step
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump({
            "input_documents": input_documents,
            "pages": extracted_data
        }, f, indent=2, ensure_ascii=False)

    print(f"✅ Text extracted and saved to {output_file}")
