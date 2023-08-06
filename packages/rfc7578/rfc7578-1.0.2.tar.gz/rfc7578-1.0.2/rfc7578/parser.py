from .file import File
from .misc import force_bytes
from .field import Field
from io import BytesIO
class Parser:
    def __init__(self,headers):
        if 'Content-Type' not in headers:
            raise TypeError('no content-type header')
        if not headers['Content-Type'].startswith('multipart/form-data'):
            raise TypeError('invalid content-type ; must be multipart/form-data')
        self.boundary=force_bytes('--'+headers['Content-Type'].split(';')[1].split('=')[1])

    def parse(self,body):
        body=force_bytes(body)
        fields=body.split(self.boundary)[1:]
        fields=[self.parse_field(f) for f in fields]
        ret={}
        for field in fields:
            if field is None:
                continue

            field.name=field.name.decode()
            if field.name not in ret:
                ret[field.name]=[field]
            else:
                ret[field.name].append(field)
        return ret
    def parse_field(self,field):
        field=field.strip()
        if field==b'--':
            return
        field=BytesIO(field)
        if not field: return
        head=[]
        content=b''
        ishead=True
        
        for x in field:
            x=x.strip()
            if not x:
                break
            head.append(x)
        content=field.read()

        return Field(head,content)
                    
                
        


        
    
