import streamlit as st
import io
from docx import Document
from datetime import date

st.set_page_config(page_title="LegalEaseAI", page_icon="⚖️")
st.title("⚖️ LegalEaseAI - Legal Document Generator")

def format_docx(text):
    doc = Document()
    doc.add_paragraph(text)
    bio = io.BytesIO()
    doc.save(bio)
    bio.seek(0)
    return bio.getvalue()

doc_type = st.sidebar.selectbox("Type", ["Rental Agreement", "NDA"])
p1 = st.text_input("Party 1")
p2 = st.text_input("Party 2")
details = st.text_area("Details")

if st.button("Generate "):
    text = f"{doc_type}\nBetween {p1} and {p2}\nDetails: {details}\nDate: {date.today()}"
    st.success("Document Generated Successfully!")
    st.text(text)
    st.download_button("Download DOCX", format_docx(text), file_name="doc.docx")