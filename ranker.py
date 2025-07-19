import json
import os
from datetime import datetime
from sentence_transformers import SentenceTransformer, util

# ---------- Helper Functions ----------
def extract_section_title(text):
    lines = text.strip().split("\n")
    for line in lines:
        if line.strip() and len(line.strip()) < 100:
            return line.strip()
    return "Unknown"

def summarize_text(text):
    sentences = text.strip().split(". ")
    return ". ".join(sentences[:2]).strip() + "." if sentences else ""

# ---------- Loaders ----------
def load_persona_task(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["job_to_be_done"], data["persona"]

def load_extracted_text(path="extracted_text.json"):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["pages"], data["input_documents"]

# ---------- Ranking ----------
def rank_sections(pages, query, top_k=10):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    query_embedding = model.encode(query, convert_to_tensor=True)

    ranked_sections = []

    for page in pages:
        text = page["text"]
        if len(text.strip()) < 100:
            continue

        page_embedding = model.encode(text, convert_to_tensor=True)
        score = float(util.cos_sim(query_embedding, page_embedding)[0][0])

        ranked_sections.append({
            "document": page["document"],
            "page_number": page["page_number"],
            "text": text,
            "similarity_score": round(score, 4)
        })

    ranked_sections.sort(key=lambda x: x["similarity_score"], reverse=True)
    top_sections = ranked_sections[:top_k]

    for i, sec in enumerate(top_sections):
        sec["importance_rank"] = i + 1
        sec["section_title"] = extract_section_title(sec["text"])

    return top_sections

# ---------- Summarization ----------
def build_sub_section_analysis(top_sections):
    refined = []
    for section in top_sections:
        refined_text = summarize_text(section["text"])
        refined.append({
            "document": section["document"],
            "page_number": section["page_number"],
            "refined_text": refined_text,
            "page_number_constraints": f"Focused summary from page {section['page_number']}"
        })
    return refined

# ---------- Save Output ----------
def save_output(case_id, input_documents, persona, query, top_sections, sub_sections):
    output = {
        "input_documents": input_documents,
        "persona": persona,
        "job_to_be_done": query,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "top_sections": top_sections,
        "sub_section_analysis": sub_sections
    }

    output_path = f"output_case{case_id}.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"✅ Output for Test Case {case_id} saved to {output_path}")

# ---------- Runner ----------
def run_all_test_cases():
    pages, input_documents = load_extracted_text()

    task_files = sorted([
        f for f in os.listdir(".")
        if f.startswith("persona_task_") and f.endswith(".json")
    ])

    if not task_files:
        print("❌ No persona_task_X.json files found.")
        return

    for case_id, file in enumerate(task_files, 1):
        print(f"\n🔍 Running Test Case {case_id}: {file}")
        query, persona = load_persona_task(file)
        top_sections = rank_sections(pages, query)
        sub_section_analysis = build_sub_section_analysis(top_sections)
        save_output(case_id, input_documents, persona, query, top_sections, sub_section_analysis)

# ---------- Main ----------
if __name__ == "__main__":
    run_all_test_cases()
