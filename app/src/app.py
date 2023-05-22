import sys
import tkinter as tk
from _tkinter import TclError

from ttkbootstrap import Style

from src.frames.app_login import App_Login
from src.frames.app_main import App_Main
from src.frames.app_solo import App_Solo
from src.frames.app_matchmaking import App_Matchmaking
from src.frames.app_multi import App_Multi

from src.utils import User



class App(tk.Tk):
	def __init__(self) -> str:
		"""Initialisation de l'objet"""
		# On utilise l'init de l'objet Tkinter de base
		tk.Tk.__init__(self)

		# On gardera l'utilisateur dans la classe, pour y accéder plus facilement (global == mauvaise pratique)
		self.user = User()
		self.match_res = None
  
		# Valeurs réutilisées dans des frames, nécessaires ici pour y accéder
		self.github_icon = tk.PhotoImage(file="ico/github.png")
		self.back_button = tk.PhotoImage(file="ico/back.png")
		self.reskin = tk.PhotoImage(file="ico/change_skin.png")

		# On attrape l'event de fermeture de la fenêtre, pour pouvoir clore le script
		self.protocol("WM_DELETE_WINDOW", self.on_close)

		# Change les paramètres basiques de la fenêtre
		self.resizable(False, False)

		# On gère le style via ttkbootstrap (juste un thème par défaut)
		self.style = Style()
		self.style.theme_use("darkly")
		self.skin_cursor = 0
		self.skins = ["darkly", "solar", "superhero", "cyborg", "vapor"]

		# Le chargement de l'icône peut échouer (si l'utilisateur est sous Linux par exemple)
		# On va donc tenter de de set l'icône, et si ça échoue on passe à la suite
		try:
			self.iconbitmap("ico/keyboard.ico")
		except TclError:
			pass

		# On crée un pack pour englober la frame
		container = tk.Frame(self, height=400, width=700)
		container.pack(side="top", fill="both", expand=True)
		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)

		# On ajoute les frames à un dictionnaire
		self.frames = {}
		for F in (App_Login, App_Main, App_Solo, App_Matchmaking, App_Multi):
			frame = F(container, self)
			self.frames[F] = frame
			frame.grid(row=0, column=0, sticky="nsew")

		# On affiche la frame de login
		self.show_frame(App_Login)


	def show_frame(self, cont: tk.Frame) -> None:
		"""Affiche une frame de la fenêtre Tkinter (voir fichiers dans frames)\n

		Args:
			cont (tk.Frame): Frame à afficher\n
		"""
		# On récupère la frame dans le dictionnaire
		frame = self.frames[cont]

		# Si c'est le login, on met la fenêtre en petit
		if cont == App_Login:
			self.title("Login")
			self.geometry("285x155")
		else: # Sinon on la met en grand
			self.title("Keyboard Master")
			self.geometry("700x400")

		# Et on l'affiche
		frame.tkraise()


	def external_show_frame(self, textFrame: str) -> None:
		"""Afficher une frame depuis une autre frame\n

		Args:
			textFrame (str): Nom en string de la fenêtre à afficher\n
		"""
		# Selon le str, on affiche une frame différente
		match textFrame:
			case "App_Main":
				self.show_frame(App_Main)
			case "App_Solo":
				self.show_frame(App_Solo)
			case "App_Matchmaking":
				self.show_frame(App_Matchmaking)
			case "App_Multi":
				self.show_frame(App_Multi)


	def on_close(self) -> None:
		"""Ferme la fenêtre ET LES THREADS quand on ferme la fenêtre"""
		self.destroy()
		sys.exit()
		#os._exit(1)


	def send_event(self, event: str) -> None:
		"""Envoi un event au niveau de la fenêtre (utilisée à partir d'une Frame)\n

		Args:
			event (str): Nom de l'event à envoyer\n
		"""
		self.event_generate(f"<<{event}>>")


	def change_skin(self) -> None:
		"""Passe au skin suivant dans la liste"""
		self.skin_cursor = (self.skin_cursor + 1) % len(self.skins)
		self.style.theme_use(self.skins[self.skin_cursor])
