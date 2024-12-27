import tkinter as tk
from tkinter import messagebox
import json


# Charger les tâches depuis un fichier JSON
def charger_taches():
    try:
        with open('taches.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []


# Sauvegarder les tâches dans un fichier JSON
def sauvegarder_taches(taches):
    with open('taches.json', 'w') as f:
        json.dump(taches, f, indent=4)


# Ajouter une tâche
def ajouter_tache():
    tache = entree_tache.get()
    if tache != "":
        taches.append({"nom": tache, "terminée": False})
        entree_tache.delete(0, tk.END)
        afficher_taches()
        sauvegarder_taches(taches)
    else:
        messagebox.showwarning("Entrée invalide", "Veuillez entrer une tâche.")


# Marquer une tâche comme terminée
def marquer_terminée(index):
    taches[index]["terminée"] = True
    afficher_taches()
    sauvegarder_taches(taches)


# Supprimer une tâche
def supprimer_tache(index):
    del taches[index]
    afficher_taches()
    sauvegarder_taches(taches)


# Modifier une tâche
def editer_tache(index):
    tache_a_editer = taches[index]["nom"]

    # Créer une nouvelle fenêtre de saisie pour modifier la tâche
    def enregistrer_modifications():
        nouveau_nom = entree_modification.get()
        if nouveau_nom != "":
            taches[index]["nom"] = nouveau_nom
            afficher_taches()
            sauvegarder_taches(taches)
            modification_window.destroy()
        else:
            messagebox.showwarning("Entrée invalide", "Le nom de la tâche ne peut pas être vide.")

    # Créer une fenêtre pour l'édition
    modification_window = tk.Toplevel(fenetre)
    modification_window.title("Modifier la tâche")

    # Label et champ de saisie pour la modification
    label_modification = tk.Label(modification_window, text="Modifier la tâche :", font=('Arial', 12))
    label_modification.pack(pady=10)

    entree_modification = tk.Entry(modification_window, font=('Arial', 14), width=40)
    entree_modification.insert(0, tache_a_editer)  # Afficher le nom actuel de la tâche
    entree_modification.pack(pady=10)

    # Bouton pour enregistrer la modification
    bouton_enregistrer = tk.Button(modification_window, text="Enregistrer", font=('Arial', 12),
                                   command=enregistrer_modifications)
    bouton_enregistrer.pack(pady=10)


# Afficher les tâches dans la fenêtre
def afficher_taches():
    for widget in frame_taches.winfo_children():
        widget.destroy()

    for index, tache in enumerate(taches):
        # Créer une étiquette pour chaque tâche
        texte_tache = tache["nom"] + (" (Terminée)" if tache["terminée"] else "")
        label_tache = tk.Label(frame_taches, text=texte_tache, font=('Arial', 12), width=50, anchor="w")
        label_tache.grid(row=index, column=0, padx=10, pady=5)

        # Ajouter un bouton pour marquer la tâche comme terminée
        if not tache["terminée"]:
            bouton_terminer = tk.Button(frame_taches, text="Terminer", command=lambda i=index: marquer_terminée(i))
            bouton_terminer.grid(row=index, column=1, padx=10, pady=5)

        # Ajouter un bouton pour supprimer la tâche
        bouton_supprimer = tk.Button(frame_taches, text="Supprimer", command=lambda i=index: supprimer_tache(i))
        bouton_supprimer.grid(row=index, column=2, padx=10, pady=5)

        # Ajouter un bouton pour éditer la tâche
        bouton_editer = tk.Button(frame_taches, text="Editer", command=lambda i=index: editer_tache(i))
        bouton_editer.grid(row=index, column=3, padx=10, pady=5)


# Initialiser la fenêtre principale
fenetre = tk.Tk()
fenetre.title("Gestionnaire de Tâches")

# Initialiser les tâches
taches = charger_taches()

# Frame pour l'affichage des tâches
frame_taches = tk.Frame(fenetre)
frame_taches.pack(padx=10, pady=10)

# Champ de saisie pour ajouter une tâche
entree_tache = tk.Entry(fenetre, font=('Arial', 14), width=40)
entree_tache.pack(padx=10, pady=10)

# Bouton pour ajouter la tâche
bouton_ajouter = tk.Button(fenetre, text="Ajouter une tâche", font=('Arial', 12), command=ajouter_tache)
bouton_ajouter.pack(pady=10)

# Afficher les tâches existantes
afficher_taches()

# Lancer l'interface graphique
fenetre.mainloop()
