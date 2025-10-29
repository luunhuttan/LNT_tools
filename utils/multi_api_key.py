"""Multi API key rotation to avoid rate limits."""
import random
from typing import List


class APIManager:
    """Manages multiple API keys for rotation."""
    
    def __init__(self, api_keys: List[str]):
        """
        Initialize API Manager with multiple keys.
        
        Args:
            api_keys: List of API key strings
        """
        self.api_keys = api_keys
        self.current_index = 0
        self.key_usage = {key: 0 for key in api_keys}  # Track usage per key
        
    def get_current_key(self) -> str:
        """Get the current API key."""
        return self.api_keys[self.current_index]
    
    def rotate_key(self):
        """Switch to next API key."""
        self.current_index = (self.current_index + 1) % len(self.api_keys)
        print(f"[INFO] Rotated to API key {self.current_index + 1}/{len(self.api_keys)}")
    
    def increment_usage(self):
        """Increment usage counter for current key."""
        current_key = self.api_keys[self.current_index]
        self.key_usage[current_key] += 1
    
    def get_usage_stats(self):
        """Get usage statistics for all keys."""
        return self.key_usage
    
    @staticmethod
    def load_from_file(filepath: str = ".api_keys_multi.txt") -> List[str]:
        """
        Load multiple API keys from file.
        
        Expected format (one key per line):
        API_KEY_1=xxx
        API_KEY_2=yyy
        API_KEY_3=zzz
        
        Returns:
            List of API key strings
        """
        try:
            keys = []
            with open(filepath, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and '=' in line:
                        key = line.split('=')[1].strip()
                        if key:
                            keys.append(key)
            return keys
        except FileNotFoundError:
            print(f"[WARNING] File {filepath} not found. Using single key mode.")
            return []


def create_api_keys_file(num_keys: int = 5):
    """
    Create template file for multiple API keys.
    
    Args:
        num_keys: Number of API key slots to create
    """
    template = """# Multiple API Keys for profile collection
# Each API key allows 100 queries/day
# Total quota: 100 * number_of_keys queries/day

"""
    for i in range(1, num_keys + 1):
        template += f"# API_KEY_{i}=YOUR_API_KEY_HERE\n"
    
    with open(".api_keys_multi.txt.template", 'w') as f:
        f.write(template)
    
    print(f"✅ Created template file: .api_keys_multi.txt.template")
    print(f"📝 Fill in your API keys and rename to .api_keys_multi.txt")

