#!/usr/bin/env python3
"""
Historical Project Health Tracking System
"""

import os
import json
from datetime import datetime
import sqlite3
import matplotlib.pyplot as plt

class ProjectHealthTracker:
    def __init__(self, db_path='project_health_history.db'):
        """
        Initialize health tracking database
        """
        self.db_path = db_path
        self._initialize_database()

    def _initialize_database(self):
        """
        Create SQLite database for tracking project health
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS project_health (
                    timestamp TEXT PRIMARY KEY,
                    health_score REAL,
                    branch TEXT,
                    details JSON
                )
            ''')
            conn.commit()

    def record_health_metrics(self, report_path, branch='main'):
        """
        Record project health metrics from comprehensive review report
        """
        with open(report_path, 'r') as f:
            report = json.load(f)
        
        health_score = report.get('project_health_score', 0)
        timestamp = datetime.utcnow().isoformat()

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO project_health 
                (timestamp, health_score, branch, details) 
                VALUES (?, ?, ?, ?)
            ''', (
                timestamp, 
                health_score, 
                branch, 
                json.dumps(report['detailed_results'])
            ))
            conn.commit()

    def generate_health_trend_report(self, days=30, branch='main'):
        """
        Generate a trend report of project health
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT timestamp, health_score 
                FROM project_health 
                WHERE branch = ? 
                  AND timestamp >= datetime('now', ?)
                ORDER BY timestamp
            ''', (branch, f'-{days} days'))
            
            results = cursor.fetchall()

        # Visualize health trend
        timestamps = [datetime.fromisoformat(r[0]) for r in results]
        health_scores = [r[1] for r in results]

        plt.figure(figsize=(10, 6))
        plt.plot(timestamps, health_scores, marker='o')
        plt.title(f'Project Health Trend (Last {days} Days)')
        plt.xlabel('Date')
        plt.ylabel('Health Score')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('project_health_trend.png')

        return {
            'trend_data': results,
            'visualization_path': 'project_health_trend.png'
        }

    def identify_health_regression_points(self, threshold=10):
        """
        Identify significant health score regressions
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT 
                    timestamp, 
                    health_score, 
                    LAG(health_score) OVER (ORDER BY timestamp) as prev_score
                FROM project_health
                ORDER BY timestamp
            ''')
            
            regression_points = []
            for row in cursor.fetchall():
                timestamp, current_score, prev_score = row
                if prev_score is not None and (prev_score - current_score) >= threshold:
                    regression_points.append({
                        'timestamp': timestamp,
                        'previous_score': prev_score,
                        'current_score': current_score,
                        'regression': prev_score - current_score
                    })
        
        return regression_points

def main():
    """
    Main execution for health tracking
    """
    tracker = ProjectHealthTracker()
    
    # Record latest health metrics
    tracker.record_health_metrics('project_review_report.json')
    
    # Generate trend report
    trend_report = tracker.generate_health_trend_report()
    print("Health Trend Report Generated")
    
    # Identify regression points
    regressions = tracker.identify_health_regression_points()
    print("Potential Health Regressions:")
    for regression in regressions:
        print(f"Regression at {regression['timestamp']}: "
              f"Score dropped from {regression['previous_score']} to {regression['current_score']}")

if __name__ == '__main__':
    main()
