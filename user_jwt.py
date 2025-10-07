from jwt import encode, decode

def createToken(data: dict):
    token: str = encode(payload=data, key='misecret', algorithm='HS256') # La key debe ser secreta y estar guardada en una variable de entorno
    return token

def validateToken(token: str) -> dict:
    data: dict = decode(token, key='misecret', algorithms='HS256')
    return data