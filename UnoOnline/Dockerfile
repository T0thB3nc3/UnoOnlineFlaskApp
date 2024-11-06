# Használjuk az nginx képet alapként
FROM nginx:alpine

# Átmásolja a template-eket a konténerbe
COPY ./WebApp/templates/index.html /usr/share/nginx/WebApp/templates/index.html

# Átmásolja a .py fájlokat a konténerbe
COPY ./WebApp/__init__.py /usr/share/nginx/WebApp/__init__.py
COPY ./WebApp/routes.py /usr/share/nginx/WebApp/routes.py
COPY ./run.py usr/share/nginx/run.py

# Alapértelmezett port beállítása
EXPOSE 8000

# Nginx elindítása (alapértelmezett CMD az nginx)
CMD [ "nginx" ]