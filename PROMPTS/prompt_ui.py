from langchain_google_genai import ChatGoogleGenerativeAI
import streamlit as st
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate, load_prompt

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash",  # Or "gemini-2.5-pro"
    temperature=0.7,
    max_output_tokens=100
)



st.header('Research Tool')


research_input = st.selectbox("Select Research Paper", ["Attention", "Bert", "Language", "Diffusion"])
explanation_input = st.selectbox("Select Explanation Style", ["Begineer", "Technical", "Mathmetics", "Code-Oriented"])
length_input = st.selectbox("Select Explanation Length", ["Medium", "Easy", "Short", "Long"])

template = load_prompt('PROMPTS/template.json')

prompt = template.invoke({
    'research_input': research_input,
    'explanation_input': explanation_input,
    'length_input': length_input
})

if st.button('Summarize'):
    with st.spinner("Generating summary..."):
        res = llm.invoke(prompt)
        print(res.content)
        
        # 1. If res.content is a list (like in your output), extract the 'text' key
        if isinstance(res.content, list):
            output_text = res.content[0].get('text', '')
        # 2. If res.content is a normal string
        else:
            output_text = res.content

        # Display clean text in Streamlit
        st.write(output_text)


