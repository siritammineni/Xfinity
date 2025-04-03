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
from langgraph.graph.state import StateGraph, START, END
from typing import TypedDict, List, Optional
from typing import List, Dict, Optional

load_dotenv()
HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")

ALLOWED_EXTENSIONS = {'py', '.java', '.js', '.cpp', '.html'}
BASE_DIR = "repos"
INDEX_DIR = "faiss_indexes"
REPORT_DIR = "reports"

os.makedirs(BASE_DIR, exist_ok=True)
os.makedirs(INDEX_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)

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

# Agents

class AgentState(TypedDict):
    code_chunks: List[str]
    optimized_code: Optional[str]
    review: Optional[str]

# Quality Analysis Agent
def quality_analysis_agent(state: AgentState):
    prompt = "Analyze the quality of the following code snippets and provide feedback: " + "\n".join(state["code_chunks"])
    response = query({"inputs": prompt})
    state["review"] = response[0].get("generated_text", "No feedback provided.")
    return state


# Auto Code Generator Agent
def auto_code_generator_agent(state: AgentState):
    prompt = "Improve and complete the following code snippets: " + "\n".join(state["code_chunks"])
    response = query({"inputs": prompt})
    state["optimized_code"] = response[0].get("generated_text", "No suggestions generated.")
    return state

# Code Optimizer Agent
def code_optimizer_agent(state: AgentState):
    prompt = "Optimize the following code for performance and readability: " + "\n".join(state["code_chunks"])
    response = query({"inputs": prompt})
    state["optimized_code"] = response[0].get("generated_text", "No optimization suggestions.")
    return state

# Code Review Phase
def code_review_phase(state: AgentState):
    prompt = f"Review the following code optimizations and provide a final report:\nIssues Found:\n{state.get('review','No issues found')}\nOptimized Code:\n{state.get('optimized_code','No Optimizations')}"
    response = query({"inputs": prompt})
    review_summary = response[0].get("generated_text", "No review generated.")
    with open(os.path.join(REPORT_DIR, "code_review_report.txt"), "w", encoding="utf-8") as f:
        f.write(review_summary)
    return state

# LangGraph Workflow
workflow = StateGraph(AgentState)
workflow.add_node("quality_analysis", quality_analysis_agent)
workflow.add_node("auto_code_gen", auto_code_generator_agent)
workflow.add_node("code_optimizer", code_optimizer_agent)
workflow.add_node("review_phase", code_review_phase)
# workflow.add_node({
#     "quality_analysis": quality_analysis_agent,
#     "auto_code_gen": auto_code_generator_agent,
#     "code_optimizer": code_optimizer_agent,
#     "review_phase": code_review_phase
# })
# workflow.set_entry_point("quality_analysis")
workflow.add_edge(START, "quality_analysis")
workflow.add_edge("quality_analysis", "auto_code_gen")
workflow.add_edge("auto_code_gen", "code_optimizer")
workflow.add_edge("code_optimizer", "review_phase")
workflow.add_edge("review_phase", END)

compiled_workflow = workflow.compile()

# Execution
def process_repository(repo_url):
    local_repo_path, repo_name = clone_repo_if_needed(repo_url)
    if local_repo_path is None:
        return
    code_files = get_code_files(local_repo_path)
    all_chunks = []
    for file in code_files:
        with open(file, "r", encoding="utf-8", errors="ignore") as f:
            all_chunks.extend(chunk_code(f.read()))
    vectors = embed_chunks(all_chunks)
    store_vectors(vectors, repo_name)
    index = load_faiss_index(repo_name)
    state = AgentState(code_chunks=all_chunks)
    final_state = compiled_workflow.invoke(state)
    print("Code review completed! Report saved.")

if __name__ == "__main__":
    repo_url = input("Enter GitHub repo URL: ").strip()
    process_repository(repo_url)