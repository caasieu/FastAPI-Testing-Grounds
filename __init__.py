from sqlmodel import SQLModel

def get_subclasses(cls):
  for subclass in cls.__subclasses__():
    yield from get_subclasses(subclass)
    yield subclass

models_dict = {cls.__name__: cls for cls in get_subclasses(SQLModel)}   

for cls in models_dict.values():
  cls.update_forward_refs(**models_dict)