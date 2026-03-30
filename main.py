from expiry_ai import ExpiryAI
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import database

ia = ExpiryAI()

database.criar_tabela()


# Alterações análise:
from ia_risco import prever_risco
from datetime import date

def calcular_risco(data_validade, estoque, consumo):

    hoje = date.today()
    dias_restantes = (data_validade - hoje).days

    risco = prever_risco(dias_restantes, estoque, consumo)

    return risco

def verificar_alertas():

    produtos = database.listar_produtos()

    mensagem = "⚠ ALERTAS DO ESTOQUE\n\n"

    alerta = False

    for p in produtos:

        nome = p[1]
        quantidade = p[3]
        validade = p[4]

        dias = ia.calcular_dias(validade)
        risco = ia.prever(validade, quantidade)

        if dias < 0:
            mensagem += f"🔴 {nome} - vencido\n"
            alerta = True

        elif dias == 0:
            mensagem += f"🔴 {nome} - vence hoje\n"
            alerta = True

        elif dias == 1:
            mensagem += f"🔴 {nome} - vence em 1 dia\n"
            alerta = True

        elif dias <= 7:
            mensagem += f"🟡 {nome} - vence em {dias} dias\n"
            alerta = True

    if alerta:
        messagebox.showwarning(
            "Alertas do Estoque",
            mensagem
        )


# Daqui pra baixo é normal.
def atualizar_tabela():

    for item in tabela.get_children():
        tabela.delete(item)

    produtos = database.listar_produtos()

    for p in produtos:

        nome = p[1]
        categoria = p[2]
        quantidade = p[3]
        validade = p[4]

        dias = ia.calcular_dias(validade)
        status = ia.prever(validade, quantidade)

        if dias < 0:
            tag = "vencido"

        elif dias <= 7:
            tag = "proximo"

        else:
            tag = "ok"

        tabela.insert(
            "",
            "end",
            values=(p[0], nome, categoria, quantidade, validade, status),
            tags=(tag,)
        )


def cadastrar_produto():

    nome = entry_nome.get()
    categoria = entry_categoria.get()
    quantidade = entry_quantidade.get()
    validade = entry_validade.get()

    if nome == "" or validade == "":
        messagebox.showwarning("Erro", "Preencha os campos obrigatórios")
        return

    database.adicionar_produto(nome, categoria, quantidade, validade)

    limpar_campos()
    atualizar_tabela()

    messagebox.showinfo("Sucesso", "Produto cadastrado!")


def limpar_campos():

    entry_nome.delete(0, tk.END)
    entry_categoria.delete(0, tk.END)
    entry_quantidade.delete(0, tk.END)
    entry_validade.delete(0, tk.END)


janela = tk.Tk()
janela.title("CheckExpiry - Controle de Validade")
janela.geometry("850x500")


titulo = tk.Label(
    janela,
    text="Sistema CheckExpiry",
    font=("Arial", 20, "bold")
)

titulo.pack(pady=10)


frame_form = tk.Frame(janela)
frame_form.pack(pady=10)


tk.Label(frame_form, text="Nome").grid(row=0, column=0)
entry_nome = tk.Entry(frame_form)
entry_nome.grid(row=0, column=1)

tk.Label(frame_form, text="Categoria").grid(row=1, column=0)
entry_categoria = tk.Entry(frame_form)
entry_categoria.grid(row=1, column=1)

tk.Label(frame_form, text="Quantidade").grid(row=2, column=0)
entry_quantidade = tk.Entry(frame_form)
entry_quantidade.grid(row=2, column=1)

tk.Label(frame_form, text="Validade (DD/MM/AAAA)").grid(row=3, column=0)
entry_validade = tk.Entry(frame_form)
entry_validade.grid(row=3, column=1)


btn_cadastrar = tk.Button(
    frame_form,
    text="Cadastrar Produto",
    command=cadastrar_produto
)

btn_cadastrar.grid(row=4, columnspan=2, pady=10)


frame_tabela = tk.Frame(janela)
frame_tabela.pack(pady=20)


colunas = ("ID", "Nome", "Categoria", "Quantidade", "Validade", "Status")

tabela = ttk.Treeview(
    frame_tabela,
    columns=colunas,
    show="headings",
    height=10
)

tabela.tag_configure("vencido", background="#ffb3b3")
tabela.tag_configure("proximo", background="#fff2a8")
tabela.tag_configure("ok", background="#b6f2b6")

for col in colunas:
    tabela.heading(col, text=col)
    tabela.column(col, width=120)

tabela.pack()


btn_atualizar = tk.Button(
    janela,
    text="Atualizar Lista",
    command=atualizar_tabela
)

btn_atualizar.pack(pady=10)


atualizar_tabela()

janela.after(500, verificar_alertas)

janela.mainloop()