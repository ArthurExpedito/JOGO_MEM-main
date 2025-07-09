"""
Memory Game - Jogo da Memória

@author ANA LUISA RODRIGUES DINIZ
@author ARTHUR EXPEDITO ARAÚJO FERREIRA
@author BEATRIZ OLIVEIRA SANTOS
@author ÍTALO RODRIGUES GONTIJO
"""


# Importa as bibliotecas
import customtkinter as ctk
from PIL import Image, ImageTk
from board import create_board


def get_names(window, entry1, entry2):# Função para obter os nomes dos jogadores e iniciar o jogo
    # Captura os textos inseridos nos campos de entrada
    name1 = entry1.get()
    name2 = entry2.get()
   
    if name1 and name2: # Verifica se ambos os nomes foram preenchidos
        window.destroy()# Fecha a janela atual
        create_board(name1, name2)# Chama a função que inicia o tabuleiro com os nomes dos jogadores

# Função principal que configura a interface gráfica
def main():
    # Cria a janela principal da aplicação usando CustomTkinter
    window = ctk.CTk()
    # Define o tamanho da janela para Full HD
    window.geometry("1920x1080")
    # Define o título da janela
    window.title("Memory Game")
    # Permite que a janela seja redimensionável tanto na horizontal quanto na vertical
    window.resizable(False, False)

    # Cria um canvas (área de desenho) dentro da janela, com dimensões 1600x900
    canvas = ctk.CTkCanvas(window, width=1600, height=900)
    # Faz o canvas ocupar todo o espaço disponível na janela
    canvas.pack(fill="both", expand=True)

    # Caminho da imagem que será usada como ícone
    img_path = "imagens/Icon/icon.png"
    # Abre a imagem e redimensiona para 100x100 pixels
    img = Image.open(img_path).resize((100, 100))
    # Converte a imagem para um formato compatível com Tkinter
    img = ImageTk.PhotoImage(img)

    # Define a cor de fundo do canvas
    canvas.configure(bg="#363636")
    # Adiciona um título "Memory Game" no topo da tela
    canvas.create_text(960, 100, text="Memory Game", font=("Arial", 40), fill="white")
    # Adiciona a imagem centralizada na tela
    canvas.create_image(960, 200, anchor='center', image=img)
    # Adiciona o texto para o jogador 1
    canvas.create_text(960, 300, text="Insira o nome do jogador 1", font=("Arial", 25), fill="white")
    # Adiciona o texto para o jogador 2
    canvas.create_text(960, 500, text="Insira o nome do jogador 2", font=("Arial", 25), fill="white")

    # Cria o campo de entrada para o nome do jogador 1
    entry1 = ctk.CTkEntry(window, placeholder_text="Nome do jogador 1", width=300, height=50, font=("Arial", 20))
    # Cria o campo de entrada para o nome do jogador 2
    entry2 = ctk.CTkEntry(window, placeholder_text="Nome do jogador 2", width=300, height=50, font=("Arial", 20))

    # Posiciona o campo de entrada do jogador 1 no canvas
    canvas.create_window(960, 400, window=entry1)
    # Posiciona o campo de entrada do jogador 2 no canvas
    canvas.create_window(960, 600, window=entry2)

    # Cria o botão "Jogar", que ao ser clicado chama a função get_names
    button = ctk.CTkButton(
        window, 
        text="Jogar", 
        command=lambda: get_names(window, entry1, entry2),  # Passa a janela e os campos como argumentos
        font=("Arial", 20), 
        width=200, 
        height=50
    )

    # Cria o botão "Sair", que fecha a aplicação ao ser clicado
    button_exit = ctk.CTkButton(
        window, 
        text="Sair", 
        command=window.destroy,  # Fecha a janela
        font=("Arial", 20), 
        fg_color="red",         # Cor de fundo do botão
        hover_color="darkred",  # Cor quando o mouse passa por cima
        width=200, 
        height=50
    )

    # Posiciona o botão "Jogar" no canvas
    canvas.create_window(960, 700, window=button)
    # Posiciona o botão "Sair" no canvas
    canvas.create_window(960, 800, window=button_exit)

    # Inicia o loop principal da interface gráfica
    window.mainloop()

# Verifica se o script está sendo executado diretamente (e não importado), foi neceessário para evitar erro de importação circular
if __name__ == "__main__":
    main()  # Chama a função principal para iniciar a aplicação
