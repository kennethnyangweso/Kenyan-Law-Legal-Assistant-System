# app.py
from flask import Flask, render_template, request, jsonify
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain_classic.chains import RetrievalQA
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Configuration
LAWS_FOLDER = "Laws"
GROQ_API_KEY = os.getenv("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")

# Global variables for the RAG system
vectorstore = None
qa_chain = None

def initialize_legal_assistant():
    """Load documents and create the RAG system"""
    global vectorstore, qa_chain
    
    print("📚 Loading Kenyan legal documents...")
    
    # Load all PDFs
    all_documents = []
    pdf_files = list(Path(LAWS_FOLDER).glob("*.pdf"))
    
    for pdf_path in pdf_files:
        law_name = pdf_path.stem.replace('_', ' ')
        print(f"   Loading: {law_name}")
        loader = PyPDFLoader(str(pdf_path))
        documents = loader.load()
        for doc in documents:
            doc.metadata['source_law'] = law_name
        all_documents.extend(documents)
    
    # Split into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\nSection ", "\nArticle ", "\nPart ", "\n\n"]
    )
    chunks = text_splitter.split_documents(all_documents)
    
    # Create vector store
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(chunks, embeddings)
    
    # Initialize LLM
    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0.3,
        groq_api_key=GROQ_API_KEY
    )
    
    # Create prompt template
    legal_prompt = PromptTemplate(
        template="""You are a Kenyan legal educator explaining the law to ordinary citizens.

Here are the relevant excerpts from Kenyan law:
{context}

The citizen asks: {question}

INSTRUCTIONS:
1. Answer in simple, everyday language
2. Mention which law the answer comes from
3. Use bullet points (•) for listing rights
4. Keep it practical and helpful (3-6 sentences)
5. DO NOT copy the legal text directly

Answer:""",
        input_variables=["context", "question"]
    )
    
    # Create QA chain
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        chain_type_kwargs={"prompt": legal_prompt}
    )
    
    print("✅ Legal assistant ready!")

@app.route('/')
def index():
    """Render the chat interface"""
    return render_template('index.html')

@app.route('/about')
def about():
    """Render the about page"""
    return render_template('about.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    data = request.get_json()
    question = data.get('question', '')
    
    if not question:
        return jsonify({'error': 'No question provided'}), 400
    
    try:
        result = qa_chain.invoke({"query": question})
        answer = result['result']
        return jsonify({'answer': answer})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    initialize_legal_assistant()
    app.run(debug=True, port=5000)