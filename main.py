import streamlit as st

import duckdb

conn = duckdb.connect("data_model/prod.duckdb", read_only=True)

query = """
    SELECT 
        rank, 
        date, 
        username, 
        level, 
        xp 
    FROM total_levels_view 
    ORDER BY rank ASC, date ASC, username"""

df = conn.execute(query).fetchdf()

st.write("Lost City - Leaderboard development")

st.dataframe(df)