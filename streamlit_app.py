import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="연령대별 독서량 분석", layout="wide")

# ---------------------------------------
# 1. 데이터 로드 & 전처리
# ---------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv(
        "종이책전자책_독서량__성인__20251203164429.csv",
        encoding="latin1"
    )

    # CSV에 맞게 컬럼명 지정
    df = df.rename(columns={
        df.columns[0]: "구분1",
        df.columns[1]: "연령대"
    })

    # 연령 데이터만 가져오기
    age_df = df[df["구분1"] == "연령"].copy()

    # wide → long 변환 (melt)
    tidy = age_df.melt(
        id_vars="연령대",
        var_name="year",
        value_name="read_amount"
    )

    # '-' 제거 후 숫자로 변환
    tidy = tidy[tidy["read_amount"] != "-"]
    tidy["read_amount"] = tidy["read_amount"].astype(float)
    tidy["year"] = tidy["year"].astype(int)

    return tidy


tidy = load_data()

st.title("📚 연령대별 독서량 분석 대시보드")
st.write("한국 성인 독서량 데이터를 연령대·연도별로 시각화한 대시보드입니다.")

# ---------------------------------------
# 2. 연령대별 추세 (line chart)
# ---------------------------------------
st.header("① 연령대별 독서량 변화 추세")

age = st.selectbox("연령대 선택", sorted(tidy["연령대"].unique()))
age_df = tidy[tidy["연령대"] == age].sort_values("year")

st.line_chart(age_df, x="year", y="read_amount")
st.write(f"선택된 연령대 **{age}**의 연도별 독서량 변화입니다.")

# ---------------------------------------
# 3. 특정 연도 기준 비교 (bar chart)
# ---------------------------------------
st.header("② 특정 연도 기준 연령대 비교")

year = st.selectbox("연도 선택", sorted(tidy["year"].unique()))
year_df = tidy[tidy["year"] == year]

st.bar_chart(year_df, x="연령대", y="read_amount")
st.write(f"선택한 연도 **{year}년** 기준의 연령대별 독서량입니다.")

# ---------------------------------------
# 4. Heatmap (전체 패턴)
# ---------------------------------------
st.header("③ 연령대 × 연도 전체 패턴 (Heatmap)")

pivot = tidy.pivot(index="연령대", columns="year", values="read_amount")

fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(pivot, annot=True, cmap="Blues", linewidths=0.5, ax=ax)
st.pyplot(fig)

st.write("전체 연령대의 연도별 독서량 패턴을 한눈에 볼 수 있습니다.")

# ---------------------------------------
# 5. 인사이트 요약
# ---------------------------------------
st.header("📌 인사이트 요약")
st.write("""
- 전반적으로 **독서량은 감소 추세**를 보입니다.
- 특히 **20대의 독서량 감소폭이 큼**을 확인할 수 있습니다.
- 30·40대 역시 꾸준히 감소하는 흐름입니다.
- Heatmap을 통해 연령 간 격차가 선명하게 드러납니다.
""")
