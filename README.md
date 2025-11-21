🛸 SQLPilot
AI-powered Natural Language → MySQL Query Generator

SQLPilot is an intelligent AI assistant that converts plain English questions into accurate MySQL queries, executes them on a real database, and returns clean results — all through an elegant Streamlit UI.

This project demonstrates LLM engineering, semantic few-shot learning, LangChain pipelines, and real database integration.


🚀 Features
✔ Natural Language → SQL
Ask anything about your database, such as:
“How many Levi's T-shirts are in size M?”
“What is the total revenue after discount for Nike?”
“Show all t-shirts without any discount.”

SQLPilot will:
Understand the question
Generate accurate SQL
Execute it on MySQL
Return clean, structured output

✔ Semantic Few-Shot Learning
Powered by:
HuggingFace MiniLM-L6-v2 embeddings
ChromaDB vectorstore
LangChain's SemanticSimilarityExampleSelector
Custom few-shot examples
This improves SQL accuracy significantly.

✔ Real MySQL Execution
Direct MySQL connection
Clean execution pipeline
Decimal → float conversion
Multi-row result support
Joins, aggregations, filters

✔ Streamlit UI
Includes:
Question input
SQL preview
Clean final answer
Query history
Sidebar info & branding


🛠️ Tech Stack

| Layer       | Technology                  |
|-------------|-----------------------------|
| LLM         | Google Gemini 2.5 Pro       |
| Framework   | LangChain                   |
| Embeddings  | HuggingFace MiniLM-L6-v2    |
| Vector DB   | ChromaDB                    |
| Backend     | Python                      |
| Database    | MySQL                       |
| UI          | Streamlit                   |


📁 Project Structure
SQLPilot/
│
├── llm.py                        # LLM + SQL generation + DB execution logic
├── few_shots.py                 # Few-shot examples for semantic retrieval
├── streamlit_app.py             # Streamlit web application
│
├── db_creation_atliq_t_shirts.sql   # MySQL schema + inserts
├── SQL.ipynb                    # Optional notebook
│
├── requirements.txt
├── README.md
└── .gitignore


⚙️ Installation

1️⃣ Clone the repo
git clone https://github.com/karanpatel9725-tech/SQLPilot.git
cd SQLPilot

2️⃣ Create & activate virtual environment (optional)
python -m venv venv
venv\Scripts\activate

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Add your Gemini API key

Create a .env file:
GOOGLE_API_KEY=your_api_key_here

▶ Run the Application

Start Streamlit:
streamlit run streamlit_app.py
Then open:
http://localhost:8501

🧪 Example Questions to Try

“How many t-shirts are available in size M for Nike?”
“What is the total discounted revenue for Levi's?”
“Which color has the highest stock count?”
“Show total revenue per brand.”


🛤️ Future Improvements

Chat-style conversational mode
Auto-generate charts/plots from SQL results
Multi-database support
Export results to CSV
Dark/light theme toggle
Deploy on Streamlit Cloud

👨‍💻 Author

Karan Patel
🔗 GitHub: https://github.com/karanpatel9725-tech

🚀 Passionate about AI, Data Science & Real-World Automation