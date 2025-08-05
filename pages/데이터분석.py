import streamlit as st
import pandas as pd
import plotly.express as px
from io import StringIO

# -----------------------------
# 1) 원본 데이터 (문자열 -> DataFrame)
# -----------------------------
data_str = """name,grade,number,kor,eng,math,info
lee,2,1,90,91,81,100
park,2,2,88,89,77,100
kim,2,3,99,99,99,100
"""

df = pd.read_csv(StringIO(data_str))
score_cols = ["kor", "eng", "math", "info"]

# Long 형태로 변환 (시각화에 편리)
df_long = df.melt(
    id_vars=["name", "grade", "number"],
    value_vars=score_cols,
    var_name="subject",
    value_name="score"
)

# -----------------------------
# 2) Streamlit UI
# -----------------------------
st.set_page_config(page_title="학생 성적 시각화", layout="wide")
st.title("학생 성적 시각화 (Plotly Express)")

with st.expander("원본 데이터 확인", expanded=True):
    st.dataframe(df, use_container_width=True)

# 사이드바: 학생 선택, 차트 선택
st.sidebar.header("옵션")
students = st.sidebar.multiselect(
    "학생 선택",
    options=df["name"].tolist(),
    default=df["name"].tolist()
)
chart_type = st.sidebar.selectbox(
    "차트 종류",
    [
        "막대그래프 (학생별 과목 점수)",
        "꺾은선그래프 (과목별 비교)",
        "레이더차트 (Polar)",
        "히트맵 (학생×과목)"
    ]
)

# 필터 적용
if students:
    dfl = df_long[df_long["name"].isin(students)].copy()
    df_wide = df[df["name"].isin(students)].copy()
else:
    dfl = df_long.copy()
    df_wide = df.copy()

# -----------------------------
# 3) 시각화
# -----------------------------
fig = None

if chart_type == "막대그래프 (학생별 과목 점수)":
    fig = px.bar(
        dfl,
        x="name",
        y="score",
        color="subject",
        barmode="group",
        text="score",
        title="학생별 과목 점수 (Grouped Bar)"
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(yaxis_title="점수", xaxis_title="학생")

elif chart_type == "꺾은선그래프 (과목별 비교)":
    # 과목 축을 x로 두고 학생별로 라인
    fig = px.line(
        dfl,
        x="subject",
        y="score",
        color="name",
        markers=True,
        title="과목별 점수 비교 (Line)"
    )
    fig.update_layout(yaxis_title="점수", xaxis_title="과목")

elif chart_type == "레이더차트 (Polar)":
    # 선택 학생이 1명 이상일 때 다중 레이더 가능
    fig = px.line_polar(
        dfl,
        r="score",
        theta="subject",
        color="name",
        line_close=True,
        markers=True,
        title="학생별 레이더 차트 (Polar)"
    )
    fig.update_polars(radialaxis=dict(range=[0, 100]))

elif chart_type == "히트맵 (학생×과목)":
    # 학생×과목 매트릭스로 변환
    pivot_df = df_wide.set_index("name")[score_cols]
    fig = px.imshow(
        pivot_df,
        text_auto=True,
        aspect="auto",
        title="히트맵 (학생×과목)"
    )

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# 4) 요약 지표 (선택)
# -----------------------------
with st.expander("요약 통계", expanded=False):
    # 학생별 평균
    student_mean = df_wide.assign(mean=df_wide[score_cols].mean(axis=1))[["name", "mean"]]
    # 과목별 평균
    subject_mean = df_wide[score_cols].mean().rename("mean").reset_index().rename(columns={"index": "subject"})
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("학생별 평균")
        st.dataframe(student_mean, use_container_width=True)
    with c2:
        st.subheader("과목별 평균")
        st.dataframe(subject_mean, use_container_width=True)
