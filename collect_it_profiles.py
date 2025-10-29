#!/usr/bin/env python3
"""Script to collect IT profiles from around the world."""

import subprocess
import sys

# IT jobs to collect
IT_JOBS = [
    "Data Engineer",
    "Backend Engineer", 
    "Frontend Engineer",
    "Fullstack Engineer",
    "DevOps Engineer",
    "ML Engineer",
    "Data Scientist",
    "Software Engineer",
    "Cloud Engineer",
    "Big Data Engineer",
    "AI Engineer",
    "Backend Developer",
    "Frontend Developer",
    "Software Developer",
]

# API credentials (modify these)
API_KEY = "AIzaSyA5tjOlmPZxbKXz9uDzvNqPO_Sco7Oq9-k"
CX = "d4849e3a9180a4ea6"

def collect_profiles():
    """Collect profiles for all IT jobs."""
    count_per_job = 200  # Target 200 profiles per job
    delay = 2.0
    
    print("=" * 60)
    print("🚀 IT Profile Collector - Global Search")
    print("=" * 60)
    print(f"Jobs to collect: {len(IT_JOBS)}")
    print(f"Target per job: {count_per_job} profiles")
    print(f"Total target: ~{len(IT_JOBS) * count_per_job} profiles")
    print("=" * 60)
    print()
    
    for i, job in enumerate(IT_JOBS, 1):
        print(f"\n[{i}/{len(IT_JOBS)}] Collecting {job} profiles...")
        
        cmd = [
            "python", "main.py",
            "--industry", job,
            "--count", str(count_per_job),
            "--api_key", API_KEY,
            "--cx", CX,
            "--delay", str(delay),
        ]
        
        try:
            result = subprocess.run(cmd, check=True)
            print(f"✅ Successfully collected {job} profiles")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to collect {job} profiles: {e}")
            continue
        except KeyboardInterrupt:
            print("\n\n⚠️ Interrupted by user. Progress saved.")
            sys.exit(0)
    
    print("\n" + "=" * 60)
    print("✅ All IT profiles collected!")
    print("=" * 60)

if __name__ == "__main__":
    collect_profiles()

