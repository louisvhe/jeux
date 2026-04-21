import tkinter as tk
import random

class Pong:
    def __init__(self, root):
        self.root = root
        self.root.title("Pong Solo")
        self.root.resizable(False, False)

        self.canvas = tk.Canvas(root, width=600, height=400, bg="black")
        self.canvas.pack()

        # Raquette
        self.raquette = self.canvas.create_rectangle(0, 0, 100, 10, fill="white")
        self.canvas.move(self.raquette, 250, 370)

        # Balle
        self.balle = self.canvas.create_oval(10, 10, 30, 30, fill="yellow")
        
        # Vitesse de la balle (pixels par mise à jour)
        self.dx = random.choice([-3, 3])
        self.dy = -3
        
        # Liaison de la souris
        self.canvas.bind("<Motion>", self.deplacer_raquette)
        
        self.jouer()

    def deplacer_raquette(self, event):
        # La raquette suit le mouvement X de la souris
        x = event.x
        self.canvas.coords(self.raquette, x - 50, 370, x + 50, 380)

    def jouer(self):
        # Déplacer la balle
        self.canvas.move(self.balle, self.dx, self.dy)
        pos = self.canvas.coords(self.balle) # [x1, y1, x2, y2]

        # Rebond murs latéraux
        if pos[0] <= 0 or pos[2] >= 600:
            self.dx *= -1
        
        # Rebond plafond
        if pos[1] <= 0:
            self.dy *= -1

        # Rebond sur la raquette
        pos_raquette = self.canvas.coords(self.raquette)
        if pos[3] >= pos_raquette[1] and pos[2] >= pos_raquette[0] and pos[0] <= pos_raquette[2]:
            if self.dy > 0: # Évite que la balle reste collée
                self.dy *= -1
                self.dy -= 0.5 # Accélère un peu à chaque rebond
                self.dx += 0.5 if self.dx > 0 else -0.5

        # Game Over
        if pos[3] >= 400:
            self.canvas.create_text(300, 200, text="GAME OVER", fill="red", font=("Arial", 30))
        else:
            self.root.after(10, self.jouer)

if __name__ == "__main__":
    fenetre = tk.Tk()
    jeu = Pong(fenetre)
    fenetre.mainloop()