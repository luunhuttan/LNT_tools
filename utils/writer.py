"""CSV writer utilities for saving profile data."""
import os
import csv
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
    
    Args:
        data: List of profile dictionaries
        filepath: Path to output CSV file
        append: If True, append to existing file. If False, overwrite.
    """
    if not data:
        print("[WARNING] No data to save.")
        return
    
    # Define CSV columns
    fieldnames = ['Name', 'Title', 'Location', 'About', 'Experience', 'Education', 'Skills', 'URL']
    
    # Create new DataFrame
    df_new = pd.DataFrame(data)
    df_new = df_new[fieldnames]
    
    if append and os.path.exists(filepath):
        # Read existing data
        try:
            df_existing = pd.read_csv(filepath, encoding='utf-8-sig')
            # Concatenate with new data
            df_combined = pd.concat([df_existing, df_new], ignore_index=True)
            # Remove duplicates based on URL (same profile)
            df_combined = df_combined.drop_duplicates(subset=['URL'], keep='first')
            df_to_save = df_combined
            print(f"[INFO] Appending to existing file. Total profiles: {len(df_to_save)}")
        except Exception as e:
            print(f"[WARNING] Could not read existing file: {e}. Creating new file.")
            df_to_save = df_new
    else:
        # Overwrite mode
        df_to_save = df_new
    
    # Save with UTF-8-BOM encoding for Excel compatibility
    df_to_save.to_csv(filepath, index=False, encoding='utf-8-sig')
    
    print(f"\n✅ Saved {len(data)} profiles. Total in file: {len(df_to_save)}")
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

