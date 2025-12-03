import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="연령대별 독서량 시각화", layout="wide")

# ---------------------------------------
# 데이터 불러오기
# ---------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("clean_reading_utf8.csv", encoding="utf-8-sig")
    return df

df = load_data()

st.title("📈 연령대별 독서량 변화 그래프")

age_list = df["연령대"].unique()
selected_age = st.selectbox("연령대를 선택하세요", age_list)

row = df[df["연령대"] == selected_age].iloc[0]

years = ["2013", "2015", "2017", "2019", "2021"]
values = row[years].astype(float).values

# ---------------------------------------
# 미니멀 그래프
# ---------------------------------------
fig, ax = plt.subplots(figsize=(8, 4))

# 선 그래프
ax.plot(years, values, marker="o", linewidth=2)

# 축 이름 제거
ax.set_xlabel("")
ax.set_ylabel("")

# 제목 제거
ax.set_title("")

# 격자 제거
ax.grid(False)

st.pyplot(fig)
