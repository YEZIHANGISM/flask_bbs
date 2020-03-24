from flask import jsonify

class HttpCode(object):
    ok = 200
    unautherror = 401
    paramerror = 400
    servererror = 500

def to_json(code, message, data=None):
    return jsonify({"code":code, "message":message, "data":data})

def success(message=None, data=None):
    return to_json(code=HttpCode.ok, message=message, data=data)

def unauth_error(message=None):
    return to_json(code=HttpCode.unautherror, message=message)

def param_error(message=None):
    return to_json(code=HttpCode.paramerror, message=message)

def server_error(message=None):
    return to_json(code=HttpCode.servererror, message=message)