from typing import Dict, Optional, List

import hashlib
from pydantic import BaseModel
from unstructured.partition.html import partition_html
from unstructured.cleaners.core import clean, replace_unicode_quotes, clean_non_ascii_chars
from unstructured.staging.huggingface import chunk_by_attention_window
from unstructured.staging.huggingface import stage_for_transformers
from transformers import AutoTokenizer, AutoModel
from tqdm import tqdm
from src.paths import JSON_DATA_DIR
from src.logger import get_console_logger

CALIFORNIA_JSON_FILE = JSON_DATA_DIR / 'california_building_codes_json' / 'california_20231015.json'
QDRANT_COLLECTION_NAME = 'california_building_codes'
QDRANT_VECTOR_SIZE = 384

# init logger
logger = get_console_logger()

# tokenizer and LLM we use to embed the document text
tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")

# init qdrant client and collection where we store the news
from src.vector_db_api import get_qdrant_client, init_collection
qdrant_client = get_qdrant_client()
qdrant_client = init_collection(
    qdrant_client=qdrant_client,
    collection_name=QDRANT_COLLECTION_NAME,
    vector_size=QDRANT_VECTOR_SIZE,
)

class Document(BaseModel):
    id: str
    group_key: Optional[str] = None
    metadata: Optional[dict] = {}
    text: Optional[list] = []
    chunks: Optional[list] = []
    embeddings: Optional[list] = []

def parse_document(chapter_data: Dict) -> Document:
    try:
        document_id = hashlib.md5(str(chapter_data).encode()).hexdigest()
        document = Document(id=document_id)
        texts = []

        for section in chapter_data['sections']:
            texts.append(section['title'])
            texts.append(section['content'])
            for subsection in section['subsections']:
                texts.append(subsection['title'])
                texts.append(subsection['content'])

        joined_text = " ".join(texts)
        document.text = [joined_text]
        document.metadata['chapter'] = chapter_data['chapter']
        
        return document
    except Exception as e:
        logger.error(f"Error parsing document: {e}")
        return None
    
def chunk(document: Document) -> Document:
    try:
        chunks = []
        for text in document.text:
            chunks += chunk_by_attention_window(
                text, tokenizer, max_input_size=QDRANT_VECTOR_SIZE)
        
        document.chunks = chunks
        return document
    except Exception as e:
        logger.error(f"Error chunking document: {e}")
        return None

def embedding(document: Document) -> Document:
    try:
        for chunk in document.text:
            inputs = tokenizer(chunk,
                               padding=True,
                               truncation=True,
                               return_tensors="pt",
                               max_length=QDRANT_VECTOR_SIZE)

            result = model(**inputs)
            embeddings = result.last_hidden_state[:, 0, :].cpu().detach().numpy()
            lst = embeddings.flatten().tolist()
            document.embeddings.append(lst)
        return document
    except Exception as e:
        logger.error(f"Error while embedding document: {e}")
        return None


def build_payloads(doc: Document) -> List:
    try:
        payloads = []
        for chunk in doc.chunks:
            payload = doc.metadata
            payload.update({"text": chunk})
            payloads.append(payload)
        return payloads
    except Exception as e:
        logger.error(f"Error while building payloads: {e}")
        return []


def push_document_to_qdrant(doc: Document) -> None:
    try:
        from qdrant_client.models import PointStruct

        _payloads = build_payloads(doc)

        qdrant_client.upsert(
            collection_name=QDRANT_COLLECTION_NAME,
            points=[
                PointStruct(
                    id=idx,
                    vector=vector,
                    payload=_payload
                )
                for idx, (vector, _payload) in enumerate(zip(doc.embeddings, _payloads))
            ]
        )
    except Exception as e:
        logger.error(f"Error while pushing document to Qdrant: {e}")


def process_one_building_code(_data: Dict) -> None:
    """Process a single building code."""
    try:
        doc = parse_document(_data)
        if doc is None:
            return None
        doc = chunk(doc)
        if doc is None:
            return None
        doc = embedding(doc)
        if doc is None:
            return None
        push_document_to_qdrant(doc)

        return doc
    except Exception as e:
        logger.error(f"Error while processing building code: {e}")
        return None

def process_one_document(_data: Dict) -> None:
    """"""
    try:
        doc = parse_document(_data)
        if doc:
            doc = chunk(doc)
            doc = embedding(doc)
            push_document_to_qdrant(doc)
        return doc
    except Exception as e:
        logger.error(f"Error while processing one building code document: {e}")
        return None
    
def embed_building_codes_into_qdrant(building_codes_data: List[Dict], n_processes: int = 1) -> None:
    """"""
    results = []
    try:
        if n_processes == 1:
            # sequential
            for _data in tqdm(building_codes_data):
                result = process_one_document(_data)
                results.append(result)
        else:
            # parallel
            import multiprocessing

            # Create a multiprocessing Pool
            with multiprocessing.Pool(processes=n_processes) as pool:
                # Use tqdm to create a progress bar
                results = list(tqdm(pool.imap(process_one_document, building_codes_data),
                                    total=len(building_codes_data),
                                    desc="Processing",
                                    unit="building_code"))

        breakpoint()
    except Exception as e:
        logger.error(f"Error while embedding building codes into Qdrant: {e}")

if __name__ == '__main__':
    """"""
    import json
    with open(CALIFORNIA_JSON_FILE, 'r') as json_file:
        building_codes_data = json.load(json_file)

    embed_building_codes_into_qdrant(
        building_codes_data,
        n_processes=1
    )