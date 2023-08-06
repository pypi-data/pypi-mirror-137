from .cjk0 import cjk0
from .cjk1 import cjk1
from .cjk2 import cjk2
from .cjk3 import cjk3
idstable=cjk2
idstable.update(cjk3)
idstable.update(cjk1)
idstable.update(cjk0)
