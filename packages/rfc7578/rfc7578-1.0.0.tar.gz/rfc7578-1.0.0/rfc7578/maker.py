import random
import string
from .file import File
from .misc import items
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
        built=''
        bdr='--'+self.boundary+'\n'
        for field in items(self.fields):
            built+=bdr
            disp='Content-Disposition: form-data; name="'+field[0]+'"'
            val=field[1]
            if isinstance(val,File):
                disp+='; filename="'+val.name+'"\nContent-Type: '+val.content_type
                val=val.read().decode()
            disp+='\n\n'
            disp+=val+'\n'
            built+=disp
        built+=bdr.strip()+'--'
        return built.encode()

            




        
        

