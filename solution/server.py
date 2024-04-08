from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import urlparse, parse_qs

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
        self.builder = CharacterBuilder()
        self.game = Game(self.builder)

    def create_character(self, post_data):
        name = post_data.get("name", None)
        level = post_data.get("level", None)       
        role = post_data.get("role", None)
        charisma = post_data.get("charisma", None)
        strength = post_data.get("strength", None)
        dexterity = post_data.get("dexterity", None)
        character = self.game.create_character(name, level, role, charisma, strength, dexterity)
        characters[len(characters)+1] = character
        return character

    def read_characters(self):
        return {index: character.__dict__ for index, character in characters.items()}
    
    def read_archer(self):
        archer = {}
        for index, character in characters.items():
            if character.role == "Archer" and character.level == 5 and character.charisma == 10:
                archer[index] = character.__dict__
        return archer

    def update_character(self, id, post_data):
        if id in characters:
            character = characters[id]
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

class HTTPDataHandler:
    @staticmethod
    def handle_response(handler, status, data):
        handler.send_response(status)
        handler.send_header("Content-type", "application/json")
        handler.end_headers()
        handler.wfile.write(json.dumps(data).encode("utf-8"))

    @staticmethod
    def handle_reader(handler):
        content_length = int(handler.headers["Content-Length"])
        post_data = handler.rfile.read(content_length)
        return json.loads(post_data.decode("utf-8"))

class CharacterHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.controller = CharacterService()
        super().__init__(*args, **kwargs)

    def do_POST(self):
        if self.path == "/characters":
            data = HTTPDataHandler.handle_reader(self)
            response_data = self.controller.create_character(data)
            HTTPDataHandler.handle_response(self, 200, response_data.__dict__)
        else:
            HTTPDataHandler.handle_response(self, 404, {"Error": "Ruta no existente"})
            
    def do_GET(self):
        if self.path == "/characters":
            response_data = self.controller.read_characters()
            HTTPDataHandler.handle_response(self, 200, response_data)
            
        elif self.path == "/characters/archer":
            archer = self.controller.read_archer()
            HTTPDataHandler.handle_response(self, 200, archer)
        else:
            HTTPDataHandler.handle_response(self, 404, {"Error": "Ruta no existente"})
 

    def do_PUT(self):
        if self.path.startswith("/characters/"):
            id = int(self.path.split("/")[2])
            data = HTTPDataHandler.handle_reader(self)
            response_data = self.controller.update_character(id, data)
            if response_data:
                HTTPDataHandler.handle_response(self, 200, response_data.__dict__)
            else:
                HTTPDataHandler.handle_response(
                    self, 404, {"Error": "id de personaje no válido"}
                )
        else:
            HTTPDataHandler.handle_response(self, 404, {"Error": "Ruta no existente"})

    def do_DELETE(self):
        if self.path.startswith("/characters/"):
            id = int(self.path.split("/")[2])
            deleted_character = self.controller.delete_character(id)
            if deleted_character:
                HTTPDataHandler.handle_response(
                    self, 200, {"message": "Personaje eliminado correctamente"}
                )
            else:
                HTTPDataHandler.handle_response(
                    self, 404, {"Error": "id de personaje no válido"}
                )
        else:
            HTTPDataHandler.handle_response(self, 404, {"Error": "Ruta no existente"})


def run(server_class=HTTPServer, handler_class=CharacterHandler, port=8000):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Iniciando servidor HTTP en puerto {port}...")
    httpd.serve_forever()


if __name__ == "__main__":
    run()