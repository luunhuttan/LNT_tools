"""Data parsing utilities for profile information extraction."""
import re
from typing import Dict, List


# Common domain patterns
DOMAIN_PATTERNS = {
    'linkedin.com/in': 'LinkedIn',
    'github.com': 'GitHub',
    'kaggle.com': 'Kaggle',
    'researchgate.net': 'ResearchGate',
    'behance.net': 'Behance'
}

# Common skills keywords
SKILL_KEYWORDS = [
    'Python', 'Java', 'JavaScript', 'SQL', 'R', 'Scala', 'Go', 'C++', 'C#',
    'Machine Learning', 'Deep Learning', 'AI', 'Data Science', 'Analytics',
    'TensorFlow', 'PyTorch', 'Scikit-learn', 'Pandas', 'NumPy',
    'Apache Spark', 'Hadoop', 'Kafka', 'Airflow', 'Docker', 'Kubernetes',
    'AWS', 'Azure', 'GCP', 'Tableau', 'Power BI', 'Excel',
    'React', 'Vue', 'Angular', 'Node.js', 'Django', 'Flask',
    'Git', 'Jira', 'Agile', 'CI/CD'
]


def parse_name_from_title(title: str) -> str:
    """
    Extract name from title (usually at the beginning before dash or pipe).
    
    Args:
        title: Profile title from search result
        
    Returns:
        Extracted name or empty string
    """
    # Common patterns: "Name - Title" or "Name | Title"
    patterns = [
        r'^([^-|]+?)(?: - | \| )',
        r'^(.*?) - (.*?) \|',
        r'^([A-Z][a-z]+ [A-Z][a-z]+)(?:\s|$)',
    ]
    
    for pattern in patterns:
        match = re.match(pattern, title.strip())
        if match:
            name = match.group(1).strip()
            # Basic validation: should have at least 2 words
            if len(name.split()) >= 2 and len(name) > 5:
                return name
    
    return ""


def parse_title_from_string(text: str) -> str:
    """
    Extract job title from text.
    
    Args:
        text: Snippet or title text
        
    Returns:
        Extracted job title
    """
    # Look for patterns like "Data Engineer at Company" or "Senior Developer"
    patterns = [
        r'([A-Z][a-zA-Z\s&]+(?:Engineer|Developer|Scientist|Analyst|Architect|Manager|Director|Lead|Specialist))',
        r'at\s+([A-Z][a-zA-Z\s]+?)(?:\s|$|,|\.)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(1).strip()
    
    return ""


def detect_skills(text: str) -> List[str]:
    """
    Extract skills from text based on common keywords.
    
    Args:
        text: Snippet or description text
        
    Returns:
        List of detected skills
    """
    found_skills = []
    text_lower = text.lower()
    
    for skill in SKILL_KEYWORDS:
        if skill.lower() in text_lower:
            found_skills.append(skill)
    
    return found_skills


def parse_location_from_snippet(snippet: str) -> str:
    """
    Try to extract location from snippet.
    
    Args:
        snippet: Text snippet from search result
        
    Returns:
        Extracted location or empty string
    """
    # Look for location patterns
    location_pattern = r'(Vietnam|Ho Chi Minh|Hanoi|HCM|HN|Đà Nẵng)'
    match = re.search(location_pattern, snippet, re.IGNORECASE)
    
    if match:
        return match.group(1)
    
    return ""


def detect_domain(link: str) -> str:
    """
    Detect the domain/platform from URL.
    
    Args:
        link: Profile URL
        
    Returns:
        Domain name or 'Other'
    """
    for pattern, domain in DOMAIN_PATTERNS.items():
        if pattern in link:
            return domain
    return "Other"


def normalize_linkedin_url(url: str) -> str:
    """
    Normalize LinkedIn URLs.
    Convert vn.linkedin.com -> www.linkedin.com for better accessibility.
    Decode URL-encoded characters.
    
    Args:
        url: LinkedIn URL
        
    Returns:
        Normalized URL
    """
    if not url or url == '-':
        return url
    
    # Convert vn.linkedin.com, hk.linkedin.com, etc to www.linkedin.com
    if 'linkedin.com' in url:
        url = url.replace('vn.linkedin.com', 'www.linkedin.com')
        url = url.replace('hk.linkedin.com', 'www.linkedin.com')
        url = url.replace('ca.linkedin.com', 'www.linkedin.com')
        url = url.replace('sg.linkedin.com', 'www.linkedin.com')
        url = url.replace('us.linkedin.com', 'www.linkedin.com')
        url = url.replace('uk.linkedin.com', 'www.linkedin.com')
        # Add more if needed
        
        # Decode URL-encoded characters (Vietnamese characters)
        from urllib.parse import unquote
        url = unquote(url)
    
    return url


def parse_profile(item: Dict[str, str]) -> Dict[str, str]:
    """
    Parse a single profile item from search results.
    
    Args:
        item: Dictionary with 'title', 'snippet', 'link'
        
    Returns:
        Parsed profile with all fields
    """
    title = item.get('title', '')
    snippet = item.get('snippet', '')
    link = item.get('link', '')
    
    # Extract information
    name = parse_name_from_title(title)
    job_title = parse_title_from_string(title + ' ' + snippet)
    location = parse_location_from_snippet(snippet)
    skills = detect_skills(title + ' ' + snippet)
    
    # If name is empty, try to extract from title differently
    if not name and title:
        # Try to get first part of title
        name = title.split(' - ')[0].split(' | ')[0].strip()
        if len(name.split()) < 2 or len(name) < 5:
            name = ""
    
    # If job_title is empty, try to get from snippet
    if not job_title and snippet:
        job_title = parse_title_from_string(snippet)
    
    # Construct about from snippet
    about = snippet[:200] if snippet else ""
    
    # Normalize LinkedIn URL
    normalized_link = normalize_linkedin_url(link)
    
    return {
        'Name': name if name else '-',
        'Title': job_title if job_title else '-',
        'Location': location if location else '-',
        'About': about if about else '-',
        'Experience': '-',
        'Education': '-',
        'Skills': ', '.join(skills) if skills else '-',
        'URL': normalized_link
    }

