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

# (int) Target Android API
android.api = 33

# (int) Minimum API your APK will support
android.min_api = 21

# (str) Android SDK version to use
android.sdk = 33

# (str) Version of the Android build tools to use
android.build_tools_version = 33.0.0

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2
