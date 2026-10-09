[app]

# (str) Title of your application
title = Análisis Sport

# (str) Package name
package.name = analysissport

source.dir = .
version = 0.1

# (str) Package domain (needed for android packaging)
package.domain = org.analysissport

# (list) Source files to include (let it include python files and assets)
source.include_exts = py,png,jpg,kv,atlas

# (list) Application requirements
# Incluye aquí las librerías que uses en tu proyecto (ej: kivy, requests, etc.)
requirements = python3,kivy

# (str) Supported orientations
orientation = portrait

# (list) Permissions
android.permissions = INTERNET

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2
