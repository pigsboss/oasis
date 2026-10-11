"""OASIS catalogue subsystem (targets layer).

Config-driven source-catalogue updater: downloads/refreshes the catalogues
listed in `catalogues.yaml` and writes a delivery manifest per catalogue
(id | path | bytes | sha256 | version | epoch | provider | licence).
"""

__version__ = "0.1.0"
