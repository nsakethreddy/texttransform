from deep_translator import MyMemoryTranslator
import streamlit as st
from PyPDF2 import PdfReader
from llama_index.llms.groq import Groq

llm = Groq(model="llama3-70b-8192",
           api_key="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")

# Function to summarize the text


def summarizer(text):
    response = llm.complete(f"Summarize the following text : {text}")
    return response

# Function to summarize the pdf


def pdf_summarizer(pdf_path):
    pdf = PdfReader(pdf_path)
    text = ""
    for page in pdf.pages:
        text += page.extract_text()
    return summarizer(text)

# Function to translate the pdf


def pdf_translator(pdf_path):
    pdf = PdfReader(pdf_path)
    text = ""
    for page in pdf.pages:
        text += page.extract_text()
    return translate(text)

# Function to summarize the text in one line


def one_line_summarizer(text):
    result = llm.complete(
        f"Summarize the following text in only one line: {text}")
    return result

# Function to split the text


def split_text(text, max_length=450):
    sentences = text.split('.')
    batches = []
    current_batch = ""

    for sentence in sentences:
        # Append the period back to the sentence
        sentence = sentence.strip() + "."

        if len(current_batch) + len(sentence) > max_length:
            if current_batch:
                batches.append(current_batch)
                current_batch = ""
            while len(sentence) > max_length:
                part = sentence[:max_length]
                last_space = part.rfind(' ')
                if last_space == -1:  # No spaces, hard cut
                    batches.append(part)
                    sentence = sentence[max_length:]
                else:
                    batches.append(sentence[:last_space])
                    sentence = sentence[last_space+1:]
        current_batch += sentence + " "

    if current_batch:
        batches.append(current_batch.strip())

    return batches

# Function to translate the text


def translator(text):
    return MyMemoryTranslator(source='english', target='kannada').translate(text)

# Function to translate the text


def translate(text):
    batches = split_text(text)
    translated_batches = []
    for batch in batches:
        translated_batches.append(translator(batch))
    return ' '.join(translated_batches)

# Main function


def main():

    st.title('Text Transform')

    if 'summary' not in st.session_state:
        st.session_state.summary = ''
    if 'translated_summary' not in st.session_state:
        st.session_state.translated_summary = ''
    if 'pdf_summary' not in st.session_state:
        st.session_state.pdf_summary = ''
    if 'pdf_translated_summary' not in st.session_state:
        st.session_state.pdf_translated_summary = ''

    with st.sidebar:
        st.sidebar.title('PDF Summarizer')
        file = st.file_uploader('Upload PDF file', type='pdf')

        if st.button('Summarize PDF') and file:
            st.session_state.pdf_summary = pdf_summarizer(file)
            st.write('Summary: ', st.session_state.pdf_summary)

        if st.session_state.pdf_summary:
            if st.button('Translate PDF Summary'):
                st.session_state.pdf_translated_summary = translate(
                    st.session_state.pdf_summary.text)
                st.write('Summary: ', st.session_state.pdf_summary,
                         'Translated Summary: ', st.session_state.pdf_translated_summary)

        elif st.button('Translate PDF') and file:
            st.write('Translated_Text: ', pdf_translator(file))

        elif file:
            st.write('PDF Uploaded')

        else:
            st.write('No PDF Uploaded')

    text = st.text_area('Enter text to summarize')

    if st.button('Summarize'):
        with st.spinner('Summarizing...'):
            st.session_state.summary = summarizer(text)
            st.session_state.translated_summary = ""
        st.write('Summary: ', st.session_state.summary)

    if st.session_state.summary:
        if st.button('Translate Summary'):
            with st.spinner('Translating...'):
                st.session_state.translated_summary = translate(
                    st.session_state.summary.text)
            st.write('Summary:', st.session_state.summary, 'Translated Summary: ',
                     st.session_state.translated_summary)

    if st.button('Summarize in one line'):
        with st.spinner('Summarizing...'):
            response = one_line_summarizer(text)
            st.write('Summary: ', response)

    if st.button('Translate'):
        with st.spinner('Translating...'):
            response = translate(text)
            st.write('Translation: ', response)

    footer = """ <style> .footer { position: fixed; left: 0; bottom: 0; width: 100%; background-color: #f1f1f1; color: #black; text-align: center; } </style> <div class="footer">This is a summarizer and translator app that uses the Llama3 to generate summaries of text and translate the text.<br/> You can input text in the text area and click the Summarize button to generate a summary and click on Translate Button to translate to Kannada<br/>You can also upload a PDF file and click the Summarize PDF button to generate a summary of the PDF file.</p> </div> """
    st.markdown(footer, unsafe_allow_html=True)


if __name__ == '__main__':
    main()
