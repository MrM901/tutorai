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

st.markdown("<div class='hero'><h1>📘 TutorAI</h1><p>Turn PDFs into smart quizzes and study notes in seconds.</p></div>", unsafe_allow_html=True)

col1, col2 = st.columns([1,1])
with col1:
    uploaded_file = st.file_uploader("Upload your file", type=["pdf", "ppt", "pptx"])
with col2:
    st.info('Best for lecture notes, textbooks, handouts, and guides.')

if uploaded_file:
    with open('temp.pdf','wb') as f:
        f.write(uploaded_file.read())
    st.success('PDF uploaded successfully')

    with st.spinner("Analyzing your document..."):

     file_ext = uploaded_file.name.split(".")[-1].lower()
    temp_file = f"temp.{file_ext}"

    with open(temp_file, "wb") as f:
        f.write(uploaded_file.read())

    if file_ext == "pdf":
         text = extract_text(temp_file)

    elif file_ext == "pptx":
        text = extract_ppt_text(temp_file)

    elif file_ext == "ppt":
        converted = convert_ppt_to_pptx(temp_file)
        text = extract_ppt_text(converted)

    chunks = chunk_text(text)
    index, chunks = create_index(chunks)


    tab1, tab2 = st.tabs(['Quiz', 'Preview'])

    with tab1:
        if st.button('Generate Questions', use_container_width=True):
            with st.spinner('Generating questions...'):
                results = retrieve('important concepts', index, chunks)
                context = '\n'.join(results)
                quiz = generate_quiz(context)
            st.markdown("<div class='card'>" + quiz.replace('\n','<br>') + "</div>", unsafe_allow_html=True)

    with tab2:
        st.write(text[:3000] + ('...' if len(text) > 3000 else ''))
else:
    st.caption('Upload a PDF to begin.')