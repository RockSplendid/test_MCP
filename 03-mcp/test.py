#!/usr/bin/env python3
"""Test script for the fetch_web_page MCP tool"""

import requests

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


def test_fetch_web_page():
    """Test the fetch_web_page function with sample URLs"""
    
    test_urls = [
        "https://example.com",
        "https://www.wikipedia.org/wiki/Python_(programming_language)",
        "https://github.com",
    ]
    
    print("Testing fetch_web_page tool...\n")
    
    for url in test_urls:
        print(f"Fetching: {url}")
        print("-" * 60)
        
        result = fetch_web_page(url)
        
        # Print first 500 characters of the result
        if len(result) > 500:
            print(result[:500] + "\n...")
        else:
            print(result)
        
        print("-" * 60)
        print(f"Total content length: {len(result)} characters\n")

if __name__ == "__main__":
    test_fetch_web_page()
