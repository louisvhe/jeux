import tkinter as tk
import random
from tkinter import messagebox

TAILLE = 3  # Grille de 3x3 (tu peux changer en 4 pour le vrai Puzzle 15)
COTE = 100  # Taille d'une case en pixels

class Taquin:
    def __init__(self, root):
        self.root = root
        self.root.title("Jeu du Taquin")
        
        self.grille = []
        self.boutons = {}
        self.case_vide = (TAILLE - 1, TAILLE - 1)
        
        self.creer_grille()
        self.melanger()
        self.dessiner_grille()

    def creer_grille(self):
        # On crée une liste de nombres de 1 à 8 (pour un 3x3) + le vide (None)
        nombres = list(range(1, TAILLE**2)) + [None]
        idx = 0
        for r in range(TAILLE):
            ligne = []
            for c in range(TAILLE):
                ligne.append(nombres[idx])
                idx += 1
            self.grille.append(ligne)

    def dessiner_grille(self):
        # On nettoie la fenêtre avant de redessiner
        for widget in self.root.winfo_children():
            widget.destroy()

        for r in range(TAILLE):
            for c in range(TAILLE):
                valeur = self.grille[r][c]
                if valeur is not None:
                    btn = tk.Button(self.root, text=str(valeur), font=("Arial", 20, "bold"),
                                    width=5, height=2, bg="lightblue",
                                    command=lambda r=r, c=c: self.deplacer(r, c))
                    btn.grid(row=r, column=c, padx=2, pady=2)
                else:
                    # La case vide est juste un espace vide dans la grille
                    self.case_vide = (r, c)

    def deplacer(self, r, c):
        vr, vc = self.case_vide
        # On vérifie si la case cliquée est adjacente à la case vide
        if (abs(r - vr) == 1 and c == vc) or (abs(c - vc) == 1 and r == vr):
            # Échange des valeurs dans la matrice
            self.grille[vr][vc], self.grille[r][c] = self.grille[r][c], self.grille[vr][vc]
            self.dessiner_grille()
            self.verifier_victoire()

    def melanger(self):
        # On simule 100 mouvements aléatoires pour que le puzzle soit solvable
        mouvements = 0
        while mouvements < 100:
            r, c = random.randint(0, TAILLE-1), random.randint(0, TAILLE-1)
            vr, vc = self.case_vide
            if (abs(r - vr) == 1 and c == vc) or (abs(c - vc) == 1 and r == vr):
                self.grille[vr][vc], self.grille[r][c] = self.grille[r][c], self.grille[vr][vc]
                self.case_vide = (r, c)
                mouvements += 1

    def verifier_victoire(self):
        actuel = [val for ligne in self.grille for val in ligne]
        gagnant = list(range(1, TAILLE**2)) + [None]
        if actuel == gagnant:
            messagebox.showinfo("Bravo !", "Vous avez reconstitué le puzzle !")

if __name__ == "__main__":
    fenetre = tk.Tk()
    jeu = Taquin(fenetre)
    fenetre.mainloop()