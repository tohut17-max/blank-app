import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Reading Dashboard", layout="wide")
st.title("📚 Reading Data Dashboard (Clean View)")

tab1, tab2, tab3, tab4 = st.tabs([
    "Overall Reading Average",
    "Weekday & Weekend Reading",
    "Reading Barriers",
    "Reading Share of Leisure Time"
])

# ==========================================================
# ① Overall Reading Average (2.csv)
# ==========================================================
with tab1:
    df = pd.read_csv("2.csv", header=1)
    df_age = df[df["통계분류(1)"] == "연령별"]

    age_col = "통계분류(2)"
    v19 = "전체 평균"
    v21 = "전체 평균.1"

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df_age[age_col], df_age[v19], linewidth=2)
    ax.plot(df_age[age_col], df_age[v21], linewidth=2)

    # 축 텍스트 제거
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.set_xticks(range(len(df_age)))
    ax.set_xticklabels(df_age[age_col])  # 연령대는 남기기
    ax.set_yticks([])

    ax.legend().remove() if ax.get_legend() else None
    ax.grid(True)

    st.pyplot(fig)


# ==========================================================
# ② Weekday & Weekend Reading (8.csv)
# ==========================================================
with tab2:
    df = pd.read_csv("8.csv", header=2)
    df_age = df[df["통계분류(1)"] == "연령별"]

    age_col = "통계분류(2)"
    w = "평일"
    h = "휴일"

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df_age[age_col], df_age[w], linewidth=2)
    ax.plot(df_age[age_col], df_age[h], linewidth=2)

    # y축 반전 = 감소 그래프처럼 보이게
    ax.invert_yaxis()

    # 텍스트 제거
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.set_xticks(range(len(df_age)))
    ax.set_xticklabels(df_age[age_col])
    ax.set_yticks([])
    ax.legend().remove() if ax.get_legend() else None
    ax.grid(True)

    st.pyplot(fig)


# ==========================================================
# ③ Reading Barriers (7.csv)
# ==========================================================
with tab3:
    df = pd.read_csv("7.csv", header=1)
    df_age = df[df["통계분류(1)"] == "연령별"]

    age_sel = st.selectbox("Select Age Group", df_age["통계분류(2)"].unique())
    row = df_age[df_age["통계분류(2)"] == age_sel].iloc[0]

    factor_cols = df.columns[3:]
    sizes = row[factor_cols].values

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(sizes, labels=None, autopct=None, wedgeprops=dict(width=0.4))
    circle = plt.Circle((0, 0), 0.6, color="white")
    ax.add_artist(circle)

    ax.set_xticks([])
    ax.set_yticks([])

    st.pyplot(fig)


# ==========================================================
# ④ Reading Share of Leisure Time (6.csv)
# ==========================================================
with tab4:
    df = pd.read_csv("6.csv", header=2)
    df_age = df[df["통계분류(1)"] == "연령별"]

    age_col = "통계분류(2)"
    w = "여가시간 중 독서시간이 차지하는 비율"
    h = "여가시간 중 독서시간이 차지하는 비율.1"

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df_age[age_col], df_age[w], linewidth=2)
    ax.plot(df_age[age_col], df_age[h], linewidth=2)

    # y축 반전 = 감소하는 그래프처럼 보이기
    ax.invert_yaxis()

    # 텍스트 제거
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.set_xticks(range(len(df_age)))
    ax.set_xticklabels(df_age[age_col])
    ax.set_yticks([])
    ax.legend().remove() if ax.get_legend() else None
    ax.grid(True)

    st.pyplot(fig)
