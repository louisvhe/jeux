import tkinter as tk
import random
import time

class JeuReflexe:
    def __init__(self, root):
        self.root = root
        self.root.title("Chasseur de Carrés")
        
        # Stats
        self.score = 0
        self.temps_restant = 30
        self.partie_active = False

        # Interface
        self.label_score = tk.Label(root, text="Score : 0", font=("Arial", 14))
        self.label_score.pack()
        
        self.label_timer = tk.Label(root, text="Temps : 30s", font=("Arial", 14), fg="red")
        self.label_timer.pack()

        self.canvas = tk.Canvas(root, width=500, height=400, bg="white", highlightthickness=2, highlightbackground="black")
        self.canvas.pack(pady=10)

        self.btn_start = tk.Button(root, text="Démarrer la partie", command=self.demarrer)
        self.btn_start.pack(pady=5)

        # Le carré à cliquer
        self.cible = None

    def demarrer(self):
        if not self.partie_active:
            self.score = 0
            self.temps_restant = 20
            self.partie_active = True
            self.btn_start.config(state="disabled")
            self.maj_labels()
            self.apparaitre_cible()
            self.compte_a_rebours()

    def apparaitre_cible(self):
        self.canvas.delete("cible")
        if self.partie_active:
            taille = random.randint(20, 50)
            x = random.randint(0, 500 - taille)
            y = random.randint(0, 400 - taille)
            
            # Création d'une cible avec un tag pour l'identifier
            self.cible = self.canvas.create_rectangle(
                x, y, x + taille, y + taille, 
                fill=random.choice(["red", "blue", "green", "purple", "orange"]),
                tags="cible"
            )
            # On lie le clic sur la cible à la fonction 'clic_reussi'
            self.canvas.tag_bind("cible", "<Button-1>", self.clic_reussi)
            
            # La cible change de place après un certain temps même si on ne clique pas
            vitesse = max(400, 1000 - (self.score * 20)) # Ça devient plus dur !
            self.timer_cible = self.root.after(vitesse, self.apparaitre_cible)

    def clic_reussi(self, event):
        if self.partie_active:
            self.score += 1
            self.canvas.delete("cible")
            self.root.after_cancel(self.timer_cible) # On annule le déplacement prévu
            self.maj_labels()
            self.apparaitre_cible()

    def compte_a_rebours(self):
        if self.temps_restant > 0:
            self.temps_restant -= 1
            self.maj_labels()
            self.root.after(1000, self.compte_a_rebours)
        else:
            self.fin_partie()

    def maj_labels(self):
        self.label_score.config(text=f"Score : {self.score}")
        self.label_timer.config(text=f"Temps : {self.temps_restant}s")

    def fin_partie(self):
        self.partie_active = False
        self.canvas.delete("all")
        self.btn_start.config(state="normal")
        self.canvas.create_text(250, 200, text=f"TERMINÉ !\nScore final : {self.score}", 
                                font=("Arial", 25), justify="center")

if __name__ == "__main__":
    fenetre = tk.Tk()
    jeu = JeuReflexe(fenetre)
    fenetre.mainloop()