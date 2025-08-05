# 🤖 SQL Query Generator & Executor

An intelligent Streamlit application that converts natural language questions into SQL queries and executes them against your database. Powered by LangChain and Groq's LLM.

## ✨ Features

- **Natural Language to SQL**: Ask questions in plain English and get SQL queries
- **Multi-Database Support**: Works with PostgreSQL, MySQL, and SQLite
- **Query Execution**: Automatically executes generated queries and displays results
- **Intelligent Explanations**: Provides natural language explanations of query results
- **Interactive Chat Interface**: Conversational experience with query history
- **Database Schema Viewer**: Inspect your database structure
- **Date-Aware Queries**: Handles temporal queries like "this month", "last 30 days"
- **Connection Testing**: Verify database connectivity

## 🚀 Quick Start

### Prerequisites

- Python 3.7+
- Groq API Key (get it from [Groq Console](https://console.groq.com))
- Access to a PostgreSQL, MySQL, or SQLite database

### Installation

1. **Clone or download the script**

2. **Install required packages**:
```bash
pip install streamlit langchain-community langchain-groq pandas sqlalchemy sqlite3
```

3. **Run the application**:
```bash
streamlit run your_script_name.py
```

## 📊 Database Setup

### SQLite (Easiest)
- Just provide the path to your `.db` file
- No additional setup required

### PostgreSQL
- Default port: 5432
- Ensure your PostgreSQL server is running
- Create a database with some tables and data

### MySQL
- Default port: 3306  
- Ensure your MySQL server is running
- Create a database with some tables and data

## 🔧 Configuration

1. **Select Database Type**: Choose from PostgreSQL, MySQL, or SQLite
2. **Enter Connection Details**:
   - Host (localhost for local databases)
   - Port (5432 for PostgreSQL, 3306 for MySQL)
   - Username and Password (not needed for SQLite)
   - Database name or file path
3. **Add Groq API Key**: Get your free API key from Groq Console
4. **Click "Connect & Initialize"**

## 💬 Usage Examples

### Sample Questions You Can Ask:

**Basic Queries:**
- "How many orders are in the database?"
- "Show me all customers"
- "What are the different product categories?"

**Date-Based Queries:**
- "How many orders were placed this month?"
- "Show me sales from the last 30 days"
- "What's the revenue for this year?"

**Analytical Queries:**
- "What are the top 5 customers by total order value?"
- "Which products have been ordered the most?"
- "What's the average order value by month?"
- "Show me customers who haven't placed orders this year"

**Complex Queries:**
- "Compare this month's sales to last month"
- "Find customers with orders above $1000"
- "Show monthly revenue trends"

## 🛠️ Advanced Features

### Database Schema Viewer
- Click "Show Database Schema" in the sidebar to inspect your database structure
- Helps you understand available tables and columns

### Connection Testing
- Use "Test Connection" to verify your database connectivity
- Shows the number of available tables

### Query History
- All queries and results are saved in the chat history
- Scroll up to see previous questions and answers

## 🔍 How It Works

1. **Schema Analysis**: The system first analyzes your database schema
2. **Query Generation**: Uses Groq's LLM to convert your question into SQL
3. **Query Execution**: Runs the SQL query against your database
4. **Result Processing**: Converts results into readable tables
5. **Natural Explanation**: Provides plain English explanation of the results

## 📋 Supported SQL Features

- SELECT statements with WHERE, ORDER BY, GROUP BY
- JOINs across multiple tables
- Aggregate functions (COUNT, SUM, AVG, etc.)
- Date/time functions and filtering
- LIKE queries for text searching
- Subqueries and complex conditions

## ⚠️ Limitations

- **Read-Only**: Only executes SELECT queries for safety
- **Schema Dependent**: Requires well-structured database with clear table/column names
- **LLM Dependent**: Query quality depends on the language model's understanding
- **No Data Modification**: Cannot INSERT, UPDATE, or DELETE data

## 🔒 Security Notes

- API keys are entered via password fields (not stored permanently)
- Only SELECT queries are executed
- Database credentials are kept in session state only
- No data is sent to external services except for query generation

## 🐛 Troubleshooting

### Connection Issues
- Verify database server is running
- Check host, port, username, and password
- Ensure database exists and is accessible
- Test with a database client first

### Query Generation Issues
- Check if your Groq API key is valid
- Ensure your question is clear and specific
- Try rephrasing complex questions
- Check if your database has relevant tables/data

### Result Display Issues
- Some complex query results may not display perfectly
- Try simpler queries first
- Check the raw SQL query for correctness

## 📦 Dependencies

```
streamlit>=1.28.0
langchain-community>=0.0.20
langchain-groq>=0.0.1
pandas>=1.5.0
sqlalchemy>=2.0.0
langchain-core>=0.1.0
```

## 🤝 Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## 📄 License

This project is open source and available under the MIT License.

## 🔗 Useful Links

- [Groq Console](https://console.groq.com) - Get your API key
- [Streamlit Documentation](https://docs.streamlit.io)
- [LangChain Documentation](https://python.langchain.com)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org)

---

**Happy Querying! 🎉**

*Convert your thoughts into insights with natural language SQL queries.*