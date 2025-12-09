import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="연령대별 독서 데이터 분석", layout="wide")
st.title("📚 연령대별 독서 데이터 분석 대시보드")

# ----------------------------------------------------------
# 탭 설정
tab1, tab2, tab3, tab4 = st.tabs([
    "① 전체 평균 독서량",
    "② 평일·휴일 독서량",
    "③ 독서 방해 요인",
    "④ 여가시간 중 독서 비율"
])
# ----------------------------------------------------------


# ==========================================================
# ① 2.csv — 전체 평균 독서량 (2019 & 2021)
# ==========================================================
with tab1:
    st.header("전체 평균 독서량 (연령대별)")

    # header=1 → 실제 의미있는 컬럼명 행
    df = pd.read_csv("2.csv", header=1)

    # 연령별만 필터링
    df_age = df[df["통계분류(1)"] == "연령별"]

    age_col = "통계분류(2)"
    value_col = "전체 평균"      # 2019 기준
    value_col2 = "전체 평균.1"    # 2021 기준

    fig, ax = plt.subplots(figsize=(10, 5))

    # 2019 & 2021 두 개 선그래프
    ax.plot(df_age[age_col], df_age[value_col], label="2019 전체 평균", linewidth=2)
    ax.plot(df_age[age_col], df_age[value_col2], label="2021 전체 평균", linewidth=2)

    # 20대 강조
    highlight = df_age[df_age[age_col] == "19~29세"]
    ax.scatter(highlight[age_col], highlight[value_col], s=150)
    ax.scatter(highlight[age_col], highlight[value_col2], s=150)
    ax.plot(highlight[age_col], highlight[value_col], linewidth=4)
    ax.plot(highlight[age_col], highlight[value_col2], linewidth=4)

    ax.set_xlabel("연령대")
    ax.set_ylabel("전체 평균 독서량")
    ax.legend()
    ax.grid(True)

    st.pyplot(fig)



# ==========================================================
# ② 8.csv — 평일 / 휴일 독서량
# ==========================================================
with tab2:
    st.header("평일·휴일 독서량 (연령대별)")

    # header=2 → 실제 의미있는 컬럼명 행
    df = pd.read_csv("8.csv", header=2)

    # 연령별만 선택
    df_age = df[df["통계분류(1)"] == "연령별"]

    age_col = "통계분류(2)"
    weekday_col = "평일"
    weekend_col = "휴일"

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(df_age[age_col], df_age[weekday_col], label="평일", linewidth=2)
    ax.plot(df_age[age_col], df_age[weekend_col],  label="휴일", linewidth=2)

    # 20대만 강조
    highlight = df_age[df_age[age_col] == "19~29세"]
    ax.scatter(highlight[age_col], highlight[weekday_col], s=150)
    ax.scatter(highlight[age_col], highlight[weekend_col], s=150)
    ax.plot(highlight[age_col], highlight[weekday_col], linewidth=4)
    ax.plot(highlight[age_col], highlight[weekend_col], linewidth=4)

    ax.set_xlabel("연령대")
    ax.set_ylabel("독서량")
    ax.legend()
    ax.grid(True)

    st.pyplot(fig)



# ==========================================================
# ③ 7.csv — 독서 방해 요인 도넛 차트
# ==========================================================
with tab3:
    st.header("독서 방해 요인 (연령대별 도넛 차트)")

    # header=1 → 실제 의미있는 컬럼명 행
    df = pd.read_csv("7.csv", header=1)

    # 연령별만 선택
    df_age = df[df["통계분류(1)"] == "연령별"]

    age_options = df_age["통계분류(2)"].unique()
    selected_age = st.selectbox("연령대를 선택하세요", age_options)

    row = df_age[df_age["통계분류(2)"] == selected_age].iloc[0]

    # 사례수 제외한 나머지 = 요인 9개
    factor_cols = df.columns[3:]

    labels = factor_cols
    sizes = row[factor_cols].values

    fig, ax = plt.subplots(figsize=(8, 8))

    wedges, texts, autotexts = ax.pie(
        sizes,
        labels=labels,
        autopct="%.1f%%",
        pctdistance=0.85,
        wedgeprops=dict(width=0.4)
    )

    # 도넛 구멍
    centre_circle = plt.Circle((0, 0), 0.60, fc='white')
    fig.gca().add_artist(centre_circle)

    ax.set_title(f"{selected_age} 독서 방해 요인")

    st.pyplot(fig)



# ==========================================================
# ④ 6.csv — 여가시간 중 독서 비율 (평일/주말)
# ==========================================================
with tab4:
    st.header("여가시간 중 독서 비율 (평일 / 주말)")

    # header=2 → 실제 의미있는 컬럼명 행
    df = pd.read_csv("6.csv", header=2)

    # 연령별
    df_age = df[df["통계분류(1)"] == "연령별"]

    age_col = "통계분류(2)"

    weekday_ratio = "여가시간 중 독서시간이 차지하는 비율"
    weekend_ratio = "여가시간 중 독서시간이 차지하는 비율.1"

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(df_age[age_col], df_age[weekday_ratio], label="평일 비율", linewidth=2)
    ax.plot(df_age[age_col], df_age[weekend_ratio], label="주말 비율", linewidth=2)

    # 20대 강조
    highlight = df_age[df_age[age_col] == "19~29세"]
    ax.scatter(highlight[age_col], highlight[weekday_ratio], s=150)
    ax.scatter(highlight[age_col], highlight[weekend_ratio], s=150)
    ax.plot(highlight[age_col], highlight[weekday_ratio], linewidth=4)
    ax.plot(highlight[age_col], highlight[weekend_ratio], linewidth=4)

    ax.set_xlabel("연령대")
    ax.set_ylabel("비율 (%)")
    ax.legend()
    ax.grid(True)

    st.pyplot(fig)
