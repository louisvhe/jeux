import tkinter as tk
import math
import random

# Configuration
LARG, HAUT = 600, 400
TAILLE_CASE = 64
MAP = [
    [1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,0,0,0,1,0,1],
    [1,0,1,0,0,0,0,1,0,1],
    [1,0,0,0,0,1,0,0,0,1],
    [1,0,0,1,1,1,1,1,0,1],
    [1,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1],
]

class DoomPython:
    def __init__(self, root):
        self.root = root
        self.root.title("Python FPS Prototype")
        self.canvas = tk.Canvas(root, width=LARG, height=HAUT, bg="black")
        self.canvas.pack()

        # Joueur
        self.px, self.py = 100, 100
        self.pa = 0.0 # Angle
        
        # Ennemis (x, y, vivant)
        self.ennemis = [[400, 100, True], [450, 350, True], [150, 350, True]]
        self.score = 0

        # Contrôles
        self.root.bind("<Left>", lambda e: self.tourner(-0.15))
        self.root.bind("<Right>", lambda e: self.tourner(0.15))
        self.root.bind("<Up>", lambda e: self.marcher(10))
        self.root.bind("<Down>", lambda e: self.marcher(-10))
        self.root.bind("<space>", self.tirer) # ESPACE pour tirer

        self.rendu()

    def tourner(self, da):
        self.pa += da
        self.rendu()

    def marcher(self, d):
        nx = self.px + math.cos(self.pa) * d
        ny = self.py + math.sin(self.pa) * d
        if MAP[int(ny/TAILLE_CASE)][int(nx/TAILLE_CASE)] == 0:
            self.px, self.py = nx, ny
        self.rendu()

    def tirer(self, event):
        # Animation flash de tir
        flash = self.canvas.create_oval(LARG/2-50, HAUT/2-50, LARG/2+50, HAUT/2+50, fill="yellow")
        self.root.after(50, lambda: self.canvas.delete(flash))

        # Vérifier si un ennemi est dans le viseur
        for en in self.ennemis:
            if not en[2]: continue
            
            # Calcul angle entre joueur et ennemi
            dx, dy = en[0] - self.px, en[1] - self.py
            angle_en = math.atan2(dy, dx)
            dist_en = math.sqrt(dx*dx + dy*dy)
            
            # Différence d'angle (normalisée entre -pi et pi)
            diff_a = (angle_en - self.pa + math.pi) % (2 * math.pi) - math.pi
            
            # Si l'ennemi est quasiment au centre du FOV (marge de 0.1 radians)
            if abs(diff_a) < 0.15 and dist_en < 400:
                en[2] = False # Mort !
                self.score += 1
                break
        self.rendu()

    def rendu(self):
        self.canvas.delete("all")
        # Plafond et Sol
        self.canvas.create_rectangle(0, 0, LARG, HAUT/2, fill="#222")
        self.canvas.create_rectangle(0, HAUT/2, LARG, HAUT, fill="#444")

        # 1. Rendu des Murs
        nb_rayons = 80
        fov = math.pi / 3
        for i in range(nb_rayons):
            angle_r = (self.pa - fov/2) + (i / nb_rayons) * fov
            for d in range(1, 600, 4):
                rx = self.px + math.cos(angle_r) * d
                ry = self.py + math.sin(angle_r) * d
                if MAP[int(ry/TAILLE_CASE)][int(rx/TAILLE_CASE)] == 1:
                    dist = d * math.cos(angle_r - self.pa)
                    h = (TAILLE_CASE * HAUT) / (dist + 0.1)
                    c = min(255, int(20000 / (dist + 1))) # Ombrage
                    couleur = f"#{c:02x}{c:02x}{c:02x}"
                    x_pos = i * (LARG/nb_rayons)
                    self.canvas.create_rectangle(x_pos, HAUT/2-h/2, x_pos+LARG/nb_rayons, HAUT/2+h/2, fill=couleur, outline="")
                    break

        # 2. Rendu des Ennemis (Sprites simplifiés)
        for en in self.ennemis:
            if not en[2]: continue
            dx, dy = en[0] - self.px, en[1] - self.py
            dist = math.sqrt(dx*dx + dy*dy)
            angle_en = math.atan2(dy, dx)
            diff_a = (angle_en - self.pa + math.pi) % (2 * math.pi) - math.pi
            
            if abs(diff_a) < fov/2: # Si dans le champ de vision
                screen_x = (0.5 + diff_a / fov) * LARG
                h = (TAILLE_CASE * HAUT) / (dist * math.cos(diff_a) + 0.1)
                self.canvas.create_rectangle(screen_x-h/4, HAUT/2-h/2, screen_x+h/4, HAUT/2+h/2, fill="green", outline="white")

        # Interface
        self.canvas.create_text(80, 20, text=f"Morts: {self.score}/3", fill="white", font=("Arial", 14))
        # Viseur
        self.canvas.create_line(LARG/2-10, HAUT/2, LARG/2+10, HAUT/2, fill="red")
        self.canvas.create_line(LARG/2, HAUT/2-10, LARG/2, HAUT/2+10, fill="red")

if __name__ == "__main__":
    root = tk.Tk()
    game = DoomPython(root)
    root.mainloop()