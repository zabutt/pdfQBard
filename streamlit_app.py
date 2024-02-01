import streamlit as st
import openai
from PyPDF2 import PdfReader

# Set OpenAI API key securely using secrets management
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.title("Ask Me Anything About Your PDF")

# Input for OpenAI API key (optional, for flexibility)
openai_key = st.text_input("Enter your OpenAI API key (optional, if not set in secrets)")
if openai_key:
    openai.api_key = openai_key

# Upload PDF file
uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file:
    pdf_reader = PdfReader(uploaded_file)
    pdf_text = ""
    for page in pdf_reader.pages:
        pdf_text += page.extract_text()

    # User's question
    user_question = st.text_input("Ask a question about the PDF:")

    if user_question:
        # Construct prompt for OpenAI, ensuring clarity and context
        prompt = f"Answer the following question about the provided PDF document:\n{user_question}\n\nDocument contents:\n{pdf_text}"

        try:
            response = openai.Completion.create(
                engine="text-davinci-003",  # Use the most capable model
                prompt=prompt,
                max_tokens=150,  # Adjust as needed
                stop=None,  # Allow for longer responses if required
                temperature=0.7,
            )
            answer = response.choices[0].text.strip()
            st.write("Answer:", answer)
        except openai.error.OpenAIError as e:
            st.error("Error:", e)

# Custom styling for a beautiful GUI
st.markdown(
    """
<style>
body {
  background-color: #f5f5f5;
  font-family: sans-serif;
}
.st-c23 {
  color: #007bff;
}
.st-b5 {
  margin-top: 20px;
  padding: 20px;
  background-color: #fff;
  border-radius: 5px;
}
</style>
""",
    unsafe_allow_html=True,
)