import os
import json
import numpy as np
import requests
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

cwd = os.getcwd()
chunks_file = os.path.join(cwd,"processed","chunks.json")
embeddings_file = os.path.join(cwd,"processed","embeddings.npy")

# Load environment variable
API_KEY = os.getenv("OPENROUTER_API_KEY")
if not API_KEY:
    raise ValueError("API key not set. Please set OPENROUTER_API_KEY environment variable.")

# Load preprocessed data : chunks
with open(chunks_file, "r", encoding="utf-8") as f:
    chunks = json.load(f)

# Load preprocessed data : embeddings (vector space of chunks)
embeddings = np.load(embeddings_file)

# Load sentence transformer model : to transform user query to embedding
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Function to retrieve relevant chunks - based on cosine similarity between vector space of prompt and chunk
def retrieve_relevant_chunks(user_input, top_k=3):
    query_embedding = model.encode([user_input])
    similarities = cosine_similarity(query_embedding, embeddings)[0]
    top_indices = similarities.argsort()[::-1][:top_k]
    top_chunks = [chunks[i] for i in top_indices]
    return "\n\n".join(top_chunks)

# Initial payload with system message
payload = {
    "model": "deepseek/deepseek-chat-v3-0324:free",
    "messages": [
        {"role": "system", "content": "You are a helpful assistant. Use the provided context if available to answer questions accurately."},
    ]
}

# Start chatbot loop
while True:

    #User can enter input
    user_input = input("([quit/exit] to quit) You: ")
    if user_input.lower() in ["exit", "quit"]:
        break

    # Retrieve relevant context based on cosine similarity between user input and chunks 
    context = retrieve_relevant_chunks(user_input)

    # Format user message with context
    full_prompt = f"""Use the following context to answer the question:\n\n{context}\n\nQuestion: {user_input}"""
    payload["messages"].append({"role": "user", "content": full_prompt})

    # Send request to OpenRouter
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        },
        data=json.dumps(payload)
    )

    if response.status_code == 200:
        reply = response.json()["choices"][0]["message"]["content"]
        print("Chimera:", reply)
        payload["messages"].append({"role": "assistant", "content": reply})
    else:
        print("Error:", response.status_code)
        print(response.text)
