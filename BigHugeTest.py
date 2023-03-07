import requests

word = input('enter your word:')

api_key='1c87fa67aa9d6cc8c69cf2723cc0fa00'
url = f'https://words.bighugelabs.com/api/2/{api_key}/{word}/json'

response = requests.get(url)

if response.status_code == 200:
    # Parse the JSON response and extract the synonyms
    result = response.json()
    print (result)
    synonyms = [syn for value in result.values() for syn in value['syn']]
    print(synonyms[:10])
else:
    print("Error:", response.status_code)
