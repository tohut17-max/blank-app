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

years = ["2013", "2015", "2017", "2019", "2021"]


# =========================================================
# 1) 연도별 연령대 비교 (선그래프) — 상단
# =========================================================
st.write("### 연도별 연령대 비교")

selected_year = st.selectbox("연도 선택", years)

line_data = df[["연령대", selected_year]].copy()
line_data[selected_year] = line_data[selected_year].astype(float)

fig1, ax1 = plt.subplots(figsize=(8, 4))
ax1.plot(line_data["연령대"], line_data[selected_year], marker="o", linewidth=2)

# 미니멀 디자인 (축/제목/격자 제거)
ax1.set_title("")
ax1.set_xlabel("")
ax1.set_ylabel("")
ax1.grid(False)

st.pyplot(fig1)


# =========================================================
# 2) 연령대별 연도 변화 (선그래프) — 하단
# =========================================================
st.write("### 연령대별 연도 변화")

age_list = df["연령대"].unique()
selected_age = st.selectbox("연령대 선택", age_list)

row = df[df["연령대"] == selected_age].iloc[0]
line_values = row[years].astype(float).values

fig2, ax2 = plt.subplots(figsize=(8, 4))
ax2.plot(years, line_values, marker="o", linewidth=2)

ax2.set_title("")
ax2.set_xlabel("")
ax2.set_ylabel("")
ax2.grid(False)

st.pyplot(fig2)
