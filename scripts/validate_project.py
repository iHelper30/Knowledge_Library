#!/usr/bin/env python3
"""
Comprehensive Project Validation Script
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def run_command(command, capture_output=True):
    """
    Run shell command and return result
    """
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=capture_output, 
            text=True, 
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {command}")
        print(f"Error: {e.stderr}")
        return None

def check_code_quality():
    """
    Run code quality checks
    """
    checks = {
        "Type Checking": "mypy tools/template_generator",
        "Linting": "flake8 tools/template_generator",
        "Security Scan": "bandit -r tools/template_generator",
        "Formatting": "black --check tools/template_generator"
    }
    
    results = {}
    for name, command in checks.items():
        try:
            run_command(command)
            results[name] = "PASS"
        except subprocess.CalledProcessError:
            results[name] = "FAIL"
    
    return results

def run_tests():
    """
    Execute test suites
    """
    test_commands = {
        "Unit Tests": "pytest tests/template_generator/",
        "Integration Tests": "pytest tests/integration/",
        "Coverage": "coverage run -m pytest && coverage report -m"
    }
    
    results = {}
    for name, command in test_commands.items():
        try:
            run_command(command)
            results[name] = "PASS"
        except subprocess.CalledProcessError:
            results[name] = "FAIL"
    
    return results

def validate_templates():
    """
    Generate and validate templates
    """
    template_types = [
        'document', 'code', 'web_app', 
        'data_science', 'microservices'
    ]
    
    results = {}
    for template_type in template_types:
        try:
            # Generate template
            generate_cmd = f"python -m tools.template_generator generate " \
                           f"--type {template_type} " \
                           f"--name 'Preview {template_type.replace('_', " ").title()}' " \
                           f"--output preview_templates/{template_type}"
            run_command(generate_cmd)
            
            # Validate template
            validate_cmd = f"python -m tools.template_generator validate " \
                           f"preview_templates/{template_type}"
            run_command(validate_cmd)
            
            results[template_type] = "PASS"
        except subprocess.CalledProcessError:
            results[template_type] = "FAIL"
    
    return results

def main():
    """
    Run comprehensive project validation
    """
    validation_results = {
        "Code Quality": check_code_quality(),
        "Tests": run_tests(),
        "Template Validation": validate_templates()
    }
    
    # Generate report
    report_path = Path('validation_report.json')
    with report_path.open('w') as f:
        json.dump(validation_results, f, indent=2)
    
    # Determine overall status
    overall_status = all(
        all(result == "PASS" for result in category.values())
        for category in validation_results.values()
    )
    
    print("\n🔍 Validation Report:")
    print(json.dumps(validation_results, indent=2))
    
    print(f"\n{'✅ All Checks Passed' if overall_status else '❌ Some Checks Failed'}")
    
    sys.exit(0 if overall_status else 1)

if __name__ == '__main__':
    main()
