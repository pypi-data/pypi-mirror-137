try:
    from PySet2 import uic
except (ModuleNotFoundError, ImportError):
    from . import uic
print("This settings page is Built with PySet2")
