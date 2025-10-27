"""Google Custom Search API integration for profile searching."""
import time
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def search_profiles(industry, count, api_key, cx, delay=2):
    """
    Search for profiles using Google Custom Search API.
    
    Args:
        industry: Industry keyword to search for
        count: Number of profiles to collect
        api_key: Google API key
        cx: Search engine ID
        delay: Delay between requests in seconds
        
    Returns:
        List of profile dictionaries with title, snippet, and link
    """
    try:
        service = build("customsearch", "v1", developerKey=api_key)
    except Exception as e:
        print(f"[ERROR] Failed to build Google API service: {e}")
        return []
    
    results = []
    start = 1
    max_results_per_query = 10
    
    print(f"[INFO] Searching for '{industry}' profiles...")
    
    while len(results) < count:
        try:
            # Build the search query targeting actual LinkedIn profiles in Vietnam
            query = f'site:linkedin.com/in {industry} Vietnam OR "Viet Nam"'
            
            res = service.cse().list(
                q=query,
                cx=cx,
                start=start,
                num=min(max_results_per_query, count - len(results))
            ).execute()
            
            items = res.get("items", [])
            
            if not items:
                print(f"[INFO] No more results found. Collected {len(results)} profiles.")
                break
            
            for item in items:
                results.append({
                    "title": item.get("title", ""),
                    "snippet": item.get("snippet", ""),
                    "link": item.get("link", "")
                })
            
            print(f"[INFO] Found {len(results)}/{count} profiles...")
            
            # Avoid hitting rate limits
            if delay > 0:
                time.sleep(delay)
            
            start += max_results_per_query
            
        except HttpError as e:
            if e.resp.status == 429:
                print("[WARNING] Rate limit exceeded. Waiting 60 seconds...")
                time.sleep(60)
                continue
            else:
                print(f"[ERROR] HTTP Error: {e}")
                break
        except Exception as e:
            print(f"[ERROR] Search failed: {e}")
            break
    
    print(f"[INFO] Successfully collected {len(results)} profiles.")
    return results

