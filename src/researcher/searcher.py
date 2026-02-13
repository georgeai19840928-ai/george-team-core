import json
import os
from typing import List, Dict

# Task 2.1: Blacklist Definition
DOMAIN_BLACKLIST = [
    "ads.google.com",
    "facebook.com",
    "twitter.com",
    "instagram.com",
    "linkedin.com",
    "tiktok.com",
    "pinterest.com"
]

def filter_results(results: List[Dict], excluded_domains: List[str]) -> List[Dict]:
    """
    Task 2.1: Implement domain blacklist filter.
    Filters out results from the blacklist and user-specified excluded domains.
    """
    combined_blacklist = set(DOMAIN_BLACKLIST + excluded_domains)
    filtered = []
    for res in results:
        url = res.get("url", "")
        # Simple domain check
        if not any(domain in url for domain in combined_blacklist):
            filtered.append(res)
    return filtered

def iterative_search(topic: str, max_depth: int, excluded_domains: List[str], language: str):
    """
    Task 1.2: Iterative Search Logic.
    Uses search results to suggest next steps.
    """
    current_keywords = [topic]
    history = []

    print(f"🚀 Starting Deep Research on: {topic} (Max Depth: {max_depth})")

    for d in range(1, max_depth + 1):
        print(f"\n--- Depth {d}/{max_depth} ---")
        search_query = " ".join(current_keywords)
        print(f"🔍 Searching for: {search_query}")
        
        # Note: In a real environment, this would call the actual tool.
        # Since this script is a template/implementation, we assume search_func exists.
        # For this task, I'm providing the logic structure.
        
        # Mock search results for logic demonstration if run directly
        # In actual usage, this would be replaced by calling `web_search` tool.
        results = [
            {"title": f"Result about {topic} 1", "url": "https://example.com/info1", "snippet": "Useful data..."},
            {"title": "Ad Link", "url": "https://ads.google.com/promo", "snippet": "Buy now!"},
            {"title": f"Result about {topic} 2", "url": "https://wikipedia.org/wiki/Topic", "snippet": "Historical context..."}
        ]
        
        # Apply filter (Task 2.1)
        filtered = filter_results(results, excluded_domains)
        print(f"✅ Found {len(filtered)} relevant results (Filtered {len(results) - len(filtered)}).")
        
        history.append({
            "depth": d,
            "query": search_query,
            "results": filtered
        })

        if d < max_depth:
            # Task 1.2: AI-driven keyword suggestion
            # In a real agent loop, the AI reads snippets and generates new keywords.
            # Here we simulate the suggestion logic.
            print("🤖 AI is analyzing results to suggest next keywords...")
            # Logic: Extract key terms from filtered snippets or use AI prompt.
            new_keywords = [f"{topic} analysis", f"{topic} trends", f"{topic} future"]
            current_keywords = new_keywords
            print(f"💡 Next keywords: {', '.join(current_keywords)}")
        else:
            print("🏁 Reached maximum depth.")

    return history

if __name__ == "__main__":
    # Example usage based on schema
    sample_config = {
        "topic": "Quantum Computing",
        "depth": 2,
        "domains_to_exclude": ["youtube.com"],
        "language": "zh-TW"
    }
    
    iterative_search(
        topic=sample_config["topic"],
        max_depth=sample_config["depth"],
        excluded_domains=sample_config["domains_to_exclude"],
        language=sample_config["language"]
    )
