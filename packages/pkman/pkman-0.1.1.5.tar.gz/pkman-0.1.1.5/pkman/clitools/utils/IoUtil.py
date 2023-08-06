
def pickle_dump(obj,fp):
    import pickle
    with open(fp,'wb') as f:
        pickle.dump(obj,f)
def pickle_load(fp):
    import pickle
    with open(fp,'rb') as f:
        return pickle.load(f)
def json_load(f,encoding='utf-8',*args,**kwargs):
    import json
    with open(f,'r',encoding=encoding) as fp:
        return json.load(fp,*args,**kwargs)
def json_dump(obj,fp,encoding='utf-8',ensure_ascii=False,*args,**kwargs):
    import json
    with open(fp,'w',encoding=encoding) as f:
        json.dump(obj,f,ensure_ascii=ensure_ascii,*args,**kwargs)
def read_txt(path,encoding='utf-8'):
    with open(path,'r',encoding=encoding) as f:
        return f.read()
def write_txt(txt,path,encoding='utf-8'):
    with open(path,'w',encoding=encoding) as f:
        f.write(txt)

def yaml_load(f,encoding='utf-8',*args,**kwargs):
    import yaml
    with open(f,'r',encoding=encoding) as fp:
        return yaml.load(fp,*args,**kwargs)
def yaml_dump(obj,fp,encoding='utf-8',allow_unicode=True,**kwargs):
    import yaml
    with open(fp,'w',encoding=encoding) as f:
        yaml.safe_dump(obj,f,allow_unicode=allow_unicode,**kwargs)