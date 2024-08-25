import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

root = tk.Tk()

class db():
    def __init__(self):
        self.conecta_db()
        self.criando_tabela()

    def conecta_db(self):
        self.con = sqlite3.connect('games.db')
        self.cur = self.con.cursor()

    def criando_tabela(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS games(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome VARCHAR(50) NOT NULL,
            descricao VARCHAR(500) NOT NULL,
            data DATE NOT NULL,
            categoria VARCHAR(50) NOT NULL
        )""")
        self.con.commit()

    def inserir_jogo(self, nome, descricao, data, categoria):
        self.cur.execute("INSERT INTO games (nome, descricao, data, categoria) VALUES (?, ?, ?, ?)", (nome, descricao, data, categoria))
        self.con.commit()

    def obter_jogos(self):
        self.cur.execute("SELECT id, nome, descricao, data, categoria FROM games")
        return self.cur.fetchall()

    def apagar_jogo(self, jogo_id):
        self.cur.execute("DELETE FROM games WHERE id = ?", (jogo_id,))
        self.con.commit()

db_instance = db()

def adicionar_jogo():
    nome = entry_nome.get()
    descricao = entry_descricao.get()
    data = entry_data.get()
    categoria = entry_categoria.get()

    if nome and descricao and data and categoria:
        db_instance.inserir_jogo(nome, descricao, data, categoria)
        messagebox.showinfo("Sucesso", "Jogo adicionado com sucesso!")
        limpando_tela()
        atualizar_tabela()
    else:
        messagebox.showwarning("Atenção", "Todos os campos são obrigatórios!")

def apagar_jogo():
    selected_item = tree.selection()
    if selected_item:
        jogo_id = tree.item(selected_item[0])['values'][0]
        db_instance.apagar_jogo(jogo_id)
        tree.delete(selected_item[0])
        messagebox.showinfo("Sucesso", "Jogo apagado com sucesso!")
    else:
        messagebox.showwarning("Atenção", "Nenhum jogo selecionado para apagar!")

def limpando_tela():
    entry_nome.delete(0, tk.END)
    entry_descricao.delete(0, tk.END)
    entry_data.delete(0, tk.END)
    entry_categoria.delete(0, tk.END)

def atualizar_tabela():
    for row in tree.get_children():
        tree.delete(row)
    for row in db_instance.obter_jogos():
        tree.insert("", tk.END, values=row)

root.title("ADD GAME")
root.geometry("1280x500")
root.resizable(False, False)
root.configure(background="#0B0B15")

# Frame esquerdo para entradas
frame_left = tk.Frame(root, background="#0B0B15")
frame_left.grid(row=0, column=0, padx=20, pady=20, sticky="n")

# Texto principal
label = tk.Label(frame_left, text="ADICIONE O GAME!", width=30, background="#9000ff", font=("Helvetica", 16))
label.grid(row=0, column=0, columnspan=2, pady=20)

# Nome do jogo
label_nome = tk.Label(frame_left, text="NOME:", background="#0B0B15", fg="white", font=("Helvetica", 14))
label_nome.grid(row=1, column=0, pady=(10, 0), sticky="w")

entry_nome = tk.Entry(frame_left, font=("Helvetica", 12), width=40)
entry_nome.grid(row=2, column=0, pady=10, sticky="w")

# Descrição do jogo
label_descricao = tk.Label(frame_left, text="DESCRIÇÃO:", background="#0B0B15", fg="white", font=("Helvetica", 14))
label_descricao.grid(row=3, column=0, pady=(10, 0), sticky="w")

entry_descricao = tk.Entry(frame_left, font=("Helvetica", 12), width=40)
entry_descricao.grid(row=4, column=0, pady=10, sticky="w")

# Data de lançamento
label_data = tk.Label(frame_left, text="DATA:", background="#0B0B15", fg="white", font=("Helvetica", 14))
label_data.grid(row=5, column=0, pady=(10, 0), sticky="w")

entry_data = tk.Entry(frame_left, font=("Helvetica", 12), width=40)
entry_data.grid(row=6, column=0, pady=10, sticky="w")

# Categoria
label_categoria = tk.Label(frame_left, text="CATEGORIA:", background="#0B0B15", fg="white", font=("Helvetica", 14))
label_categoria.grid(row=7, column=0, pady=(10, 0), sticky="w")

entry_categoria = tk.Entry(frame_left, font=("Helvetica", 12), width=40)
entry_categoria.grid(row=8, column=0, pady=10, sticky="w")

# Botão de adicionar
button_add = tk.Button(frame_left, text="ADICIONAR", background="#9000FF", fg="black", font=("Helvetica", 14), command=adicionar_jogo, width=20)
button_add.grid(row=9, column=0, pady=10)

# Frame direito para tabela
frame_right = tk.Frame(root, background="#0B0B15")
frame_right.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
frame_right.rowconfigure(0, weight=1)
frame_right.columnconfigure(0, weight=1)

# Tabela Treeview
columns = ("ID", "Nome", "Descrição", "Data", "Categoria")
tree = ttk.Treeview(frame_right, columns=columns, show="headings")
tree.heading("ID", text="ID")
tree.heading("Nome", text="Nome")
tree.heading("Descrição", text="Descrição")
tree.heading("Data", text="Data")
tree.heading("Categoria", text="Categoria")
tree.column("ID", width=50)
tree.pack(fill=tk.BOTH, expand=True)

# Botão de apagar
button_delete = tk.Button(frame_right, text="APAGAR", background="#FF0000", fg="white", font=("Helvetica", 14), command=apagar_jogo, width=20)
button_delete.pack(pady=10)

# Inicializa a tabela com os dados do banco de dados
atualizar_tabela()

root.mainloop()
