import tkinter as tk
import random

class CourseJeu:
    def __init__(self, root):
        self.root = root
        self.root.title("Traffic Dodge")
        
        self.canvas = tk.Canvas(root, width=300, height=500, bg="#333333") # Route grise
        self.canvas.pack()
        
        # Dessiner les lignes de la route
        self.canvas.create_line(100, 0, 100, 500, fill="white", dash=(20, 20))
        self.canvas.create_line(200, 0, 200, 500, fill="white", dash=(20, 20))

        # Ma voiture (un rectangle bleu)
        self.joueur = self.canvas.create_rectangle(125, 400, 175, 460, fill="cyan", outline="white")
        
        self.obstacles = []
        self.score = 0
        self.vitesse = 5
        self.en_cours = True

        # Contrôles
        self.root.bind("<Left>", lambda e: self.deplacer(-25))
        self.root.bind("<Right>", lambda e: self.deplacer(25))
        
        self.ajouter_obstacle()
        self.actualiser()

    def deplacer(self, dx):
        pos = self.canvas.coords(self.joueur)
        # Empêcher de sortir de la route
        if 0 <= pos[0] + dx <= 250:
            self.canvas.move(self.joueur, dx, 0)

    def ajouter_obstacle(self):
        if self.en_cours:
            x_pos = random.choice([25, 125, 225]) # Trois voies possibles
            obs = self.canvas.create_rectangle(x_pos, -60, x_pos + 50, 0, fill="red")
            self.obstacles.append(obs)
            # Ajoute un nouvel obstacle de plus en plus vite
            intervalle = max(400, 1000 - (self.score * 10))
            self.root.after(intervalle, self.ajouter_obstacle)

    def actualiser(self):
        if not self.en_cours:
            return

        for obs in self.obstacles[:]:
            self.canvas.move(obs, 0, self.vitesse)
            pos_obs = self.canvas.coords(obs)
            
            # Vérifier si l'obstacle est dépassé
            if pos_obs[1] > 500:
                self.canvas.delete(obs)
                self.obstacles.remove(obs)
                self.score += 1
                if self.score % 5 == 0: self.vitesse += 0.5 # Accélération
            
            # Détection de collision
            pos_j = self.canvas.coords(self.joueur)
            if self.collision(pos_j, pos_obs):
                self.game_over()
                return

        self.root.after(20, self.actualiser)

    def collision(self, a, b):
        # Vérifie si deux rectangles se chevauchent
        return not (a[2] < b[0] or a[0] > b[2] or a[3] < b[1] or a[1] > b[3])

    def game_over(self):
        self.en_cours = False
        self.canvas.create_text(150, 250, text=f"CRASH !\nScore: {self.score}", 
                                fill="yellow", font=("Arial", 24, "bold"), justify="center")

if __name__ == "__main__":
    fenetre = tk.Tk()
    jeu = CourseJeu(fenetre)
    fenetre.mainloop()