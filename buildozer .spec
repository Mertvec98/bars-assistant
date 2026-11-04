[app]
title = Bars AI
package.name = barsassistant
package.domain = org.adam
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,gguf
version = 1.0
requirements = python3,kivy==2.3.0,cython==0.29.38,pillow
orientation = portrait
fullscreen = 1
android.permissions = CAMERA,RECORD_AUDIO,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 34
android.minapi = 21
android.ndk_api = 21
android.archs = arm64-v8a
paddles = False
