"""
Memory Game - Jogo da Memória

@author ANA LUISA RODRIGUES DINIZ
@author ARTHUR EXPEDITO ARAÚJO FERREIRA
@author BEATRIZ OLIVEIRA SANTOS
@author ÍTALO RODRIGUES GONTIJO
"""


import tkinter as tk  # Biblioteca GUI padrão do Python
import customtkinter as ctk  # Versão moderna do Tkinter
from PIL import Image, ImageTk  # Manipulação de imagens
import random  # Para embaralhar e sortear cartas
from result import show_result  # Tela de resultado
from result import show_draw  # Tela de empate

# Classe que representa uma carta
class MemoryCard:
    def __init__(self, master, front_img, back_img, card_id, click_callback, idx):
        self.front_img = front_img  # Imagem da frente
        self.back_img = back_img  # Imagem de trás
        self.card_id = card_id  # ID da carta (para identificar par)
        self.revealed = False  # Estado (virada ou não)
        self.idx = idx  # Índice da carta

        self.label = tk.Label(master, image=back_img, bg="#363636")  # Cria rótulo com imagem de trás
        self.label.image = back_img  # Garante que a imagem não seja coletada
        self.label.bind("<Button-1>", lambda e: click_callback(self))  # Clica para revelar

    def show(self):
        self.label.configure(image=self.front_img)  # Troca para imagem da frente
        self.label.image = self.front_img  # Atualiza referência

    def hide(self):
        self.label.configure(image=self.back_img)  # Volta imagem para trás
        self.label.image = self.back_img  # Atualiza referência

    def grid(self, row, col):
        self.label.grid(row=row, column=col, padx=10, pady=10)  # Posiciona no tabuleiro

# Cria baralho embaralhado com 24 pares (48 cartas)
def create_deck():
    card_ids = random.sample(range(1, 53), 24)  # Seleciona 24 IDs únicos
    deck = []
    for cid in card_ids:
        path = f"imagens/Cards/{cid}.png"  # Caminho da imagem
        img1 = Image.open(path).resize((120, 120))  # Redimensiona imagem
        photo1 = ImageTk.PhotoImage(img1)  # Converte para Tkinter
        photo2 = ImageTk.PhotoImage(img1.copy())  # Cópia para o par
        deck.append((photo1, cid))  # Adiciona primeira carta
        deck.append((photo2, cid))  # Adiciona par
    random.shuffle(deck)  # Embaralha cartas
    return deck

# Cria a interface do jogo
def create_board(player1, player2):
    window = ctk.CTk()  # Cria janela principal
    window.geometry("1920x1080")  # Define resolução
    window.title("Memory Game")  # Título da janela
    window.resizable(False, False)  # Redimensionável

    after_ids = []  # Armazena callbacks do after
    current_turn = tk.StringVar(value=f"Vez: {player1}")  # Turno inicial
    score1 = tk.IntVar(value=0)  # Pontuação jogador 1
    score2 = tk.IntVar(value=0)  # Pontuação jogador 2
    player_turn = [1]  # Jogador atual (1 ou 2)
    revealed_cards = []  # Cartas reveladas no turno

    # Cabeçalho com título
    frame_top = ctk.CTkFrame(window, height=100)
    frame_top.pack(fill="x")
    ctk.CTkLabel(frame_top, text="Memory Game", font=("Arial", 28)).pack(pady=10)

    # Infos dos jogadores e placar
    frame_info = ctk.CTkFrame(window, height=80)
    frame_info.pack(fill="x", pady=(0, 10))
    ctk.CTkLabel(frame_info, text=f"{player1} - Pontos:", font=("Arial", 23)).pack(side="left", padx=10)
    ctk.CTkLabel(frame_info, textvariable=score1, font=("Arial", 23)).pack(side="left")
    ctk.CTkLabel(frame_info, textvariable=current_turn, font=("Arial", 23)).pack(side="left", expand=True)
    ctk.CTkLabel(frame_info, textvariable=score2, font=("Arial", 23)).pack(side="right", padx=10)
    ctk.CTkLabel(frame_info, text=f"{player2} - Pontos:", font=("Arial", 23)).pack(side="right")

    # Área do tabuleiro
    frame_main = ctk.CTkFrame(window, fg_color="#363636")
    frame_main.pack(fill="both", expand=True)

    # Frame centralizado para as cartas
    frame_grid = tk.Frame(frame_main, bg="#363636")
    frame_grid.place(relx=0.5, rely=0.5, anchor="center")

    back_img = ImageTk.PhotoImage(Image.open("imagens/Cards/back.png").resize((120, 120)))  # Imagem do verso

    deck_data = create_deck()  # Cria as cartas
    cards = []  # Lista de objetos MemoryCard

    # Cancela todas as ações pendentes do after
    def clear_after():
        for aid in after_ids:
            window.after_cancel(aid)
        after_ids.clear()

    # Verifica se as duas cartas reveladas são um par
    def check_match():
        if len(revealed_cards) == 2:
            c1, c2 = revealed_cards
            if c1.card_id == c2.card_id:
                if player_turn[0] == 1:
                    score1.set(score1.get() + 1)
                else:
                    score2.set(score2.get() + 1)
            else:
                after_ids.append(window.after(1000, lambda: hide_cards(c1, c2)))  # Esconde após 1s
                player_turn[0] = 2 if player_turn[0] == 1 else 1  # Alterna jogador
                current_turn.set(f"Vez: {player1 if player_turn[0] == 1 else player2}")
            revealed_cards.clear()

            # Fim de jogo
            if score1.get() + score2.get() == 24:
                clear_after()
                if score1.get() == score2.get():
                    window.destroy()
                    show_draw(player1, player2)
                else:
                    winner = player1 if score1.get() > score2.get() else player2
                    loser = player2 if winner == player1 else player1
                    window.destroy()
                    show_result(winner, max(score1.get(), score2.get()), loser, min(score1.get(), score2.get()))

    # Esconde duas cartas
    def hide_cards(c1, c2):
        c1.hide()
        c1.revealed = False
        c2.hide()
        c2.revealed = False

    # Ação ao clicar em uma carta
    def on_card_click(card):
        if len(revealed_cards) < 2 and not card.revealed:
            card.show()
            card.revealed = True
            revealed_cards.append(card)
            if len(revealed_cards) == 2:
                check_match()

    # Cria as 48 cartas e coloca na tela
    for i in range(48):
        img, cid = deck_data[i]
        card = MemoryCard(frame_grid, img, back_img, cid, on_card_click, i)
        card.grid(row=i // 8, col=i % 8)
        cards.append(card)

    window.mainloop()  # Inicia a janela

# Executa o jogo se rodar direto o script
if __name__ == "__main__":
    create_board("Jogador 1", "Jogador 2")
