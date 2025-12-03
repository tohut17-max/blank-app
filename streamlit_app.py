import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="연령대별 독서량 분석", layout="wide")

# ---------------------------------------
# 데이터 불러오기
# ---------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("clean_reading_utf8.csv", encoding="utf-8-sig")
    return df

df = load_data()


# =========================================================
# 1) 연도별 → 연령대 독서권수 비교 (막대그래프, 위에 배치)
# =========================================================
st.title("📊 연도별 연령대 독서량 비교")

years = ["2013", "2015", "2017", "2019", "2021"]
selected_year = st.selectbox("연도를 선택하세요", years)

# 선택된 연도의 모든 연령대 값을 추출
bar_data = df[["연령대", selected_year]].copy()
bar_data[selected_year] = bar_data[selected_year].astype(float)

fig1, ax1 = plt.subplots(figsize=(8, 4))
ax1.bar(bar_data["연령대"], bar_data[selected_year"])

# 축 라벨 / 제목 제거 (깔끔하게)
ax1.set_xlabel("")
ax1.set_ylabel("")
ax1.set_title("")

st.pyplot(fig1)


# =========================================================
# 2) 연령대 선택 → 연도별 선그래프 (아래 배치)
# =========================================================
st.subheader("📈 선택한 연령대의 연도별 독서량 변화")

age_list = df["연령대"].unique()
selected_age = st.selectbox("연령대를 선택하세요", age_list)

row = df[df["연령대"] == selected_age].iloc[0]
line_values = row[years].astype(float).values

fig2, ax2 = plt.subplots(figsize=(8, 4))
ax2.plot(years, line_values, marker="o", linewidth=2)

# 축 라벨·제목 제거
ax2.set_xlabel("")
ax2.set_ylabel("")
ax2.set_title("")

# 격자 제거
ax2.grid(False)

st.pyplot(fig2)
