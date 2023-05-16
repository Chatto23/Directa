"""Creo un software che tramite una interfaccia grafica chiede di inserire quali strumenti finanziari monitorare.
 Input chiderà il ticker di uno o più strumenti, max 6,nella variabile titoli.
 Creo collegamneto socket dati Directa tramite Api.
 Creo un grafico con i dati ricevuti e una tabella che mostri i dati. 
 Creo un file di log che registri i dati ricevuti.
 """
# importo le librerie necessarie
import tkinter as tk
import socket
import threading
import time
import datetime
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import pandas as pd
import numpy as np

# definiamo le liste bid ask per i titoli
primobid=[]
primoask=[]
secondobid=[]
secondoask=[]
terzobid=[]
terzoask=[]
quartobid=[]
quartoask=[]
quintobid=[]
quintoask=[]
sestobid=[]
sestoask=[]
settimobid=[]
settimoask=[]
ottavobid=[]
ottavoask=[]

df = pd.DataFrame 
titoli = [] # lista per i titoli da monitorare

# creo socket directa
def datafeed() :
    porta = 10005
    buffersize = 256 # dimensione del buffer
    comando = "SUBPRZALL titoli\n"  # Modifica il comando per sottoscrivere due titoli
    host = "127.0.0.1" # Indirizzo IP del server
    # Creo il socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as err:
        print("Errore nella creazione del socket: %s" % err)
        exit()
    # Connessione al server
    try:
        s.connect((host, porta))
    except socket.error as err:
        print("Errore nella connessione al server: %s" % err)
        exit()
    # Invio del comando
    comando = comando.encode()
    s.send(comando)

    # Ricezione dei dati
    while True:
        dati = s.recv(buffersize) # Ricezione dei dati
        print(dati.decode()) # Decodifica dei dati
        if dati.startswith(b"BIDASK"):  # Check if the dati is a bid/ask message
                        data = dati.decode('utf-8').split(";")  # Split the dati by semicolons
                        # Aggiorniamo le liste con i valori Bid e Ask
                        if data[1] == titoli[0]:
                            primobid.append(float(data[5]))
                            primoask.append(float(data[8]))
                        elif data[1] == titoli[1]:
                            secondobid.append(float(data[5]))
                            secondoask.append(float(data[8]))
                        elif data[1] == titoli[2]:
                            terzobid.append(float(data[5]))
                            terzoask.append(float(data[8]))
                        elif data[1] == titoli[3]:
                            quartobid.append(float(data[5]))
                            quartoask.append(float(data[8]))
                        elif data[1] == titoli[4]:
                            quintobid.append(float(data[5]))
                            quintoask.append(float(data[8]))
                        elif data[1] == titoli[5]:
                            sestobid.append(float(data[5]))
                            sestoask.append(float(data[8]))
                        elif data[1] == titoli[6]:
                            settimobid.append(float(data[5]))
                            settimoask.append(float(data[8]))
                        elif data[1] == titoli[7]:
                            ottavobid.append(float(data[5]))
                            ottavoask.append(float(data[8]))
         # Salva i dati in un DataFrame
        data_dict = {
                    titoli[0] + "_bid": primobid,
                    titoli[0] + "_ask": primoask,
                    titoli[1] + "_bid": secondobid,
                    titoli[1] + "_ask": secondoask,
                    titoli[2] + "_bid": terzobid,
                    titoli[2] + "_ask": terzoask,
                    titoli[3] + "_bid": quartobid,
                    titoli[3] + "_ask": quartoask,
                    titoli[4] + "_bid": quintobid,
                    titoli[4] + "_ask": quintoask,
                    titoli[5] + "_bid": sestobid,
                    titoli[5] + "_ask": sestoask,
                    titoli[6] + "_bid": settimobid,
                    titoli[6] + "_ask": settimoask,
                    titoli[7] + "_bid": ottavobid,
                    titoli[7] + "_ask": ottavoask,
                              }
        df = pd.DataFrame(data_dict) 
        # Salva i dati in un file CSV
        df.to_csv("dati.csv")
        # Chiusura del socket
        s.close() 


# creo interfaccia grafica con tkinter e input dei titoli da monitorare
import tkinter as tk

class GUI(tk.Frame):
    def __init__(self, master=None): 
        super().__init__(master) 
        self.master = master 
        self.pack() 
        self.create_widgets() 

    def create_widgets(self): 
        # Etichetta per la spiegazione
        self.label = tk.Label(self, text="Inserisci fino a 8 titoli:")
        self.label.pack()

        # Lista per memorizzare le stringhe inserite dall'utente
        self.strings = []

        # Entry per l'inserimento delle stringhe
        for i in range(8):
            entry = tk.Entry(self)
            entry.pack()
            self.strings.append(entry)

        # Bottone per salvare le stringhe nella lista
        self.save_button = tk.Button(self, text="Salva", command=self.save_strings)
        self.save_button.pack()

    def save_strings(self):
        # Ottieni le stringhe inserite dall'utente
        for i in range(8):
            string = self.strings[i].get()
            if string:
                self.strings[i] = string
            else:
                self.strings[i] = None

        # Stampa la lista di stringhe
        print(self.strings)
        titoli = self.strings
        return titoli
    
# creo interfaccia grafica con tkinter per la tabella
import tkinter as tk2
from tkinter import ttk
import pandas as pd
class GUI2(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        # Creazione della tabella
        self.table = ttk.Treeview(self, columns=tuple(df.columns))
        self.table.heading("#0", text="Elemento")
        for column in df.columns:
            self.table.heading(column, text=column)
        self.table.pack()

        # Caricamento dei dati dal DataFrame
        self.load_data(df)

    def load_data(self, df):
        # Pulizia della tabella
        self.table.delete(*self.table.get_children())

        # Caricamento dei dati dal DataFrame
        for index, row in df.iterrows():
            element = row.name
            values = row.values.tolist()

            # Inserimento dei dati nella tabella
            self.table.insert("", "end", text=element, values=values)





root = tk.Tk() # Creazione della finestra principale 
app = GUI(master=root) # Creazione dell'oggetto GUI 
app.mainloop() # Esecuzione dell'interfaccia grafica

datafeed_thread = threading.Thread(target=datafeed) # Creazione del thread per il datafeed
datafeed_thread.start()  # Avvio del thread

#root = tk2.Tk() # Creazione della finestra principale
#app = GUI2(master=root) # Creazione dell'oggetto GUI
#app.mainloop() # Esecuzione dell'interfaccia grafica

   







 




     


