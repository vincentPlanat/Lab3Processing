# Dockerfile

# Image for Dedalus test env
# FROM python:3.13-slim

# Image for vpl raspberry test env
FROM arm64v8/python:3.12-slim-bookworm

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers de l'application dans le conteneur
COPY mllp /app

# Installer les dépendances de l'application
# (Si requirements.txt existe, sinon cette ligne est inutile)
RUN pip install --no-cache-dir -r requirements.txt

# Spécifier la commande pour exécuter l'application
#CMD ["python", "server_side/mllp_server.py", "-c", "$MY_COMMENTS"]
#CMD python server_side/mllp_server.py
CMD python server_side/mllp_server.py -c $MY_COMMENTS -o $MY_OUTDIR