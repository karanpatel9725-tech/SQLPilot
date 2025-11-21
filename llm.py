# ---- LLM: Google Gemini Chat Model ----
from langchain_google_genai import ChatGoogleGenerativeAI  
# Used to generate SQL queries and final answers using Google's Gemini models.

# ---- Database Utility (SQLAlchemy Wrapper) ----
from langchain_community.utilities import SQLDatabase  
# Provides a unified interface to connect and run queries on MySQL/PostgreSQL/SQLite etc.

# ---- SQL Query Generator Chain ----
from langchain.chains import create_sql_query_chain  
# This creates a chain where the LLM generates an SQL query based on the input question.

# ---- Embeddings (Used for Semantic Search) ----
from langchain.embeddings import HuggingFaceEmbeddings  
# Converts your few-shot examples into numerical vectors so they can be semantically compared.

# ---- Vector Database (Chroma for Few-Shot Retrieval) ----
from langchain.vectorstores import Chroma  
# Stores embeddings + metadata and retrieves the most similar few-shot examples.

# ---- Few-Shot Example Selector ----
from langchain.prompts import SemanticSimilarityExampleSelector  
# Automatically picks the most relevant examples based on cosine similarity.

# ---- MySQL Prompt Components (LangChain SQL Templates) ----
from langchain.chains.sql_database.prompt import MYSQL_PROMPT, PROMPT_SUFFIX  
# MYSQL_PROMPT = LangChain’s built-in MySQL-specific SQL generation template
# PROMPT_SUFFIX = End section of the SQL generation prompt format

# ---- Prompt Template (Used to Define Example Format) ----
from langchain.prompts.prompt import PromptTemplate  
# Creates structured prompt blocks for examples (Question → SQLQuery → SQLResult → Answer).

# ---- Few-Shot Prompt Builder ----
from langchain.prompts import FewShotPromptTemplate  
# Combines examples + prefix + suffix into one big prompt given to the LLM.

from few_shots import few_shots
# Importing the few-shot examples defined in a separate file

from few_shots import clean_metadata
# Importing the cleaned metadata for few-shot examples

import os
#importing os module to access environment variables

from dotenv import load_dotenv
#to import api key from env file 

load_dotenv()
#this method will look for .env file in the current directory and load the variables defined in it into the environment variables

def get_few_shot_db_chain():
    db_user = "root"
    db_password = "root"
    db_host = "localhost"
    db_name = "atliq_tshirts"
    
    db = SQLDatabase.from_uri(
        f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}",
        sample_rows_in_table_info=3)
    #print(db.table_info)

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-pro",
        api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0.1)

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    to_vectorize = [" ".join([str(v) for v in example.values()]) for example in few_shots]

    vectorstore = Chroma.from_texts(
        to_vectorize,
        embedding=embeddings,
        metadatas=clean_metadata)

    exemple_selector = SemanticSimilarityExampleSelector(
        vectorstore=vectorstore,
        k=3)

    mysql_prompt = """You are a MySQL expert. Given an input question, first create a syntactically correct MySQL query to run, then look at the results of the query and return the answer to the input question.
    Unless the user specifies in the question a specific number of examples to obtain, query for at most {top_k} results using the LIMIT clause as per MySQL. You can order the results to return the most informative data in the database.
    Never query for all columns from a table. You must query only the columns that are needed to answer the question. Wrap each column name in backticks (`) to denote them as delimited identifiers.
    Pay attention to use only the column names you can see in the tables below. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.
    Pay attention to use CURDATE() function to get the current date, if the question involves "today".

    Use the following format:

    Question: Question here
    SQLQuery: Query to run with no pre-amble
    SQLResult: Result of the SQLQuery
    Answer: Final answer here

    No pre-amble.
    """

    example_prompt = PromptTemplate(
        input_variables=["Question", "SQLQuery", "SQLResult", "Answer"],
        template="""
    Question: {Question}
    SQLQuery: {SQLQuery}
    SQLResult: {SQLResult}
    Answer: {Answer}
    """)

    few_shot_prompt = FewShotPromptTemplate(
        example_selector=exemple_selector,
        example_prompt=example_prompt,
        prefix=MYSQL_PROMPT.template,
        suffix=PROMPT_SUFFIX,
        input_variables=["input", "table_info", "top_k"])

    new_chain = create_sql_query_chain(
        llm=llm,
        db=db,
        prompt=few_shot_prompt)
    
    return new_chain, db

    
def ask_databasel1(question, new_chain, db):
    import ast
    import decimal

    # Step 1 — Generate SQL using the NEW CHAIN
    query = new_chain.invoke({"question": question})
    print("Generated SQL Query:\n", query)

    # Step 2 — Extract SQL
    sql = query.split("SQLQuery:")[-1].strip()
    sql = sql.replace("```sql", "").replace("```", "").strip()

    # Step 3 — Run SQL
    raw = db.run(sql)
    print("Answer:", raw)

    # Step 4 — Convert ANY output into a Python list
    raw_str = str(raw)
    raw_str = raw_str.replace("Decimal", "")  
    try:
        result = ast.literal_eval(raw_str)
    except:
        result = raw

    # CASE 1: Single value
    if (isinstance(result, list)
        and len(result) == 1
        and isinstance(result[0], tuple)
        and len(result[0]) == 1):
        
        val = result[0][0]
        print(val)
        return val

    # CASE 2: Multiple rows
    if isinstance(result, list):
        clean = []
        for row in result:
            clean_row = []
            for col in row:
                clean_row.append(col)
            clean.append(tuple(clean_row))
        print(clean)
        return clean
    # Fallback
    return result




# if __name__ == "__main__":
    new_chain, db = get_few_shot_db_chain()
    
    question = "how many t-shirts are available in size M for Nike brand?"
    answer = ask_databasel1(question, new_chain, db)
    print("Final Answer:", answer)