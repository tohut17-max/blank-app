import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Reading Data Dashboard", layout="wide")
st.title("📚 Reading Data Dashboard")

# ----------------------------------------------------------
# Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "Overall Reading Average",
    "Weekday & Weekend Reading",
    "Reading Barriers",
    "Reading Ratio of Leisure Time"
])
# ----------------------------------------------------------


# ==========================================================
# ① Overall Reading Average (2.csv)
# ==========================================================
with tab1:
    st.header("Overall Reading Average by Age Group")

    df = pd.read_csv("2.csv", header=1)
    df_age = df[df["통계분류(1)"] == "연령별"]

    age_col = "통계분류(2)"
    avg_2019 = "전체 평균"
    avg_2021 = "전체 평균.1"

    fig, ax = plt.subplots(figsize=(10, 5))

    # Plot lines
    ax.plot(df_age[age_col], df_age[avg_2019], linewidth=2)
    ax.plot(df_age[age_col], df_age[avg_2021], linewidth=2)

    # Highlighting 20s
    highlight = df_age[df_age[age_col] == "19~29세"]
    ax.scatter(highlight[age_col], highlight[avg_2019], s=150)
    ax.scatter(highlight[age_col], highlight[avg_2021], s=150)
    ax.plot(highlight[age_col], highlight[avg_2019], linewidth=4)
    ax.plot(highlight[age_col], highlight[avg_2021], linewidth=4)

    # Remove text
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.legend().remove() if ax.get_legend() else None

    st.pyplot(fig)



# ==========================================================
# ② Weekday & Weekend Reading (8.csv)
# ==========================================================
with tab2:
    st.header("Weekday & Weekend Reading by Age Group")

    df = pd.read_csv("8.csv", header=2)
    df_age = df[df["통계분류(1)"] == "연령별"]

    age_col = "통계분류(2)"
    weekday = "평일"
    weekend = "휴일"

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(df_age[age_col], df_age[weekday], linewidth=2)
    ax.plot(df_age[age_col], df_age[weekend], linewidth=2)

    highlight = df_age[df_age[age_col] == "19~29세"]
    ax.scatter(highlight[age_col], highlight[weekday], s=150)
    ax.scatter(highlight[age_col], highlight[weekend], s=150)
    ax.plot(highlight[age_col], highlight[weekday], linewidth=4)
    ax.plot(highlight[age_col], highlight[weekend], linewidth=4)

    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.legend().remove() if ax.get_legend() else None

    st.pyplot(fig)



# ==========================================================
# ③ Reading Barriers (7.csv) — Donut Chart
# ==========================================================
with tab3:
    st.header("Reading Barriers (Donut Chart)")

    df = pd.read_csv("7.csv", header=1)
    df_age = df[df["통계분류(1)"] == "연령별"]

    age_options = df_age["통계분류(2)"].unique()
    selected_age = st.selectbox("Select Age Group", age_options)

    row = df_age[df_age["통계분류(2)"] == selected_age].iloc[0]

    # All barrier columns (exclude count)
    barrier_cols = df.columns[3:]
    sizes = row[barrier_cols].values

    fig, ax = plt.subplots(figsize=(8, 8))

    ax.pie(
        sizes,
        labels=None,       # no text
        autopct=None,      # no percentages
        wedgeprops=dict(width=0.4)
    )

    center = plt.Circle((0, 0), 0.60, fc="white")
    fig.gca().add_artist(center)

    ax.set_xticks([])
    ax.set_yticks([])

    st.pyplot(fig)



# ==========================================================
# ④ Ratio of Reading in Leisure Time (6.csv)
# ==========================================================
with tab4:
    st.header("Reading Ratio of Leisure Time (Weekday / Weekend)")

    df = pd.read_csv("6.csv", header=2)
    df_age = df[df["통계분류(1)"] == "연령별"]

    age_col = "통계분류(2)"
    weekday_ratio = "여가시간 중 독서시간이 차지하는 비율"
    weekend_ratio = "여가시간 중 독서시간이 차지하는 비율.1"

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(df_age[age_col], df_age[weekday_ratio], linewidth=2)
    ax.plot(df_age[age_col], df_age[weekend_ratio], linewidth=2)

    highlight = df_age[df_age[age_col] == "19~29세"]
    ax.scatter(highlight[age_col], highlight[weekday_ratio], s=150)
    ax.scatter(highlight[age_col], highlight[weekend_ratio], s=150)
    ax.plot(highlight[age_col], highlight[weekday_ratio], linewidth=4)
    ax.plot(highlight[age_col], highlight[weekend_ratio], linewidth=4)

    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.legend().remove() if ax.get_legend() else None

    st.pyplot(fig)
