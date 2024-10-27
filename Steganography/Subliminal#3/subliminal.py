import cv2
import numpy as np

# On divise l'image en groupe de 20 pixels
def split_image(image):
    h, w, _ = image.shape
    return [image[i:i+20, j:j+20] for j in range(0, w, 20) for i in range(0, h, 20)]  # Modifié pour parcourir en premier les lignes (verticalement) avant les colonnes

def hide_image(video_path, image_path, output_path):
    image = cv2.imread(image_path)
    image_parts = split_image(image)
    video = cv2.VideoCapture(video_path)
    
    width = int(video.get(3))
    height = int(video.get(4))
    
    # Utiliser un fichier AVI sans compression
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # Non compressé dans AVI
    out = cv2.VideoWriter(output_path, fourcc, 20.0, (width, height))

    i = 0

    # On itère sur toutes les frames de la vidéo
    while True:
        
        ret, frame = video.read()
        
        # Si la vidéo n'a plus de frames
        if not ret:
            break
        
        # Si il y a encore des parties de l'image à cacher
        if i < len(image_parts):
            x = (i // (height // 20)) * 20  # Colonne (de gauche à droite)
            y = (i % (height // 20)) * 20  # Ligne (de haut en bas)
            frame[y:y+20, x:x+20] = image_parts[i]
            i += 1
            out.write(frame)
        else:
            break
    
    # Libérer les ressources utilisées
    video.release()
    out.release()

def retrieve_image(video_path, output_path):
    video = cv2.VideoCapture(video_path)
    width = int(video.get(3))
    height = int(video.get(4))

    # Initialisation d'une image vide
    image = np.zeros((height, width, 3), np.uint8)

    i = 0
    while True:
        # Lire un frame de la vidéo
        ret, frame = video.read()
        if not ret:
            break

        # Récupérer les groupes de pixels dans le même ordre vertical
        x = (i // (height // 20)) * 20
        y = (i % (height // 20)) * 20
        image[y:y+20, x:x+20] = frame[y:y+20, x:x+20]
        i += 1
    
    cv2.imwrite(output_path, image)
    video.release()

# Exécution de la fonction pour cacher et récupérer l'image
hide_image('subliminal.mp4', 'flag.png', 'subliminal_hide.mp4')
retrieve_image('subliminal_hide.mp4', 'output_flag.png')
