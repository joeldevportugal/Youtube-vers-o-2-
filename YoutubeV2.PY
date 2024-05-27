# importar as Bibliotecas a Usar ------------------------------------------------------------------------
from tkinter import *
from tkinter import filedialog, messagebox
from tkinter.ttk import Combobox, Progressbar
from pytube import YouTube
import threading
#--------------------------------------------------------------------------------------------------------
# Criar O backend ---------------------------------------------------------------------------------------
# Função para atualizar a qualidade no Combobox Liga com O btnMostrar
def atualizar_qualidade():
    url = Eurl.get()
    formato = formato_var.get()
    if not url:
        return
    try:
        yt = YouTube(url)
        if formato == 'Mp3':
            # Filtra apenas streams de áudio
            qualidades = [stream.abr for stream in yt.streams.filter(only_audio=True)]
        else:
            # Filtra streams progressivas (vídeo com áudio)
            qualidades = [stream.resolution for stream in yt.streams.filter(progressive=True)]
            qualidades = list(set(qualidades))  # Remove duplicatas
            qualidades.sort(key=lambda x: int(x[:-1]))  # Ordena as resoluções

        CMBQualidade['values'] = qualidades
        if qualidades:
            CMBQualidade.current(0)
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao buscar qualidades: {e}")
        CMBQualidade['values'] = ['Erro ao buscar qualidades']

# Função para abrir o diálogo de salvar arquivo e atualizar EGuardar Liga Com O btnGuardar
def salvar_arquivo():
    formato = formato_var.get()
    if formato == 'Mp3':
        filetypes = [('MP3 Files', '*.mp3')]
        default_extension = '.mp3'
    else:
        filetypes = [('MP4 Files', '*.mp4')]
        default_extension = '.mp4'

    file_path = filedialog.asksaveasfilename(defaultextension=default_extension, filetypes=filetypes)
    if file_path:
        EGuardar.delete(0, END)
        EGuardar.insert(0, file_path)
    messagebox.showinfo('Guardar', 'Ficheiro Guardado com sucesso !')
# Função para atualizar a barra de progresso
def atualizar_progresso(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    porcentagem_completa = int(bytes_downloaded / total_size * 100)
    Avanco['value'] = porcentagem_completa
    Janela.update_idletasks()

# Função de download em thread separada Interliga com a função Baixar Video onde tem O theard para Tornar O download mais Rapido
def iniciar_download():
    url = Eurl.get()
    qualidade = CMBQualidade.get()
    formato = formato_var.get()
    caminho = EGuardar.get()

    if not url or not qualidade or not caminho:
        messagebox.showerror("Erro", "Todos os campos devem estar preenchidos")
        return

    try:
        yt = YouTube(url, on_progress_callback=atualizar_progresso)

        if formato == 'Mp3':
            stream = yt.streams.filter(only_audio=True, abr=qualidade).first()
        else:
            stream = yt.streams.filter(progressive=True, file_extension='mp4', resolution=qualidade).first()

        Avanco['value'] = 0
        Janela.update_idletasks()

        # Inicia o download
        stream.download(output_path=caminho.rsplit('/', 1)[0], filename=caminho.rsplit('/', 1)[1])

        # Atualiza a barra de progresso para 100% antes de mostrar a mensagem de sucesso
        Avanco['value'] = 100
        Janela.update_idletasks()

        # Mostra mensagem de sucesso
        messagebox.showinfo("Download Concluído", "Download concluído com sucesso")

        # Reset da barra de progresso para o próximo download
        Avanco['value'] = 100
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao fazer o download: {e}")
        Avanco['value'] = 0  # Reset da barra de progresso em caso de falha

# Função para iniciar a thread de download esta Funação apos conectar a funçao Iniciar Download Liga com BtnDownload
def baixar_video():
    thread = threading.Thread(target=iniciar_download)
    thread.start()
# Esta Função Liga Com o BtnLimar
def Limpar ():
    Eurl.delete(0, END)
    EGuardar.delete(0, END)
    # Reseta os campos de entrada e combobox
    CMBQualidade.set('Selecione a Qualidade')
    CMBQualidade['values'] = []  # Remove os valores da combobox
    # Reseta os RadioButtons
    formato_var.set('Nenhum')  # Reseta para o valor que não corresponde a uma seleção visível
    # Reseta a barra de progresso para 0
    Avanco['value'] = 0
    Janela.update_idletasks()  # Atualiza a interface gráfica para refletir a mudança imediatamente
    messagebox.showinfo('Limpar', "Dados Limpos com sucesso")

# Função chamada ao clicar no botão 'Sair' Liga Com O BtnSair
def sair():
    # Pergunta ao usuário se realmente deseja sair
    resposta = messagebox.askyesno("Sair", "Você realmente deseja sair da aplicação?")
    if resposta:
        Janela.destroy()  # Destroi a janela e encerra a aplicação
#------------------------------------------------------------------------------------------------------
# defenir Cores a Usar ---------------------------------------------------------------------------------
Co0 ="#ffffff"; # cor Brancar 
Co1 ="#ffd2c3"; # cor laranja 
Co2 ="#ffffec"; # Amarelo Claro
#------------------------------------------------------------------------------------------------------- 
# configurara a Nossa janela --------------------------------------------------------------------------
Janela = Tk()
Janela.geometry('800x205+100+100')
Janela.title('Youtube V2 Dev Joel Portugal ')
Janela.resizable(False, False)
Janela.config(bg=Co0)
Janela.iconbitmap('C:\\Users\HP\\Desktop\\Python tkinter\\Youtube downloader Versões\\Youtube versão 2\\icon\\icon.ico')
#------------------------------------------------------------------------------------------------------
# criar todo O fronte end  ----------------------------------------------------------------------------

# Entry para Colocar a Url
Eurl = Entry(Janela, font=('arial 12'), width=85, bg=Co2)
Eurl.place(x=10, y=10)

# comobobox qualidade
CMBQualidade = Combobox(Janela, font=('arial 13'))
CMBQualidade.place(x=10, y=45)
CMBQualidade.set('Selecione a Qualidade')

# Variável para os Radiobuttons
formato_var = StringVar()
formato_var.set('Mp3')  # Definir o valor padrão

# radiobutons 
rdMp3 = Radiobutton(Janela, text='Formato Mp3', font=('Arial 13'), variable=formato_var, value='Mp3', bg=Co0)
rdMp3.place(x=250, y=45)
rdMp4 = Radiobutton(Janela, text='Formato Mp4', font=('arial 13'), variable=formato_var, value='Mp4',bg=Co0)
rdMp4.place(x=430, y=45)

# Entry para mostrar O caminho do Ficheiro Guardado
EGuardar = Entry(Janela, font=('arial 12'), width=65, bg=Co2)
EGuardar.place(x=10, y=85)
BtnGuardar = Button(Janela, text='Guardar', font=('arial 12'), relief=RAISED, overrelief=RIDGE, command=salvar_arquivo, bg=Co1)
BtnGuardar.place(x=605, y=80)

# Botões Mostrar Download Limpar e Sair
BtnMostrar = Button(Janela, text='Mostrar', font=('arial 12'), relief=RAISED, overrelief=RIDGE, command=atualizar_qualidade, bg=Co1)
BtnMostrar.place(x=10, y=115)
BtnDownload = Button(Janela, text='Download', font=('arial 12'), relief=RAISED, overrelief=RIDGE, command=baixar_video, bg=Co1)
BtnDownload.place(x=80, y=115)
BtnLimpar = Button(Janela, text='Limpar', font=('arial 12'), relief=RAISED, overrelief=RIDGE, command=Limpar, bg=Co1)
BtnLimpar.place(x=165, y=115)
BtnSair = Button(Janela, text='Fechar Aplicação', font=('arial 12'), relief=RAISED, overrelief=RIDGE, command=sair, bg=Co1)
BtnSair.place(x=230, y=115)

# barra de Progresso
Avanco = Progressbar(Janela, length=780)
Avanco.place(x=10, y=155)
#--------------------------------------------------------------------------------------------------
# inicar a Janela
Janela.mainloop()