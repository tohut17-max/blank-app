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

    # 컬럼명 정리
    df = df.rename(columns={df.columns[0]: "구분1", df.columns[1]: "연령대"})

    # 연령만 선택
    age_df = df[df["구분1"].str.contains("연령", na=False)].copy()

    # Tidy 변환
    tidy = age_df.melt(
        id_vars="연령대", 
        var_name="year", 
        value_name="read_amount"
    )

    # 결측치 제거
    tidy = tidy[tidy["read_amount"] != "-"]

    # 숫자형 변환
    tidy["read_amount"] = tidy["read_amount"].astype(float)
    tidy["year"] = tidy["year"].astype(int)

    return tidy

tidy = load_data()

st.title("📚 연령대별 독서량 분석 대대시보드")
st.write("KOSIS 독서실태조사를 기반으로 연령대별 독서량 변화를 시각화합니다.")

# ---------------------------------------
# 2. 연령대별 연도 추세 (Line Chart)
# ---------------------------------------
st.header("① 연령대별 독서량 변화 추세")

age = st.selectbox("연령대 선택", tidy["연령대"].unique())

age_df = tidy[tidy["연령대"] == age].sort_values("year")

st.line_chart(age_df, x="year", y="read_amount")

st.write(f"선택된 연령대 **{age}**의 연도별 독서량 변화입니다.")

# ---------------------------------------
# 3. 연도별 연령대 비교 (Bar Chart)
# ---------------------------------------
st.header("② 특정 연도 기준 연령대별 비교")

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
sns.heatmap(pivot, annot=True, cmap="Blues", linewidths=.5, ax=ax)
st.pyplot(fig)

st.write("전체 연령대와 연도에 걸친 독서량 패턴을 한눈에 확인할 수 있습니다.")

# ---------------------------------------
# 5. 결론 및 인사이트
# ---------------------------------------
st.header("📌 인사이트 요약")

st.write("""
- 전반적으로 **독서량이 지속적으로 감소**하는 경향이 나타납니다.  
- 특히 **20대 연령층의 감소폭이 큼**을 확인할 수 있습니다.  
- 30대·40대 또한 꾸준히 감소하는 흐름을 보여줍니다.  
- 일부 연령대는 특정 시점 이후 변화가 큰 편이며, 사회적·환경적 요인과 연관 가능성이 있습니다.  
- Heatmap을 통해 연령별 격차가 명확히 드러나며, 이는 독서 정책 및 문화적 관심 필요성을 시사합니다.
""")

