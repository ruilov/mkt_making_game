import os

__all__ = []

for f in os.listdir("./models/"):
  if f.endswith(".py") and f!="__init__.py":
    __all__.append(f.replace(".py",""))