"""SE CARGAN LAS CREDENCIALES DE credential.yml"""
import yaml

class LoadCredential:
    def __init__(self):
        self.config_file = 'credential.yml'
        self.config = self._load_file()

    def _load_file(self):
        with open(self.config_file, "r") as file:
            return yaml.safe_load(file)

    def get_user(self):
        # Devolver el valor del usuario
        return self.config['credentials']['username']

    def get_pass(self):
        # Devolver el valor de la contraseña
        return self.config['credentials']['password']