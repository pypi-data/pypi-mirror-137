from .file import File
class Field:
    def __init__(self,head,content):
        print(head)
        self.content=content
        disp=head[0]
        raw_data=disp.split(b'form-data;')[1].strip()
        data=dict([[i.strip().replace(b'"',b'') for i in x.split(b'=')] for x in raw_data.split(b';')])
        self.name=data[b'name']
        self.filename=data.get(b'filename')
        self.isfile=bool(self.filename)
        self.content_type='text/plain'
        for line in head[1:]:
            if line.split(b':')[0].strip()==b'Content-Type':
                self.content_type=line.split(b':')[1].strip()

        if self.isfile:
            self.file=File(content,self.filename,self.content_type)

