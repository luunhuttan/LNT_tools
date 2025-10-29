"""CSV writer utilities for saving profile data."""
import os
import pandas as pd
from pathlib import Path
from typing import List, Dict


def create_directory(industry: str) -> str:
    """
    Create output directory for industry if it doesn't exist.
    
    Args:
        industry: Industry name
        
    Returns:
        Path to the created directory
    """
    base_dir = Path("data_collected")
    industry_dir = base_dir / industry
    
    # Create directory if it doesn't exist
    os.makedirs(industry_dir, exist_ok=True)
    
    return str(industry_dir)


def save_to_csv(data: List[Dict[str, str]], filepath: str, append=False):
    """
    Save profile data to CSV file with UTF-8-SIG encoding.
    Automatically filters duplicates based on URL to prevent duplicate profiles.
    
    Args:
        data: List of profile dictionaries
        filepath: Path to output CSV file
        append: If True, automatically append to existing file and filter duplicates.
    """
    if not data:
        print("[WARNING] No data to save.")
        return
    
    # Define CSV columns
    fieldnames = ['Name', 'Title', 'Location', 'About', 'Experience', 'Education', 'Skills', 'URL']
    
    # Create new DataFrame - ensure all columns exist
    df_new = pd.DataFrame(data)
    # Only select columns that exist, and ensure all required columns exist
    for col in fieldnames:
        if col not in df_new.columns:
            df_new[col] = '-'
    df_new = df_new[fieldnames]
    
    # Auto-append mode: append if file exists and append flag is True
    if append and os.path.exists(filepath):
        # Read existing data
        try:
            df_existing = pd.read_csv(filepath, encoding='utf-8-sig')
            
            # Check if URL column exists in existing file
            if 'URL' not in df_existing.columns:
                print("[WARNING] Existing file doesn't have 'URL' column. Creating new file.")
                df_to_save = df_new
            else:
                # Get existing URLs
                existing_urls = set(df_existing['URL'].tolist())
                
                # Count new profiles (not in existing data)
                unique_new_profiles = df_new[~df_new['URL'].isin(existing_urls)]
                duplicate_count = len(df_new) - len(unique_new_profiles)
                
                if len(unique_new_profiles) == 0:
                    print(f"[INFO] All {len(df_new)} profiles are duplicates (already in file). No new profiles added.")
                    print(f"[INFO] Total profiles in file: {len(df_existing)} (unchanged)")
                    df_to_save = df_existing
                    # Skip saving since nothing changed
                    return
                else:
                    if duplicate_count > 0:
                        print(f"[INFO] Found {duplicate_count} duplicate profiles (already in file), skipping them.")
                    
                    # Concatenate with new data
                    df_combined = pd.concat([df_existing, unique_new_profiles], ignore_index=True)
                    # Remove any potential duplicates (safety check)
                    df_combined = df_combined.drop_duplicates(subset=['URL'], keep='first')
                    df_to_save = df_combined
                    
                    new_count = len(unique_new_profiles)
                    print(f"[INFO] Added {new_count} new profiles. Total profiles in file: {len(df_to_save)}")
            
        except Exception as e:
            print(f"[WARNING] Could not read existing file: {e}. Creating new file.")
            df_to_save = df_new
    else:
        # Overwrite mode or new file
        if os.path.exists(filepath):
            print(f"[INFO] Overwriting existing file: {filepath}")
        df_to_save = df_new
    
    # Save with UTF-8-BOM encoding for Excel compatibility
    df_to_save.to_csv(filepath, index=False, encoding='utf-8-sig')
    
    # Print final summary
    print(f"\n✅ Saved {len(df_to_save)} total profiles.")
    print(f"📁 File: {filepath}")


def get_output_path(industry: str) -> str:
    """
    Get the output CSV file path for an industry.
    
    Args:
        industry: Industry name
        
    Returns:
        Full path to output CSV file
    """
    directory = create_directory(industry)
    filename = "profiles.csv"
    
    return os.path.join(directory, filename)

