# legal_assistant.py - Complete Kenyan Legal Assistant
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain_classic.chains import RetrievalQA
import os
from pathlib import Path

print("="*70)
print("🇰🇪 KENYAN LEGAL ASSISTANT")
print("Constitution | Employment | Children | Sexual Offences | Data Protection")
print("="*70)

# ============================================
# CONFIGURATION
# ============================================
LAWS_FOLDER = "Laws"  # Folder containing all your PDFs
GROQ_API_KEY = "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"  # Get from https://console.groq.com

# ============================================
# LOAD ALL PDFs
# ============================================
def load_all_laws(folder_path):
    """Load every PDF in the laws folder"""
    all_documents = []
    pdf_files = list(Path(folder_path).glob("*.pdf"))
    
    if not pdf_files:
        print(f"\n❌ No PDF files found in '{folder_path}/' folder!")
        print("   Please add your PDF files and run again.")
        return []
    
    print(f"\n📚 Loading {len(pdf_files)} legal documents...\n")
    
    for pdf_path in pdf_files:
        # Clean up the filename for display
        law_name = pdf_path.stem.replace('_', ' ').replace('.pdf', '')
        print(f"   📄 Loading: {law_name}")
        
        try:
            loader = PyPDFLoader(str(pdf_path))
            documents = loader.load()
            
            # Add metadata so the bot knows which law each chunk comes from
            for doc in documents:
                doc.metadata['source_law'] = law_name
            
            all_documents.extend(documents)
            print(f"      ✓ {len(documents)} pages loaded")
        except Exception as e:
            print(f"      ✗ Error: {e}")
    
    print(f"\n✅ Total: {len(all_documents)} pages loaded across all laws")
    return all_documents

# Load everything
documents = load_all_laws(LAWS_FOLDER)

if not documents:
    print("\n⚠️ No documents loaded. Exiting.")
    exit()

# ============================================
# SPLIT INTO CHUNKS
# ============================================
print("\n✂️  Splitting into searchable chunks...")
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    separators=["\nSection ", "\nArticle ", "\nPart ", "\n\n", " "]
)
chunks = text_splitter.split_documents(documents)
print(f"✅ Created {len(chunks)} text chunks")

# ============================================
# CREATE VECTOR DATABASE
# ============================================
print("\n🔢 Creating search index (first time only, takes 2-3 minutes)...")
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
vectorstore = FAISS.from_documents(chunks, embeddings)
print("✅ Vector database ready!")

# Save for faster loading next time
vectorstore.save_local("kenyan_laws_vectorstore")
print("💾 Vector database saved for future use (will load faster next time)")

# ============================================
# SET UP THE LLM
# ============================================
print("\n🤖 Initializing AI...")
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.3,
    groq_api_key=GROQ_API_KEY
)

# ============================================
# THE PROMPT - This makes answers plain language
# ============================================
legal_prompt = PromptTemplate(
    template="""You are a Kenyan legal educator explaining the law to ordinary citizens.

Here are the relevant excerpts from Kenyan law:
{context}

The citizen asks: {question}

INSTRUCTIONS:
1. Answer in simple, everyday language - like explaining to a neighbor
2. Mention which law the answer comes from (Constitution, Employment Act, etc.)
3. Use bullet points (•) for listing rights
4. Keep it practical and helpful (3-6 sentences)
5. DO NOT copy the legal text directly - explain it

Now provide a clear, helpful answer:""",
    input_variables=["context", "question"]
)

# Create retriever
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

# Create the chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    chain_type_kwargs={"prompt": legal_prompt}
)

# ============================================
# READY!
# ============================================
print("\n" + "="*70)
print("✅ KENYAN LEGAL ASSISTANT IS READY!")
print("="*70)
print("\n📋 You can ask questions about:")
print("   • Constitutional rights (arrest, speech, voting, land)")
print("   • Employment (leave, termination, maternity, wages)")
print("   • Children (custody, maintenance, parental responsibility)")
print("   • Sexual offences (defilement, rape, consent)")
print("   • Data protection (privacy, personal information)")
print("\n" + "="*70 + "\n")

# ============================================
# CHAT LOOP
# ============================================
while True:
    question = input("👤 You: ")
    
    if question.lower() in ['exit', 'quit', 'bye']:
        print("\n🤝 Know your rights, know the law! Goodbye.\n")
        break
    
    if not question.strip():
        continue
    
    print("\n🤔 Searching Kenyan law...")
    
    try:
        result = qa_chain.invoke({"query": question})
        print(f"\n⚖️ Bot: {result['result']}\n")
    except Exception as e:
        print(f"\n⚠️ Error: {e}")
        print("   Please try again.\n")
    
    print("-"*70)