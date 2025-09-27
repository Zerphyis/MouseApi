import logging
from flask import jsonify

class HandleController:
    def __init__(self):
        logging.basicConfig(level=logging.ERROR)
        self.logger = logging.getLogger("HandleController")

    def handle(self, func):
        """
        Decorador para capturar exceções e retornar resposta padronizada.
        """
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                self.logger.error(f"Erro em {func.__name__}: {str(e)}", exc_info=True)
                return jsonify({
                    "status": "error",
                    "message": str(e),
                    "controller": func.__name__
                }), 500
        return wrapper
