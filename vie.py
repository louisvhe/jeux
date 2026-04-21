import tkinter as tk
import random

class JeuDeVie:
    def __init__(self, root):
        self.root = root
        self.root.title("L'Automate Cellulaire")
        
        self.taille_grille = 40
        self.cell_size = 15
        self.en_pause = True
        
        self.canvas = tk.Canvas(root, width=self.taille_grille*self.cell_size, 
                               height=self.taille_grille*self.cell_size, bg="white")
        self.canvas.pack()

        # Initialisation de la grille (0 = mort, 1 = vivant)
        self.grille = [[random.choice([0, 0, 0, 1]) for _ in range(self.taille_grille)] 
                       for _ in range(self.taille_grille)]

        # Contrôles
        btn_frame = tk.Frame(root)
        btn_frame.pack(fill="x")
        
        self.btn_play = tk.Button(btn_frame, text="Démarrer / Pause", command=self.basculer_pause)
        self.btn_play.pack(side="left")
        
        tk.Button(btn_frame, text="Réinitialiser", command=self.reset).pack(side="left")

        self.canvas.bind("<Button-1>", self.cliquer_cellule)
        self.boucle_simulation()

    def cliquer_cellule(self, event):
        # Permet de dessiner des cellules à la souris
        x, y = event.x // self.cell_size, event.y // self.cell_size
        self.grille[y][x] = 1 if self.grille[y][x] == 0 else 0
        self.dessiner()

    def basculer_pause(self):
        self.en_pause = not self.en_pause

    def reset(self):
        self.grille = [[0 for _ in range(self.taille_grille)] for _ in range(self.taille_grille)]
        self.dessiner()

    def verifier_voisins(self, x, y):
        compte = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0: continue
                nx, ny = (x + i) % self.taille_grille, (y + j) % self.taille_grille
                compte += self.grille[ny][nx]
        return compte

    def mise_a_jour_logique(self):
        nouvelle_grille = [[0 for _ in range(self.taille_grille)] for _ in range(self.taille_grille)]
        for y in range(self.taille_grille):
            for x in range(self.taille_grille):
                voisins = self.verifier_voisins(x, y)
                if self.grille[y][x] == 1:
                    nouvelle_grille[y][x] = 1 if voisins in [2, 3] else 0
                else:
                    nouvelle_grille[y][x] = 1 if voisins == 3 else 0
        self.grille = nouvelle_grille

    def dessiner(self):
        self.canvas.delete("all")
        for y in range(self.taille_grille):
            for x in range(self.taille_grille):
                if self.grille[y][x] == 1:
                    x1, y1 = x * self.cell_size, y * self.cell_size
                    self.canvas.create_rectangle(x1, y1, x1+self.cell_size, y1+self.cell_size, 
                                               fill="black", outline="gray")

    def boucle_simulation(self):
        if not self.en_pause:
            self.mise_a_jour_logique()
            self.dessiner()
        else:
            self.dessiner()
        self.root.after(100, self.boucle_simulation)

if __name__ == "__main__":
    root = tk.Tk()
    jeu = JeuDeVie(root)
    root.mainloop()