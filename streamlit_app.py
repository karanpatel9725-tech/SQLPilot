import streamlit as st
from llm import get_few_shot_db_chain, ask_databasel1

# ------------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------------
st.set_page_config(
    page_title="SQLPilot",
    page_icon="🛸",
    layout="centered",
)

# ------------------------------------------------------
# SESSION STATE INIT (MUST BE AT TOP!)
# ------------------------------------------------------
if "history" not in st.session_state:
    st.session_state.history = []

# ------------------------------------------------------
# TITLE
# ------------------------------------------------------
st.markdown("""
# 🛸 SQLPilot  
### *Natural Language → MySQL Queries → Actual Answers*
""")

st.write("---")

# ------------------------------------------------------
# SIDEBAR
# ------------------------------------------------------
with st.sidebar:
    st.header("ℹ️ About SQLPilot")
    st.write("""
SQLPilot converts natural-language questions  
into **MySQL SQL queries** using LLM + few-shot learning.

**Capabilities:**
- Generate correct SQL queries  
- Run against live MySQL database  
- Parse SQL results  
- Semantic few-shot examples  
- History tracking  
""")
    st.write("Made with ❤️ using Streamlit, LangChain & Gemini.")

# ------------------------------------------------------
# USER INPUT
# ------------------------------------------------------
question = st.text_input("Ask something about your T-shirt database:")

run_button = st.button("Run Query", type="primary")

# ------------------------------------------------------
# MAIN PROCESSING
# ------------------------------------------------------
if run_button:
    if question.strip() == "":
        st.error("Please enter a question before running.")
    else:
        with st.spinner("🧠 Thinking… generating SQL + executing..."):
            try:
                # Build chain + connect DB
                new_chain, db = get_few_shot_db_chain()

                # Get final answer
                answer = ask_databasel1(question, new_chain, db)

                # Store in history
                st.session_state.history.append(
                    {"question": question, "answer": answer}
                )

                # -------------------------------
                # DISPLAY ANSWER
                # -------------------------------
                st.success("Query executed successfully!")

                st.subheader("✅ Final Answer:")
                st.write(f"### **{answer}**")

                # -------------------------------
                # DISPLAY GENERATED SQL
                # -------------------------------
                st.subheader("📝 Generated SQL Query:")
                sql_preview = new_chain.invoke({"question": question})
                st.code(sql_preview, language="sql")

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

st.write("---")

# ------------------------------------------------------
# QUERY HISTORY
# ------------------------------------------------------
st.subheader("📜 Query History")

if len(st.session_state.history) == 0:
    st.info("No questions asked yet. Try asking one above!")
else:
    for idx, item in enumerate(reversed(st.session_state.history), start=1):
        with st.expander(f"Q{idx}: {item['question']}"):
            st.write(f"**Answer:** {item['answer']}")
