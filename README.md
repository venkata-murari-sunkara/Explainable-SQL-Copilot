# Explainable SQL Copilot 🤖

An AI-powered SQL assistant that converts natural language questions into SQL queries, explains the generated SQL in plain English, safely validates the query, executes it against a PostgreSQL database, and visualizes the results.

---

## 🌐 Live Demo

* **Frontend (Streamlit App):** [Try it here](your-streamlit-url)
* **Backend API (Swagger Docs):** [View API docs](your-render-url/docs)

> ⚠️ Note: The backend is hosted on Render's free tier and may take 30–60 seconds to wake up if it has been inactive. Please be patient on first load.

---

## 🚀 Features

* Upload CSV datasets and automatically ingest them into PostgreSQL
* Dynamic schema discovery — no manual configuration required
* Natural Language → SQL generation using Gemini 2.5 Flash
* Two-layer SQL validation for safe, schema-aware execution
* SQL explanation in plain English before execution
* Human-in-the-loop approval workflow — user confirms before query runs
* Query execution against PostgreSQL (read-only)
* Interactive result visualization with Plotly
* Automatic chart generation for analytical queries
* Protection against all destructive SQL operations

---

📊 Project Highlights
Supports dynamic CSV uploads and schema inference
Handles datasets with 1,000+ rows and arbitrary schemas
Generates schema-aware PostgreSQL queries using Gemini 2.5 Flash
Prevents destructive SQL operations through multi-layer validation
Produces automatic visualizations for analytical queries

---

## 🏗️ Architecture

```text
[ User / Browser ]
        │
        ▼
[ Streamlit UI ]
  CSV Upload | Ask Question | Approve Query
        │
        ▼
[ FastAPI Backend ]
        │
        ├── CSV Ingestion → Pandas → PostgreSQL
        │
        ├── Schema Inspector → Table/Column Metadata
        │
        ├── Gemini LLM → NL2SQL Generation
        │
        ├── SQL Validator → Safety + Schema Checks
        │       │
        │       └── Invalid/Unsafe → Error Response to UI
        │
        ├── SQL Explainer → Plain-English Explanation
        │
        └── Query Executor → Read-Only PostgreSQL Query
        │
        ▼
[ PostgreSQL Database ]
        │
        ▼
[ Results Table + Plotly Visualization ]
```

---

## 📸 Demo

Dataset Upload
![Dataset Upload](assets/ui_1.png)

Generated SQL & Explanation
![Generated SQL & Explanation](assets/ui_2.png)

Query Results
![Query Results](assets/ui_3.png)

Data Visualization
![Data Visualization](assets/ui_4.png)

---

## Example Questions

#### **Vehicle Dataset**
- What is the highest vehicle price?
- What is the average vehicle price by vehicle maker?
- Show the number of vehicles by color.
- Which vehicle maker has the most vehicles?
- Show average vehicle price by model year.

#### **Customer Dataset**

- Show customer count by country.
- How many customers use each credit card type?
- Show customer count by state.
- Which country has the most customers?

---

## 🛠️ Tech Stack

### Backend
* Python
* FastAPI
* PostgreSQL
* SQLAlchemy
* Pandas

### AI Layer
* Google Gemini 2.5 Flash

### Frontend
* Streamlit
* Plotly

---

## 📂 Project Structure

```text
SQL_Copilot_Project/
│
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── ingest.py
│   ├── schema_inspector.py
│   ├── sql_generator.py
│   ├── validator.py
│   ├── explainer.py
│   ├── query_executor.py
│   └── schemas.py
│
├── frontend/
│   └── app.py
│
├── uploads/
│
├── .env
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation & Setup

### 1. Clone Repository

```bash
git clone https://github.com/venkata-murari-sunkara/explainable-sql-copilot.git
cd explainable-sql-copilot
```

### 2. Set Up Virtual Environment

```bash
# Create environment
python -m venv venv

# Activate (Mac/Linux)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory:

```text
GEMINI_API_KEY=your_gemini_api_key_here
DATABASE_URL=postgresql://user:password@localhost:5432/sqlcopilot
```

### 5. Run Backend

```bash
uvicorn backend.main:app --reload
```

Backend URL: `http://127.0.0.1:8000`

### 6. Run Frontend

```bash
streamlit run frontend/app.py
```

Frontend URL: `http://localhost:8501`

---

## 🔄 How It Works

### 1. Upload Dataset

Upload a CSV file through the Streamlit interface. The application:
* Infers column types automatically (integer, float, text, date)
* Creates a PostgreSQL table dynamically
* Loads the CSV data into the table
* Discovers the schema for query generation

### 2. Ask a Question in Plain English

Example:

```text
What is the highest vehicle price?
```

Generated SQL:

```sql
SELECT MAX(vehicle_price) AS highest_vehicle_price
FROM product_t_csv;
```

### 3. Review the Plain-English Explanation

Before execution, the application explains what the SQL will do in simple terms — no SQL knowledge required to understand the result.

### 4. Approve and Execute

After reviewing the explanation and generated SQL, the user approves execution. The query runs against PostgreSQL in read-only mode and results are displayed as a table.

### 5. Visualize Results

For analytical queries, the application automatically generates charts. Example:

```text
Show average vehicle price by vehicle maker
```

Generates a bar chart with Plotly — no additional configuration needed.

---

## 🔒 Security Features

Only `SELECT` statements are permitted. The validator explicitly blocks:

* `DROP`
* `DELETE`
* `UPDATE`
* `INSERT`
* `ALTER`
* `TRUNCATE`

Queries referencing columns that do not exist in the actual PostgreSQL schema are also rejected — preventing LLM hallucinations from reaching the database.

---

## 🧠 Engineering Decisions & Tradeoffs

* **Two-layer SQL validation:** Rule-based blocking of destructive operations combined with schema validation against live PostgreSQL metadata. Application-level checks alone are insufficient — both layers working together provide defense in depth against unsafe LLM-generated queries.
* **Human-in-the-loop approval:** Users see the generated SQL and its plain-English explanation before execution — a deliberate design decision that builds trust and catches errors before they reach the database. Prioritizes transparency over speed.
* **Schema-aware prompting:** Live table and column metadata is injected into the Gemini prompt at query time. This prevents hallucinated column names and significantly improves SQL accuracy compared to static prompting.
* **Gemini Flash over GPT-4:** Chose Gemini 2.5 Flash for SQL generation — faster response times and lower cost per query than GPT-4o-mini, with comparable accuracy for structured NL2SQL tasks. Demonstrates provider-agnostic architecture across the portfolio.
* **Read-only PostgreSQL connection:** The query executor connects with read-only database permissions at the infrastructure level — not just application-level checks. Multiple layers of protection against accidental or malicious data modification.

---

## 🚧 Challenges Solved

* **Dynamic schema inference:** Automatically detecting PostgreSQL column types from CSV data without manual annotation — required handling mixed-type columns, empty values, and ambiguous formats (e.g., dates stored as strings).
* **Schema-aware prompting:** Injecting live table and column metadata into the Gemini prompt at query time to prevent hallucinated column names — significantly improved SQL accuracy on real-world datasets.
* **LLM output parsing:** Gemini occasionally returns SQL wrapped in markdown code fences or with explanatory text. Built a cleaning and extraction layer to strip formatting before validation and execution — ensuring consistent, parseable output.
* **Type mismatch handling:** CSV columns with mixed types (e.g., numeric values with occasional string entries) required preprocessing logic to coerce types safely before PostgreSQL insertion.

---

## 🎯 Key Concepts Demonstrated

- Natural Language to SQL (NL2SQL)
- LLM-Powered Application Development
- FastAPI REST API Design
- PostgreSQL Integration with SQLAlchemy
- Dynamic Schema Inference
- SQL Safety Validation
- Human-in-the-Loop AI Systems
- Responsible AI Principles
- Data Visualization with Plotly
- Production-Style AI System Architecture

---

## 🔮 Future Improvements

- SQL query history and session management
- Download query results as CSV
- Multi-table JOIN support with relationship inference
- User authentication and role-based access
- Cloud deployment with persistent PostgreSQL
- Advanced chart type selection
- Conversational follow-up questions with context retention
- RAG evaluation metrics for SQL accuracy

---

## 👨‍💻 Author

**Venkata Murari**

- GitHub: [venkata-murari-sunkara](https://github.com/venkata-murari-sunkara)
- LinkedIn: [venkata-murari](https://www.linkedin.com/in/venkata-murari/)