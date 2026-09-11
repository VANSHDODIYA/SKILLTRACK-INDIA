import os
os.chdir(r"C:\Users\VANSH\OneDrive\hackathon\Skilltrackaizipped\SkillTrackAI")
import app
client = app.app.test_client()
page = client.get('/chatbot')
api = client.post('/api/chatbot', json={'message': 'I want to become a data analyst'})
print('chatbot_page', page.status_code)
print('chatbot_api', api.status_code)
print(api.get_json())
