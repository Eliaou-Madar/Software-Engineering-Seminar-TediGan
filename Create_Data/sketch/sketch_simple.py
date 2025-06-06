import cv2
import numpy as np
import os
import sys

def sobel(img):
    opImgx = cv2.Sobel(img, cv2.CV_8U, 0, 1, ksize=3)
    opImgy = cv2.Sobel(img, cv2.CV_8U, 1, 0, ksize=3)
    return cv2.bitwise_or(opImgx, opImgy)

def sketch(frame):
    frame = cv2.GaussianBlur(frame, (3, 3), 0)
    invImg = 255 - frame
    edgImg0 = sobel(frame)
    edgImg1 = sobel(invImg)
    edgImg = cv2.addWeighted(edgImg0, 0.75, edgImg1, 0.75, 0)
    opImg = 255 - edgImg
    return opImg

def create_sketch(image_path):
    # Lire l’image
    original = cv2.imread(image_path)
    if original is None:
        print(f"Erreur : l’image '{image_path}' est introuvable.")
        return

    # Conversion en niveaux de gris
    gray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)

    # Créer le sketch
    sketch_img = sketch(gray)

    # Créer le nom du fichier de sortie
    basename = os.path.splitext(os.path.basename(image_path))[0]
    output_path = f"{basename}_sketch.jpg"

    # Sauvegarder le résultat
    cv2.imwrite(output_path, sketch_img)
    print(f"Sketch sauvegardé dans : {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage : python sketch_simple.py monimage.jpg")
    else:
        create_sketch(sys.argv[1])
