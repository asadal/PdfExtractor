import os
import PyPDF3
import streamlit as st
import tempfile as tf
from tempfile import NamedTemporaryFile
import pdfplumber
from tqdm import tqdm

def get_page_numbers(pdf_file):
    pdfReader = PyPDF3.PdfFileReader(pdf_file)
    pages = pdfReader.numPages
    return pages

def app():
    # Set page title and icon
    st.set_page_config(
        page_title="PDF Extractor",
        page_icon="https://cdn-icons-png.flaticon.com/512/80/80942.png"
    )

    # Featured image
    st.image(
        "https://cdn-icons-png.flaticon.com/512/80/80942.png",
        width=120
    )

    # Main title and description
    st.title("PDF Extractor")
    st.subheader("Extract text from a PDF file.")
    
    pdf_file = st.file_uploader("PDF 파일을 업로드하세요.", type="pdf")
    if pdf_file is not None:
        try:
            with st.spinner("텍스트를 추출하고 있습니다..."):
                with NamedTemporaryFile(suffix="pdf", delete=True) as tmp_file:
                    tmp_file.write(pdf_file.getvalue())
                    file_path = tmp_file.name
                    print("PDF 파일 경로: ", file_path)
                    final_txt = ""
                    pdf_pages = get_page_numbers(file_path)
                    with pdfplumber.open(file_path) as pdf:
                        for i in tqdm(range(0, pdf_pages)):
                            page = pdf.pages[i]
                            text = page.extract_text()
                            print(text)
                            final_txt += text
            # 텍스트 출력
            st.header("추출된 텍스트")
            st.text_area("", value=final_txt, height=500)
            # 추출된 텍스트를 txt 파일로 다운로드
            st.header("텍스트 다운로드")
            st.download_button(
                            label="📥 Download Script 🗒️",
                            data=final_txt,
                            file_name='extracted_text.txt',
                            mime='text/plain'
                            )
        except Exception as e:
                st.error("오류가 발생했습니다. 😥")
                st.error(e)

if __name__ == "__main__":
    app()
