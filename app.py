import streamlit as st
import sqlite3
from langchain_community.utilities import SQLDatabase
from langchain_groq import ChatGroq
from langchain.agents import create_sql_agent, AgentType
import pandas as pd
from sqlalchemy import create_engine
from typing import Optional, Tuple
from langchain_core.prompts import ChatPromptTemplate
from datetime import datetime

# Page config
st.set_page_config(
    page_title="SQL Chatbot",
    page_icon="🤖",
    layout="wide"
)

def create_database_connection(db_type: str, host: str, port: str, database: str, username: str, password: str) -> Optional[SQLDatabase]:
    """Create database connection from individual parameters"""
    try:
        if db_type == "PostgreSQL":
            connection_string = f"postgresql://{username}:{password}@{host}:{port}/{database}"
        elif db_type == "MySQL":
            connection_string = f"mysql://{username}:{password}@{host}:{port}/{database}"
        elif db_type == "SQLite":
            connection_string = f"sqlite:///{database}"
        else:
            raise ValueError("Unsupported database type")
        
        engine = create_engine(connection_string)
        db = SQLDatabase(engine)
        # Test the connection
        db.get_usable_table_names()
        return db
    except Exception as e:
        st.error(f"Database connection failed: {str(e)}")
        return None

def generate_and_execute_sql(llm: ChatGroq, db: SQLDatabase, user_question: str) -> Tuple[str, pd.DataFrame, str]:
    """Generate SQL query and execute it, returning query, results, and explanation"""
    
    # Get database schema information
    table_info = db.get_table_info()
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    # Create the prompt template for SQL generation
    sql_prompt = ChatPromptTemplate.from_messages([
        ("system", f"""You are a SQL expert. Given a database schema and a user question, write a SQL query that answers the question.

Current date: {current_date}
Database Schema:
{{schema}}

Rules:
1. Only return the SQL query, nothing else
2. Use proper SQL syntax for the database type
3. Don't include any explanations or markdown
4. Make sure the query is executable
5. Use appropriate table and column names from the schema
6. For date/time questions:
   - Use appropriate date functions for the database type
   - For "this month": use current month and year
   - For "today": use current date
   - For relative dates, calculate from current date
7. Handle case-insensitive searches appropriately
8. Use proper JOIN syntax when multiple tables are involved"""),
        ("human", "{question}")
    ])
    
    # Create the chain and invoke
    chain = sql_prompt | llm
    
    try:
        response = chain.invoke({
            "schema": table_info,
            "question": user_question,
        })
        
        # Extract the SQL query from response
        sql_query = response.content.strip()
        
        # Clean up the response (remove any markdown or extra text)
        if "```sql" in sql_query:
            start = sql_query.find("```sql") + 6
            end = sql_query.find("```", start)
            sql_query = sql_query[start:end].strip()
        elif "```" in sql_query:
            start = sql_query.find("```") + 3
            end = sql_query.find("```", start)
            sql_query = sql_query[start:end].strip()
        
        # Execute the query
        try:
            result = db.run(sql_query)
            
            # Convert result to DataFrame if it's not empty
            if result:
                # Handle different result formats
                if isinstance(result, str):
                    # Try to parse the string result
                    lines = result.strip().split('\n')
                    if len(lines) > 1:
                        # Multiple rows
                        data = []
                        for line in lines:
                            if line.strip():
                                # Simple parsing - you might need to adjust based on your DB output format
                                data.append(line.strip().split('\t') if '\t' in line else [line.strip()])
                        df = pd.DataFrame(data)
                    else:
                        # Single value
                        df = pd.DataFrame([result], columns=['Result'])
                else:
                    # Already in a structured format
                    df = pd.DataFrame([result]) if not isinstance(result, list) else pd.DataFrame(result)
            else:
                df = pd.DataFrame([['No results found']], columns=['Result'])
            
            # Generate explanation
            explanation = generate_explanation(llm, user_question, sql_query, df)
            
            return sql_query, df, explanation
            
        except Exception as e:
            error_df = pd.DataFrame([f'Query execution error: {str(e)}'], columns=['Error'])
            return sql_query, error_df, f"Query generated but execution failed: {str(e)}"
        
    except Exception as e:
        raise Exception(f"Failed to generate SQL: {str(e)}")

def generate_explanation(llm: ChatGroq, question: str, sql_query: str, results: pd.DataFrame) -> str:
    """Generate a natural language explanation of the results"""
    
    explanation_prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a helpful data analyst. Given a user's question, the SQL query used, and the results, 
        provide a clear, concise explanation of what the results mean in natural language.

Rules:
1. Be conversational and easy to understand
2. Mention key numbers/findings from the results
3. Keep it brief but informative
4. If there are no results, explain why that might be"""),
        ("human", """
Question: {question}
SQL Query: {sql_query}
Results: {results}

Please explain what these results mean.""")
    ])
    
    try:
        chain = explanation_prompt | llm
        response = chain.invoke({
            "question": question,
            "sql_query": sql_query,
            "results": results.to_string() if not results.empty else "No results"
        })
        return response.content.strip()
    except:
        return "Results retrieved successfully."

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'initialized' not in st.session_state:
    st.session_state.initialized = False

# Main interface
st.title("🤖 SQL Query Generator & Executor")
st.markdown("Enter natural language questions to generate and execute SQL queries!")

# Setup (simplified)
if not st.session_state.initialized:
    st.subheader("Database Connection")
    
    # Database type selection
    db_type = st.selectbox("Database Type", ["PostgreSQL", "MySQL", "SQLite"])
    
    col1, col2 = st.columns(2)
    
    with col1:
        host = st.text_input("Host", value="localhost" if db_type != "SQLite" else "", disabled=db_type=="SQLite")
        username = st.text_input("Username", disabled=db_type=="SQLite")
        
    with col2:
        port = st.text_input("Port", value="5432" if db_type == "PostgreSQL" else "3306" if db_type == "MySQL" else "", disabled=db_type=="SQLite")
        password = st.text_input("Password", type="password", disabled=db_type=="SQLite")
    
    if db_type == "SQLite":
        database = st.text_input("Database File Path", placeholder="e.g., /path/to/database.db")
    else:
        database = st.text_input("Database Name")
    
    api_key = st.text_input("Enter Groq API Key:", type="password")
    
    # Validation
    if db_type == "SQLite":
        can_connect = database and api_key
    else:
        can_connect = all([host, port, database, username, password, api_key])
    
    if can_connect and st.button("Connect & Initialize"):
        try:
            # Connect to database
            db = create_database_connection(db_type, host, port, database, username, password)
            if db:
                # Initialize LLM
                llm = ChatGroq(groq_api_key=api_key, model_name="llama3-8b-8192", temperature=0)
                
                st.session_state.llm = llm
                st.session_state.db = db
                st.session_state.db_type = db_type
                st.session_state.initialized = True
                
                # Show available tables
                tables = db.get_usable_table_names()
                st.success(f"✅ Connected to {db_type}! Available tables: {', '.join(tables)}")
                st.rerun()
        except Exception as e:
            st.error(f"Setup failed: {str(e)}")
    
    elif not can_connect:
        if db_type == "SQLite":
            st.info("Please provide database file path and API key")
        else:
            st.info("Please fill in all connection details and API key")

else:
    # Show available tables and sample questions
    try:
        tables = st.session_state.db.get_usable_table_names()
        st.info(f"📊 Available tables: {', '.join(tables)}")
        
        # Sample questions
        with st.expander("💡 Sample Questions"):
            st.markdown("""
            - How many orders were placed this month?
            - What are the top 5 customers by total order value?
            - Show me all orders from the last 30 days
            - Which products have been ordered the most?
            - What's the average order value by month?
            """)
    except:
        st.info("📊 Database connected")
    
    # Chat interface
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "sql_query" in message:
                st.code(message["sql_query"], language="sql")
            if "results" in message and not message["results"].empty:
                st.dataframe(message["results"], use_container_width=True)

    # Chat input
    if prompt := st.chat_input("Ask a question about the database..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate and execute SQL query
        with st.chat_message("assistant"):
            try:
                with st.spinner("Generating and executing SQL query..."):
                    sql_query, results_df, explanation = generate_and_execute_sql(
                        st.session_state.llm, 
                        st.session_state.db, 
                        prompt
                    )
                    
                    if sql_query:
                        st.subheader("🔍 Generated SQL Query:")
                        st.code(sql_query, language="sql")
                        
                        st.subheader("📊 Results:")
                        if not results_df.empty and 'Error' not in results_df.columns:
                            st.dataframe(results_df, use_container_width=True)
                            st.subheader("💬 Explanation:")
                            st.markdown(explanation)
                        else:
                            st.warning("No results found or query error occurred.")
                            st.dataframe(results_df, use_container_width=True)
                        
                        # Save to chat history
                        st.session_state.messages.append({
                            "role": "assistant", 
                            "content": explanation,
                            "sql_query": sql_query,
                            "results": results_df
                        })
                    else:
                        st.warning("Could not generate SQL query. Try rephrasing your question.")
                        st.session_state.messages.append({
                            "role": "assistant", 
                            "content": "Could not generate a valid SQL query. Please try rephrasing your question."
                        })
                        
            except Exception as e:
                error_msg = f"Error: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})

    # Sidebar with additional options
    with st.sidebar:
        st.subheader("🔧 Advanced Options")
        
        if st.button("Show Database Schema"):
            try:
                schema_info = st.session_state.db.get_table_info()
                st.text_area("Database Schema", schema_info, height=300)
            except Exception as e:
                st.error(f"Could not retrieve schema: {e}")
        
        if st.button("Test Connection"):
            try:
                tables = st.session_state.db.get_usable_table_names()
                st.success(f"✅ Connection active. Tables: {len(tables)}")
            except Exception as e:
                st.error(f"❌ Connection failed: {e}")

    # Database connection help
    st.subheader("💡 Connection Help")
    st.markdown("""
    **PostgreSQL:** Default port 5432
    
    **MySQL:** Default port 3306
    
    **SQLite:** Only needs the database file path
    
    **For date queries:** The system understands relative dates like "this month", "last 30 days", etc.
    """)
    
    if st.button("Reset Connection", type="secondary"):
        st.session_state.initialized = False
        st.session_state.messages = []
        st.rerun()