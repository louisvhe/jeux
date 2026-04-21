import tkinter as tk
from tkinter import messagebox
import random

class JeuDevinette:
    def __init__(self, root):
        self.root = root
        self.root.title("Le Nombre Secret")
        self.root.geometry("400x250")

        # Variables du jeu
        self.nombre_secret = random.randint(1, 100)
        self.tentatives = 0

        # Éléments de l'interface
        self.label_instruction = tk.Label(root, text="Devinez le nombre entre 1 et 100 :")
        self.label_instruction.pack(pady=20)

        self.entree_nombre = tk.Entry(root)
        self.entree_nombre.pack(pady=10)

        self.bouton_valider = tk.Button(root, text="Vérifier", command=self.verifier_choix)
        self.bouton_valider.pack(pady=20)

        self.label_feedback = tk.Label(root, text="", fg="blue")
        self.label_feedback.pack(pady=10)

    def verifier_choix(self):
        try:
            choix = int(self.entree_nombre.get())
            self.tentatives += 1

            if choix < self.nombre_secret:
                self.label_feedback.config(text="C'est plus ! ⬆️", fg="orange")
            elif choix > self.nombre_secret:
                self.label_feedback.config(text="C'est moins ! ⬇️", fg="orange")
            else:
                messagebox.showinfo("Bravo !", f"Gagné en {self.tentatives} coups !")
                self.reinitialiser_jeu()
        except ValueError:
            messagebox.showwarning("Erreur", "Veuillez entrer un nombre valide.")

    def reinitialiser_jeu(self):
        self.nombre_secret = random.randint(1, 100)
        self.tentatives = 0
        self.entree_nombre.delete(0, tk.END)
        self.label_feedback.config(text="")

# Lancement du jeu
if __name__ == "__main__":
    fenetre = tk.Tk()
    application = JeuDevinette(fenetre)
    fenetre.mainloop()