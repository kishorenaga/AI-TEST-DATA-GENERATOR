import json
import requests
import argparse
from pathlib import Path

def load_file(path):
    return Path(path).read_text()

def call_llm(api_url, model, prompt, temperature=0.2):
    headers = {"Content-Type": "application/json"}
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are an expert test data generator."},
            {"role": "user", "content": prompt}
        ],
        "temperature": temperature
    }
    resp = requests.post(api_url, headers=headers, data=json.dumps(payload))
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]

def build_prompt(schema, rules):
    return f"""
You are an expert test data generator.

Your task:
1. Read the GraphQL schema.
2. Read the validation rules.
3. Generate two sets of JSON:
   - ValidData (follows rules)
   - InvalidData (violates rules)

Output strictly as JSON with this format:
{{
  "ValidData": {{ ... }},
  "InvalidData": {{ ... }}
}}

Schema:
<<<
{schema}
>>>

Validation Rules:
<<<
{rules}
>>>
"""

def main(schema_path, rules_path, config_path, out_dir):
    schema = load_file(schema_path)
    rules = load_file(rules_path)
    config = json.loads(load_file(config_path))

    prompt = build_prompt(schema, rules)

    result = call_llm(
        config["api_url"],
        config["model"],
        prompt,
        config.get("temperature", 0.2)
    )

    try:
        parsed = json.loads(result)
    except json.JSONDecodeError:
        print("❌ LLM returned invalid JSON, please check output:")
        print(result)
        return

    Path(out_dir).mkdir(exist_ok=True)
    (Path(out_dir) / "valid.json").write_text(json.dumps(parsed.get("ValidData", {}), indent=2))
    (Path(out_dir) / "invalid.json").write_text(json.dumps(parsed.get("InvalidData", {}), indent=2))
    print("✅ Generated test data saved in", out_dir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--schema", default="schema.graphql", help="Path to GraphQL schema file")
    parser.add_argument("--rules", default="rules.txt", help="Path to validation rules text file")
    parser.add_argument("--config", default="config.json", help="Path to config file")
    parser.add_argument("--out", default="outputs", help="Directory to save outputs")
    args = parser.parse_args()
    main(args.schema, args.rules, args.config, args.out)
