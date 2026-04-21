import tkinter as tk
import random

class MemoryGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Memory Python")
        
        # Configuration
        self.symboles = list("AABBCCDDEEFFGGHH") # 8 paires
        random.shuffle(self.symboles)
        
        self.boutons = []
        self.selection = [] # Stocke les deux cartes choisies
        self.trouvees = 0
        
        # Grille de 4x4
        for i in range(16):
            btn = tk.Button(root, text=" ", font=("Arial", 24, "bold"), 
                            width=4, height=2, bg="gray",
                            command=lambda idx=i: self.clic_carte(idx))
            btn.grid(row=i//4, column=i%4, padx=5, pady=5)
            self.boutons.append(btn)

    def clic_carte(self, idx):
        bouton = self.boutons[idx]
        
        # On ne fait rien si la carte est déjà révélée ou si on a déjà 2 cartes en attente
        if bouton["text"] != " " or len(self.selection) >= 2:
            return
        
        # Révéler la carte
        bouton.config(text=self.symboles[idx], bg="white")
        self.selection.append(idx)
        
        if len(self.selection) == 2:
            self.root.after(1000, self.verifier_paire)

    def verifier_paire(self):
        idx1, idx2 = self.selection
        if self.symboles[idx1] == self.symboles[idx2]:
            # Paire trouvée !
            self.boutons[idx1].config(bg="lightgreen", state="disabled")
            self.boutons[idx2].config(bg="lightgreen", state="disabled")
            self.trouvees += 1
            if self.trouvees == 8:
                self.victoire()
        else:
            # Pas de match, on cache
            self.boutons[idx1].config(text=" ", bg="gray")
            self.boutons[idx2].config(text=" ", bg="gray")
            
        self.selection = []

    def victoire(self):
        label = tk.Label(self.root, text="Bravo ! Gagné !", font=("Arial", 16), fg="green")
        label.grid(row=4, column=0, columnspan=4)

if __name__ == "__main__":
    fenetre = tk.Tk()
    jeu = MemoryGame(fenetre)
    fenetre.mainloop()