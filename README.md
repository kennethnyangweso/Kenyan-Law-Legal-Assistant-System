# 🇰🇪 Kenyan Legal Assistant - AI-Powered Legal Q&A System

<div align="center">
  <img src="https://upload.wikimedia.org/wikipedia/commons/e/e8/Coat_of_arms_of_Kenya.svg" alt="Kenya Coat of Arms" width="120">
  <h3>Know Your Rights | Understand the Law</h3>
  <p>An AI-powered RAG system that answers questions about Kenyan law in plain language</p>
</div>

---

## 📋 Project Overview

The **Kenyan Legal Assistant** is a Retrieval-Augmented Generation (RAG) system that helps Kenyan citizens understand their legal rights and obligations in simple, everyday language. Instead of navigating complex legal documents, users can ask natural language questions and receive clear, actionable answers sourced directly from Kenyan law.

**Live Demo:** [https://kenyan-legal-assistant.onrender.com](https://kenyan-legal-assistant.onrender.com)

### Key Features

| Feature | Description |
|---------|-------------|
| 🔍 **RAG Architecture** | Retrieves relevant legal text from official Kenyan documents |
| 🗣️ **Plain Language Answers** | No legal jargon - explanations anyone can understand |
| ⚖️ **5 Major Laws** | Constitution, Employment Act, Children Act, Sexual Offences Act, Data Protection Act |
| 💬 **Chat Interface** | User-friendly web interface with conversation history |
| 🔗 **Source Attribution** | Answers include which law they come from |
| 📱 **Responsive Design** | Works on desktop, tablet, and mobile devices |

---

## 📊 Business Understanding

### The Problem

Modern businesses and citizens face several challenges when trying to understand Kenyan law:

| Challenge | Impact |
|-----------|--------|
| **Complex Legal Language** | Ordinary citizens cannot understand legal terminology |
| **Document Volume** | The Constitution alone has 187+ pages across multiple documents |
| **Scattered Information** | Laws are distributed across multiple PDFs and websites |
| **Legal Consultation Costs** | Hiring a lawyer is expensive for routine questions |
| **Time Constraints** | Manually searching through legal documents is time-consuming |

### The Solution

The Kenyan Legal Assistant addresses these challenges by providing:

- **Instant answers** to legal questions
- **Plain language** explanations of complex legal concepts
- **Free access** to legal information for all Kenyans
- **Accurate citations** from official legal documents
- **24/7 availability** without appointment or cost

---

## ❓ Problem Statement

How might we build an accessible, accurate, and easy-to-use legal information system that helps Kenyan citizens understand their legal rights and obligations without requiring legal expertise or expensive consultations?

### Key Challenges Addressed

1. **Intent Detection**: Accurately identifying what legal area the user is asking about
2. **Response Generation**: Producing coherent, helpful, and legally accurate responses
3. **Knowledge Integration**: Combining information from multiple legal documents
4. **Accessibility**: Making the system available to users with varying technical literacy
5. **Resource Constraints**: Running on limited hardware without expensive GPUs

---

## 🎯 Objectives

### Primary Objectives

| # | Objective | Status |
|---|-----------|--------|
| 1 | Develop a chatbot capable of answering legal questions about Kenyan law | ✅ Achieved |
| 2 | Implement RAG to retrieve relevant legal text from multiple documents | ✅ Achieved |
| 3 | Generate plain-language responses that ordinary citizens can understand | ✅ Achieved |
| 4 | Provide source attribution for all answers | ✅ Achieved |
| 5 | Deploy a publicly accessible web interface | ✅ Achieved |

### Secondary Objectives

- Handle questions across 5 major Kenyan laws
- Provide conversation history for context
- Ensure responses are legally accurate
- Make the system scalable for additional laws

---

## 📈 Metrics & Evaluation

### Performance Metrics

| Metric | Target | Achieved |
|--------|--------|----------|
| **Response Accuracy** | >85% relevant answers | ✅ Met |
| **Response Time** | <5 seconds | ✅ Met |
| **Plain Language Score** | 90% of responses jargon-free | ✅ Met |
| **Document Coverage** | 5 major laws | ✅ Met |
| **User Satisfaction** | Positive feedback | ✅ Met |

### Technical Metrics

| Component | Metric | Value |
|-----------|--------|-------|
| **Chunk Size** | Text split length | 1000 characters |
| **Retrieval k** | Documents retrieved per query | 4 |
| **Embedding Model** | all-MiniLM-L6-v2 | 384 dimensions |
| **LLM Model** | Groq Llama 3.1 | 8B parameters |

---

## 📚 The Data

### Document Sources

All documents are sourced from [Kenya Law](https://new.kenyalaw.org) - the official repository of Kenyan legal information.

| Document | Pages | Key Topics Covered |
|----------|-------|---------------------|
| **Constitution of Kenya (2010)** | 187 | Bill of Rights, governance, devolution, fundamental freedoms |
| **Employment Act (2007)** | 45 | Contracts, leave, termination, wages, child employment |
| **Children Act (2022)** | 32 | Child rights, custody, maintenance, adoption, foster care |
| **Sexual Offences Act (2006)** | 26 | Defilement, rape, consent, sexual assault |
| **Data Protection Act (2019)** | 30 | Privacy, data consent, personal information rights |

### Data Processing

<img width="788" height="2465" alt="deepseek_mermaid_20260603_4fd477" src="https://github.com/user-attachments/assets/c02a2a1d-7ad2-445f-ad5a-515de0be041a" />



