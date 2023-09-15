import streamlit as st
import pandas as pd
import pyodbc
import altair as alt

# Initialize connection.
# Uses st.cache_resource to only run once.
@st.cache_resource
def init_connection():
    SERVER = st.secrets["host"]
    DATABASE = st.secrets["database"]
    UID = st.secrets["username"]
    PWD = st.secrets["password"]
    connectionString = f'DRIVER={{SQL Server}};SERVER={SERVER};DATABASE={DATABASE};UID={UID};PWD={PWD}'
    
    return pyodbc.connect(connectionString)

conn = init_connection()

# Perform query.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

query = "SELECT CASE WHEN status IS NULL THEN '[tyhjä]' ELSE status END status, COUNT(*) count FROM yritykset GROUP BY CASE WHEN status IS NULL THEN '[tyhjä]' ELSE status END ORDER BY count DESC"

data = pd.read_sql(query, conn)
st.code(query, language="sql")
st.write(data)
st.bar_chart(data, x="status", y="count")

chart = alt.Chart(data).mark_bar().encode(alt.X("status", sort="-y"), y="count")
st.altair_chart(chart, use_container_width=True)

query = "SELECT CASE WHEN yhtiömuoto IS NULL THEN '[tyhjä]' ELSE yhtiömuoto END yhtiömuoto, COUNT(*) count FROM yritykset GROUP BY CASE WHEN yhtiömuoto IS NULL THEN '[tyhjä]' ELSE yhtiömuoto END"
data = pd.read_sql(query, conn)
st.code(query, language="sql")
st.write(data)
st.bar_chart(data, x="yhtiömuoto", y="count")

