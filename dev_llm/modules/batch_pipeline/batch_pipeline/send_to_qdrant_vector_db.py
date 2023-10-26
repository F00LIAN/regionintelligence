from typing import Dict, Optional, List

import hashlib
from pydantic import BaseModel
from unstructured.partition.html import partition_html
from unstructured.cleaners.core import clean, replace_unicode_quotes, clean_non_ascii_chars
from unstructured.staging.huggingface import chunk_by_attention_window
from unstructured.staging.huggingface import stage_for_transformers
from transformers import AutoTokenizer, AutoModel
from tqdm import tqdm
from utils import TRAINING_DATA_DIR
from utils import get_console_logger
from utils import model, tokenizer
import os
import datetime
from qdrant_client import QdrantClient
import json

from typing import Dict, List

logger = get_console_logger()

class Document(BaseModel):
        id: str
        group_key: Optional[str] = None
        metadata: Optional[dict] = {}
        text: Optional[list] = []
        chunks: Optional[list] = []
        embeddings: Optional[list] = []

class BuildingCodeProcessor:
    def __init__(self):
        self.QDRANT_API_URL = os.getenv('QDRANT_API_URL')
        self.QDRANT_API_KEY = os.getenv('QDRANT_API_KEY')
        self.current_date = datetime.datetime.now().strftime('%Y%m%d')
        self.CALIFORNIA_JSON_FILE = f"concatenated_california_building_code_data_{self.current_date}.json"
        self.QDRANT_COLLECTION_NAME = 'q_and_a_generator'
        self.QDRANT_VECTOR_SIZE = 384
        self.logger = get_console_logger()
        self.tokenizer = tokenizer
        self.model = model
        self.qdrant_client = self.get_qdrant_client()
        self.init_collection()

    def get_qdrant_client(self) -> QdrantClient:
        qdrant_client = QdrantClient(
            url=self.QDRANT_API_URL, 
            api_key=self.QDRANT_API_KEY,
        )
        return qdrant_client

    def init_collection(self):
        from qdrant_client.http.api_client import UnexpectedResponse
        from qdrant_client.http.models import Distance, VectorParams

        try: 
            self.qdrant_client.get_collection(collection_name=self.QDRANT_COLLECTION_NAME)
        except (UnexpectedResponse, ValueError):
            self.qdrant_client.recreate_collection(
                collection_name=self.QDRANT_COLLECTION_NAME,
                vectors_config=VectorParams(
                    size=self.QDRANT_VECTOR_SIZE,
                    distance=Distance.COSINE
                )
            )

    def parse_document(self, chapter_data: Dict) -> Document:
        # Parsing code goes here
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

    def chunk(self, document: Document) -> Document:
        try:
            chunks = []
            for text in document.text:
                chunks += chunk_by_attention_window(
                    text, tokenizer, max_input_size=self.QDRANT_VECTOR_SIZE)

            document.chunks = chunks
            return document
        except Exception as e:
            logger.error(f"Error chunking document: {e}")
            return None

    def embedding(self, document: Document) -> Document:
        try:
            for chunk in document.text:
                inputs = tokenizer(chunk,
                                   padding=True,
                                   truncation=True,
                                   return_tensors="pt",
                                   max_length=self.QDRANT_VECTOR_SIZE)

                result = model(**inputs)
                embeddings = result.last_hidden_state[:, 0, :].cpu().detach().numpy()
                lst = embeddings.flatten().tolist()
                document.embeddings.append(lst)
            return document
        except Exception as e:
            logger.error(f"Error while embedding document: {e}")
            return None

    def build_payloads(self, doc: Document) -> List:
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

    def push_document_to_qdrant(self, doc: Document) -> None:
        try:
            from qdrant_client.models import PointStruct

            _payloads = self.build_payloads(doc)

            self.qdrant_client.upsert(
                collection_name=self.QDRANT_COLLECTION_NAME,
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

    def process_one_building_code(self, _data: Dict) -> None:
        """Process a single building code."""
        try:
            doc = self.parse_document(_data)
            if doc is None:
                 return None
            doc = self.chunk(doc)
            if doc is None:
             return None
            doc = self.embedding(doc)
            if doc is None:
                 return None
            self.push_document_to_qdrant(doc)

            return doc
        except Exception as e:
            logger.error(f"Error while processing building code: {e}")
            return None

    
    def process_one_document(self, _data: Dict) -> None:
        """"""
        try:
            doc = self.parse_document(_data)
            if doc:
                doc = self.chunk(doc)
                doc = self.embedding(doc)
                self.push_document_to_qdrant(doc)
            return doc
        except Exception as e:
            logger.error(f"Error while processing one building code document: {e}")
            return None

    def embed_building_codes_into_qdrant(self, building_codes_data: List[Dict], n_processes: int = 1) -> None:
        """"""
        results = []
        try:
            if n_processes == 1:
                # sequential
                for _data in tqdm(building_codes_data):
                    result = self.process_one_document(_data)
                    results.append(result)
            else:
                # parallel
                import multiprocessing

               # Create a multiprocessing Pool
                with multiprocessing.Pool(processes=n_processes) as pool:
                    # Use tqdm to create a progress bar
                    results = list(tqdm(pool.imap(self.process_one_document, building_codes_data),
                                        total=len(building_codes_data),
                                        desc="Processing",
                                        unit="building_code"))

            breakpoint()
        except Exception as e:
            logger.error(f"Error while embedding building codes into Qdrant: {e}")
    
    def send_to_s3(self):
        pass

    def run(self):
        # Read from file and process the data
        with open(TRAINING_DATA_DIR / self.CALIFORNIA_JSON_FILE, 'r') as json_file:
            building_codes_data = json.load(json_file)
        self.embed_building_codes_into_qdrant(building_codes_data)
        pass





