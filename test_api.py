import requests

url = 'http://localhost:8000/api/v1/user-data'

response = requests.post(url=url, data={'user_id': '12321', 'name': 'test2', 'phone_number': '1234567'})

print(response.status_code)