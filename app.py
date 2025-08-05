import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
fig = go.Figure()

df = pd.read_csv('./data/mydata.csv')

# global variable 
url = 'https://www.youtube.com/watch?v=XyEOEBsa8I4'

# dictionary
ulrs = {
    '윤리': ['1', '2'], 
    '코딩': ['3', '4']
}

st.title('This is my fist webapp!!')
col1, col2 = st.columns((4,1))
with col1:
    with st.expander('SubContent1...'):
        st.subheader('SubContent1...')
        st.video(url)

    with st.expander('SubContent2...'):
        st.subheader('Image Content...')
        st.image('./images/catdog.jpg')

    with st.expander('SubContent3...'):
        st.subheader('HTML Content...')
        import streamlit.components.v1 as htmlviewer
        with open('./htmls/index.html', 'r', encoding='utf-8') as f:
            html1 = f.read()
            f.close()
        htmlviewer.html(html1, height=800)

    with st.expander('SubContent4...'):
        st.subheader('Data App Content...')
        st.table(df)
        st.write(df.describe())

        # Bar chart for individual subject scores
        st.subheader("Subject Scores by Student")
        subjects = ['kor', 'eng', 'math', 'info']
        fig_bar = px.bar(df, x='name', y=subjects, barmode='group', title="Scores by Subject")
        fig_bar.update_layout(xaxis_title="Student", yaxis_title="Score")
        st.plotly_chart(fig_bar, use_container_width=True)

        # Scatter matrix for subject correlations
        st.subheader("Correlation Between Subjects")
        fig_scatter = px.scatter_matrix(df, dimensions=subjects, color='name', title="Scatter Matrix of Subject Scores")
        st.plotly_chart(fig_scatter, use_container_width=True)

        # Average score per student
        st.subheader("Average Score per Student")
        df['average'] = df[subjects].mean(axis=1)
        fig_avg = px.bar(df, x='name', y='average', title="Average Score Across Subjects")
        fig_avg.update_layout(xaxis_title="Student", yaxis_title="Average Score")
        st.plotly_chart(fig_avg, use_container_width=True)

        # # fig, ax = plt.subplots(figsize=(20,10))
        # # df.plot(ax=ax)
        # # plt.savefig('./images/mygraph.png')
        # st.image('./images/mygraph.png')
        # st.plotly_chart(fig, config = {'scrollZoom': False})

with col2:
    with st.expander('Tips...'):
        st.info('Tips.........')