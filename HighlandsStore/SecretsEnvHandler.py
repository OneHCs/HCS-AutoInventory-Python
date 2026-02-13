from dotenv import load_dotenv

class SecretsEnvHandler:
    def __init__(self):
        load_dotenv("secret.env")