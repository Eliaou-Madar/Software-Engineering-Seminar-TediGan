Creer un sketch: 

python -m venv venv 
venv\Scripts\activate 
pip install opencv-python numpy 
cd C:\Users\eliao\OneDrive\Bureau\Create_Data_Tedigan\sketch 
python sketch_simple.py Capture.PNG 

Enlever le background: 

pip install rembg pillow 
pip install onnxruntime 
cd C:\Users\eliao\OneDrive\Bureau\Create_Data_Tedigan\remove_background 
python rembg.py Capture.png 

Générer 10 ligne de texte descriptif: 

cd C:\Users\eliao\OneDrive\Bureau\Create_Data_Tedigan\texte 
python create_captions.py --anno annotations.txt --n_captions 10 

Generer le label dune image:  

pip install torch torchvision transformers pillow numpy 
1) mask brut (0–18, très sombre) 
python label.py Capture.png 
2) mask coloré seul 
python label.py Capture.png --color 
3) overlay semi-transparent 
python label.py Capture.png --color --overlay -o Capture_overlay.png 
