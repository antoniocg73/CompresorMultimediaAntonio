# CompresorMultimediaAntonio

## Generación del requirements (al cual hay que quitarle lo no utilizado)
pip freeze > requirements.txt

## Comando para conseguir el ejecutable
pyinstaller --onefile --add-binary "ffmpeg/bin/ffmpeg.exe;ffmpeg/bin/" --add-binary "ffmpeg/bin/ffprobe.exe;ffmpeg/bin/" --add-data "imagenes:imagenes" Compressly.py

sin ffmpeg, instalarlo en el equipo destino. 
pyinstaller --onefile --add-data "imagenes:imagenes" Compressly.py
