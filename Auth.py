from .config import Config


class Auth:
    @staticmethod
    def check_request(req) -> bool:
        auth = req.headers.get('Authorization', '')
        if auth.startswith('Bearer '):
            token = auth.split(' ', 1)[1].strip()
            return token == Config.API_TOKEN
        return False
