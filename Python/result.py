"""
Memory Game - Jogo da Memória

@author ANA LUISA RODRIGUES DINIZ
@author ARTHUR EXPEDITO ARAÚJO FERREIRA
@author BEATRIZ OLIVEIRA SANTOS
@author ÍTALO RODRIGUES GONTIJO
"""


# Importa a biblioteca
import customtkinter as ctk

# Função para reiniciar o jogo
def restart_game(window):
    # Fecha a janela atual de resultado
    window.destroy()
    # Importa o módulo principal do jogo novamente e chama a função main() para reiniciar, fiz assim para evitar erros de importação circular
    import main
    main.main()

# Função que mostra a tela de resultado final do jogo
def show_result(winner, points, loser, loser_points):
    # Cria uma nova janela usando a biblioteca CustomTkinter
    window = ctk.CTk()
    window.geometry("600x400")
    window.resizable(True, True)
    window.title("Resultado Final")

    # Cria um rótulo de título principal ("Fim de Jogo!")
    label = ctk.CTkLabel(window, text="Fim de Jogo!", font=("Arial", 32))
    label.pack(pady=20)  # Coloca o elemento na tela comm o espaçamento vertical (padding y)

    # Cria um rótulo mostrando o nome do vencedor
    winner_label = ctk.CTkLabel(window, text=f"Vencedor: {winner}", font=("Arial", 24))
    winner_label.pack(pady=10)

    # Cria um rótulo mostrando os pontos do vencedor
    points_label = ctk.CTkLabel(window, text=f"Pontos: {points}", font=("Arial", 24))
    points_label.pack(pady=10)

    # Cria um rótulo mostrando o nome do perdedor
    loser_label = ctk.CTkLabel(window, text=f"Perdedor: {loser}", font=("Arial", 24))
    loser_label.pack(pady=10)

    # Cria um rótulo mostrando os pontos do perdedor
    loser_points_label = ctk.CTkLabel(window, text=f"Pontos: {loser_points}", font=("Arial", 24))
    loser_points_label.pack(pady=10)

    # Cria um botão para sair do jogo (fecha a janela)
    button = ctk.CTkButton(window, text="Sair", command=window.destroy)
    
    # Cria um botão para reiniciar o jogo (chama a função restart_game)
    button_restart = ctk.CTkButton(window, text="Reiniciar", command=lambda: restart_game(window))

    # Adiciona o botão de sair à janela com espaço vertical maior
    button.pack(pady=30)

    # Adiciona o botão de reiniciar logo abaixo
    button_restart.pack(pady=0)

    # Inicia o loop principal da interface gráfica (mantém a janela aberta e responsiva)
    window.mainloop()

# Função que mostra a tela de empate
def show_draw(player1, player2):
    # Cria uma nova janela usando a biblioteca CustomTkinter
    window = ctk.CTk()
    window.geometry("600x400")
    window.resizable(True, True)
    window.title("Resultado Final")

    # Cria um rótulo de título principal ("Fim de Jogo!")
    label = ctk.CTkLabel(window, text="Fim de Jogo!", font=("Arial", 32))
    label.pack(pady=20)  # Coloca o elemento na tela comm o espaçamento vertical (padding y)

    # Cria um rótulo mostrando o empate
    winner_label = ctk.CTkLabel(window, text=f"Empate!", font=("Arial", 29))
    winner_label.pack(pady=10)
    draw_label = ctk.CTkLabel(window, text=f"Empate entre {player1} e {player2}", font=("Arial", 24))
    draw_label.pack(pady=10)

    # Cria um botão para sair do jogo (fecha a janela)
    button = ctk.CTkButton(window, text="Sair", command=window.destroy)
    # Cria um botão para reiniciar o jogo (chama a função restart_game)
    button_restart = ctk.CTkButton(window, text="Reiniciar", command=lambda: restart_game(window))
    button.pack(pady=30)  # Adiciona o botão de sair à janela com espaço vertical maior
    button_restart.pack(pady=0)  # Adiciona o botão de reiniciar logo abaixo
    window.mainloop()
