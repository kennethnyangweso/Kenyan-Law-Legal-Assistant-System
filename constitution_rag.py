# constitution_plain_language_bot.py
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain_classic.chains import RetrievalQA

print("📚 Loading Kenyan Constitution...")

# Load the Constitution
loader = PyPDFLoader("The Constitution of Kenya.pdf")
documents = loader.load()
print(f"✅ Loaded {len(documents)} pages")

# Split into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    separators=["\nArticle ", "\nSection ", "\nChapter ", "\n\n"]
)
chunks = text_splitter.split_documents(documents)
print(f"✅ Created {len(chunks)} text chunks")

# Create vector search
print("🔢 Creating search index...")
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectorstore = FAISS.from_documents(chunks, embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

# Your Groq API key
GROQ_API_KEY = "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"  # 🔑 Paste your key here!

# Use Llama 3.1 (excellent for plain language)
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.4,
    groq_api_key=GROQ_API_KEY
)

# The magic is in this prompt - it forces plain language answers
plain_language_prompt = PromptTemplate(
    template="""You are a Kenyan human rights educator explaining the Constitution to ordinary citizens.

Here are the relevant sections from the Constitution of Kenya:
{context}

The citizen asks: {question}

IMPORTANT INSTRUCTIONS:
1. DO NOT quote or copy the Constitution directly
2. Write in simple, everyday language like you're explaining to a friend
3. Use bullet points (•) for listing rights
4. Make it practical and helpful - tell them what this means for them
5. Write 3-8 sentences total
6. If something isn't in the Constitution, just say so

EXAMPLE of good answer format:
"In Kenya, when you are arrested, you have several important rights. First, police must tell you why you're being arrested in a language you understand. You also have the right to remain silent and talk to a lawyer before answering questions. Police must bring you to court within 24 hours, and you can apply for bail in most cases."

Now write a clear, practical answer:""",
    input_variables=["context", "question"]
)

# Create the chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    chain_type_kwargs={"prompt": plain_language_prompt}
)

print("\n" + "="*70)
print("🇰🇪 KENYAN CONSTITUTION BOT - KNOW YOUR RIGHTS")
print("="*70)
print("\nExamples of what you can ask:")
print("• What rights do I have if I'm arrested?")
print("• Can the government take my land?")
print("• What are my voting rights?")
print("• Can I protest peacefully?")
print("\n" + "="*70 + "\n")

while True:
    question = input("👤 Citizen: ")
    if question.lower() in ['exit', 'quit']:
        print("\n🤝 Remember: Knowledge of your rights is power! Goodbye.")
        break
    
    print("🤔 Finding your rights in the Constitution...")
    result = qa_chain.invoke({"query": question})
    print(f"\n🗣️ Bot: {result['result']}\n")
    print("-"*70)