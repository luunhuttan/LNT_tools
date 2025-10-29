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


def search_profiles(industry, count, api_key, cx, delay=2, api_manager=None, existing_urls=None):
    """
    Search for profiles using Google Custom Search API.
    
    Args:
        industry: Industry keyword to search for
        count: Number of profiles to collect
        api_key: Google API key
        cx: Search engine ID
        delay: Delay between requests in seconds
        api_manager: Optional APIManager for key rotation
        
    Returns:
        List of profile dictionaries with title, snippet, and link
    """
    current_api_key = api_key
    current_cx = cx
    
    try:
        service = build("customsearch", "v1", developerKey=current_api_key)
    except Exception as e:
        print(f"[ERROR] Failed to build Google API service: {e}")
        return []
    
    results = []
    start = 1
    max_results_per_query = 10
    
    # Generate query variations to find more unique profiles
    query_variations = generate_query_variations(industry)
    # Shuffle order each run to increase variety across runs
    random.shuffle(query_variations)
    print(f"[INFO] Searching for '{industry}' profiles with {len(query_variations)} query variations...")
    
    query_index = 0
    # Track seen URLs to avoid duplicates within and across runs
    seen_urls = set(existing_urls or [])
    
    # Switch queries frequently to get variety
    queries_per_variation = random.randint(1, 3)  # Randomize pages per variation
    
    while len(results) < count and query_index < len(query_variations):
        try:
            # Use different query variations to find different profiles
            query = query_variations[query_index % len(query_variations)]
            
            # Execute request with retries and transient error handling
            request = service.cse().list(
                q=query,
                cx=current_cx,
                start=start,
                num=max_results_per_query
            )

            # Built-in retries for Http errors
            max_exec_retries = 3
            attempt = 0
            while True:
                try:
                    res = request.execute(num_retries=max_exec_retries)
                    break
                except HttpError as e:
                    # Bubble up HttpError (handled below) for proper rate limit/backoff logic
                    raise e
                except Exception as e:
                    # Handle transient connection resets (e.g., WinError 10054) or network hiccups
                    err_msg = str(e)
                    if "10054" in err_msg or "Connection aborted" in err_msg or "reset" in err_msg.lower():
                        attempt += 1
                        if attempt <= 3:
                            wait_s = min(10 * attempt, 30)
                            print(f"[WARNING] Transient network error (attempt {attempt}/3). Waiting {wait_s}s and retrying...")
                            time.sleep(wait_s)
                            continue
                    # Non-transient or exhausted retries
                    raise
            
            items = res.get("items", [])
            
            if not items or len(items) < max_results_per_query:
                print(f"[INFO] No more results for this query. Trying next variation...")
                query_index += 1
                start = random.choice([1, 11, 21, 31])
                
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
                # Reset start for new query variation to a random page to improve variety
                start = random.choice([1, 11, 21, 31])
                print(f"[INFO] Switching to query variation {query_index}/{len(query_variations)}")
                # Small delay before switching queries
                if delay > 0:
                    time.sleep(delay / 2)
                
            # Avoid hitting rate limits
            if delay > 0:
                time.sleep(delay)
            
            start += max_results_per_query
            
        except HttpError as e:
            status = getattr(e, 'resp', None).status if getattr(e, 'resp', None) else None
            content_str = getattr(e, 'content', b'')
            try:
                content_text = content_str.decode('utf-8') if isinstance(content_str, (bytes, bytearray)) else str(content_str)
            except Exception:
                content_text = str(content_str)

            # Handle rate/quota limits: 429 or 403 with limit messages
            if status == 429 or (status == 403 and any(s in content_text.lower() for s in [
                'rate limit', 'user rate limit', 'daily limit', 'quota', 'limit exceeded'
            ])):
                print("[WARNING] Rate limit exceeded for current API key.")
                
                # Try rotate to next key if api_manager provided
                if api_manager and len(api_manager.api_keys) > 1:
                    print("[INFO] Rotating to next API key...")
                    api_manager.rotate_key()
                    current_api_key = api_manager.get_current_key()
                    service = build("customsearch", "v1", developerKey=current_api_key)
                    # If APIManager has paired CXs, rotate CX as well
                    try:
                        current_cx_candidate = getattr(api_manager, 'get_current_cx', None)
                        if current_cx_candidate is not None:
                            cx_value = api_manager.get_current_cx()
                            if cx_value:
                                current_cx = cx_value
                    except Exception:
                        pass
                    print("[INFO] Waiting 60 seconds before retry with new key...")
                    time.sleep(60)
                    continue
                else:
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

