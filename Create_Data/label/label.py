# -*- coding: utf-8 -*-
"""
label.py : Génère un mask (brut ou coloré) et, avec --overlay, superpose le mask coloré
Usage :
    python label.py Capture.png
    python label.py Capture.png --color
    python label.py Capture.png --color --overlay
"""

import argparse, os
from PIL import Image
import numpy as np
import torch
import torch.nn.functional as F
from transformers import SegformerImageProcessor, SegformerForSemanticSegmentation

def get_palette():
    # Palette 19 classes, index = class ID
    palette = [0,0,0]  # 0 background = noir
    palette += [255,0,0]    # 1 skin = rouge
    palette += [0,255,255]  # 2 left eyebrow = cyan
    palette += [0,255,255]  # 3 right eyebrow = cyan
    palette += [0,255,255]  # 4 left eye = cyan
    palette += [0,255,255]  # 5 right eye = cyan
    palette += [0,255,0]    # 6 nose = vert
    palette += [255,0,0]    # 7 upper lip = rouge
    palette += [0,255,0]    # 8 bottom lip = vert
    palette += [0,0,255]    # 9 hair = bleu
    # Les autres classes on leur donne des couleurs génériques
    extras = [
        (128,  0,128),  # 10 hat = violet
        (255,165,  0),  # 11 earring = orange
        (255,255,  0),  # 12 necklace = jaune
        (  0,128,128),  # 13 neck = teal
        (128,128,  0),  # 14 cloth = olive
        (128,  0,  0),  # 15 earpiece = marron
        (  0,  0,128),  # 16 neck accessory = marine
        (128,128,128),  # 17 eye shadow = gris
        (192,192,192),  # 18 lipstick = argent
    ]
    for c in extras:
        palette += list(c)
    # Remplir jusqu'à 256*3
    palette += [0]* (256*3 - len(palette))
    return palette

def save_color_mask(mask: np.ndarray, path: str):
    pal = Image.fromarray(mask.astype(np.uint8), mode="P")
    pal.putpalette(get_palette())
    pal.save(path)

def overlay_mask(img: Image.Image, mask: Image.Image, alpha=0.5):
    """Superpose mask paletté (mode P) sur img (RGB) avec opacité alpha."""
    color_mask = mask.convert("RGBA")
    base = img.convert("RGBA")
    return Image.blend(base, color_mask, alpha)

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("input", help="Image d'entrée")
    p.add_argument("-o","--output", help="Fichier de sortie")
    p.add_argument("--color", action="store_true",
                   help="Générer mask coloré (paletté)")
    p.add_argument("--overlay", action="store_true",
                   help="Superposer mask coloré sur l'image")
    return p.parse_args()

def main():
    args = parse_args()
    if not os.path.isfile(args.input):
        raise FileNotFoundError(args.input)
    base, ext = os.path.splitext(args.input)
    out = args.output or (base + ("_ov" if args.overlay else "_label") + ".png")

    # 1. charger modèle
    proc = SegformerImageProcessor.from_pretrained("jonathandinu/face-parsing")
    model = SegformerForSemanticSegmentation.from_pretrained("jonathandinu/face-parsing")
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    # 2. pré-traiter l'image
    img = Image.open(args.input).convert("RGB")
    inputs = proc(images=img, return_tensors="pt").to(device)

    # 3. inférence
    with torch.no_grad():
        logits = model(**inputs).logits
    up = F.interpolate(logits,
                       size=img.size[::-1],
                       mode="bilinear",
                       align_corners=False)
    mask = up.argmax(dim=1)[0].cpu().numpy().astype(np.uint8)

    # 4. sauver
    if args.overlay or args.color:
        # créer mask coloré paletté temporaire
        tmp_mask = Image.fromarray(mask, mode="P")
        tmp_mask.putpalette(get_palette())
        if args.overlay:
            res = overlay_mask(img, tmp_mask)
        else:
            res = tmp_mask
    else:
        # mask brut niveau de gris
        res = Image.fromarray(mask)

    res.save(out)
    print(f"✔️  Sortie enregistrée → {out}")

if __name__ == "__main__":
    main()
