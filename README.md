# 🧠 RAG-based Chatbot using OpenRouter and DeepSeek

This project demonstrates a simple Retrieval-Augmented Generation (RAG) chatbot using the [DeepSeek V3 0324 (free)](https://openrouter.ai/tngtech/deepseek-r1t2-chimera:free) LLM model via [OpenRouter](https://openrouter.ai). The chatbot can answer queries based on a dataset (e.g., FAQ or instruction manual) using semantic search and context-aware generation.

---

## ✅ Prerequisites

- Python 3.8 or later
- Windows (commands provided are for Windows; minor adjustments may be needed for macOS/Linux)

---

## 🚀 Setup Instructions

### 🔑 Step 1: Get OpenRouter API Key

1. Go to [https://openrouter.ai/settings/keys](https://openrouter.ai/settings/keys)
2. Click **Create Key**
3. Copy and **save your key** securely — you can only view it once.

---

### ⚙️ Step 2: Set Environment Variable

In **VSCode terminal**, run:

```powershell
$env:OPENROUTER_API_KEY = "<your_openrouter_api_key>"
```

---

### 📦 Step 3: Install Dependencies

Install required libraries using:

```bash
pip install -r requirements.txt
```

---

### 🧹 Step 4: Preprocess the Dataset

The dataset is stored at: `data/dataset.txt`  
(Source: [reichenbch/RAG-examples](https://github.com/reichenbch/RAG-examples/blob/main/dataset.txt))

Run the following script to process the data:

```bash
python preprocess_dataset.py
```

This script will:

- Parse the dataset
- Split it into meaningful text chunks
- Generate semantic embeddings (vector space)
- Save the output in the `processed/` directory:
  - `chunks.json` – JSON file with chunked dataset
  - `embeddings.npy` – NumPy file containing vector embeddings

---

### 💬 Step 5: Run the Chatbot

Start the chatbot using:

```bash
python chatbot.py
```

Ask questions related to the dataset (e.g., PAN card info). The chatbot uses the RAG approach to find relevant chunks and provides informed responses.

---

## 🧪 Sample Prompts

You can try questions like:

- ✅ `How can I get a PAN card?`
- ✅ `What is a PAN card?`
- ❌ `Is Germany in Europe?`
  > Will be flagged as _out of context_ (since it’s unrelated to the dataset)

---

## 📌 Notes

- You can swap out the model by modifying the `model` field in `chatbot.py`
- The output quality depends on the LLM used — you're currently using `DeepSeek V3 0324 (free)`
