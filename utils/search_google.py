"""Google Custom Search API integration for profile searching."""
import time
import random
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def generate_query_variations(industry):
    """
    Generate multiple query variations to find more unique profiles.
    
    Args:
        industry: Base industry keyword
        
    Returns:
        List of different query strings
    """
    variations = []
    
    # Base industry variations
    base_keywords = [
        industry,
        f"{industry} at",
        f"Senior {industry}",
        f"Junior {industry}",
        f"{industry} manager",
        f"Lead {industry}",
    ]
    
    # Location variations
    locations = [
        "Vietnam",
        '"Viet Nam"',
        "Ho Chi Minh",
        "Hanoi",
        "Da Nang",
        "HCMC",
    ]
    
    # Generate query combinations
    for keyword in base_keywords:
        for location in locations:
            query = f'site:linkedin.com/in {keyword} {location}'
            variations.append(query)
    
    # Add some without location to get broader results
    for keyword in base_keywords:
        query = f'site:linkedin.com/in {keyword} Vietnam'
        variations.append(query)
    
    return variations


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
    
    # Generate query variations to find more unique profiles
    query_variations = generate_query_variations(industry)
    print(f"[INFO] Searching for '{industry}' profiles with {len(query_variations)} query variations...")
    
    query_index = 0
    seen_urls = set()  # Track seen URLs to avoid duplicates within one run
    
    while len(results) < count and query_index < len(query_variations):
        try:
            # Use different query variations to find different profiles
            query = query_variations[query_index % len(query_variations)]
            
            res = service.cse().list(
                q=query,
                cx=cx,
                start=start,
                num=max_results_per_query
            ).execute()
            
            items = res.get("items", [])
            
            if not items or len(items) < max_results_per_query:
                print(f"[INFO] No more results for this query. Trying next variation...")
                query_index += 1
                start = 1
                
                # Don't sleep if switching query, just continue
                continue
            
            # Add items only if they're unique
            new_profiles_count = 0
            for item in items:
                url = item.get("link", "")
                if url not in seen_urls:
                    seen_urls.add(url)
                    results.append({
                        "title": item.get("title", ""),
                        "snippet": item.get("snippet", ""),
                        "link": url
                    })
                    new_profiles_count += 1
                    
                    if len(results) >= count:
                        break
            
            print(f"[INFO] Found {len(results)}/{count} profiles (+{new_profiles_count} new from this query: {query[:50]}...)")
            
            # Switch to next query variation if we're not getting new results
            if new_profiles_count == 0 or start >= 100:
                query_index += 1
                start = 1  # Reset start for new query variation
                # Small delay before switching queries
                if delay > 0:
                    time.sleep(delay / 2)
                
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

