import json
import os
import sys
from pathlib import Path


APP_DIR = Path(__file__).resolve().parent
os.chdir(APP_DIR)
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

import app


client = app.app.test_client()
results = {
    'health': client.get('/api/health').status_code,
    'chatbot_page': client.get('/chatbot').status_code,
    'chatbot_api': client.post('/api/chatbot', json={'message': 'I want to become a data analyst'}).status_code,
    'assessments': client.get('/api/assessments/questions').status_code,
    'counsellors': client.get('/api/counselling/counsellors').status_code,
    'verify': client.post('/api/candidate/verify', json={'skill_id': 'SKL-GJ-26-8F4A92', 'mobile_or_email': '9876543210'}).status_code,
    'booking': client.post('/api/counselling/book', json={'candidate_id': 1, 'counsellor_id': 1, 'slot_id': 1, 'reason': 'Need help', 'candidate_name': 'Demo Learner', 'skill_id': 'SKL-GJ-26-8F4A92'}).status_code,
    'payment': client.post('/api/counselling/pay', json={'booking_id': 1, 'candidate_id': 1, 'payment_method': 'UPI'}).status_code,
}

print(json.dumps(results, indent=2))
