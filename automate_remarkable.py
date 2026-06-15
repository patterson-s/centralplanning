import pyautogui
import pygetwindow as gw
import time

# Attendre 3 secondes pour que vous puissiez vous positionner sur le bureau
time.sleep(3)

# Appuyer sur la touche Windows
pyautogui.hotkey('win')

# Attendre un court instant pour que le menu Démarrer s'ouvre
time.sleep(0.5)

# Taper "remarkable"
pyautogui.write("remarkable")

# Attendre un court instant pour que la recherche s'affiche
time.sleep(0.5)

# Appuyer sur la touche Entrée
pyautogui.press('enter')

# Attendre que l'application Remarkable s'ouvre et se synchronise
time.sleep(15)

# Cliquer au centre de la fenêtre Remarkable
try:
    # Obtenir la fenêtre Remarkable
    remarkable_window = gw.getWindowsWithTitle("Remarkable")[0]
    
    # Calculer le centre de la fenêtre
    center_x = remarkable_window.left + (remarkable_window.width // 2)
    center_y = remarkable_window.top + (remarkable_window.height // 2)
    
    # Cliquer au centre
    pyautogui.click(center_x, center_y)
    print(f"Cliqué au centre de la fenêtre Remarkable : ({center_x}, {center_y})")
except IndexError:
    print("Fenêtre Remarkable non trouvée. Cliquer au centre de l'écran à la place.")
    screen_width, screen_height = pyautogui.size()
    pyautogui.click(screen_width // 2, screen_height // 2)

# Appuyer sur Ctrl + F pour ouvrir la recherche
pyautogui.hotkey('ctrl', 'f')

# Attendre un court instant pour que la barre de recherche s'affiche
time.sleep(0.5)

# Taper "exploit"
pyautogui.write("exploit")

# Attendre un court instant pour que les résultats s'affichent
time.sleep(0.5)

# Appuyer sur la flèche vers le bas pour sélectionner le premier résultat
pyautogui.press('down')

# Attendre un court instant
time.sleep(0.3)

# Appuyer sur Entrée
pyautogui.press('enter')

# Attendre un court instant
time.sleep(0.3)

# Appuyer sur Ctrl + Entrée
pyautogui.hotkey('ctrl', 'enter')

# Attendre un court instant
time.sleep(0.3)

# Appuyer sur Ctrl + Entrée une seconde fois
pyautogui.hotkey('ctrl', 'enter')

# Attendre un court instant
time.sleep(0.3)

# Sélectionner tout avec Ctrl + A
pyautogui.hotkey('ctrl', 'a')

# Attendre un court instant
time.sleep(0.3)

# Copier avec Ctrl + C
pyautogui.hotkey('ctrl', 'c')

# Attendre un court instant pour que la copie soit terminée
time.sleep(0.5)

# Fermer l'application avec Alt + F4
pyautogui.hotkey('alt', 'f4')

# Attendre un court instant pour que l'application se ferme
time.sleep(1)

# Récupérer le contenu du presse-papiers
import pyperclip

# Lire le contenu copié
copied_text = pyperclip.paste()

# Générer le nom du fichier avec la date et un numéro incrémentiel
from datetime import datetime
import os

# Chemin du dossier de sortie
output_dir = r"C:\Users\spatt\Desktop\RemarkableExploit\processed"

# Créer le dossier s'il n'existe pas
os.makedirs(output_dir, exist_ok=True)

# Obtenir la date actuelle au format YYYYMMDD
today_date = datetime.now().strftime("%Y%m%d")

# Trouver le numéro incrémentiel pour aujourd'hui
# Lister tous les fichiers dans le dossier qui commencent par file_YYYYMMDD_
existing_files = [
    f for f in os.listdir(output_dir) 
    if f.startswith(f"file_{today_date}_") and f.endswith(".md")
]

# Extraire les numéros existants et trouver le prochain
file_numbers = []
for f in existing_files:
    try:
        # Extraire le numéro après la date (format: file_YYYYMMDD_n.md)
        n = int(f.split("_")[2].split(".")[0])
        file_numbers.append(n)
    except (IndexError, ValueError):
        pass

# Déterminer le prochain numéro
next_n = max(file_numbers) + 1 if file_numbers else 1

# Générer le nom du fichier
filename = f"file_{today_date}_{next_n}.md"

# Chemin complet du fichier
filepath = os.path.join(output_dir, filename)

# Ajouter la date au début du contenu (sans l'heure)
timestamp = datetime.now().strftime("%Y-%m-%d")
content = f"# Exploit - {timestamp}\n\n{copied_text}"

# Écrire le contenu dans le fichier
with open(filepath, "w", encoding="utf-8") as file:
    file.write(content)

print(f"Contenu enregistré dans : {filepath}")
print("Script terminé.")