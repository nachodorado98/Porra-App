from flask_login import UserMixin

class Usuario(UserMixin):

    def __init__(self, usuario:str, nombre:str, codigo_liga:str, admin:bool)->None:

        self.id=usuario
        self.nombre=nombre
        self.codigo_liga=codigo_liga
        self.admin=admin