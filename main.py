import streamlit as st
from millify import millify
import duckdb

st.set_page_config(
    page_title="Lost City - Leaderboard",
    page_icon="🏆",
    layout="wide",
)

conn = duckdb.connect("data_model/prod.duckdb", read_only=True)

query = """
    SELECT 
        rank, 
        date, 
        username, 
        level, 
        xp,
        xp - LAG(xp, 1) OVER (PARTITION BY username ORDER BY date ASC) AS xp_diff
    FROM total_levels_view 
    ORDER BY rank ASC, date ASC, username"""

df = conn.execute(query).fetchdf()

st.title("Lost City - Leaderboard development")

col_1, col_2, col_3 = st.columns([1, 2, 2])

with col_1:
    rank = st.selectbox(
        "Select rank",
        df["rank"].unique(),
        index=0,
    )

    df_rank = df[df["rank"] == rank]

    max_date = df["date"].max()
    username = df_rank[(df_rank["date"] == max_date)]["username"].values[0]

    xp_now = df_rank.sort_values(by="date", ascending=False)["xp"].values[0]
    xp_before = df_rank.sort_values(by="date", ascending=False)["xp"].values[3]

    df_rank_filtered = df_rank[df_rank["username"] == username].sort_values(
        by="date", ascending=False
    )
    df_rank_filtered["date_diff"] = df_rank_filtered["date"].diff(-1).dt.days
    uninterrupted_count = (df_rank_filtered["date_diff"] == 1).cumprod().sum() + 1

    df_rank_filtered["uninterrupted_streak"] = (
        df_rank_filtered["date_diff"] == 1
    ).cumprod()
    xp_gained_streak = df_rank_filtered[df_rank_filtered["uninterrupted_streak"] == 1][
        "xp_diff"
    ].sum()

    st.metric(
        label=f"Rank {rank}",
        value=username,
        delta=f"{millify(xp_gained_streak, precision=2)} xp",
    )

    st.markdown(
        f"""**Rank {rank}** is currently held by 
        **{username}** with **{millify(xp_now, precision=2)} xp**.
        {username} has held this rank for **{uninterrupted_count}** days.
        """
    )

    st.markdown(
        f"""During this time, **{username}** has gained a total of
        **{millify(xp_gained_streak, precision=2)} xp**. 
        This is an average of **{millify(xp_gained_streak / uninterrupted_count)} xp** per day.
        """
    )

with col_2:
    st.subheader(f"XP Progression for {username}")
    st.line_chart(
        df[df["username"] == username],
        x="date",
        x_label="Date",
        y="xp",
        y_label="Total XP",
    )

with col_3:
    st.subheader(f"XP Gained for {username}")
    st.bar_chart(
        df[df["username"] == username],
        x="date",
        x_label="Date",
        y="xp_diff",
        y_label="XP Difference",
    )

