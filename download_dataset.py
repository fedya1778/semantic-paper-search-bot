import json
import logging
from pathlib import Path

def download_dataset():
    
    from datasets import load_dataset
    
    dataset = load_dataset("CShorten/ML-ArXiv-Papers")
    
    return dataset['train']


def convert_to_jsonl(dataset, output_path="data/papers.jsonl", max_papers=10000):
    
    
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    num_papers = min(max_papers, len(dataset))
    
    saved_count = 0
    skipped_count = 0
    
    with open(output_path, 'w', encoding='utf-8') as f:
        for i, paper in enumerate(dataset):
            if i >= num_papers:
                break
            
            title = paper.get('title', '').strip()
            abstract = paper.get('abstract', '').strip()
            
            if not title or not abstract:
                skipped_count += 1
                continue
            
            record = {
                'title': title,
                'abstract': abstract,
                'authors': paper.get('authors', ''),
                'published': paper.get('published', ''),
                'arxiv_id': paper.get('id', ''),
                'url': f"https://arxiv.org/abs/{paper.get('id', '')}"
            }
            
            f.write(json.dumps(record, ensure_ascii=False) + '\n')
            
            saved_count += 1

def main():

    dataset = download_dataset()
    
    convert_to_jsonl(
        dataset,
        output_path="data/papers.jsonl", 
        max_papers=10000
    )
  
if __name__ == '__main__':
    main()