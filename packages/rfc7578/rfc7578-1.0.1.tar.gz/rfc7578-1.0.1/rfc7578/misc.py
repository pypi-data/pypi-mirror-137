def force_bytes(anything):
    if isinstance(anything,bytes):
        return anything
    elif isinstance(anything,str):
        return anything.encode()
    else:
        return bytes(anything)
def force_string(anything):
    if isinstance(anything,str):
        return anything
    elif isinstance(anything,bytes):
        return anything.decode()
    else:
        return str(anything)

def items(dct):
    its=[]
    for k in dct:
        v=dct[k]
        if isinstance(v,list) or isinstance(v,tuple):
            for i in v:
                its.append([k,i])
        else:

            its.append([k,v])
    return its
