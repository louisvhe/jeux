import tkinter as tk
import random
from tkinter import messagebox

class Demineur:
    def __init__(self, root):
        self.root = root
        self.root.title("Démineur")
        
        self.taille = 8
        self.nb_mines = 10
        self.boutons = {}
        self.mines = set()
        self.cases_decouvertes = 0
        
        self.creer_widgets()
        self.initialiser_jeu()

    def creer_widgets(self):
        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=10, pady=10)
        
        for r in range(self.taille):
            for c in range(self.taille):
                btn = tk.Button(self.frame, width=3, height=1, font=('Arial', 12, 'bold'),
                                relief="raised", bg="lightgrey")
                # Clic gauche : révéler / Clic droit : drapeau
                btn.bind('<Button-1>', lambda e, r=r, c=c: self.reveler(r, c))
                btn.bind('<Button-3>', lambda e, r=r, c=c: self.poser_drapeau(r, c))
                btn.grid(row=r, column=c)
                self.boutons[(r, c)] = btn

    def initialiser_jeu(self):
        # Placer les mines aléatoirement
        positions = [(r, c) for r in range(self.taille) for c in range(self.taille)]
        self.mines = set(random.sample(positions, self.nb_mines))

    def poser_drapeau(self, r, c):
        btn = self.boutons[(r, c)]
        if btn['text'] == "":
            btn.config(text="🚩", fg="red")
        elif btn['text'] == "🚩":
            btn.config(text="")

    def compter_mines_voisines(self, r, c):
        compte = 0
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if (r + dr, c + dc) in self.mines:
                    compte += 1
        return compte

    def reveler(self, r, c):
        btn = self.boutons[(r, c)]
        if (r, c) in self.mines:
            btn.config(text="💣", bg="red")
            messagebox.showinfo("BOOM", "Dommage, vous avez touché une mine !")
            self.root.destroy()
            return

        if btn['relief'] == "sunken": return # Déjà révélée

        mines_autour = self.compter_mines_voisines(r, c)
        btn.config(relief="sunken", bg="white")
        self.cases_decouvertes += 1
        
        if mines_autour > 0:
            btn.config(text=str(mines_autour), fg=self.couleur_nombre(mines_autour))
        else:
            # Si 0 mines autour, on révèle récursivement les voisins
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    nr, nc = r + dr, c + dc
                    if (nr, nc) in self.boutons and self.boutons[(nr, nc)]['relief'] == "raised":
                        self.reveler(nr, nc)

        if self.cases_decouvertes == (self.taille**2 - self.nb_mines):
            messagebox.showinfo("Victoire", "Bravo ! Vous avez déminé la zone.")
            self.root.destroy()

    def couleur_nombre(self, n):
        couleurs = {1: "blue", 2: "green", 3: "red", 4: "purple"}
        return couleurs.get(n, "black")

if __name__ == "__main__":
    fenetre = tk.Tk()
    jeu = Demineur(fenetre)
    fenetre.mainloop()