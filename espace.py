import tkinter as tk
import random
import string

# --- Configuration du jeu ---
LARG, HAUT = 600, 500
VITESSE_BASE = 0.5
INTERVALLE_BASE = 1500 # ms entre chaque ennemi
TAILLE_TEXTE = 14
FONTS = ("Courier New", TAILLE_TEXTE, "bold") # Police "Hacker"
TAILLE_ENNEMI = 20

class SpaceHacker:
    def __init__(self, root):
        self.root = root
        self.root.title("Space Hacker: Final Line")
        
        # Structure de l'écran
        # Zone de jeu (Action)
        self.canvas = tk.Canvas(root, width=LARG, height=HAUT-100, bg="#000011") # Espace sombre
        self.canvas.pack()
        
        # Zone de console (Saisie)
        self.console_frame = tk.Frame(root, height=100, bg="#111111")
        self.console_frame.pack(fill="x")
        
        # Éléments de la console
        tk.Label(self.console_frame, text="SYS@HACKER:>", font=FONTS, fg="cyan", bg="#111111").pack(side="left", padx=10)
        self.entree_console = tk.Entry(self.console_frame, font=FONTS, fg="#00FF00", bg="#111111", insertbackground="white", width=40)
        self.entree_console.pack(side="left", padx=5)
        self.entree_console.bind("<Return>", self.envoyer_commande)
        
        self.label_score = tk.Label(self.console_frame, text="SCORE: 0", font=FONTS, fg="yellow", bg="#111111")
        self.label_score.pack(side="right", padx=10)

        # Dessiner la ligne de défense
        self.ligne_def = self.canvas.create_line(0, HAUT-120, LARG, HAUT-120, fill="cyan", dash=(10, 10))
        self.canvas.create_text(LARG/2, HAUT-105, text="-- LIGNE DE DÉFENSE --", fill="cyan", font=("Arial", 10))

        # État du jeu
        self.ennemis = []
        self.score = 0
        self.niveau = 1
        self.perdu = False
        self.id_timer_spawn = None

        self.initialiser_niveau()
        self.boucle_principale()

    def initialiser_niveau(self):
        self.score = 0
        self.niveau = 1
        self.vitesse = VITESSE_BASE
        self.intervalle = INTERVALLE_BASE
        self.entree_console.delete(0, tk.END)
        self.nettoyer_ennemis()
        self.maj_score()
        self.lancer_spawn()

    def nettoyer_ennemis(self):
        for e in self.ennemis:
            self.canvas.delete(e['corps'])
            self.canvas.delete(e['label'])
        self.ennemis = []

    def generer_code(self):
        # Code plus long avec les niveaux
        longeur = min(8, 3 + self.niveau // 2)
        caract = string.ascii_uppercase + string.digits
        return "".join(random.choice(caract) for _ in range(longeur))

    def spawn_ennemi(self):
        if not self.perdu:
            # Position et code
            x = random.randint(50, LARG-50)
            code = self.generer_code()
            
            # Création visuelle (Corps + Code)
            corps = self.canvas.create_rectangle(x, -TAILLE_ENNEMI, x+TAILLE_ENNEMI, 0, fill="red", outline="white")
            label = self.canvas.create_text(x + TAILLE_ENNEMI/2, -TAILLE_ENNEMI*2, text=code, fill="white", font=FONTS)
            
            self.ennemis.append({'corps': corps, 'label': label, 'code': code, 'y': -TAILLE_ENNEMI*2})
            
            # Planifier le prochain spawn
            self.intervalle = max(300, INTERVALLE_BASE - (self.niveau * 100))
            self.id_timer_spawn = self.root.after(self.intervalle, self.spawn_ennemi)

    def lancer_spawn(self):
        if self.id_timer_spawn: self.root.after_cancel(self.id_timer_spawn)
        self.id_timer_spawn = self.root.after(self.intervalle, self.spawn_ennemi)

    def boucle_principale(self):
        if self.perdu: return

        for e in self.ennemis[:]:
            e['y'] += self.vitesse
            self.canvas.move(e['corps'], 0, self.vitesse)
            self.canvas.move(e['label'], 0, self.vitesse)
            
            # Vérifier la défaite
            if e['y'] > HAUT - 120:
                self.game_over()
                return

        # Augmenter la difficulté progressivement
        self.vitesse = VITESSE_BASE + (self.niveau * 0.1)
        
        self.root.after(30, self.boucle_principale)

    def envoyer_commande(self, event):
        cmd = self.entree_console.get().strip().upper()
        self.entree_console.delete(0, tk.END)
        
        trouve = False
        for e in self.ennemis[:]:
            if e['code'] == cmd:
                # Robot désactivé !
                trouve = True
                self.canvas.delete(e['corps'])
                self.canvas.delete(e['label'])
                self.ennemis.remove(e)
                self.score += len(cmd) * 10 # Plus long code = plus de points
                self.maj_score()
                break
        
        if not trouve and cmd != "":
            self.effets_visuels("red") # Feedback d'erreur

    def maj_score(self):
        self.niveau = 1 + self.score // 200
        self.label_score.config(text=f"LVL:{self.niveau} | SCORE:{self.score}")

    def effets_visuels(self, couleur):
        current_bg = self.entree_console.cget("bg")
        self.entree_console.config(bg=couleur)
        self.root.after(100, lambda: self.entree_console.config(bg=current_bg))

    def game_over(self):
        self.perdu = True
        if self.id_timer_spawn: self.root.after_cancel(self.id_timer_spawn)
        self.nettoyer_ennemis()
        self.canvas.create_text(LARG/2, HAUT/2, text=f"LIGNE PERDUE!\n\nScore Final: {self.score}", fill="red", font=("Courier New", 30, "bold"), justify="center")
        self.canvas.create_text(LARG/2, HAUT-50, text="-- Appuyez sur Entrée pour réessayer --", fill="yellow", font=("Arial", 12))
        self.root.bind("<Return>", self.recommencer)

    def recommencer(self, event):
        self.perdu = False
        self.canvas.delete("all")
        # Recréer la ligne
        self.ligne_def = self.canvas.create_line(0, HAUT-120, LARG, HAUT-120, fill="cyan", dash=(10, 10))
        self.canvas.create_text(LARG/2, HAUT-105, text="-- LIGNE DE DÉFENSE --", fill="cyan", font=("Arial", 10))
        self.initialiser_niveau()
        self.root.bind("<Return>", self.envoyer_commande)
        self.boucle_principale()

if __name__ == "__main__":
    root = tk.Tk()
    application = SpaceHacker(root)
    # Force le focus sur l'entrée de texte
    application.entree_console.focus_set()
    root.mainloop()