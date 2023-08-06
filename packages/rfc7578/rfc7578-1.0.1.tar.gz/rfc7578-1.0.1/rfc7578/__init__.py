from .parser import Parser
from .maker import Maker
from .file import File

def parse(headers,body):
    return Parser(headers).parse(body)
def make(fields):
    maker=Maker(fields)
    return maker.headers,maker.make()
