
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from rains.kit.api.api_plant import ApiPlant


api_plant = ApiPlant()

a = api_plant.get('http://127.0.0.1:5000/get1')
print(a.data)

a = api_plant.post('http://127.0.0.1:5000/post1', data={'v1': 1, 'v2': 2})
print(a.data)

api_plant.set_token('123123123')
a = api_plant.post('http://127.0.0.1:5000/post2', data={'v1': 1, 'v2': 2})
print(a.data)
