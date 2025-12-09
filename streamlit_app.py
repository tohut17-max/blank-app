import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 페이지 설정
st.set_page_config(page_title="연령대별 독서 데이터 분석", layout="wide")

st.title("📚 연령대별 독서 데이터 분석 대시보드")

# ---------------------------------------------------------
# 탭 구성
# ---------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "① 연령대별 전체 평균",
    "② 평일·휴일 독서량",
    "③ 독서 방해요인 도넛 차트",
    "④ 여가시간 중 독서비율"
])

# ---------------------------------------------------------
# ① 연령대별 전체 평균 선그래프 (2.csv)
# ---------------------------------------------------------
with tab1:
    st.header("연령대별 전체 평균 선그래프")

    df = pd.read_csv("2.csv")
    age_col = "연령대"
    value_col = "전체평균"

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(df[age_col], df[value_col], linewidth=2)

    # 20대 강조
    highlight = df[df[age_col].astype(str).str.contains("20")]
    ax.plot(highlight[age_col], highlight[value_col], linewidth=4)
    ax.scatter(highlight[age_col], highlight[value_col], s=150)

    ax.set_xlabel("연령대")
    ax.set_ylabel("전체 평균 독서량")
    ax.grid(True)

    st.pyplot(fig)


# ---------------------------------------------------------
# ② 평일·휴일 독서량 (8.csv)
# ---------------------------------------------------------
with tab2:
    st.header("평일·휴일 독서량 비교")

    df = pd.read_csv("8.csv")

    age_col = "연령대"
    weekday_col = "평일"
    weekend_col = "휴일"

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(df[age_col], df[weekday_col], label="평일", linewidth=2)
    ax.plot(df[age_col], df[weekend_col], label="휴일", linewidth=2)

    # 20대 강조
    highlight = df[df[age_col].astype(str).str.contains("20")]
    ax.plot(highlight[age_col], highlight[weekday_col], linewidth=4)
    ax.scatter(highlight[age_col], highlight[weekday_col], s=120)
    ax.plot(highlight[age_col], highlight[weekend_col], linewidth=4)
    ax.scatter(highlight[age_col], highlight[weekend_col], s=120)

    ax.set_xlabel("연령대")
    ax.set_ylabel("독서량")
    ax.legend()
    ax.grid(True)

    st.pyplot(fig)


# ---------------------------------------------------------
# ③ 독서 방해요인 도넛 차트 (7.csv)
# ---------------------------------------------------------
with tab3:
    st.header("독서 방해 요인 도넛 차트")

    df = pd.read_csv("7.csv")

    age_col = df.columns[0]         # 첫 컬럼 = 연령대
    factor_cols = df.columns[1:]    # 나머지 = 요인 9개

    selected_age = st.selectbox("연령대를 선택하세요", df[age_col].unique())

    row = df[df[age_col] == selected_age][factor_cols].iloc[0]

    labels = factor_cols
    sizes = row.values

    fig, ax = plt.subplots(figsize=(8, 8))

    wedges, texts, autotexts = ax.pie(
        sizes,
        labels=labels,
        autopct="%.1f%%",
        pctdistance=0.85,
        wedgeprops=dict(width=0.4)
    )

    # 도넛 구멍
    centre_circle = plt.Circle((0, 0), 0.60, fc="white")
    fig.gca().add_artist(centre_circle)

    ax.set_title(f"{selected_age} 독서 방해 요인 비중")

    st.pyplot(fig)


# ---------------------------------------------------------
# ④ 여가시간 중 독서비율 바그래프 (6.csv)
# ---------------------------------------------------------
with tab4:
    st.header("여가시간 중 독서 비율")

    df = pd.read_csv("6.csv")

    age_col = "연령대"
    value_col = "독서비율"

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(df[age_col], df[value_col])

    ax.set_xlabel("연령대")
    ax.set_ylabel("독서 비율 (%)")
    ax.grid(axis="y")

    st.pyplot(fig)
