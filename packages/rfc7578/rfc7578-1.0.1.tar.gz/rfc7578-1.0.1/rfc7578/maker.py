import random
import string
from .file import File
from .misc import items,force_bytes
def _boundary():
    return ''.join(random.choices(string.ascii_letters+string.digits,k=10))
class Maker:
    def __init__(self,fields,boundary=None):
        if boundary is None:
            boundary=_boundary()
        self.boundary=boundary
        self.fields=fields
        self.headers={"Content-Type":"multipart/form-data; boundary="+self.boundary}
    def make(self):
        built=b''
        bdr=b'--'+self.boundary.encode()+b'\n'
        for field in items(self.fields):
            built+=bdr
            disp=b'Content-Disposition: form-data; name="'+force_bytes(field[0])+b'"'
            val=field[1]
            if isinstance(val,File):
                disp+=b'; filename="'+force_bytes(val.name)+b'"\nContent-Type: '+force_bytes(val.content_type)
                val=val.read()
            disp+=b'\n\n'
            disp+=force_bytes(val)+b'\n'
            built+=disp
        built+=bdr.strip()+b'--'
        return built

            




        
        

