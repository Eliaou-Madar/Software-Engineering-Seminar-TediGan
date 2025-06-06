#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Génère N descriptions courtes par image à partir d’un fichier d’attributs.
Usage:
    python create_custom_captions.py --anno annotations.txt [--n_captions 10]
Les sorties seront écrites dans le dossier où se trouve ce script.
"""

import os
import argparse
from random import randint, choice, sample

# Nombre par défaut de captions par image
DEFAULT_N = 10

# Catégories et attributs
ATTRIBUTES = {
    'IsAttributes':   ['Smiling', 'Young', 'Male'],
    'HasAttributes':  ['Black_Hair', 'Eyeglasses'],
    'WearAttributes': [],
}

# Sujets selon genre
GENDER_SUBJECT = {
    'female': ['She', 'This woman', 'The woman', 'The person'],
    'male':   ['He', 'This man', 'The man', 'The person'],
}

# Listes de verbes
IS_VERBS   = [' is ', ' looks ', ' appears to be ']
HAVE_VERBS = [' has ', ' is with ']
WEAR_VERBS = [' wears ', ' is wearing ']

def parse_args():
    p = argparse.ArgumentParser(
        description="Génère N captions par image à partir d'un fichier d'attributs CelebA-HQ"
    )
    p.add_argument(
        '--anno', required=True,
        help="Fichier d'attributs (format CelebA-HQ)"
    )
    p.add_argument(
        '--n_captions', type=int, default=DEFAULT_N,
        help="Nombre de phrases à générer par image"
    )
    return p.parse_args()

def load_annotations(path):
    """Lit annotations.txt au format :
       1ʳᵉ ligne = nombre d'images,
       2ᵉ ligne = en-têtes (attributs),
       lignes suivantes = image_id val1 val2 ...
    """
    with open(path, 'r', encoding='utf-8') as f:
        lines = [l.strip() for l in f if l.strip()]
    num = int(lines[0])
    headers = lines[1].split()
    data = {}
    for line in lines[2:2+num]:
        parts = line.split()
        img_id, vals = parts[0], parts[1:]
        data[img_id] = dict(zip(headers, vals))
    return data

def get_subject(attr):
    """Choisit le pronom selon le genre (Male = 1 indique un homme)."""
    return GENDER_SUBJECT['male'] if attr.get('Male', '-1') == '1' else GENDER_SUBJECT['female']

def get_feature(attr):
    """
    Récupère pour chaque catégorie la liste des attributs :
    - si value == '1'  → 'Attribute'
    - si value == '-1' → 'not Attribute'
    """
    feat = {}
    for cat, items in ATTRIBUTES.items():
        lst = []
        for a in items:
            v = attr.get(a, '0')
            if v == '1':
                lst.append(a)
            elif v == '-1':
                lst.append('not ' + a)
        feat[cat] = lst
    return feat

def make_captions(attr, n):
    """Construit jusqu'à n captions pour un même jeu d'attributs."""
    subj_opts = get_subject(attr)
    feat      = get_feature(attr)
    captions = []
    for _ in range(n):
        parts = []
        # IsAttributes
        vals = feat.get('IsAttributes', [])
        if vals:
            parts.append(
                choice(subj_opts)
                + choice(IS_VERBS)
                + ', '.join(v.replace('_', ' ').lower() for v in vals)
            )
        # HasAttributes
        vals = feat.get('HasAttributes', [])
        if vals:
            parts.append(
                choice(subj_opts)
                + choice(HAVE_VERBS)
                + ', '.join(v.replace('_', ' ').lower() for v in vals)
            )
        # WearAttributes
        vals = feat.get('WearAttributes', [])
        if vals:
            parts.append(
                choice(subj_opts)
                + choice(WEAR_VERBS)
                + ', '.join(v.replace('_', ' ').lower() for v in vals)
            )
        # N’ajoute la phrase que si on a au moins un segment
        if parts:
            captions.append('. '.join(parts) + '.')
    return captions

def main():
    args = parse_args()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    annos = load_annotations(os.path.join(script_dir, args.anno))

    for img_id, attr in annos.items():
        caps = make_captions(attr, args.n_captions)
        name, _ = os.path.splitext(img_id)
        out_file = os.path.join(script_dir, f"{name}.txt")
        with open(out_file, 'w', encoding='utf-8') as f:
            if caps:
                f.write('\n'.join(caps))
            else:
                f.write('<!-- no attributes found -->')

    print(f"[✔] Généré {args.n_captions} captions par image dans «{script_dir}»")

if __name__ == "__main__":
    main()
