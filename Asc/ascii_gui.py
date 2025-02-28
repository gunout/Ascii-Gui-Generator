from PIL import Image, ImageDraw, ImageFont
import math
import tkinter as tk
from tkinter import messagebox, Scale
from tkinterdnd2 import TkinterDnD, DND_FILES  # Bibliothèque pour le glisser-déposer

# Définir les caractères pour l'art ASCII
chars = "Gleaphe __ Gvq Crew "[::-1]
charArray = list(chars)
charLength = len(charArray)
interval = charLength / 256

# Paramètres par défaut
oneCharWidth = 10
oneCharHeight = 18

def getChar(inputInt):
    return charArray[math.floor(inputInt * interval)]

def generate_ascii_art(image_path, scale_factor):
    try:
        # Ouvrir l'image
        im = Image.open(image_path)
        print(f"Image chargée : {image_path}")

        # Convertir l'image en mode RGB si elle est en mode RGBA
        if im.mode == 'RGBA':
            im = im.convert('RGB')

        width, height = im.size
        im = im.resize((int(scale_factor * width), int(scale_factor * height * (oneCharWidth / oneCharHeight))), Image.NEAREST)
        width, height = im.size
        pix = im.load()

        outputImage = Image.new('RGB', (oneCharWidth * width, oneCharHeight * height), color=(0, 0, 0))
        d = ImageDraw.Draw(outputImage)

        for i in range(height):
            for j in range(width):
                r, g, b = pix[j, i]
                h = int(r / 3 + g / 3 + b / 3)
                d.text((j * oneCharWidth, i * oneCharHeight), getChar(h), font=fnt, fill=(r, g, b))

        # Sauvegarder l'image ASCII
        outputImage.save('output.png')

        # Afficher un message de succès
        messagebox.showinfo("Succès", "L'art ASCII a été généré avec succès !")
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur s'est produite : {str(e)}")

def handle_drop(event):
    # Récupérer le chemin du fichier déposé
    file_path = event.data.strip('{}')  # Supprimer les accolades ajoutées par tkinterdnd2
    if file_path:
        # Afficher le chemin en majuscules dans l'interface
        file_path_upper = file_path.upper()
        entry_path.delete(0, tk.END)
        entry_path.insert(0, file_path_upper)
        # Stocker le chemin original (sensible à la casse) dans une variable globale
        global original_file_path
        original_file_path = file_path

def start_generation():
    global original_file_path
    if original_file_path:
        scale_factor = scale.get() / 100.0  # Convertir le pourcentage en facteur d'échelle
        generate_ascii_art(original_file_path, scale_factor)
    else:
        messagebox.showwarning("Avertissement", "Veuillez glisser-déposer une image.")

# Utiliser TkinterDnD pour la fonctionnalité de glisser-déposer
root = TkinterDnD.Tk()
root.title("Générateur d'art ASCII")

# Charger la police personnalisée
try:
    fnt = ImageFont.truetype('Plymouth D.ttf', 25)  # Utiliser la police Heylabs Stroyed.ttf
except Exception as e:
    messagebox.showerror("Erreur de police", f"La police Plymouth D.ttf n'a pas pu être chargée : {str(e)}")
    exit()

# Variable pour stocker le chemin original du fichier
original_file_path = None

# Frame pour les contrôles
frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

# Zone de texte pour afficher le chemin du fichier en majuscules
label_path = tk.Label(frame, text="Glissez-déposez une image ici :")
label_path.grid(row=0, column=0, sticky="w")

entry_path = tk.Entry(frame, width=50)
entry_path.grid(row=1, column=0, padx=5, pady=5)

# Réglage de l'échelle
label_scale = tk.Label(frame, text="Échelle (définition) :")
label_scale.grid(row=2, column=0, sticky="w")

scale = Scale(frame, from_=10, to=200, orient=tk.HORIZONTAL, length=300)
scale.set(50)  # Valeur par défaut (50%)
scale.grid(row=3, column=0, pady=10)

# Bouton pour générer l'art ASCII
button_generate = tk.Button(frame, text="Générer l'art ASCII", command=start_generation)
button_generate.grid(row=4, column=0, pady=10)

# Activer le glisser-déposer sur la fenêtre principale
root.drop_target_register(DND_FILES)
root.dnd_bind('<<Drop>>', handle_drop)

# Lancer l'interface
root.mainloop()