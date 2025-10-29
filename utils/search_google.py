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
    
    # Diverse keyword variations (reduced to avoid rate limits)
    base_keywords = [
        industry,
        f"Senior {industry}",
        f"Lead {industry}",
        f"Big Data {industry}",
        f"Cloud {industry}",
    ]
    
    # Location variations - priotitize VN, then global
    locations = [
        "Vietnam",
        "Ho Chi Minh",
        "Hanoi",
        "HCMC",
        "",  # Global search (no location)
    ]
    
    # Generate query combinations - prioritized by variation
    for keyword in base_keywords:
        for location in locations:
            if location:
                query = f'site:linkedin.com/in {keyword} {location}'
            else:
                query = f'site:linkedin.com/in {keyword}'
            variations.append(query)
    
    # Add alternate search patterns
    patterns = [
        f'{industry} "Viet Nam"',
        f'{industry} site:vn.linkedin.com',
        f'{industry} LinkedIn',
        f'{industry} profile',
        f'"{industry}"',
    ]
    
    variations.extend(patterns)
    
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
    
    # Switch queries frequently to get variety
    queries_per_variation = 3  # Only get 3 pages per query variation
    
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
            
            # Switch queries more frequently to get variety
            if new_profiles_count == 0 or start > (queries_per_variation * max_results_per_query):
                query_index += 1
                start = 1  # Reset start for new query variation
                print(f"[INFO] Switching to query variation {query_index}/{len(query_variations)}")
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
                # Increase delay after hitting rate limit
                delay = min(delay * 1.5, 10)  # Cap at maximum 10 seconds
                print(f"[INFO] Increasing delay to {delay:.1f} seconds to avoid rate limits...")
                continue
            else:
                print(f"[ERROR] HTTP Error: {e}")
                break
        except Exception as e:
            print(f"[ERROR] Search failed: {e}")
            break
    
    print(f"[INFO] Successfully collected {len(results)} profiles.")
    return results

