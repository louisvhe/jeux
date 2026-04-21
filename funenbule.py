import tkinter as tk
import random
import time

# --- Configuration ---
LARG, HAUT = 400, 500
LARG_PLATEFORME = 200
HAUT_PLATEFORME = 20
LARG_BARRE = 100
HAUT_BARRE = 10
PUISSANCE_VENT_BASE = 0.2
FORCE_CONTROLE = 1.0

class FunambuleJeu:
    def __init__(self, root):
        self.root = root
        self.root.title("Le Funambule Numérique")
        
        self.canvas = tk.Canvas(root, width=LARG, height=HAUT, bg="#e0f7fa") # Ciel clair
        self.canvas.pack()

        # Dessiner le décor simplifié
        self.canvas.create_rectangle(0, HAUT-50, LARG, HAUT, fill="#8d6e63", outline="") # Sol
        self.canvas.create_line(LARG/2, HAUT-50, LARG/2, HAUT/2 + 50, fill="black", width=2) # Poteau

        # Plateforme d'équilibre
        self.plateforme = self.canvas.create_rectangle(LARG/2 - LARG_PLATEFORME/2, HAUT/2, 
                                                     LARG/2 + LARG_PLATEFORME/2, HAUT/2 + HAUT_PLATEFORME, 
                                                     fill="#616161", outline="white")

        # La barre d'équilibre (Le Funambule)
        self.barre = self.canvas.create_rectangle(LARG/2 - LARG_BARRE/2, HAUT/2 - HAUT_BARRE, 
                                                 LARG/2 + LARG_BARRE/2, HAUT/2, 
                                                 fill="#f44336", outline="white")

        # État du jeu
        self.pos_barre_x = LARG/2
        self.vitesse_barre = 0.0
        self.force_vent = 0.0
        self.score = 0
        self.temps_debut = time.time()
        self.perdu = False
        self.niveau = 1

        # Affichage Score et Vent
        self.text_score = self.canvas.create_text(LARG-70, 30, text="Temps: 0s", font=("Arial", 12, "bold"))
        self.text_vent = self.canvas.create_text(70, 30, text="Vent: Neutre", font=("Arial", 10), fill="blue")
        
        # Flèche du vent visuelle
        self.fleche_vent = self.canvas.create_line(LARG/2, 60, LARG/2, 60, fill="blue", arrow=tk.LAST, width=3)

        # Contrôles
        self.root.bind("<Left>", lambda e: self.controler(-FORCE_CONTROLE))
        self.root.bind("<Right>", lambda e: self.controler(FORCE_CONTROLE))
        
        # Initialisation du vent
        self.changer_vent()
        self.boucle_principale()

    def controler(self, force):
        if not self.perdu:
            self.vitesse_barre += force

    def changer_vent(self):
        if not self.perdu:
            # Vent aléatoire entre -1 et 1, multiplié par la puissance du niveau
            puissance = PUISSANCE_VENT_BASE * (1 + self.niveau * 0.2)
            self.force_vent = random.uniform(-puissance, puissance)
            
            # Mise à jour visuelle du vent
            direction = "Gauche ⬅️" if self.force_vent < -0.05 else "Droite ➡️" if self.force_vent > 0.05 else "Neutre"
            color = "red" if abs(self.force_vent) > puissance * 0.7 else "blue"
            self.canvas.itemconfig(self.text_vent, text=f"Vent: {direction}", fill=color)
            
            # Flèche du vent
            longueur_fleche = self.force_vent * 100
            self.canvas.coords(self.fleche_vent, LARG/2, 60, LARG/2 + longueur_fleche, 60)
            
            # Planifier le prochain changement de vent (plus rapide à haut niveau)
            intervalle = max(500, 3000 - self.niveau * 200)
            self.root.after(intervalle, self.changer_vent)

    def boucle_principale(self):
        if self.perdu: return

        # 1. Appliquer la Physique
        # Le vent influence la vitesse
        self.vitesse_barre += self.force_vent
        
        # La gravité/déséquilibre naturel (plus on est loin du centre, plus on tombe vite)
        desequilibre = (self.pos_barre_x - LARG/2) * 0.01
        self.vitesse_barre += desequilibre
        
        # Appliquer la vitesse à la position
        self.pos_barre_x += self.vitesse_barre
        
        # Déplacer la barre visuellement
        self.canvas.coords(self.barre, self.pos_barre_x - LARG_BARRE/2, HAUT/2 - HAUT_BARRE, 
                                     self.pos_barre_x + LARG_BARRE/2, HAUT/2)

        # 2. Vérifier la Défaite
        if self.pos_barre_x - LARG_BARRE/2 < LARG/2 - LARG_PLATEFORME/2 or \
           self.pos_barre_x + LARG_BARRE/2 > LARG/2 + LARG_PLATEFORME/2:
            self.game_over()
            return

        # 3. Mettre à jour Score et Niveau
        self.score = int(time.time() - self.temps_debut)
        self.niveau = 1 + self.score // 10
        self.canvas.itemconfig(self.text_score, text=f"Temps: {self.score}s")

        self.root.after(20, self.boucle_principale)

    def game_over(self):
        self.perdu = True
        self.canvas.create_text(LARG/2, HAUT/2 - 50, text="CHUTE !", fill="red", font=("Arial", 36, "bold"))
        self.canvas.create_text(LARG/2, HAUT/2 + 20, text=f"Score final: {self.score} secondes\nNiveau atteint: {self.niveau}", 
                                fill="black", font=("Arial", 14), justify="center")
        
        self.canvas.create_text(LARG/2, HAUT-20, text="-- Appuyez sur Espace pour réessayer --", fill="#333", font=("Arial", 10))
        self.root.bind("<space>", self.recommencer)

    def recommencer(self, event):
        self.perdu = False
        self.canvas.delete("all")
        # Recréer le décor
        self.canvas.create_rectangle(0, HAUT-50, LARG, HAUT, fill="#8d6e63", outline="") # Sol
        self.canvas.create_line(LARG/2, HAUT-50, LARG/2, HAUT/2 + 50, fill="black", width=2) # Poteau
        self.plateforme = self.canvas.create_rectangle(LARG/2 - LARG_PLATEFORME/2, HAUT/2, 
                                                     LARG/2 + LARG_PLATEFORME/2, HAUT/2 + HAUT_PLATEFORME, 
                                                     fill="#616161", outline="white")
        self.barre = self.canvas.create_rectangle(LARG/2 - LARG_BARRE/2, HAUT/2 - HAUT_BARRE, 
                                                 LARG/2 + LARG_BARRE/2, HAUT/2, 
                                                 fill="#f44336", outline="white")
        # Affichages
        self.text_score = self.canvas.create_text(LARG-70, 30, text="Temps: 0s", font=("Arial", 12, "bold"))
        self.text_vent = self.canvas.create_text(70, 30, text="Vent: Neutre", font=("Arial", 10), fill="blue")
        self.fleche_vent = self.canvas.create_line(LARG/2, 60, LARG/2, 60, fill="blue", arrow=tk.LAST, width=3)

        # Reset état
        self.pos_barre_x = LARG/2
        self.vitesse_barre = 0.0
        self.temps_debut = time.time()
        self.niveau = 1
        self.root.unbind("<space>")
        
        self.changer_vent()
        self.boucle_principale()

if __name__ == "__main__":
    root = tk.Tk()
    game = FunambuleJeu(root)
    root.mainloop()