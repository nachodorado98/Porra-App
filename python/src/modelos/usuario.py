from flask_login import UserMixin

class Usuario(UserMixin):

    def __init__(self, usuario:str, nombre:str, codigo_liga:str, imagen_perfil:str, admin:bool, paso_porra:int)->None:

        self.id=usuario
        self.nombre=nombre
        self.codigo_liga=codigo_liga
        self.imagen_perfil=imagen_perfil
        self.admin=admin
        self.paso_porra=paso_porra