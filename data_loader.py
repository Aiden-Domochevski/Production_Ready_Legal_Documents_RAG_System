from google import genai
from llama_index.readers.file import PDFReader
from llama_index.core.node_parser import SentenceSplitter
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))


EMBED_MODEL = "gemini-embedding-001"
EMBED_DIM = 3072  

splitter = SentenceSplitter(chunk_size=1000, chunk_overlap=200)

def load_and_chunk_pdf(path: str):
    docs = PDFReader().load_data(file=path)
    texts = [d.text for d in docs if getattr(d, "text", None)]
    chunks = []
    for t in texts:
        chunks.extend(splitter.split_text(t))
    return chunks

def embed_texts(texts: list[str]) -> list[list[float]]:
    embeddings = []
    for i in range(0, len(texts), 100):
        response = client.models.embed_content(
            model=EMBED_MODEL,
            contents=texts[i:i + 100],
        )
        embeddings.extend(e.values for e in response.embeddings)
    return embeddings