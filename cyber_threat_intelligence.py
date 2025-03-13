import requests
import json
import csv
import sqlite3
from datetime import datetime
from typing import List, Dict

class ThreatIntelligence:
    def __init__(self, db_name: str):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        with self.conn:
            self.conn.execute('''CREATE TABLE IF NOT EXISTS threats (
                                    id INTEGER PRIMARY KEY,
                                    source TEXT,
                                    threat_type TEXT,
                                    description TEXT,
                                    date_reported TEXT
                                )''')
    
    def insert_threat(self, source: str, threat_type: str, description: str, date_reported: str):
        with self.conn:
            self.conn.execute('''INSERT INTO threats (source, threat_type, description, date_reported)
                                VALUES (?, ?, ?, ?)''', (source, threat_type, description, date_reported))

    def fetch_threats(self) -> List[Dict]:
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM threats')
        rows = cursor.fetchall()
        return [{'id': row[0], 'source': row[1], 'threat_type': row[2],
                 'description': row[3], 'date_reported': row[4]} for row in rows]

class ThreatFeed:
    def __init__(self, api_url: str):
        self.api_url = api_url

    def fetch_data(self) -> List[Dict]:
        response = requests.get(self.api_url)
        if response.status_code == 200:
            return json.loads(response.text)
        else:
            return []

class CSVExporter:
    @staticmethod
    def export_to_csv(data: List[Dict], file_name: str):
        with open(file_name, mode='w', newline='') as csv_file:
            fieldnames = data[0].keys() if data else []
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for entry in data:
                writer.writerow(entry)

def main():
    db_name = 'threats.db'
    api_url = 'https://api.example.com/threats'
    exporter_file_name = f'threats_export_{datetime.now().strftime("%Y%m%d")}.csv'

    threat_intelligence = ThreatIntelligence(db_name)
    threat_feed = ThreatFeed(api_url)

    threats_data = threat_feed.fetch_data()
    for threat in threats_data:
        threat_intelligence.insert_threat(
            source=threat.get('source', 'Unknown'),
            threat_type=threat.get('type', 'Unknown'),
            description=threat.get('description', 'No description'),
            date_reported=threat.get('reported_at', datetime.now().isoformat())
        )

    all_threats = threat_intelligence.fetch_threats()
    CSVExporter.export_to_csv(all_threats, exporter_file_name)

if __name__ == '__main__':
    main()