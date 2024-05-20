from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
import pyodbc
from langchain_community.utilities import SQLDatabase
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
import streamlit as st
from sqlmodel import SQLModel, create_engine, Session


def init_database(user: str, password: str, host: str, port: str, database: str):
    try:
        conn = pyodbc.connect(
            "DRIVER=ODBC Driver 18 for SQL Server;"
            f"SERVER={host};"
            f"DATABASE={database};"
            f"UID={user};"
            f"PWD={password};TrustServerCertificate=yes;"
        )
        return conn
    except pyodbc.Error as e:
        st.error(f"Error connecting to database: {e}")
        return None

load_dotenv()

st.set_page_config(page_title="Chat with SQL Server", page_icon=":speech_balloon:")

st.title("Chat with SQL Server")

with st.sidebar:
    st.subheader("Settings")
    st.write("This is a simple chat application using SQL Server. Connect to the database and start chatting.")
    
    st.text_input("Host", value="localhost", key="Host")
    st.text_input("Port", value="1433", key="Port")
    st.text_input("User", value="sa", key="User")
    st.text_input("Password", type="password", value="admin", key="Password")
    st.text_input("Database", value="TestDatabase", key="Database")
    
    if st.button("Connect"):
        with st.spinner("Connecting to database..."):
            # Create a connection to the database
            conn = init_database(st.session_state["User"], st.session_state["Password"],st.session_state["Host"],st.session_state["Port"], st.session_state["Database"])

            if conn:
                st.success("Connected to the database successfully!")

                # Close the connection
                conn.close()
            else:
                st.error("Failed to connect to the database.")


footer = """<style>.footer {position: fixed;left: 0;bottom: 0;width: 100%;background-color: #000;color: white;text-align: center;}</style><div class='footer'><p>Copyright 2024, feel free to contact leodeveloper@gmail.com</p></div>"""
st.markdown(footer, unsafe_allow_html=True)