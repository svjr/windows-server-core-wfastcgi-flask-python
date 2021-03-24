import datetime
from flask import request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash

from src.config.config import configuration
from src.config.init_config import logger
from functools import wraps
import jwt


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            token = request.args.get('token')
            if not token: return {'message': 'token não informado', 'data': []}, 401
            data = jwt.decode(token, configuration.applicacao_configuracaotoken_secret)
        except Exception as e:
            return {'message': 'token inválido ou expirado', 'data': []}, 401
        return f(*args, **kwargs)
    return decorated


def exec_auth():
    logger.info("Inicio do metodo [auth]")
    auth = request.authorization
    if not auth or not auth.username or not auth.password:  raise Exception("WWW-Authenticate': 'Basic auth=Login required")
    logger.info("====> Password Hash: " + generate_password_hash(auth.password))
    if auth.username != configuration.configuration_app.username:  raise Exception("Usuário incorreto")
    if check_password_hash(configuration.configuration_app.password, auth.password):
        exp_time = datetime.datetime.now() + datetime.timedelta(hours=12)
        token = jwt.encode({'username': configuration.configuration_app.username, 'exp': exp_time},configuration.configuration_app.token_secret)
        return {'message': 'Login realizado com sucesso', 'token': token.decode('UTF-8'), 'exp': exp_time}
    else:
        raise Exception("Senha Incorreta")