import os
import git
import glob
import faiss
import numpy as np
import requests
import re
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv


load_dotenv()
HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")


def query(payload):
    API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3"
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"}
    response = requests.post(API_URL, headers=headers, json=payload) 
    return response.json()


def get_repo_name(repo_url):
    return repo_url.split("/")[-1].replace(".git", "")


def clone_repo_if_needed(repo_url, base_dir="repos"):
    repo_name = get_repo_name(repo_url)
    local_dir = os.path.join(base_dir, repo_name)

    if os.path.exists(local_dir):
        print(f"Repo '{repo_name}' already cloned.")
        return None, repo_name  
    else:
        print(f"Cloning repo: {repo_url} ...")
        git.Repo.clone_from(repo_url, local_dir)
        return local_dir, repo_name


def get_code_files(repo_path, extensions=[".py", ".java", ".js", ".cpp", ".html"]):
    code_files = []
    for ext in extensions:
        code_files.extend(glob.glob(f"{repo_path}/**/*{ext}", recursive=True))
    return code_files


def chunk_code(code, chunk_size=256, overlap=50):
    chunks = []
    pattern = re.compile(r"(class\s+\w+\s*\(.*?\):|def\s+\w+\s*\(.*?\):)", re.MULTILINE)
    matches = list(pattern.finditer(code))

    prev_end = 0
    for match in matches:
        start = match.start()
        if start > prev_end:
            chunks.append(code[prev_end:start].strip())

        end = start
        while end < len(code) and code[end] != '\n':
            end += 1
        while end < len(code) and (code[end] == '\n' or code[end] == ' '):
            end += 1
        
        next_match = pattern.search(code, end)
        if next_match:
            end = next_match.start()

        chunks.append(code[start:end].strip())
        prev_end = end

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=overlap)
    remaining_text = code[prev_end:].strip()
    if remaining_text:
        chunks.extend(text_splitter.split_text(remaining_text))

    return chunks


def embed_chunks(chunks, model_name="all-MiniLM-L6-v2"):
    if not chunks:
        print("Error: No code chunks to embed")
        return np.array([])
    model = SentenceTransformer(model_name)
    vectors = model.encode(chunks)
    return np.array(vectors, dtype=np.float32)


def store_vectors(vectors, repo_name, index_dir="faiss_indexes"):
    os.makedirs(index_dir, exist_ok=True)
    index_path = os.path.join(index_dir, f"{repo_name}.index")

    if vectors is None or len(vectors) == 0:
        print("Error: No vectors found")
        return
    print(f"vectors shape: {vectors.shape}")

    dimension = vectors.shape[1]
    num_vectors = len(vectors)
    if len(vectors) <1000:
        index = faiss.IndexFlatL2(dimension)
    else:
        num_clusters = min(100, num_vectors)
        quantizer = faiss.IndexFlatL2(dimension)
        index = faiss.IndexIVFFlat(quantizer, dimension, num_clusters)
        if num_vectors >= num_clusters:
            index.train(vectors)
        else:
            index = faiss.IndexFlatL2(dimension)

    # if use_hnsw:
    #     index = faiss.IndexHNSWFlat(dimension, 32)  
    # else:
    #     index = faiss.IndexFlatL2(dimension)  

    index.add(vectors)
    faiss.write_index(index, index_path)

    print(f"Stored {len(vectors)} vectors in {index_path}")


def load_faiss_index(repo_name, index_dir="faiss_indexes"):
    index_path = os.path.join(index_dir, f"{repo_name}.index")
    if not os.path.exists(index_path):
        print(f"FAISS index for {repo_name} not found!")
        return None
    index = faiss.read_index(index_path)
    print(f"Loaded FAISS index for {repo_name}")
    return index


def reconstruct_code_from_vectors(index, stored_chunks):
    if index is None or index.ntotal == 0:
        print("No vectors found in FAISS index.")
        return ""

    print("Reconstructing code from stored vectors...")
    return "\n".join(stored_chunks)


def generate_code_review(reconstructed_code):
    if not reconstructed_code:
        print("No code found for analysis.")
        return "No code found for analysis."

    system_prompt = """
    You are an expert code reviewer. Analyze the provided code and provide a structured review.
    
    **Review Guidelines:**
    - Identify **only real issues** (syntax errors, security vulnerabilities, bad practices).
    - **Highlight maintainability and readability** improvements.
    - Provide **clear and concise** suggestions.
    - **Avoid unnecessary changes** (changing working code for no reason).
    
    **Review Structure:**
    1. **Correctness Assessment**
    2. **Optimization Suggestions**
    3. **Best Practices Check**
    4. **Security Analysis**
    5. **Optimized Version (if needed)**

    DO NOT INCLUDE ANYTHING IN THE RESPOSE. ONLY RETURN THE STRUCTURED REVIEW. ADD THE OPTIMIZED CODE ALSO.
    """

    chunk_size = 10000
    # chunks = chunk_code(reconstructed_code, chunk_size=chunk_size, overlap=5000)
    chunks = [reconstructed_code[i:i+chunk_size] for i in range(0, len(reconstructed_code), chunk_size)]

    full_review = []
    for i, chunk in enumerate(chunks):
        print(f"Processing chunk {i+1}/{len(chunks)}...")
        prompt = f"{system_prompt}\n\nCode to review:\n{chunk}"
        response = query({
            "inputs": prompt,
            "parameters": {"max_new_tokens": 10000, "return_full_text": False, "temperature": 0.3}
        })

        # print(f"API Response for chunk {i+1}: {response}")


    


    #     if isinstance(response, list) and len(response) > 0 and "generated_text" in response[0]:
    #         review_text = response[0]["generated_text"].strip()
    #         print(f" Extracted Review Text for chunk {i+1}:\n{review_text}\n")  # Debugging print

    #         if review_text:
    #             full_review.append(review_text)
    #         else:
    #             print(" Warning: API returned an empty response for this chunk.")
    #     else:
    #         print("Warning: API response format is incorrect or empty.")

    # final_review = "\n\n".join(full_review)

    # if not final_review.strip():
    #     print(" Error: Generated report is empty. Skipping file save.")
    
    # return final_review

        
        if response and isinstance(response, list) and 'generated_text' in response[0]:
            full_review.append(response[0]['generated_text'].strip())

    return "\n\n".join(full_review)


def save_review_report(repo_name, report_text, report_dir="reports"):
    os.makedirs(report_dir, exist_ok=True)
    report_path = os.path.join(report_dir, f"{repo_name}_review.txt")

    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_text)

    print(f"Review report saved: {report_path}")
# def save_review_report(repo_name, report_text, report_dir="reports"):
#     os.makedirs(report_dir, exist_ok=True)
#     report_path = os.path.join(report_dir, f"{repo_name}_review.txt")

#     print(f"Report Content Before Saving (First 500 chars): {report_text[:500]}")  # Debugging print

#     if not report_text.strip():
#         print("Error: Generated report is empty. Skipping file save.")
#         return  

#     try:
#         with open(report_path, "w", encoding="utf-8") as f:
#             f.write(report_text)
#         print(f"Review report saved: {report_path}")
#     except Exception as e:
#         print(f"File Write Error: {e}")


if __name__ == "__main__":
    repo_url = input("Enter GitHub repo URL:").strip()

    local_repo_path, repo_name = clone_repo_if_needed(repo_url)

    if local_repo_path is not None:
        code_files = get_code_files(local_repo_path)

        all_chunks = []
        for file in code_files:
            with open(file, "r", encoding="utf-8", errors="ignore") as f:
                code = f.read()
                chunks = chunk_code(code)
                all_chunks.extend(chunks)
        vectors = embed_chunks(all_chunks)
        store_vectors(vectors, repo_name)

    index = load_faiss_index(repo_name)
    reconstructed_code = reconstruct_code_from_vectors(index, all_chunks)
    review_report = generate_code_review(reconstructed_code)
    save_review_report(repo_name, review_report)

    print("Code review completed!")
