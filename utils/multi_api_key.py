"""Multi API key rotation to avoid rate limits."""
import random
from typing import List


class APIManager:
    """Manages multiple API keys (and optional CXs) for rotation."""

    def __init__(self, api_keys: List[str], cxs: List[str] | None = None):
        """
        Initialize API Manager with multiple keys and optional CXs.

        Args:
            api_keys: List of API key strings
            cxs: Optional list of CX strings paired by index with api_keys
        """
        self.api_keys = api_keys
        self.cxs = cxs if cxs and len(cxs) == len(api_keys) else None
        # Start at a random index to distribute usage across runs
        self.current_index = random.randint(0, len(self.api_keys) - 1) if self.api_keys else 0
        self.key_usage = {key: 0 for key in api_keys}  # Track usage per key
        
    def get_current_key(self) -> str:
        """Get the current API key."""
        return self.api_keys[self.current_index]
    
    def get_current_cx(self) -> str | None:
        """Get the current CX if provided."""
        if self.cxs is None:
            return None
        return self.cxs[self.current_index]
    
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
        Backward-compatible loader: returns only API keys from file.
        """
        try:
            keys: List[str] = []
            with open(filepath, 'r') as f:
                for raw in f:
                    line = raw.strip()
                    if not line or '=' not in line:
                        continue
                    name, value = line.split('=', 1)
                    if name.strip().upper().startswith('API_KEY'):
                        value = value.strip()
                        if value:
                            keys.append(value)
            return keys
        except FileNotFoundError:
            print(f"[WARNING] File {filepath} not found. Using single key mode.")
            return []

    @staticmethod
    def load_pairs_from_file(filepath: str = ".api_keys_multi.txt") -> tuple[List[str], List[str]]:
        """
        Load API_KEY_n and CX_n pairs from file.

        Expected lines (order can vary):
            API_KEY_1=xxx
            CX_1=aaa
            API_KEY_2=yyy
            CX_2=bbb

        Returns:
            (api_keys, cxs) — if some CXs are missing, cxs may be shorter.
        """
        try:
            key_by_index: dict[int, str] = {}
            cx_by_index: dict[int, str] = {}
            with open(filepath, 'r') as f:
                for raw in f:
                    line = raw.strip()
                    if not line or '=' not in line:
                        continue
                    name, value = line.split('=', 1)
                    name = name.strip()
                    value = value.strip()
                    if not value:
                        continue
                    name_u = name.upper()
                    if name_u.startswith('API_KEY_'):
                        try:
                            idx = int(name_u.split('_')[-1])
                            key_by_index[idx] = value
                        except ValueError:
                            continue
                    elif name_u.startswith('CX_'):
                        try:
                            idx = int(name_u.split('_')[-1])
                            cx_by_index[idx] = value
                        except ValueError:
                            continue

            # Assemble lists in ascending index order
            print(f"[DEBUG] key_by_index: {key_by_index}")
            print(f"[DEBUG] cx_by_index: {cx_by_index}")
            indices = sorted(key_by_index.keys())
            print(f"[DEBUG] indices: {indices}")
            api_keys = [key_by_index[i] for i in indices]
            cxs = [cx_by_index[i] if i in cx_by_index else None for i in indices]
            # Log nếu thiếu CX ở đâu đó
            if None in cxs:
                missing = [i for i, v in zip(indices, cxs) if v is None]
                print(f"[WARNING] Missing CX for index: {missing}")
            return api_keys, cxs
        except FileNotFoundError:
            print(f"[WARNING] File {filepath} not found. Using single key mode.")
            return [], []


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

