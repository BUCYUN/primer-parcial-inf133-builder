import requests

url = "http://localhost:8000/characters"
headers = {'Content-type': 'application/json'}

new_personaje1 = {
    "name": "Gandalf",
    "level": 10,
    "role": "Wizard",
    "charisma": 15,
    "strength": 10,
    "dexterity": 10
}
new_personaje2 = {
    "name": "Aragon",
    "level": 10,
    "role": "Warrior",
    "charisma": 15,
    "strength": 10,
    "dexterity": 10
}
new_personaje3 = {
    "name": "Robin",
    "level": 5,
    "role": "Archer",
    "charisma": 10,
    "strength": 10,
    "dexterity": 10
}
new_personaje4 = {
    "name": "Legolas",
    "level": 5,
    "role": "Archer",
    "charisma": 15,
    "strength": 10,
    "dexterity": 10
}
response = requests.post(url, json=new_personaje1, headers=headers)
response = requests.post(url, json=new_personaje2, headers=headers)
response = requests.post(url, json=new_personaje3, headers=headers)
response = requests.post(url, json=new_personaje4, headers=headers)

response = requests.get(url)
print(response.json())
response = requests.get(url + "/archer")
print(response.json())

response = requests.get(url + "/?role=Arecher&level=5&charisma=10")
update_personaje = {
    "charisma": 20,
    "strength": 15,
    "dexterity": 15
}

response = requests.put(url+ "/2", json=update_personaje, headers=headers)

response = requests.delete(url + "/1")
print(response.json())

response = requests.get(url+ "/2")
print(response.json())

