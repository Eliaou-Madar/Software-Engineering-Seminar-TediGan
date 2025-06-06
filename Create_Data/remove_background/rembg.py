# rembg.py
# -*- coding: utf-8 -*-
import sys
import os

# 1) Empêcher l'ombre locale (script) de masquer le package 'rembg'
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir in sys.path:
    sys.path.remove(script_dir)

# 2) S'assurer que site-packages est dans la recherche de modules
import site
for sp in site.getsitepackages() + [site.getusersitepackages()]:
    if os.path.isdir(os.path.join(sp, 'rembg')):
        sys.path.insert(0, sp)
        break

# 3) Importer l'API de suppression de fond
from rembg import remove
from PIL import Image

def main():
    if len(sys.argv) < 2:
        print("Usage : python rembg.py <input_image> [<output_image>]")
        sys.exit(1)

    in_path = sys.argv[1]
    if not os.path.isfile(in_path):
        print(f"[✘] Le fichier '{in_path}' n'existe pas.")
        sys.exit(1)

    # Extraction de l'extension (en minuscule) pour détecter le format d'entrée
    base, ext = os.path.splitext(in_path)
    ext_lower = ext.lower()

    # Formats d'entrée généralement pris en charge par Pillow
    supported_in = {'.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff', '.tif'}
    if ext_lower not in supported_in:
        print(f"[! ] Attention : '{ext}' n’est pas un format d’image standard reconnu.")
        print("       Le script va tenter de l’ouvrir, mais le résultat n’est pas garanti.")

    # Si l'utilisateur fournit un chemin de sortie, on l'utilise ;
    # sinon on génère automatiquement avec suffixe "_no_bg" en .png
    if len(sys.argv) >= 3:
        out_path = sys.argv[2]
        # Si l’extension de sortie n’est pas .png, on la remplace par .png
        _, out_ext = os.path.splitext(out_path)
        if out_ext.lower() not in ('.png',):
            out_path = os.path.splitext(out_path)[0] + ".png"
    else:
        # On force la sortie en .png pour préserver la transparence
        out_path = f"{base}_no_bg.png"

    try:
        # Ouvrir l’image d’entrée (quelque soit le format)
        img = Image.open(in_path).convert("RGBA")
    except Exception as e:
        print(f"[✘] Impossible d’ouvrir '{in_path}' : {e}")
        sys.exit(1)

    try:
        # Suppression du fond
        result = remove(img)
        # Sauvegarde en PNG (RGBA)
        result.save(out_path, format="PNG")
    except Exception as e:
        print(f"[✘] Erreur lors de la suppression du fond : {e}")
        sys.exit(1)

    print(f"[✔] Fond supprimé → {out_path}")

if __name__ == "__main__":
    main()
