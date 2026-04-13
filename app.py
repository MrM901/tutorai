import streamlit as st
from rag_engine import extract_text, extract_ppt_text, convert_ppt_to_pptx, chunk_text, create_index, retrieve
from llm import generate_quiz

st.set_page_config(page_title='TutorAI', page_icon='📘', layout='wide')

st.markdown('''
<style>
.main {padding-top: 1rem;}
.hero {background: linear-gradient(90deg,#4f46e5,#06b6d4); padding: 2rem; border-radius: 18px; color: white;}
.card {padding: 1rem; border:1px solid #e5e7eb; border-radius:16px; margin-top:1rem;}
</style>
''', unsafe_allow_html=True)

st.markdown("<div class='hero'><h1>📘 TutorAI</h1><p>Turn PDFs into smart quizzes and study notes in seconds.</p></div>\nBest for lecture notes, textbooks, handouts, and guides.", unsafe_allow_html=True)

col1, col2 = st.columns([1,1])
with col1:
    uploaded_file = st.file_uploader("Upload your file", type=["pdf", "ppt", "pptx"])
with col2:
    st.info('Best for lecture notes, textbooks, handouts, and guides.')

if uploaded_file:
    file_ext = uploaded_file.name.split(".")[-1].lower()
    temp_file = f"temp.{file_ext}"

    with open(temp_file, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("File uploaded successfully")

    with st.spinner("Analyzing your document..."):

        if file_ext == "pdf":
            text = extract_text(temp_file)

        elif file_ext == "pptx":
            text = extract_ppt_text(temp_file)

        elif file_ext == "ppt":
            st.error("Please convert .ppt to .pptx and upload again.")
            st.stop()

        else:
            st.error("Unsupported file type")
            st.stop()

        chunks = chunk_text(text)
        index, chunks = create_index(chunks)

    tab1, tab2 = st.tabs(['Questions', 'Preview'])

    with tab1:
      num_questions = st.number_input(
        "How many questions do you want?",
        min_value=1,
        max_value=20,
        value=3,
        step=1
    )

    if st.button('Generate Questions', use_container_width=True):
        with st.spinner('Generating questions...'):
            results = retrieve('important concepts', index, chunks)
            context = '\n'.join(results)
            quiz = generate_quiz(context, num_questions)

        st.markdown(
            "<div class='card'>" + quiz.replace('\n', '<br>') + "</div>",
            unsafe_allow_html=True
        )

        with tab2:
         st.write(text[:3000] + ('...' if len(text) > 3000 else ''))

    else:
      st.caption('Upload a file to begin.')
