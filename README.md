# 🧪 DQaaS - Data Quality as a Service with Great Expectations

This project demonstrates how to turn **Great Expectations (GE)** into a **data quality validation service**, accessible via a lightweight **Flask API**.

It allows dynamic validation of any CSV file by simply sending a request with the file path and (optional) suite name.

---

## 📁 Project Structure

```
dqaas-project/
├── app.py                    # Flask API for triggering validations
├── run_validation.py         # Core validation logic using GE
├── data/                     # Input CSV files
│   └── employees.csv
├── gx/                       # Great Expectations project folder
├── requirements.txt          # Python dependencies
└── README.md                 # 📄 You are here
```

---

## 🚀 How It Works

1. Great Expectations is initialized with a `local_filesystem` datasource
2. Expectations are defined for the dataset via code (no CLI or notebooks needed)
3. A validation suite (`employees_suite`) is either created or updated
4. A checkpoint runs the suite and generates a report
5. Results are returned via API response and viewable in HTML Data Docs

---

## ⚙️ Setup Instructions

### ✅ 1. Clone the Repo

```bash
git clone https://github.com/<your-username>/dqaas-project.git
cd dqaas-project
```

### 🐍 2. Create and Activate Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 📦 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 🚀 4. Start the Flask API

```bash
python app.py
```

---

## 🔁 Example Usage (via `curl`)

```bash
curl -X POST http://127.0.0.1:5000/validate      -H "Content-Type: application/json"      -d '{"file_path": "data/employees.csv", "suite_name": "employees_suite"}'
```

✅ If successful:

```json
{
  "success": true,
  "message": "Validation completed",
  "data_docs_url": "gx/uncommitted/data_docs/local_site/index.html"
}
```

📂 Open the Data Docs report in your browser:
```
gx/uncommitted/data_docs/local_site/index.html
```

---

## 📌 Current Expectations Defined

- `employee_id` column must:
  - exist
  - not contain nulls
  - be unique
- `age` column must:
  - not contain nulls
  - have values between 20 and 60

---

## 📅 Roadmap

- [x] Build DQaC pipeline in code
- [x] Expose validation as Flask API (DQaaS)
- [ ] ✨ Auto-generate expectations from new CSVs
- [ ] ⏱️ Schedule validations via cron/job
- [ ] 🧪 Add unit tests for expectation logic
- [ ] 📝 Publish technical blog with screenshots

---

## 🙋‍♀️ Author

**Sneha Shrivastav**  
_Data Quality Architect | Python & DataOps Enthusiast_

🔗 [GitHub](https://github.com/sneha-dq)  
📝 [Blog](https://sneha-dq.github.io)

---

## 🧠 Inspiration

This project is inspired by the need to **make data quality validations reusable, automatable, and callable** — turning DQ tools into developer-friendly services for modern data platforms.
