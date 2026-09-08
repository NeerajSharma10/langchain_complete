from langchain_core.prompts import PromptTemplate

template = PromptTemplate(
    template="Summarize this research paper {research_input} with type {explanation_input} and length inpurt {length_input}",
    input_variables=["research_input", "explanation_input", "length_input"],
    validate_template=True,
)


template.save('PROMPTS/template.json')