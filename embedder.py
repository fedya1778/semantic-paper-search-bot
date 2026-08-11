import numpy as np
import json
import logging
from pathlib import Path
from sentence_transformers import SentenceTransformer


logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
logger = logging.getLogger(__name__)


class SemanticSearchEngine:


    def __init__(self):
        logger.info('BERT model initialization')

        self.model = SentenceTransformer(
            "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
        )

        logger.info('BERT model initialized successfully')

        self.embeddings = None
        self.documents = None


    def load_documents(self, file_path):

        logger.info(f"data loading from {file_path}")
        
        self.documents = []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            for line_number, line in enumerate(f, 1):
                if line.strip():
                    try:
                        doc = json.loads(line)
                        self.documents.append(doc)
                    except json.JSONDecodeError:
                        logger.warning(f"parsing error on line {line_number}")
                        continue
        
        logger.info(f"Loaded {len(self.documents)} documents")


    def create_index(self):
        logger.info("Index creating...")
        
        if not self.documents:
            raise ValueError("You have to load documents via load_documents()")
    
        texts = []
        for doc in self.documents:
            title = doc.get("title", "")
            abstract = doc.get("abstract", "")
            text = f"{title} {abstract}"
            texts.append(text)
        
        logger.info(f"Combined {len(texts)} texts")
        logger.info("BERT encoding, this may take 1-10 minutes...")
    
        
        self.embeddings = self.model.encode(
            texts,
            show_progress_bar=True,
            convert_to_numpy=True,
            normalize_embeddings=True
        )
        
        logger.info("")
        logger.info("Index created")
        logger.info(f"Index size: {self.embeddings.shape}")
        logger.info(f"   - Documents: {self.embeddings.shape[0]}")
        logger.info(f"   - Vector size: {self.embeddings.shape[1]}")


    def search(self, query, top_k=3):
        if self.embeddings is None:
            raise ValueError("You should call create_index()")
        
        logger.info(f"SEARCH: '{query}'")
        
        logger.info("converting to vector...")
        query_embedding = self.model.encode(query, 
                                            convert_to_numpy=True,
                                            normalize_embeddings=True)
        logger.info(f"vector created: {query_embedding.shape}")
        
        logger.info("calculating similarities")
        scores = np.dot(self.embeddings, query_embedding)
        logger.info(f"max similarity: {scores.max():.4f}")
        logger.info(f"minimum similarity: {scores.min():.4f}")
        
        logger.info(f"top-{top_k} results...")
        top_indices = np.argsort(scores)[::-1][:top_k]
        
        results = []
        for rank, idx in enumerate(top_indices, 1):
            doc = self.documents[int(idx)]
            score = float(scores[idx])
            
            result = {
                "title": doc.get("title", "Untitled"),
                "abstract": doc.get("abstract", "")[:300],
                "score": score,
                "authors": doc.get("authors", ""),
                "url": doc.get("url", "")
            }
            results.append(result)
            
            logger.info(f"   #{rank}. {result['title'][:60]}... ({score*100:.1f}%)")
    
        logger.info(f"✅ Found {len(results)} results")
        
        return results


engine = None


def initialize_engine():
    global engine
        
    logger.info("")
    logger.info("searcher initializing".center(68))
    logger.info("")
        
    try:
        engine = SemanticSearchEngine()
        engine.load_documents("data/papers.jsonl")
        engine.create_index()
        
        logger.info("")
        logger.info("searcher ready".center(68))
        logger.info("")
        
    except Exception as e:
        logger.error(f"initialization failed: {e}")
        raise

def search(query, top_k=3):
    if engine is None:
        raise RuntimeError("search engine not initialized! call initialize_engine()")
        
    return engine.search(query, top_k)