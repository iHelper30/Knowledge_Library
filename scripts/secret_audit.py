#!/usr/bin/env python3
"""
GitHub Actions Secrets Audit and Management Tool
"""

import os
import re
import json
from typing import Dict, List, Optional
import requests

class SecretAuditor:
    def __init__(self, github_token: Optional[str] = None):
        """
        Initialize GitHub Secret Auditor
        
        Args:
            github_token: GitHub Personal Access Token with repo permissions
        """
        self.github_token = github_token or os.environ.get('GITHUB_TOKEN')
        if not self.github_token:
            raise ValueError("GitHub Token is required for secret management")
        
        self.headers = {
            'Authorization': f'token {self.github_token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        # Predefined secret patterns
        self.secret_patterns = {
            'api_token': r'^[A-Za-z0-9_-]{30,}$',
            'access_key': r'^(A3T[A-Z0-9]|AKIA|AGPA|AIDA|AROA|AIPA|ANPA|ANVA|ASIA)[A-Z0-9]{16}$',
            'jwt_token': r'^[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+$',
            'database_url': r'^(postgresql|mysql|mongodb)://.*:.*@.*$'
        }

    def list_repository_secrets(self, owner: str, repo: str) -> List[Dict]:
        """
        List all secrets in a GitHub repository
        
        Args:
            owner: GitHub repository owner
            repo: Repository name
        
        Returns:
            List of secret names
        """
        url = f'https://api.github.com/repos/{owner}/{repo}/actions/secrets'
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        
        return response.json().get('secrets', [])

    def analyze_secret_strength(self, secret_name: str, secret_value: str) -> Dict:
        """
        Analyze the strength and potential risks of a secret
        
        Args:
            secret_name: Name of the secret
            secret_value: Value of the secret
        
        Returns:
            Dictionary with secret analysis results
        """
        analysis = {
            'name': secret_name,
            'length': len(secret_value),
            'complexity_score': 0,
            'potential_risks': []
        }
        
        # Length-based scoring
        if len(secret_value) < 16:
            analysis['potential_risks'].append('Too short')
        elif len(secret_value) > 64:
            analysis['complexity_score'] += 2
        
        # Pattern matching
        for pattern_name, pattern in self.secret_patterns.items():
            if re.match(pattern, secret_value):
                analysis['potential_risks'].append(f'Matches {pattern_name} pattern')
        
        # Entropy calculation
        unique_chars = len(set(secret_value))
        analysis['complexity_score'] += unique_chars
        
        # Check for common weak patterns
        weak_patterns = [
            r'^[0-9]+$',  # Only numbers
            r'^[a-zA-Z]+$',  # Only letters
            r'^[a-zA-Z0-9]+$',  # Alphanumeric
            r'^(.)\1+$'  # Repeated characters
        ]
        
        for pattern in weak_patterns:
            if re.match(pattern, secret_value):
                analysis['potential_risks'].append('Weak pattern detected')
        
        return analysis

    def generate_secret_report(self, owner: str, repo: str) -> Dict:
        """
        Generate a comprehensive secret health report
        
        Args:
            owner: GitHub repository owner
            repo: Repository name
        
        Returns:
            Comprehensive secret health report
        """
        secrets = self.list_repository_secrets(owner, repo)
        
        report = {
            'total_secrets': len(secrets),
            'secret_analysis': [],
            'recommendations': []
        }
        
        for secret in secrets:
            # Note: This is a simulated analysis as we can't retrieve secret values
            analysis = {
                'name': secret['name'],
                'created_at': secret.get('created_at', 'Unknown'),
                'visibility': 'Repository-wide'
            }
            report['secret_analysis'].append(analysis)
        
        # Generate recommendations
        if len(secrets) > 10:
            report['recommendations'].append('Consider consolidating secrets')
        
        return report

def main():
    """
    Main execution for secret auditing
    """
    # Retrieve GitHub credentials from environment
    github_token = os.environ.get('GITHUB_TOKEN')
    github_owner = os.environ.get('GITHUB_REPOSITORY_OWNER', 'default_owner')
    github_repo = os.environ.get('GITHUB_REPOSITORY', 'default_repo').split('/')[-1]
    
    auditor = SecretAuditor(github_token)
    
    try:
        report = auditor.generate_secret_report(github_owner, github_repo)
        
        # Output report
        print(json.dumps(report, indent=2))
        
        # Optional: Save report to file
        with open('secret_audit_report.json', 'w') as f:
            json.dump(report, f, indent=2)
    
    except Exception as e:
        print(f"Error during secret audit: {e}")
        exit(1)

if __name__ == '__main__':
    main()
