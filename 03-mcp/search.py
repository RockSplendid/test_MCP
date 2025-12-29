import zipfile
import os
from pathlib import Path
import minsearch

def extract_md_files_from_zip(zip_path):
    """
    Extract md and mdx files from zip, removing the first path component.
    Returns list of dicts with 'filename' and 'content' fields.
    """
    documents = []
    
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        for file_info in zip_ref.filelist:
            # Check if file is md or mdx
            if file_info.filename.endswith(('.md', '.mdx')):
                # Read the content
                with zip_ref.open(file_info.filename) as f:
                    content = f.read().decode('utf-8')
                
                # Remove first path component (e.g., "fastmcp-main/")
                path_parts = Path(file_info.filename).parts
                if len(path_parts) > 1:
                    new_filename = str(Path(*path_parts[1:]))
                else:
                    new_filename = file_info.filename
                
                documents.append({
                    'filename': new_filename,
                    'content': content
                })
    
    return documents

def create_search_index(documents):
    """
    Create a minsearch index from documents.
    """
    index = minsearch.Index(
        text_fields=['content', 'filename'],
        keyword_fields=[]
    )
    index.fit(documents)
    return index

def search(query, index, num_results=5):
    """
    Search the index and return top num_results documents.
    """
    boost_dict = {
        'filename': 2.0,  # Boost filename matches
        'content': 1.0
    }
    
    results = index.search(
        query,
        boost_dict=boost_dict,
        num_results=num_results
    )
    
    return results

if __name__ == "__main__":
    # Extract documents from zip
    print("Extracting md/mdx files from fastmcp-main.zip...")
    documents = extract_md_files_from_zip('fastmcp-main.zip')
    print(f"Found {len(documents)} markdown files")
    
    # Create search index
    print("\nIndexing documents...")
    index = create_search_index(documents)
    print("Index created successfully!")
    
    # Test searches
    test_queries = [
        "how to create a tool",
        "fastmcp server",
        "getting started"
    ]
    
    print("\n" + "="*60)
    print("Testing search functionality")
    print("="*60)
    
    for query in test_queries:
        print(f"\nQuery: '{query}'")
        print("-" * 60)
        results = search(query, index, num_results=5)
        
        for i, doc in enumerate(results, 1):
            print(f"{i}. {doc['filename']}")
            # Show first 100 chars of content
            preview = doc['content'][:100].replace('\n', ' ')
            print(f"   Preview: {preview}...")
        print()
