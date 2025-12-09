import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Age Group Reading Dashboard", layout="wide")
st.title("📚 Age Group Reading Dashboard")

# ----------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "① Overall Reading Average",
    "② Weekday & Weekend Reading",
    "③ Reading Barriers",
    "④ Reading Share of Leisure Time"
])
# ----------------------------------------------------------


# ==========================================================
# ① 2.csv — Overall Reading Average
# ==========================================================
with tab1:
    st.header("Overall Reading Average by Age Group")

    df = pd.read_csv("2.csv", header=1)
    df_age = df[df["통계분류(1)"] == "연령별"]

    ages = df_age["통계분류(2)"]
    val_2019 = df_age["전체 평균"]
    val_2021 = df_age["전체 평균.1"]

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=ages, y=val_2019,
                             mode="lines+markers",
                             name="2019"))
    fig.add_trace(go.Scatter(x=ages, y=val_2021,
                             mode="lines+markers",
                             name="2021"))

    fig.update_layout(
        hovermode="x unified",
        xaxis_title="Age Group",
        yaxis_title="Reading Amount"
    )

    st.plotly_chart(fig, use_container_width=True)



# ==========================================================
# ② 8.csv — Weekday & Weekend Reading (Corrected Columns)
# ==========================================================
with tab2:
    st.header("Weekday & Weekend Reading Time")

    df = pd.read_csv("8.csv", header=2)
    df_age = df[df["통계분류(1)"] == "연령별"]

    ages = df_age["통계분류(2)"]

    # ✔ 실제 존재하는 컬럼명으로 수정
    weekday_read = df_age["평일"]
    weekend_read = df_age["휴일"]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=ages, y=weekday_read,
                             mode="lines+markers",
                             name="Weekday"))
    fig.add_trace(go.Scatter(x=ages, y=weekend_read,
                             mode="lines+markers",
                             name="Weekend"))

    fig.update_layout(
        hovermode="x unified",
        xaxis_title="Age Group",
        yaxis_title="Reading Time"
    )

    st.plotly_chart(fig, use_container_width=True)



# ==========================================================
# ③ 7.csv — Reading Barriers (Donut Chart)
# ==========================================================
with tab3:
    st.header("Reading Barriers by Age Group")

    df = pd.read_csv("7.csv", header=1)
    df_age = df[df["통계분류(1)"] == "연령별"]

    age_list = df_age["통계분류(2)"].unique()
    selected_age = st.selectbox("Select Age Group", age_list)

    row = df_age[df_age["통계분류(2)"] == selected_age].iloc[0]

    factor_cols = df.columns[3:]  # 사례수 제외
    labels = factor_cols
    values = row[factor_cols].values

    fig = go.Figure(
        data=[go.Pie(labels=labels, values=values, hole=0.5)]
    )

    fig.update_layout(hovermode="closest")

    st.plotly_chart(fig, use_container_width=True)



# ==========================================================
# ④ 6.csv — Share of Leisure Time Spent Reading
# ==========================================================
with tab4:
    st.header("Reading Share of Leisure Time")

    df = pd.read_csv("6.csv", header=2)
    df_age = df[df["통계분류(1)"] == "연령별"]

    ages = df_age["통계분류(2)"]

    # ✔ 실제 존재하는 컬럼명
    weekday_ratio = df_age["여가시간 중 독서시간이 차지하는 비율"]
    weekend_ratio = df_age["여가시간 중 독서시간이 차지하는 비율.1"]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=ages, y=weekday_ratio,
                             mode="lines+markers",
                             name="Weekday Ratio"))
    fig.add_trace(go.Scatter(x=ages, y=weekend_ratio,
                             mode="lines+markers",
                             name="Weekend Ratio"))

    fig.update_layout(
        hovermode="x unified",
        xaxis_title="Age Group",
        yaxis_title="Share (%)"
    )

    st.plotly_chart(fig, use_container_width=True)
