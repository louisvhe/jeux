import tkinter as tk
import random

class FlappyBird:
    def __init__(self, root):
        self.root = root
        self.root.title("Flappy Python")
        self.canvas = tk.Canvas(root, width=400, height=500, bg="skyblue")
        self.canvas.pack()

        # Le "Bird"
        self.oiseau = self.canvas.create_oval(50, 250, 80, 280, fill="yellow")
        
        # Variables physiques
        self.gravite = 0.5
        self.vitesse_y = 0
        self.tuyaux = []
        self.score = 0
        self.en_vie = True

        # Score
        self.texte_score = self.canvas.create_text(200, 50, text="0", font=("Arial", 30), fill="white")

        # Contrôles
        self.root.bind("<space>", self.sauter)
        
        self.creer_tuyau()
        self.boucle_jeu()

    def sauter(self, event):
        if self.en_vie:
            self.vitesse_y = -8 # Impulsion vers le haut

    def creer_tuyau(self):
        trou = 120
        hauteur_haut = random.randint(50, 300)
        t_haut = self.canvas.create_rectangle(400, 0, 450, hauteur_haut, fill="green")
        t_bas = self.canvas.create_rectangle(400, hauteur_haut + trou, 450, 500, fill="green")
        self.tuyaux.append((t_haut, t_bas))

    def boucle_jeu(self):
        if not self.en_vie:
            return

        # Appliquer la gravité
        self.vitesse_y += self.gravite
        self.canvas.move(self.oiseau, 0, self.vitesse_y)

        # Déplacer les tuyaux
        for t_haut, t_bas in self.tuyaux[:]:
            self.canvas.move(t_haut, -5, 0)
            self.canvas.move(t_bas, -5, 0)
            
            # Vérifier si le tuyau est sorti de l'écran
            if self.canvas.coords(t_haut)[2] < 0:
                self.canvas.delete(t_haut)
                self.canvas.delete(t_bas)
                self.tuyaux.remove((t_haut, t_bas))
                self.score += 1
                self.canvas.itemconfig(self.texte_score, text=str(self.score))

        # Ajouter de nouveaux tuyaux
        if len(self.tuyaux) == 0 or self.canvas.coords(self.tuyaux[-1][0])[0] < 200:
            self.creer_tuyau()

        # Vérifier les collisions
        if self.verifier_mort():
            self.en_vie = False
            self.canvas.create_text(200, 250, text="GAME OVER", font=("Arial", 40), fill="red")
        else:
            self.root.after(20, self.boucle_jeu)

    def verifier_mort(self):
        pos = self.canvas.coords(self.oiseau)
        # Sortie écran (haut ou bas)
        if pos[1] <= 0 or pos[3] >= 500:
            return True
        
        # Collision avec les tuyaux
        items = self.canvas.find_overlapping(pos[0], pos[1], pos[2], pos[3])
        for item in items:
            if item != self.oiseau and item != self.texte_score:
                return True
        return False

if __name__ == "__main__":
    fenetre = tk.Tk()
    jeu = FlappyBird(fenetre)
    fenetre.mainloop()