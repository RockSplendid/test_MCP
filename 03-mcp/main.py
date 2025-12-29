from fastmcp import FastMCP
import requests
from search import extract_md_files_from_zip, create_search_index, search as search_docs

mcp = FastMCP("Demo 🚀")

# Load and index FastMCP documentation on startup
print("Loading FastMCP documentation...")
docs = extract_md_files_from_zip('fastmcp-main.zip')
doc_index = create_search_index(docs)
print(f"Indexed {len(docs)} documentation files")

@mcp.tool
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@mcp.tool
def fetch_web_page(url: str) -> str:
    """
    Download and convert web page content to markdown using Jina Reader.
    
    Args:
        url: The URL of the web page to fetch
        
    Returns:
        The page content converted to markdown format
    """
    try:
        # Jina Reader API endpoint
        jina_url = f"https://r.jina.ai/{url}"
        
        headers = {
            "Accept": "application/json"
        }
        
        response = requests.get(jina_url, headers=headers, timeout=30)
        response.raise_for_status()
        
        # Parse the JSON response
        data = response.json()
        
        if "data" in data and "content" in data["data"]:
            return data["data"]["content"]
        else:
            return response.text
            
    except requests.exceptions.RequestException as e:
        return f"Error fetching the webpage: {str(e)}"
    except Exception as e:
        return f"Error processing the webpage: {str(e)}"

@mcp.tool
def search_fastmcp_docs(query: str, num_results: int = 5) -> str:
    """
    Search the FastMCP documentation for relevant information.
    
    Args:
        query: The search query to find relevant documentation
        num_results: Number of results to return (default: 5)
        
    Returns:
        Formatted search results with filenames and content previews
    """
    try:
        results = search_docs(query, doc_index, num_results=num_results)
        
        if not results:
            return f"No results found for query: '{query}'"
        
        output = [f"Search results for '{query}':\n"]
        
        for i, doc in enumerate(results, 1):
            output.append(f"\n{i}. {doc['filename']}")
            # Show first 200 chars of content
            preview = doc['content'][:200].replace('\n', ' ').strip()
            output.append(f"   {preview}...")
        
        return "\n".join(output)
    
    except Exception as e:
        return f"Error searching documentation: {str(e)}"

if __name__ == "__main__":
    mcp.run()