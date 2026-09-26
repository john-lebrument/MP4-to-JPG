# MP4 to Images Studio 🎬 ➡️ 🖼️

Application **Windows** moderne pour charger une vidéo, sélectionner une séquence à l'aide de marqueurs de début et de fin, et **exporter l'intégralité des trames** au format d'image de votre choix.

---

## ✨ Fonctionnalités

- **Import facile**
  - Bouton `Ouvrir une vidéo...` (`.mp4`, `.mov`, `.avi`, `.mkv`, etc.)
  - Support complet du **glisser-déposer** (drag & drop)
- **Lecteur vidéo & découpe de séquence**
  - Lecture / pause fluide (barre d'espace)
  - Déplacement pas-à-pas à la trame près (`⏮ -1 trame`, `⏭ +1 trame`, flèches du clavier)
  - Marqueur de début **[In]** (vert) et de fin **[Out]** (rouge)
  - Timeline visuelle avec la zone sélectionnée en surbrillance
  - Compteur d'images estimées et durée exacte au millième de seconde
- **Options d'extraction**
  - Formats : `JPG` (qualité 10-100 %), `PNG` (sans perte), `WEBP`, `BMP`
  - Cadence : toutes les images, 1/2, 1/5, 1/10, ou 1 image/seconde
  - Dossier de destination et préfixe de fichiers personnalisables
- **Performances & confort**
  - Extraction multithreadée avec OpenCV, sans blocage de l'interface
  - Barre de progression avec vitesse en temps réel (images/s)
  - Annulation en cours de route
  - Ouverture directe du dossier de sortie dans l'Explorateur
  - Thèmes sombre et clair

---

## 🚀 Démarrage rapide (avec Python installé)

```bash
python -m venv venv
# Windows
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Ou utilisez directement **`run.bat`** : il crée l'environnement virtuel s'il manque, installe les dépendances automatiquement, puis lance l'application.

### Lancement silencieux (sans console)
Double-cliquez sur **`Lancer_Application.vbs`** pour lancer l'application sans fenêtre de console.

---

## 💻 Compilation en exécutable autonome (.exe)

Pour générer un `.exe` unique fonctionnant **sans Python** sur n'importe quel PC Windows :

1. Exécutez une première fois `run.bat` (pour créer le `venv`).
2. Double-cliquez sur **`compilation_exe.bat`**.
3. Le fichier autonome est généré dans `dist\MP4_to_Images_Studio.exe`.

---

## ⌨️ Raccourcis clavier

| Touche      | Action                              |
|-------------|-------------------------------------|
| `Espace`    | Lecture / Pause                     |
| `←` `→`     | Reculer / Avancer d'une trame       |
| `I`         | Définir le point de début (**In**)  |
| `O`         | Définir le point de fin (**Out**)   |

---

## 🧱 Structure

```
app.py              # Interface graphique (PyQt6)
extractor.py        # Thread d'extraction des trames (OpenCV)
timeline_slider.py  # Widget de timeline personnalisé
run.bat             # Lancement + init automatique de l'environnement
compilation_exe.bat # Compilation du .exe autonome
requirements.txt    # Dépendances Python
```

## 📦 Dépendances

- Python 3.10+
- [PyQt6](https://pypi.org/project/PyQt6/)
- [opencv-python](https://pypi.org/project/opencv-python/)

## 📄 Licence

Projet sous licence MIT — voir [LICENSE](LICENSE).