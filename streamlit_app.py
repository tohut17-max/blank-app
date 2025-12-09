import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Reading Dashboard by Age", layout="wide")
st.title("📚 Reading Data Dashboard")

# ----------------------------------------------------------
# Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "Overall Reading Average",
    "Weekday & Weekend Reading",
    "Reading Barriers",
    "Reading Share of Leisure Time"
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
    value_2019 = "전체 평균"
    value_2021 = "전체 평균.1"

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(df_age[age_col], df_age[value_2019], linewidth=2)
    ax.plot(df_age[age_col], df_age[value_2021], linewidth=2)

    highlight = df_age[df_age[age_col] == "19~29세"]
    ax.scatter(highlight[age_col], highlight[value_2019], s=150)
    ax.scatter(highlight[age_col], highlight[value_2021], s=150)
    ax.plot(highlight[age_col], highlight[value_2019], linewidth=4)
    ax.plot(highlight[age_col], highlight[value_2021], linewidth=4)

    # Remove text elements
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.legend().remove() if ax.get_legend() else None

    st.pyplot(fig)



# ==========================================================
# ② Weekday / Weekend Reading (8.csv)
# ==========================================================
with tab2:
    st.header("Weekday & Weekend Reading by Age Group")

    df = pd.read_csv("8.csv", header=2)

    df_age = df[df["통계분류(1)"] == "연령별"]

    age_col = "통계분류(2)"
    weekday_col = "평일"
    weekend_col = "휴일"

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(df_age[age_col], df_age[weekday_col], linewidth=2)
    ax.plot(df_age[age_col], df_age[weekend_col], linewidth=2)

    highlight = df_age[df_age[age_col] == "19~29세"]
    ax.scatter(highlight[age_col], highlight[weekday_col], s=150)
    ax.scatter(highlight[age_col], highlight[weekend_col], s=150)
    ax.plot(highlight[age_col], highlight[weekday_col], linewidth=4)
    ax.plot(highlight[age_col], highlight[weekend_col], linewidth=4)

    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.legend().remove() if ax.get_legend() else None

    st.pyplot(fig)



# ==========================================================
# ③ Reading Barriers (Donut Chart, 7.csv)
# ==========================================================
with tab3:
    st.header("Reading Barriers (Donut Chart)")

    df = pd.read_csv("7.csv", header=1)

    df_age = df[df["통계분류(1)"] == "연령별"]

    age_options = df_age["통계분류(2)"].unique()
    selected_age = st.selectbox("Select Age Group", age_options)

    row = df_age[df_age["통계분류(2)"] == selected_age].iloc[0]

    factor_cols = df.columns[3:]  # exclude 사례수
    sizes = row[factor_cols].values

    fig, ax = plt.subplots(figsize=(8, 8))

    ax.pie(
        sizes,
        labels=None,  # Remove labels
        autopct=None, 
        wedgeprops=dict(width=0.4)
    )

    centre = plt.Circle((0, 0), 0.60, fc="white")
    fig.gca().add_artist(centre)

    ax.set_xticks([])
    ax.set_yticks([])

    st.pyplot(fig)



# ==========================================================
# ④ Reading Share of Leisure Time (6.csv)
# ==========================================================
with tab4:
    st.header("Reading Share of Total Leisure Time")

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
