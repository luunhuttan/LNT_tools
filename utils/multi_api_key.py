"""Multi API key rotation to avoid rate limits."""
import random
from typing import List, Dict, Optional, Union


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
        self.daily_quota = 100  # Google Custom Search API daily quota per key
        
    def get_current_key(self) -> str:
        """Get the current API key."""
        return self.api_keys[self.current_index]
    
    def get_current_cx(self) -> Optional[str]:
        """Get the current CX if provided."""
        if self.cxs is None:
            return None
        return self.cxs[self.current_index]
    
    def rotate_key(self, forced: bool = False) -> bool:
        """
        Switch to next API key.
        
        Args:
            forced: If True, force rotation even if current key hasn't hit quota
            
        Returns:
            True if rotation was successful, False if no more valid keys available
        """
        initial_index = self.current_index
        
        # Try rotating through all keys
        for _ in range(len(self.api_keys)):
            self.current_index = (self.current_index + 1) % len(self.api_keys)
            current_key = self.api_keys[self.current_index]
            
            # Check if the new key has available quota
            if forced or self.key_usage[current_key] < self.daily_quota:
                print(f"[INFO] Rotated to API key {self.current_index + 1}/{len(self.api_keys)}")
                return True
                
            # If we've tried all keys and came back to start
            if self.current_index == initial_index:
                print("[WARNING] All API keys have reached their daily quota")
                return False
                
        return False
    
    def increment_usage(self) -> bool:
        """
        Increment usage counter for current key.
        
        Returns:
            True if key still has quota, False if quota exceeded
        """
        current_key = self.api_keys[self.current_index]
        self.key_usage[current_key] += 1
        
        # Return True if still within quota
        return self.key_usage[current_key] < self.daily_quota
    
    def get_usage_stats(self) -> Dict[str, Dict[str, int]]:
        """
        Get detailed usage statistics for all keys.
        
        Returns:
            Dict containing usage stats and quota info for each key
        """
        stats = {}
        for i, key in enumerate(self.api_keys):
            stats[f"key_{i+1}"] = {
                "usage": self.key_usage[key],
                "remaining": self.daily_quota - self.key_usage[key],
                "total_quota": self.daily_quota
            }
        return stats
    
    @staticmethod
    def _validate_key_value(key: str, value: str) -> bool:
        """
        Validate an API key or CX value.
        
        Args:
            key: The key name (API_KEY_n or CX_n)
            value: The value to validate
            
        Returns:
            True if valid, False otherwise
        """
        if not value or not isinstance(value, str):
            return False
            
        value = value.strip()
        if not value:
            return False
            
        # Basic API key validation (for Google API keys)
        if key.startswith('API_KEY'):
            return value.startswith('AIza') and len(value) >= 30
            
        # Basic CX validation
        if key.startswith('CX'):
            return len(value) >= 10 and not value.startswith(('http', 'www'))
            
        return True

    @staticmethod
    def load_from_file(filepath: str = ".api_keys_multi.txt") -> List[str]:
        """
        Backward-compatible loader: returns only API keys from file.
        
        Args:
            filepath: Path to the keys file
            
        Returns:
            List of API keys
        """
        try:
            keys: List[str] = []
            with open(filepath, 'r', encoding='utf-8') as f:
                for raw in f:
                    line = raw.strip()
                    if not line or line.startswith('#') or '=' not in line:
                        continue
                    name, value = line.split('=', 1)
                    name = name.strip().upper()
                    if name.startswith('API_KEY'):
                        value = value.strip()
                        if APIManager._validate_key_value(name, value):
                            keys.append(value)
            return keys
        except FileNotFoundError:
            print(f"[WARNING] File {filepath} not found. Using single key mode.")
            return []
        except Exception as e:
            print(f"[ERROR] Failed to load API keys: {e}")
            return []

    @staticmethod
    def load_pairs_from_file(filepath: str = ".api_keys_multi.txt") -> tuple[List[str], List[str]]:
        """
        Load API_KEY_n and CX_n pairs from file.

        Expected format:
            API_KEY_1=xxx
            CX_1=aaa
            API_KEY_2=yyy
            CX_2=bbb

        Args:
            filepath: Path to the keys file
            
        Returns:
            Tuple of (api_keys, cxs). If CXs are missing, cxs may be empty.
        """
        try:
            key_by_index: Dict[int, str] = {}
            cx_by_index: Dict[int, str] = {}
            
            with open(filepath, 'r', encoding='utf-8') as f:
                for raw in f:
                    line = raw.strip()
                    if not line or line.startswith('#') or '=' not in line:
                        continue
                        
                    name, value = line.split('=', 1)
                    name = name.strip().upper()
                    
                    try:
                        if name.startswith('API_KEY_') or name.startswith('CX_'):
                            prefix = name.rsplit('_', 1)[0]
                            idx = int(name.split('_')[-1])
                            
                            if APIManager._validate_key_value(prefix, value):
                                if prefix == 'API_KEY':
                                    key_by_index[idx] = value.strip()
                                elif prefix == 'CX':
                                    cx_by_index[idx] = value.strip()
                    except ValueError:
                        continue

<<<<<<< HEAD
            # Validate and assemble lists
            if not key_by_index:
                print("[WARNING] No valid API keys found in file")
                return [], []
                
            # Sort indices for consistent ordering
=======
            # Assemble lists in ascending index order
            print(f"[DEBUG] key_by_index: {key_by_index}")
            print(f"[DEBUG] cx_by_index: {cx_by_index}")
>>>>>>> 04cfcfb986b4578528d7e239e1358d72058e6c6b
            indices = sorted(key_by_index.keys())
            print(f"[DEBUG] indices: {indices}")
            api_keys = [key_by_index[i] for i in indices]
<<<<<<< HEAD
            
            # Only include CXs if we have them for all keys
            cxs = []
            if cx_by_index:
                cxs = [cx_by_index.get(i, '') for i in indices]
                # Only return CXs if we have them for all keys
                if not all(cxs):
                    print("[WARNING] Incomplete CX pairs found - some keys missing CX values")
                    cxs = []
                
=======
            cxs = [cx_by_index[i] if i in cx_by_index else None for i in indices]
            # Log nếu thiếu CX ở đâu đó
            if None in cxs:
                missing = [i for i, v in zip(indices, cxs) if v is None]
                print(f"[WARNING] Missing CX for index: {missing}")
>>>>>>> 04cfcfb986b4578528d7e239e1358d72058e6c6b
            return api_keys, cxs
            
        except FileNotFoundError:
            print(f"[WARNING] File {filepath} not found")
            return [], []
        except Exception as e:
            print(f"[ERROR] Failed to load API keys and CXs: {e}")
            return [], []


def create_api_keys_file(num_keys: int = 5, output_path: Optional[str] = None):
    """
    Create template file for multiple API keys.
    
    Args:
        num_keys: Number of API key slots to create
        output_path: Custom output path, if None uses default template name
    """
    template = """# Multiple API Keys for profile collection
# Each API key allows 100 queries/day
# Total quota: {total} queries/day
#
# Format:
#   API_KEY_n=your_google_api_key_here  (must start with 'AIza')
#   CX_n=your_search_engine_id_here     (optional, but recommended)
#
# Example:
#   API_KEY_1=AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
#   CX_1=123456789012345678901:abcdef
#
# Note: 
# - Each API_KEY_n should have a matching CX_n
# - Keys must be numbered sequentially (1, 2, 3, ...)
# - Comments start with #
# - Empty lines are ignored

""".format(total=num_keys * 100)

    # Add key/CX pairs
    for i in range(1, num_keys + 1):
        template += f"API_KEY_{i}=YOUR_API_KEY_HERE\n"
        template += f"CX_{i}=YOUR_SEARCH_ENGINE_ID_HERE\n\n"
    
    # Determine output path
    if not output_path:
        output_path = ".api_keys_multi.txt.template"
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(template)
        
        print(f"✅ Created template file: {output_path}")
        if output_path.endswith('.template'):
            print(f"📝 Fill in your API keys and rename to .api_keys_multi.txt")
    except Exception as e:
        print(f"[ERROR] Failed to create template file: {e}")

