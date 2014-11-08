import os

__all__ = []

for f in os.listdir("./server_apis/"):
  if f.endswith(".py") and f!="__init__.py":
    __all__.append(f.replace(".py",""))