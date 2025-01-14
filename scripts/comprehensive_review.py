#!/usr/bin/env python3
"""
Comprehensive Project Review and Validation Framework
"""

import os
import sys
import ast
import re
import json
import importlib
import subprocess
from typing import Dict, List, Any, Optional
from pathlib import Path

class ComprehensiveProjectReviewer:
    def __init__(self, project_root: str):
        """
        Initialize project review with root directory
        """
        self.project_root = Path(project_root)
        self.review_results = {
            'structural_analysis': {},
            'code_quality': {},
            'dependency_analysis': {},
            'security_assessment': {},
            'template_type_validation': {},
            'performance_metrics': {}
        }

    def structural_analysis(self) -> Dict[str, Any]:
        """
        Perform comprehensive structural analysis of project
        """
        results = {
            'directory_structure': {},
            'module_dependencies': {},
            'import_graph': {}
        }

        # Analyze directory structure
        for root, dirs, files in os.walk(self.project_root):
            relative_path = Path(root).relative_to(self.project_root)
            results['directory_structure'][str(relative_path)] = {
                'directories': dirs,
                'files': files
            }

        # Analyze module dependencies
        sys.path.insert(0, str(self.project_root))
        try:
            template_generator = importlib.import_module('tools.template_generator')
            results['module_dependencies'] = self._analyze_module_dependencies(template_generator)
        except ImportError as e:
            results['module_dependencies_error'] = str(e)

        return results

    def _analyze_module_dependencies(self, module):
        """
        Create a dependency graph for a given module
        """
        dependencies = {}
        for name, module_obj in list(sys.modules.items()):
            if name.startswith('tools.template_generator'):
                try:
                    source_file = module_obj.__file__
                    dependencies[name] = {
                        'source_file': source_file,
                        'imported_modules': [
                            imp.name for imp in ast.parse(
                                open(source_file, 'r').read()
                            ).body if isinstance(imp, ast.Import)
                        ]
                    }
                except Exception as e:
                    dependencies[name] = {'error': str(e)}
        return dependencies

    def code_quality_analysis(self) -> Dict[str, Any]:
        """
        Comprehensive code quality assessment
        """
        results = {
            'complexity_metrics': {},
            'style_violations': {},
            'potential_improvements': []
        }

        # Run radon for cyclomatic complexity
        try:
            complexity_output = subprocess.check_output([
                'radon', 'cc', 
                str(self.project_root / 'tools' / 'template_generator'),
                '-a', '-nc'
            ], text=True)
            results['complexity_metrics'] = self._parse_complexity_metrics(complexity_output)
        except subprocess.CalledProcessError as e:
            results['complexity_metrics_error'] = str(e)

        # Run pylint for style and potential issues
        try:
            pylint_output = subprocess.check_output([
                'pylint', 
                str(self.project_root / 'tools' / 'template_generator')
            ], text=True, stderr=subprocess.STDOUT)
            results['style_violations'] = self._parse_pylint_output(pylint_output)
        except subprocess.CalledProcessError as e:
            results['style_violations'] = str(e)

        return results

    def _parse_complexity_metrics(self, output: str) -> Dict[str, Any]:
        """
        Parse radon complexity metrics
        """
        complexity_map = {}
        for line in output.split('\n'):
            if line.strip():
                match = re.match(r'(\S+)\s*\((\w+)\):\s*(.+)', line)
                if match:
                    module, complexity_type, details = match.groups()
                    complexity_map[module] = {
                        'type': complexity_type,
                        'details': details
                    }
        return complexity_map

    def _parse_pylint_output(self, output: str) -> Dict[str, List[str]]:
        """
        Parse pylint output for style violations
        """
        violations = {}
        for line in output.split('\n'):
            match = re.match(r'(\S+):(\d+):\s*(\w+)\s*(.+)', line)
            if match:
                file, line_num, violation_type, message = match.groups()
                if file not in violations:
                    violations[file] = []
                violations[file].append({
                    'line': line_num,
                    'type': violation_type,
                    'message': message
                })
        return violations

    def template_type_validation(self) -> Dict[str, Any]:
        """
        Validate each template type implementation
        """
        results = {}
        template_types = ['document', 'code', 'web_app', 'data_science', 'microservices']
        
        for template_type in template_types:
            try:
                # Simulate template generation
                generate_cmd = [
                    sys.executable, '-m', 'tools.template_generator', 
                    'generate', 
                    '--type', template_type, 
                    '--name', f'Validation_{template_type}',
                    '--output', f'temp_validation_{template_type}'
                ]
                output = subprocess.check_output(generate_cmd, text=True)
                
                # Validate generated template
                validate_cmd = [
                    sys.executable, '-m', 'tools.template_generator', 
                    'validate', 
                    f'temp_validation_{template_type}'
                ]
                validation_output = subprocess.check_output(validate_cmd, text=True)
                
                results[template_type] = {
                    'generation_output': output,
                    'validation_output': validation_output,
                    'status': 'PASS'
                }
            except subprocess.CalledProcessError as e:
                results[template_type] = {
                    'error': str(e),
                    'status': 'FAIL'
                }
            finally:
                # Clean up temporary directories
                subprocess.run(['rm', '-rf', f'temp_validation_{template_type}'], 
                               capture_output=True)
        
        return results

    def security_assessment(self) -> Dict[str, Any]:
        """
        Comprehensive security vulnerability scanning
        """
        results = {
            'bandit_scan': {},
            'safety_check': {},
            'potential_vulnerabilities': []
        }

        # Run Bandit for security analysis
        try:
            bandit_output = subprocess.check_output([
                'bandit', '-r', 
                str(self.project_root / 'tools' / 'template_generator')
            ], text=True)
            results['bandit_scan'] = self._parse_bandit_output(bandit_output)
        except subprocess.CalledProcessError as e:
            results['bandit_scan_error'] = str(e)

        # Run safety to check for known vulnerabilities in dependencies
        try:
            safety_output = subprocess.check_output([
                'safety', 'check'
            ], text=True)
            results['safety_check'] = self._parse_safety_output(safety_output)
        except subprocess.CalledProcessError as e:
            results['safety_check_error'] = str(e)

        return results

    def _parse_bandit_output(self, output: str) -> Dict[str, List[Dict]]:
        """
        Parse Bandit security scan results
        """
        vulnerabilities = {}
        current_file = None
        for line in output.split('\n'):
            file_match = re.match(r'>> (\S+)', line)
            vuln_match = re.match(r'(\d+)\s+(\w+)\s+(.+)', line)
            
            if file_match:
                current_file = file_match.group(1)
                vulnerabilities[current_file] = []
            elif vuln_match and current_file:
                vulnerabilities[current_file].append({
                    'line': vuln_match.group(1),
                    'severity': vuln_match.group(2),
                    'description': vuln_match.group(3)
                })
        
        return vulnerabilities

    def _parse_safety_output(self, output: str) -> List[Dict]:
        """
        Parse Safety dependency vulnerability check
        """
        vulnerabilities = []
        for line in output.split('\n'):
            match = re.match(r'(\S+)==(\S+)\s+(.+)', line)
            if match:
                vulnerabilities.append({
                    'package': match.group(1),
                    'version': match.group(2),
                    'vulnerability': match.group(3)
                })
        return vulnerabilities

    def generate_comprehensive_report(self) -> Dict[str, Any]:
        """
        Generate a comprehensive project review report
        """
        # Perform all analyses
        self.review_results['structural_analysis'] = self.structural_analysis()
        self.review_results['code_quality'] = self.code_quality_analysis()
        self.review_results['template_type_validation'] = self.template_type_validation()
        self.review_results['security_assessment'] = self.security_assessment()

        # Calculate overall project health
        health_score = self._calculate_project_health()
        
        return {
            'project_health_score': health_score,
            'detailed_results': self.review_results
        }

    def _calculate_project_health(self) -> float:
        """
        Calculate an overall project health score
        """
        # Initialize scoring components
        scores = {
            'structural_complexity': 0,
            'code_quality': 0,
            'template_type_coverage': 0,
            'security_rating': 0
        }

        # Structural Analysis Score
        structure_depth = len(self.review_results['structural_analysis'].get('directory_structure', {}))
        scores['structural_complexity'] = min(structure_depth * 10, 100)

        # Code Quality Score
        complexity_violations = sum(
            len(violations) 
            for violations in self.review_results['code_quality'].get('style_violations', {}).values()
        )
        scores['code_quality'] = max(100 - (complexity_violations * 5), 0)

        # Template Type Validation Score
        template_validation = self.review_results['template_type_validation']
        passed_templates = sum(1 for result in template_validation.values() if result.get('status') == 'PASS')
        scores['template_type_coverage'] = (passed_templates / 5) * 100

        # Security Assessment Score
        security_issues = sum(
            len(vulnerabilities) 
            for vulnerabilities in self.review_results['security_assessment'].get('bandit_scan', {}).values()
        )
        scores['security_rating'] = max(100 - (security_issues * 10), 0)

        # Weighted average
        total_score = sum(
            score * weight for score, weight in zip(
                scores.values(), 
                [0.2, 0.3, 0.25, 0.25]
            )
        )

        return round(total_score, 2)

    def export_report(self, output_path: Optional[str] = None):
        """
        Export comprehensive review report
        """
        report = self.generate_comprehensive_report()
        
        if output_path:
            with open(output_path, 'w') as f:
                json.dump(report, f, indent=2)
        
        return report

def main():
    """
    Main execution point for comprehensive project review
    """
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    reviewer = ComprehensiveProjectReviewer(project_root)
    
    print("🔍 Initiating Comprehensive Project Review...")
    report = reviewer.export_report('project_review_report.json')
    
    print("\n📊 Project Health Assessment:")
    print(f"Overall Health Score: {report['project_health_score']}/100")
    
    print("\n🚨 Key Findings:")
    for category, results in report['detailed_results'].items():
        print(f"\n{category.replace('_', ' ').title()}:")
        print(json.dumps(results, indent=2)[:500] + "...")  # Truncate for readability

if __name__ == '__main__':
    main()
