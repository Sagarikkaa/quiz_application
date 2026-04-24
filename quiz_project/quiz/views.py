from django.shortcuts import render
from .services.quiz_generator import generate_mcq
from docx import Document
import PyPDF2
import requests
from bs4 import BeautifulSoup


def _extract_text_from_file(uploaded_file):
    name = uploaded_file.name.lower()
    if name.endswith(".txt"):
        return uploaded_file.read().decode("utf-8", errors="ignore")
    elif name.endswith(".docx"):
        doc = Document(uploaded_file)
        return "\n".join(para.text for para in doc.paragraphs)
    elif name.endswith(".pdf"):
        reader = PyPDF2.PdfReader(uploaded_file)
        text = []
        for page in reader.pages:
            text.append(page.extract_text() or "")
        return "\n".join(text)
    else:
        return ""


def _extract_text_from_url(url):
    if not url:
        return ""
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(url, headers=headers, timeout=8)
    resp.raise_for_status()
    html = resp.text
    soup = BeautifulSoup(html, "html.parser")
    for s in soup(["script", "style", "noscript"]):
        s.decompose()
    return "\n".join([p.get_text(" ", strip=True) for p in soup.find_all("p")])


def quiz_view(request):
    if request.method == "POST":
        action = request.POST.get("action", "generate")

        if action == "submit_quiz":
            question_count = int(request.POST.get("question_count", 0))
            results = []
            correct_count = 0
            questions = []

            for i in range(question_count):
                q_text = request.POST.get(f"question_{i}", "")
                correct_answer = request.POST.get(f"correct_{i}", "")
                selected_answer = request.POST.get(f"answer_{i}", "")
                options = request.POST.getlist(f"options_{i}")
                is_correct = selected_answer == correct_answer
                if is_correct:
                    correct_count += 1
                questions.append({
                    "question": q_text,
                    "options": options,
                    "answer": correct_answer,
                })
                results.append({
                    "question": q_text,
                    "selected": selected_answer,
                    "correct": correct_answer,
                    "is_correct": is_correct,
                })

            return render(request, "home.html", {
                "questions": questions,
                "results": results,
                "score_text": f"You got {correct_count}/{question_count} correct.",
            })

        input_mode = request.POST.get("input_mode", "file")
        text = ""
        error = None

        if input_mode == "file":
            uploaded_file = request.FILES.get("content_file")
            if not uploaded_file:
                error = "Please upload a file."
            else:
                try:
                    text = _extract_text_from_file(uploaded_file)
                except Exception:
                    error = "Could not read uploaded file. Supported: .txt, .docx, .pdf"
        elif input_mode == "text":
            text = request.POST.get("content_text", "")
            if not text.strip():
                error = "Please enter text content."
        elif input_mode == "link":
            link = request.POST.get("content_link", "").strip()
            if not link:
                error = "Please enter a link."
            else:
                try:
                    text = _extract_text_from_url(link)
                except Exception:
                    error = "Could not fetch text from link. Please provide a valid URL."
        else:
            error = "Unknown input mode."

        if error:
            return render(request, "home.html", {"error": error})

        num_questions = 5
        try:
            num_questions = int(request.POST.get("num_questions", 5))
            num_questions = max(1, min(num_questions, 15))
        except ValueError:
            num_questions = 5

        questions = generate_mcq(text, num_questions=num_questions)
        return render(request, "home.html", {"questions": questions})

    return render(request, "home.html")