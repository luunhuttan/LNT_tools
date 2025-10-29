"""CV Collector CLI - Collect public CV/Profile data using Google Custom Search API."""
import argparse
import sys
from tqdm import tqdm

from utils.search_google import search_profiles
from utils.parser import parse_profile
from utils.writer import save_to_csv, get_output_path
from utils.multi_api_key import APIManager


def main():
    """Main entry point for the CLI tool."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description='CV Collector - Collect public CV/Profile data by industry',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --industry "Data Engineer" --count 50 --api_key "AIza..." --cx "1a2b3c..."
  python main.py --industry "Frontend Developer" --count 30 --api_key "YOUR_KEY" --cx "YOUR_CX" --delay 3
  python main.py --industry "Data Engineer" --count 50 --api_key "YOUR_KEY" --cx "YOUR_CX" --overwrite
  
Note: By default, new profiles are automatically merged with existing profiles.csv (duplicates filtered by URL).
Use --overwrite flag to replace existing file instead.
        """
    )
    
    parser.add_argument(
        '--industry',
        type=str,
        required=True,
        help='Industry/profession name (e.g., "Data Engineer", "Frontend Developer")'
    )
    
    parser.add_argument(
        '--count',
        type=int,
        default=20,
        help='Number of profiles to collect (default: 20)'
    )
    
    parser.add_argument(
        '--api_key',
        type=str,
        default=None,
        help='Google Custom Search API key (optional if using multi-keys mode)'
    )
    
    parser.add_argument(
        '--use_multi_keys',
        action='store_true',
        help='Use multiple API keys from .api_keys_multi.txt file'
    )
    
    parser.add_argument(
        '--cx',
        type=str,
        required=True,
        help='Google Custom Search Engine ID (CSE)'
    )
    
    parser.add_argument(
        '--delay',
        type=float,
        default=2.0,
        help='Delay between API requests in seconds (default: 2.0, to avoid rate limits)'
    )
    
    parser.add_argument(
        '--overwrite',
        action='store_true',
        help='Overwrite existing CSV file instead of appending (default: append to avoid duplicates)'
    )
    
    args = parser.parse_args()
    
    # Validate arguments
    if args.count <= 0:
        print("[ERROR] Count must be greater than 0.")
        sys.exit(1)
    
    if args.delay < 0:
        print("[ERROR] Delay must be non-negative.")
        sys.exit(1)
    
    # Handle API key selection
    if args.use_multi_keys:
        api_keys = APIManager.load_from_file()
        if not api_keys:
            print("[ERROR] No API keys found in .api_keys_multi.txt")
            print("[INFO] Run 'python -c \"from utils.multi_api_key import *; create_api_keys_file()\"' to create template")
            sys.exit(1)
        api_manager = APIManager(api_keys)
        print(f"[INFO] Using {len(api_keys)} API keys for rotation")
        api_key = api_manager.get_current_key()
    else:
        if not args.api_key:
            print("[ERROR] --api_key is required or use --use_multi_keys")
            sys.exit(1)
        api_key = args.api_key
    
    # Print startup information
    print("=" * 60)
    print("🚀 CV Collector CLI")
    print("=" * 60)
    print(f"Industry: {args.industry}")
    print(f"Target Count: {args.count}")
    print(f"API Delay: {args.delay}s")
    print("=" * 60)
    print()
    
    try:
        # Step 1: Search for profiles using Google API
        print(f"[STEP 1/3] Searching profiles for '{args.industry}'...")
        results = search_profiles(
            industry=args.industry,
            count=args.count,
            api_key=args.api_key,
            cx=args.cx,
            delay=args.delay
        )
        
        if not results:
            print("[ERROR] No results found or search failed.")
            sys.exit(1)
        
        print(f"[INFO] Found {len(results)} search results.")
        print()
        
        # Step 2: Parse results
        print(f"[STEP 2/3] Parsing profile information...")
        profiles = []
        
        for item in tqdm(results, desc="Parsing profiles", unit="profile"):
            try:
                profile = parse_profile(item)
                profiles.append(profile)
            except Exception as e:
                print(f"[WARNING] Failed to parse profile: {e}")
                continue
        
        print(f"[INFO] Successfully parsed {len(profiles)} profiles.")
        print()
        
        # Step 3: Save to CSV
        print(f"[STEP 3/3] Saving to CSV...")
        output_path = get_output_path(args.industry)
        append_mode = not args.overwrite  # Default to append (not overwrite)
        save_to_csv(profiles, output_path, append=append_mode)
        
        print()
        print("=" * 60)
        print("✅ Collection completed successfully!")
        print(f"📁 Output file: {output_path}")
        print("=" * 60)
        
    except KeyboardInterrupt:
        print("\n[INFO] Interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n[ERROR] An error occurred: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()

