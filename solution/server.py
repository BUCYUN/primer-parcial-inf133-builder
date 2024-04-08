from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import urlparse

characters = {}

class Character:
    def __init__(self):
        self.name = None
        self.level = None
        self.role = None
        self.charisma = None
        self.strength = None
        self.dexterity = None

    def __str__(self):
        return f"name: {self.name}, level: {self.level}, role: {self.role}, charisma: {self.charisma}, strength: {self.strength}, dexterity: {self.dexterity}"
    
class CharacterBuilder:
    def __init__(self):
        self.character = Character()

    def set_name(self, name):
        self.character.name = name
        
    def set_level(self, level):
        self.character.level = level
    
    def set_role(self, role):
        self.character.role = role
        
    def set_charisma(self, charisma):
        self.character.charisma = charisma
        
    def set_strength(self, strength):
        self.character.strength = strength
        
    def set_dexterity(self, dexterity):
        self.character.dexterity = dexterity

    def get_character(self):
        return self.character
    
class Game:
    def __init__(self, builder):
        self.builder = builder

    def create_character(self, name, level, role, charisma, strength, dexterity):
        self.builder.set_name(name)
        self.builder.set_level(level)
        self.builder.set_role(role)
        self.builder.set_charisma(charisma)
        self.builder.set_strength(strength)
        self.builder.set_dexterity(dexterity)
        return self.builder.get_character()   


class CharacterService:
    def __init__(self):
        def __init__(self):
            self.builder = CharacterBuilder()
            self.game = Game(self.builder)

    def create_character(self, post_data):
        name = post_data.get("name", None)
        level = post_data.get("level", None)       
        role = post_data.get("role", None)
        charisma = post_data.get("charisma", None)
        strength = post_data.get("strength", None)
        dexterity = post_data.get("dexterity", None)
        character = self.game.create_character(id, name, level, role, charisma, strength, dexterity)
        
        return character

    def read_characters(self):
        return {index: character.__dict__ for index, character in characters.items()}
    
    def read_archer_create_characters(self):
        archer_create_characters = {}
        for index, create_character in characters.items():
            if create_character.role == "Archer" and create_character.level == 5 and create_character.charisma == 10:
                archer_create_characters[index] = create_character.to_dict()
        return archer_create_characters


    def update_character(self, id, post_data):
        if id in characters:
            character = characters[id]
            id = post_data.get("id", None)
            name = post_data.get("name", None)
            level = post_data.get("level", None)       
            role = post_data.get("role", None)
            charisma = post_data.get("charisma", None)
            strength = post_data.get("strength", None)
            dexterity = post_data.get("dexterity", None)
            
            if name:
                character.name = name
            if level:
                character.level = level
            if role:
                character.role = role
            if charisma:
                character.charisma = charisma
            if strength:
                character.strength = strength
            if dexterity:
                character.dexterity = dexterity
            return character
        else:
            return None

    def delete_character(self, id):
        if id in characters:
            return characters.pop(id)
        else:
            return None

class CharacterHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.character_service = CharacterService()
        super().__init__(*args, **kwargs)

    def do_POST(self):
        if self.path == "/characters":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            character_data = json.loads(post_data)
            new_character = self.character_service.create_character(character_data)
            self.send_response(201)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"message": "Character created successfully", "character": new_character.__dict__}).encode())
        else:
            self.send_response(404)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Endpoint not found"}).encode())

    def do_GET(self):
        if self.path == "/characters":
            characters_list = self.character_service.read_characters()
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(characters_list).encode())
        elif self.path == "/archer_create_characters":
            archer_create_characters_list = self.character_service.read_archer_create_characters()
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(archer_create_characters_list).encode())
        else:
            self.send_response(404)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Endpoint not found"}).encode())

    def do_PUT(self):
        if self.path.startswith("/characters/"):
            character_id = int(self.path.split("/")[2])
            content_length = int(self.headers["Content-Length"])
            put_data = self.rfile.read(content_length)
            update_data = json.loads(put_data)
            updated_character = self.character_service.update_character(character_id, update_data)
            if updated_character:
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"message": "Character updated successfully", "character": updated_character.__dict__}).encode())
            else:
                self.send_response(404)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Character not found"}).encode())
        else:
            self.send_response(404)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Endpoint not found"}).encode())

    def do_DELETE(self):
        if self.path.startswith("/characters/"):
            character_id = int(self.path.split("/")[2])
            deleted_character = self.character_service.delete_character(character_id)
            if deleted_character:
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"message": "Character deleted successfully", "deleted_character": deleted_character.__dict__}).encode())
            else:
                self.send_response(404)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Character not found"}).encode())
        else:
            self.send_response(404)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Endpoint not found"}).encode())


def run(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

if __name__ == "__main__":
    run()