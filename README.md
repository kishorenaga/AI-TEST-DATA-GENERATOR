# AI Test Data Generator

This project demonstrates how to generate **valid and invalid test JSON data** from a **GraphQL schema** and **validation rules** using a locally running **Llama 3** model.

## 📂 Project Structure

```
ai-test-data-generator/
│── schema.graphql     # Example GraphQL schema
│── rules.txt          # Validation rules in text format
│── config.json        # LLM configuration (endpoint, model, temperature)
│── main.py            # Main script to run the generator
│── check_consistency.py # Script to check schema vs rules consistency
│── outputs/           # Generated JSON data will be saved here
```

## ⚙️ Prerequisites

- Python 3.9+
- [Requests library](https://docs.python-requests.org/en/master/)
- [graphql-core](https://github.com/graphql-python/graphql-core) (for consistency check)
- A locally running **Llama 3** server (e.g., via [Ollama](https://ollama.ai/) or [llama.cpp](https://github.com/ggerganov/llama.cpp))

Example for starting with **Ollama**:

```bash
ollama run llama3
```

## 🛠️ Setup

1. Clone or unzip this project:

```bash
unzip ai-test-data-generator.zip
cd ai-test-data-generator
```

2. Install dependencies:

```bash
pip install requests graphql-core
```

3. Adjust `config.json` if needed:

```json
{
  "api_url": "http://localhost:11434/v1/chat/completions",
  "model": "llama3",
  "temperature": 0.2
}
```

## ▶️ Run

```bash
python3 main.py --schema schema.graphql --rules rules.txt --config config.json --out outputs/
```

- ✅ `outputs/valid.json` → data following rules
- ❌ `outputs/invalid.json` → data violating rules

## 🔎 Consistency Check

To check for mismatches between schema and validation rules:

```bash
python check_consistency.py
```

This will report:
- Fields missing in rules
- Fields in rules but not in schema

## 🔧 Customization

- Replace **`schema.graphql`** with your own GraphQL schema.
- Replace **`rules.txt`** with your own validation rules in text format.
- Update **`config.json`** to point to your local LLM server.

---

🚀 Happy testing!
