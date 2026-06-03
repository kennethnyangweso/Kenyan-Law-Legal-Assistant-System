# app.py - Using LCEL (LangChain Expression Language) - No langchain-classic needed
import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_groq import ChatGroq
from pathlib import Path

load_dotenv()
app = Flask(__name__)

# Configuration
LAWS_FOLDER = "Laws"
vectorstore = None
rag_chain = None

def format_docs(docs):
    """Format retrieved documents for the prompt"""
    return "\n\n---\n\n".join([doc.page_content for doc in docs])

def initialize_legal_assistant():
    """Load documents and create the RAG system"""
    global vectorstore, rag_chain
    
    # Check for API key
  
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
    
    # Hardcode for local testing
     api_key = "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"
    print("✅ Using hardcoded API key")
    
    print("📚 Loading Kenyan legal documents...")
    
    # Load all PDFs
    all_documents = []
    pdf_files = list(Path(LAWS_FOLDER).glob("*.pdf"))
    
    if not pdf_files:
        print(f"❌ No PDF files found in '{LAWS_FOLDER}/' folder!")
        return False
    
    for pdf_path in pdf_files:
        law_name = pdf_path.stem.replace('_', ' ')
        print(f"   Loading: {law_name}")
        try:
            loader = PyPDFLoader(str(pdf_path))
            documents = loader.load()
            for doc in documents:
                doc.metadata['source_law'] = law_name
            all_documents.extend(documents)
        except Exception as e:
            print(f"   Error loading {law_name}: {e}")
    
    if not all_documents:
        print("❌ No documents loaded!")
        return False
    
    print(f"✅ Total: {len(all_documents)} pages loaded")
    
    # Split into chunks
    print("✂️  Splitting into searchable chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\nSection ", "\nArticle ", "\nPart ", "\n\n", " "]
    )
    chunks = text_splitter.split_documents(all_documents)
    print(f"✅ Created {len(chunks)} text chunks")
    
    # Create vector store
    print("🔢 Creating search index...")
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local("kenyan_laws_vectorstore")
    print("✅ Vector database ready!")
    
    # Initialize LLM
    print("🤖 Initializing AI...")
    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0.3,
        api_key=api_key
    )
    
    # Create prompt template
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a Kenyan legal educator explaining the law to ordinary citizens.

Relevant excerpts from Kenyan law:
{context}

INSTRUCTIONS:
1. Answer in simple, everyday language
2. Mention which law the answer comes from
3. Use bullet points (•) for listing rights
4. Keep it practical and helpful (3-6 sentences)
5. DO NOT copy the legal text directly"""),
        ("human", "{question}")
    ])
    
    # Create retriever
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
    
    # Create LCEL RAG chain
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    print("✅ Legal assistant ready!\n")
    return True

# Flask routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat')
def chat_page():
    return render_template('chat.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/chat_api', methods=['POST'])
def chat_api():
    global rag_chain
    
    if rag_chain is None:
        return jsonify({'error': 'Legal assistant not initialized'}), 500
    
    data = request.get_json()
    question = data.get('question', '')
    
    if not question:
        return jsonify({'error': 'No question provided'}), 400
    
    try:
        answer = rag_chain.invoke(question)
        return jsonify({'answer': answer})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🇰🇪 KENYAN LEGAL ASSISTANT")
    print("="*60)
    
    if initialize_legal_assistant():
        print("\n✅ Starting web server...")
        print("   Open http://127.0.0.1:5000")
        app.run(debug=True, port=5000)
    else:
        print("\n❌ Failed to initialize. Check your API key and Laws folder.")