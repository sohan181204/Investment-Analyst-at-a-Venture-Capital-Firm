## Adobe India Hackathon - Round 1B Submission

### Persona: Investment Analyst at a Venture Capital Firm

### 🧠 Problem Understanding

The challenge is to build a document intelligence system that understands the intent of a given **persona**, reads a collection of **PDF documents**, and extracts the most relevant content to support the user's **goal or job-to-be-done**.

For our use case, we selected the persona of an **Investment Analyst** analyzing **Infosys Annual Reports (2012–2021)** with the goal of identifying **revenue growth**, **R&D investments**, and **strategic business priorities**.

---

### 📁 Data Collection

We sourced official Infosys annual reports from 2012 to 2021 from their [Investor Relations website](https://www.infosys.com/investors/reports-filings/annual-report/). All PDFs were stored in an `input_pdfs/` folder.

---

### 🧾 Text Extraction

We used **PyMuPDF (fitz)** for parsing and extracting structured text from each page. Each document was processed page-wise and saved to `extracted_text.json`, preserving metadata like:
- Document name
- Page number
- Page text

This extraction runs entirely offline and is compatible with PDFs of varying layout and formatting.

---

### 🧑‍💻 Persona & Task Modeling

Each use case is stored as a `persona_task_X.json` file and contains:
- `persona`: e.g., “Investment Analyst”
- `job_to_be_done`: a query describing the user's objective

Examples include:
- Identifying ESG-related sections
- Finding innovation strategies
- Comparing financial trends over time

---

### 🧠 Semantic Ranking with Sentence-BERT

We used the lightweight **Sentence-BERT** model `all-MiniLM-L6-v2` (80MB) to embed both:
- The user’s query
- All page texts

For each persona, we calculate **cosine similarity** between the query and each page’s embedding to find the **top 10 most relevant pages**.

---

### 🔍 Output Format

We generate a structured `output_caseX.json` with:
1. Metadata
   - Input documents
   - Persona & task
   - Timestamp
2. Top Sections
   - Document, Page number, Section Title, Text, Importance Rank
3. Sub-section Analysis
   - A refined 2-sentence summary per section

---

### ⚙️ Technologies Used

- **Python 3.11**
- **PyMuPDF (fitz)** for PDF parsing
- **sentence-transformers** for semantic similarity
- **VS Code** for development

---

### ✅ Performance & Constraints

- ✔ CPU-Only execution
- ✔ Model size < 1GB (SBERT MiniLM)
- ✔ Processing time < 60 seconds (for 3–5 PDFs)
- ✔ No internet access required during runtime

---

### 📦 Project Files

- `extract.py`
- `ranker.py`
- `persona_task_1.json` to `persona_task_3.json`
- `output_case1.json` to `output_case3.json`
- `extracted_text.json`
- `requirements.txt`
- `approach_explanation.md`
- `Dockerfile`

---

### 🚀 Extensibility

The solution is modular and can support:
- Any number of personas
- Any document type (PDFs, research papers, textbooks)
- New models (if needed offline)
