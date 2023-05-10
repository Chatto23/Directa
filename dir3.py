# Importiamo le librerie necessarie
import socket
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Definiamo le liste per i valori Bid e Ask dei due titoli
bid_F32346 = []
ask_F32346 = []
bid_P1K9O1 = []
ask_P1K9O1 = []

# Funzione per printare il messaggio di errore
def errore(messaggio):
    print(messaggio)
    exit(0)

# Funzione per la connessione e la ricezione del feed
def datafeed():
    porta = 10005
    buffersize = 256
    comando = "SUBPRZALL F32346,P1K9O1\n"  # Modifica il comando per sottoscrivere due titoli
    host = "127.0.0.1"
    bid1=bid2=ask1=ask2 = 0

    # Socket
    try:
        with socket.socket(socket.AF_INET,
                           socket.SOCK_STREAM) as sfeed:  # Usiamo la funzione with per gestire il socket
            # Connessione al socket
            try:
                sfeed.connect((host, porta))
            except socket.error as err:
                errore(f"errore di connessione: {err}")

            # Invio comando
            try:
                sfeed.sendall(comando.encode('utf-8'))
            except socket.error as err:
                errore(f"errore di invio del comando: {err}")

            # Ricezione
            while True:
                try:
                    response = sfeed.recv(buffersize)

                    print(response)

                    if response.startswith(b"BIDASK"):  # Check if the response is a bid/ask message
                        data = response.decode('utf-8').split(";")  # Split the response by semicolons
                        # Aggiorniamo le liste con i valori Bid e Ask
                        if data[1] == "F32346":
                            bid_F32346.append(float(data[5]))
                            ask_F32346.append(float(data[8]))
                        elif data[1] == "P1K9O1":
                            bid_P1K9O1.append(float(data[5]))
                            ask_P1K9O1.append(float(data[8]))
                        # Verifica se il messaggio riguarda uno dei due titoli sottoscritti
                        if data[1] in ["F32346", "P1K9O1"]:
                            name = data[1]
                            bid = data[5]  # Get the bid price
                            ask = data[8]  # Get the ask price

                            print(f"Bid: {bid}, Ask: {ask}")  # Print the bid and ask prices

                            # Aggiorniamo il testo della etichetta con i dati ricevuti
                            if name == "F32346":
                                bid1=float(bid)
                                ask1=float(ask)
                                label1.config(text=f"F32346 Bid: {bid}, Ask: {ask}")
                            elif name == "P1K9O1":
                                bid2=float(bid)
                                ask2=float(ask)
                                label2.config(text=f"P1K9O1 Bid: {bid}, Ask: {ask}")
                            pre1=ask2-bid1
                            pre2=ask1-bid2
                            label3.config(text=f" BuyP  {pre1}   ,BuyF  {pre2}")
                        # crea il grafico
                        plt.clf()  # pulisci il grafico precedente
                        plt.plot(bid_P1K9O1, label='P1K9O1 Bid')
                        plt.plot(ask_P1K9O1, label='P1K9O1 Ask')
                        plt.plot(bid_F32346, label='F32346 Bid')
                        plt.plot(ask_F32346, label='F32346 Ask')
                        plt.legend()  # mostra le etichette delle linee
                        plt.pause(0.01)  # attende un po' per aggiornare il grafico
                        



                except socket.error as err:
                    errore(f"errore di ricezione del datafeed: {err}")

    except socket.error as err:  # Chiudiamo il blocco try con un except
        errore(f"errore nel creare il socket: {err}")  # Gestiamo l'errore


window = tk.Tk()
window.title("DataFeed ")
window.geometry("300x200")
# Creiamo una etichetta vuota dove mostrare i dati
label1 = tk.Label(window, text="F32346 BidAsk")
label1.pack()
label2 = tk.Label(window, text="P1K9O1 BidAsk")
label2.pack()
label3 = tk.Label(window, text="PREF")
label3.pack()
# Avviamo la funzione datafeed in un thread separato
import threading
datafeed_thread = threading.Thread(target=datafeed)
datafeed_thread.start()

window.mainloop()  # Avviamo il loop principale della finestra grafica

