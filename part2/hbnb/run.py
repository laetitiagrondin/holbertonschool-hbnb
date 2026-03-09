""" Point d'entrée principal pour lancer l'application.
Lance le serveur de développement.
"""
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
