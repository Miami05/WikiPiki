import json
from textwrap import dedent

from dotenv import load_dotenv
from openai import OpenAI

# Load variables from .env into environment
load_dotenv()

# Create client (automatically picks up key from env)
client = OpenAI()


def build_prompt(summary, n):
    return dedent(f"""\
                You are a quiz generator for a CLI game.

                TASK
                - Create EXACTLY {n} questions based ONLY on the ARTICLE SUMMARY provided below.
                - Use a RANDOM mix of formats for variety. Allowed formats (value for "question_format"):
                  1) "multiple" — classic multiple choice question.
                  2) "fill_blank" — sentence with ONE blank "____"; the correct option completes the sentence.
                  3) "true_false" — a plain True/False style question with options a–d.
                  4) "riddle" — a clue-style riddle; players must infer the answer.
                  5) "scenario" — a mini-situation or roleplay; ask what happens or what the person should do.
                  6) "combo_multiple" — meta-question: list [A]–[D] claims inside the question; options a–d are combinations like "A and D", "B only", "A, B and D". Exactly one option matches the true subset.

                STRICT RULES
                - The output MUST be a JSON array of objects.
                - Each object MUST have EXACTLY these keys:
                  - "question": string
                  - "options": object with string keys "a", "b", "c", "d"
                  - "answer": one of "a", "b", "c", "d"
                  - "difficulty": one of "easy", "medium", "hard"
                  - "question_format": one of "multiple", "fill_blank", "true_false", "riddle", "scenario", "combo_multiple"
                - No extra keys. No markdown, no prose outside the JSON.
                - Use ONLY facts present or directly implied in the summary. No outside knowledge.
                - Options "a"–"d" must be plausible; exactly one is correct and matches "answer".
                - Keep questions concise and unambiguous. Avoid duplicates.

                DIFFICULTY DISTRIBUTION & ORDER
                - Make the distribution as equal as possible across easy, medium, hard:
                  • Let base = floor({n}/3). Set E = M = H = base.
                  • Let r = {n} - (E + M + H). Distribute the remaining r by adding +1 to Easy, then Medium, then Hard (in that order) until r=0.
                  • Output order MUST BE grouped by difficulty: all easy first, then all medium, then all hard.
                  • Within each difficulty group, question formats should appear RANDOMLY, not in a fixed sequence.
                - HARD must be genuinely hard:
                  • Require combining 2+ facts from the summary OR multi-step elimination.
                  • Distractors are near-miss options (subtle wording, closely related terms).
                  • Avoid trivial giveaways. No “All of the above”/“None of the above”.

                FILL-IN-THE-BLANK (for "fill_blank")
                - Use exactly one blank "____" in the sentence.
                - Each option should be a feasible completion; only one correct.

                TRUE/FALSE (for "true_false")
                - A plain True/False style question.
                - Always provide 2 options, phrased plausibly (e.g., "True", "False").
                - Exactly one is correct.

                RIDDLE (for "riddle")
                - Phrase the question as a short clue or riddle about something in the summary.
                - Options should be four possible answers; only one is correct.

                SCENARIO (for "scenario")
                - Describe a short situation or roleplay based on the summary.
                - Ask what happens next, or what the character should do according to the article.
                - Provide four plausible choices; exactly one is correct.

                COMBO MULTIPLE (for "combo_multiple")
                - Inside "question", FIRST list four mini-claims labelled [A], [B], [C], [D], each on its own line, based ONLY on the summary.
                - Then ask: "Which combination is correct?"
                - The four options (a–d) are combinations such as:
                  • "A and D" • "B only" • "B and C" • "A, B and D"
                - Exactly ONE option reflects the true subset of correct claims; set "answer" to that option's key.
                - Include at least one tricky false combination that is close to correct but off by one element.

                FORMAT MIX
                - If {n} >= 3, include at least TWO different "question_format" values.
                - If {n} >= 6, include at least one of EACH: "fill_blank", "true_false", "riddle", "scenario", and "combo_multiple".

                ARTICLE SUMMARY:
                \"\"\"{summary}\"\"\"
            """)



def ask_chatgpt(content, stream=False, max_tokens=1000):
    if stream:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": content}],
            max_tokens=max_tokens,
            stream=True,
            temperature=0.2,
        )
        chunks = []
        for event in response:
            if "choices" in event and len(event.choices) > 0:
                delta = event.choices[0].delta.get("content")
                if delta:
                    chunks.append(delta)

        full_response = "".join(chunks)

    else:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": content}],
            max_tokens=max_tokens,
        )
        full_response = response.choices[0].message.content


    try:
        return json.loads(full_response)
    except Exception as e:
        print("⚠️ JSON parsing failed:", e)
        print("Raw output:\n", full_response)
        return []



def make_questions(article, number):
    content = build_prompt(article, number)
    questions = ask_chatgpt(content)
    return questions
