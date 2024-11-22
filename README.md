# CompresorMultimediaAntonio

## Generación del requirements (al cual hay que quitarle lo no utilizado)
pip freeze > requirements.txt

### Necesarios en mi caso
- ffmpeg-python==0.2.0
- imageio==2.36.0
- imageio-ffmpeg==0.5.1
- Kivy==2.3.0
- kivy-deps.angle==0.4.0
- kivy-deps.glew==0.3.1
- kivy-deps.sdl2==0.7.0
- Kivy-Garden==0.1.5
- kivymd==1.2.0
- moviepy==1.0.3
- pillow==11.0.0
- pydub==0.25.1

## Comando para conseguir el ejecutable
pyinstaller --onefile --add-binary "ffmpeg/bin/ffmpeg.exe;ffmpeg/bin/" --add-binary "ffmpeg/bin/ffprobe.exe;ffmpeg/bin/" --add-data "imagenes:imagenes" --add-data "vc_redist.x64.exe;." --icon "imagenes/reposteria.ico" Compressly.py



