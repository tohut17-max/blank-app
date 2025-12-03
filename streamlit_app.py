import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

st.set_page_config(page_title="연령대별 독서량 시각화", layout="wide")

# ---------------------------------------
# 0. 한글 폰트 설정 (중요!)
# ---------------------------------------
# Mac: AppleGothic, Windows: Malgun Gothic, Linux/Streamlit Cloud: NanumGothic
plt.rcParams['font.family'] = 'AppleGothic'   # Mac 사용 시
plt.rcParams['axes.unicode_minus'] = False    # 마이너스 깨짐 방지


# ---------------------------------------
# 1. 데이터 로드
# ---------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("clean_reading_utf8.csv", encoding="utf-8-sig")
    return df

df = load_data()

st.title("📚 연령대별 독서량 변화 (연도별 선그래프)")

age_list = df["연령대"].unique()
selected_age = st.selectbox("연령대를 선택하세요", age_list)

row = df[df["연령대"] == selected_age].iloc[0]

years = ["2013", "2015", "2017", "2019", "2021"]
values = row[years].astype(float).values

# ---------------------------------------
# 2. 그래프
# ---------------------------------------
fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(years, values, marker="o", linewidth=2)

ax.set_title(f"{selected_age} 독서량 변화")
ax.set_xlabel("연도")
ax.set_ylabel("독서량(권)")
ax.grid(True)

st.pyplot(fig)
