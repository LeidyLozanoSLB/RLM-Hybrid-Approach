import os
import json
from dotenv import load_dotenv
from rlm import RLM
from rlm.logger import RLMLogger
from pathlib import Path

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
source_file = BASE_DIR.parent / "data" / "concatenated_docs.txt"
input_json = BASE_DIR.parent / "data" / "benchmark_answers.json"
output_json = BASE_DIR.parent / "data" / "benchmark_answers_complete_rlm.json"

def sanitize_for_cp1252(text: str) -> str:
    return text.encode("cp1252", errors="ignore").decode("cp1252")


def build_input(query: str, context: str) -> str:
    return f"""# USER QUERY
{query}

# CONTEXT - Do not read all at once.
{context}
"""


def main():


    # Load context once
    with open(source_file, "r", encoding="utf-8") as f:
        context = f.read()

    # Load JSON dataset
    with open(input_json, "r", encoding="utf-8") as f:
        data = json.load(f)

    logger = RLMLogger(log_dir="./logs")

    rlm = RLM(
        backend="azure_openai",
        backend_kwargs={
            "model_name": "gpt-4o-2-gb",
            "api_key": os.getenv("OPENAI_API_KEY"),
        },
        environment="local",
        environment_kwargs={},
        max_depth=1,
        logger=logger,
        verbose=False,
    )

    # Process each question
    for item in data:
        query = item.get("question", "").strip()

        if not query:
            item["RLM_answer"] = ""
            continue

        combined_input = build_input(query, context)
        combined_input = sanitize_for_cp1252(combined_input)

        print(f"Processing question_id={item.get('question_id')}...")

        try:
            result = rlm.completion(combined_input)
            item["RLM_answer"] = result.response
        except Exception as e:
            item["RLM_answer"] = f"ERROR: {str(e)}"

    # Save updated JSON
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"\n Results saved to {output_json}")


if __name__ == "__main__":
    main()