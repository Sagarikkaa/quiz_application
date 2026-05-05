import re
import random


def generate_mcq(content, num_questions=5):

    num_questions = max(1, min(15, num_questions))

    if not content or not content.strip():
        return [{"question": "No valid content found", "options": [], "answer": ""}]

    text = re.sub(r"\s+", " ", content.strip())

    if len(text) < 40:
        return [{"question": "Input content is too short to generate MCQs.", "options": [], "answer": ""}]

    # Split text into sentences
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if len(s.strip()) > 30]

    facts = []

    # Extract facts like "X is Y"
    for s in sentences:

        matches = re.findall(r"([A-Za-z ]{3,})\s+is\s+(?:an?|the)?\s*([A-Za-z ]{3,})", s)

        for m in matches:

            subject = m[0].strip().strip(".,")
            predicate = m[1].strip().strip(".,")

            if len(subject) > 2 and len(predicate) > 2:
                facts.append((subject, predicate))

    if not facts:
        return [{
            "question": "No clear factual statements found in content.",
            "options": [],
            "answer": ""
        }]

    # Vocabulary pool for distractors
    tokens = list(set(re.findall(r"\b[A-Za-z]{5,}\b", text)))

    questions = []
    used_subjects = set()

    for subject, predicate in facts:

        if len(questions) >= num_questions:
            break

        if subject in used_subjects:
            continue

        used_subjects.add(subject)

        correct = predicate

        # Generate distractors
        distractors = set()

        attempts = 0
        while len(distractors) < 3 and attempts < 20 and tokens:

            choice = random.choice(tokens)

            if choice.lower() != correct.lower() and choice.lower() not in subject.lower():
                distractors.add(choice)

            attempts += 1

        options = list(distractors)
        options.append(correct)

        # Ensure exactly 4 options
        while len(options) < 4:
            options.append("None of the above")

        options = options[:4]

        random.shuffle(options)

        question_text = f"What is {subject}?"

        questions.append({
            "question": question_text,
            "options": options,
            "answer": correct
        })

    if not questions:
        return [{
            "question": "Could not generate questions from provided content.",
            "options": [],
            "answer": ""
        }]

    return questions