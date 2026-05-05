# AI-Powered Quiz Generator

This project is an intelligent quiz generation system that creates multiple-choice questions (MCQs) from various input sources including plain text, web links, and PDF documents. It leverages AI to analyze content and generate meaningful, context-aware questions based on user requirements.

## 🚀 Features
- 📄 Accepts multiple input formats:
  - Raw text
  - URLs (web content)
  - PDF documents
- 🤖 AI-based MCQ generation
- 🎯 Customizable quiz generation (number of questions, difficulty level)
- ✅ Automatically generated options with correct answers
- 👤 User-friendly interface
- 🔐 Admin & user role support (optional)

## 🛠️ Tech Stack
- Backend: Python, Django
- Frontend: HTML, CSS, JavaScript
- AI Integration: Gemini API / NLP models
- File Handling: PDF parsing libraries (PyPDF / pdfplumber)
- Web Scraping: BeautifulSoup / Requests
- Database: SQLite / PostgreSQL

## 💡 How It Works
1. User provides input (text, link, or PDF)
2. System extracts and processes the content
3. AI model analyzes the content
4. Relevant MCQs are generated with options and answers
5. Quiz is displayed or stored for later use

