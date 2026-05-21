# constitution_rag.py
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_classic.chains import RetrievalQA
from langchain_community.llms import HuggingFacePipeline
from transformers import pipeline
import os

print("📚 Loading the Kenyan Constitution...")

# Step 1: Load the PDF
loader = PyPDFLoader("The Constitution of Kenya.pdf")
documents = loader.load()
print(f"✅ Loaded {len(documents)} pages")

# Step 2: Split into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    separators=["\nArticle ", "\nSection ", "\nChapter ", "\n\n", " "]
)
chunks = text_splitter.split_documents(documents)
print(f"✅ Created {len(chunks)} text chunks")

print("🔢 Creating embeddings (this may take 2-3 minutes)...")

# Step 3: Create embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Step 4: Build FAISS vector database
vectorstore = FAISS.from_documents(chunks, embeddings)
print("✅ Vector database created!")

# Step 5: Save it for later use
vectorstore.save_local("constitution_vectorstore")
print("💾 Vector database saved to 'constitution_vectorstore' folder")

# Step 6: Load a small LLM
print("🤖 Loading LLM (this will take a moment)...")
llm_pipeline = pipeline(
    "text-generation",  # ✅ FIXED: Changed from "text2text-generation"
    model="google/flan-t5-small",
    max_length=200
)
llm = HuggingFacePipeline(pipeline=llm_pipeline)

# Step 7: Create the QA chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever(search_kwargs={"k": 3})
)

print("\n" + "="*50)
print("✅ KENYAN CONSTITUTION BOT IS READY!")
print("="*50 + "\n")

# Step 8: Interactive Q&A loop
while True:
    question = input("\n🔍 Ask about the Constitution (or type 'exit' to quit): ")
    if question.lower() == 'exit':
        break
    
    print("🤔 Thinking...")
    answer = qa_chain.run(question)
    print(f"\n⚖️ ANSWER: {answer}\n")
    print("-"*50)