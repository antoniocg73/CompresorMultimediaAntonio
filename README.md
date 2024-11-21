# CompresorMultimediaAntonio

## Generación del requirements (al cual hay que quitarle lo no utilizado)
pip freeze > requirements.txt

## Comando para conseguir el ejecutable
pyinstaller --onefile --add-data "imagenes;imagenes" --add-data "ffmpeg/bin;ffmpeg/bin" --icon="imagenes/reposteria.png" main.py

