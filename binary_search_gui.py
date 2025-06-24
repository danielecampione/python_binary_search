# Importazione delle librerie fondamentali per l'implementazione dell'interfaccia grafica
# e delle funzionalità algoritmiche del visualizzatore di ricerca binaria
import tkinter as tk  # Framework GUI principale per la creazione dell'interfaccia utente
from tkinter import ttk, messagebox  # Componenti avanzati e dialoghi modali per l'interazione utente
import time  # Modulo per la gestione temporale delle animazioni e dei ritardi computazionali
import threading  # Libreria per l'esecuzione asincrona degli algoritmi senza bloccare l'interfaccia
import random  # Generatore di numeri pseudocasuali per la creazione di dataset di test
import math  # Libreria matematica per calcoli logaritmici e operazioni di complessità computazionale

# Definizione della classe principale che implementa il pattern Model-View-Controller
# per la visualizzazione interattiva dell'algoritmo di ricerca binaria
class BinarySearchGUI:
    # Costruttore della classe: inizializza lo stato dell'applicazione e configura
    # l'interfaccia grafica secondo i principi di usabilità e design responsivo
    def __init__(self, root):
        # Riferimento al widget radice della gerarchia Tkinter
        self.root = root
        # Configurazione del titolo della finestra principale dell'applicazione
        self.root.title("Visualizzatore Ricerca Binaria")
        # Definizione delle dimensioni iniziali della finestra in pixel (larghezza x altezza)
        self.root.geometry("1200x900")
        # Impostazione del colore di sfondo utilizzando notazione esadecimale RGB
        self.root.configure(bg='#faf8f3')
        
        # Strutture dati e variabili di stato per l'implementazione dell'algoritmo di ricerca binaria
        # Array dinamico che contiene la sequenza di elementi su cui operare
        self.array = []
        # Valore target da ricercare nell'array ordinato
        self.target = 0
        # Indice sinistro del sottointervallo di ricerca corrente
        self.left = 0
        # Indice destro del sottointervallo di ricerca corrente
        self.right = 0
        # Indice centrale calcolato come floor((left + right) / 2)
        self.mid = 0
        # Flag booleano che indica se l'elemento target è stato localizzato
        self.found = False
        # Semaforo per prevenire esecuzioni concorrenti dell'algoritmo di ricerca
        self.searching = False
        # Semaforo per prevenire esecuzioni concorrenti dell'algoritmo di ordinamento
        self.sorting = False
        # Invariante booleano che certifica l'ordinamento dell'array
        self.is_sorted = False
        # Intervallo temporale in secondi per la sincronizzazione delle animazioni
        self.delay = 1.5
        # Cardinalità predefinita dell'insieme di elementi da processare
        self.array_size = 10
        
        # Dizionario contenente la palette cromatica dell'interfaccia utente
        # Implementa un sistema di design coerente basato su teoria del colore
        self.colors = {
            'bg': '#faf8f3',           # Colore di sfondo principale (crema chiaro)
            'primary': '#6b73ff',       # Colore primario per elementi di enfasi
            'secondary': '#ff6b9d',     # Colore secondario per contrasti cromatici
            'success': '#00d4aa',       # Indicatore di stato positivo (operazioni riuscite)
            'warning': '#ffb347',       # Indicatore di attenzione (stati intermedi)
            'text': '#2d3748',          # Colore del testo per massima leggibilità
            'card': '#ffffff',          # Sfondo per componenti elevati (card design)
            'shadow': '#e2e8f0',        # Colore per effetti di profondità visiva
            'accent': '#ffd93d',        # Colore di accento per elementi decorativi
            'gradient_start': '#667eea', # Punto iniziale per gradienti lineari
            'gradient_end': '#764ba2'    # Punto finale per gradienti lineari
        }
        
        # Variabili di controllo per il sistema di animazioni procedurali
        # Contatore incrementale per la gestione dei frame di animazione
        self.animation_step = 0
        # Direzione del movimento nell'animazione pulsante (1 = espansione, -1 = contrazione)
        self.pulse_direction = 1
        
        # Invocazione sequenziale dei metodi di inizializzazione dell'interfaccia utente
        # Costruzione della gerarchia di widget secondo il pattern compositivo
        self.setup_ui()
        # Configurazione del sistema di animazioni interattive per i componenti
        self.setup_button_animations()
        # Generazione dell'array iniziale con distribuzione pseudocasuale
        self.generate_array()
        # Attivazione del sistema di animazioni continue per il titolo
        self.animate_title()
        
    # Metodo responsabile della costruzione dell'interfaccia utente principale
    # Implementa il layout gerarchico utilizzando il geometry manager pack()
    def setup_ui(self):
        # Creazione del contenitore principale per il titolo dell'applicazione
        # Frame container che incapsula gli elementi di intestazione
        title_frame = tk.Frame(self.root, bg=self.colors['bg'])
        # Posizionamento del frame con padding verticale per spaziatura ottimale
        title_frame.pack(pady=20)
        
        # Widget Label per la visualizzazione del titolo principale
        # Utilizza Unicode emoji per migliorare l'appeal visivo
        title_label = tk.Label(
            title_frame,
            text="🔍 VISUALIZZATORE RICERCA BINARIA 🔍",
            font=('Segoe UI', 28, 'bold'),  # Font sans-serif con dimensione 28pt e peso bold
            fg=self.colors['primary'],  # Colore del testo dal sistema cromatico definito
            bg=self.colors['bg']  # Colore di sfondo coerente con il tema
        )
        # Posizionamento del widget nel contenitore padre
        title_label.pack()
        
        # Widget Label per il sottotitolo esplicativo dell'applicazione
        # Fornisce contesto educativo sull'obiettivo del software
        subtitle_label = tk.Label(
            title_frame,
            text="✨ Impara come funziona l'algoritmo di ricerca! ✨",
            font=('Segoe UI', 14, 'italic'),  # Font corsivo per differenziazione tipografica
            fg=self.colors['text'],  # Colore del testo per leggibilità ottimale
            bg=self.colors['bg']  # Mantenimento della coerenza cromatica
        )
        # Posizionamento con padding asimmetrico (8px sopra, 0px sotto)
        subtitle_label.pack(pady=(8, 0))
        
        # Elemento decorativo di separazione visiva
        # Frame utilizzato come linea orizzontale per delimitazione sezioni
        separator = tk.Frame(title_frame, height=3, bg=self.colors['primary'])
        # Espansione orizzontale completa con margini laterali simmetrici
        separator.pack(fill='x', padx=100, pady=10)
        
        # Costruzione del sistema di controlli interattivi dell'applicazione
        # Container principale che implementa il pattern di composizione gerarchica
        control_container = tk.Frame(self.root, bg=self.colors['bg'])
        # Posizionamento con spaziatura verticale per separazione logica delle sezioni
        control_container.pack(pady=25)
        
        # Implementazione dell'effetto ombra mediante sovrapposizione di frame
        # Tecnica di design per simulare profondità tridimensionale
        shadow_frame = tk.Frame(control_container, bg=self.colors['shadow'], height=5)
        # Espansione orizzontale con margini per effetto di elevazione
        shadow_frame.pack(fill='x', padx=5)
        
        # Frame principale contenente i controlli operativi dell'interfaccia
        # Utilizza relief='flat' per design moderno e minimalista
        control_frame = tk.Frame(control_container, bg=self.colors['card'], relief='flat', bd=0)
        # Posizionamento con padding interno (ipady) per spaziatura dei contenuti
        control_frame.pack(fill='x', padx=20, pady=(0, 5), ipady=15)
        
        # Sezione dedicata alla configurazione della cardinalità dell'array
        # Frame container per i controlli di dimensionamento del dataset
        size_frame = tk.Frame(control_frame, bg=self.colors['card'])
        # Posizionamento laterale sinistro con spaziatura orizzontale
        size_frame.pack(side=tk.LEFT, padx=25)
        
        # Widget Label per l'etichetta descrittiva del controllo
        # Utilizza emoji Unicode per migliorare l'identificazione visiva
        tk.Label(
            size_frame,
            text="📏 Elementi array:",
            font=('Segoe UI', 13, 'bold'),  # Font con peso bold per enfasi
            fg=self.colors['text'],  # Colore del testo per contrasto ottimale
            bg=self.colors['card']  # Sfondo coerente con il contenitore
        ).pack()
        
        # Container decorativo per il widget Listbox con bordo colorato
        # Implementa il pattern di incapsulamento visivo per coerenza estetica
        listbox_container = tk.Frame(size_frame, bg=self.colors['primary'], relief='flat')
        # Posizionamento con padding verticale per spaziatura
        listbox_container.pack(pady=8)
        
        # Widget Listbox per la selezione della dimensione dell'array
        # Componente di input che permette selezione da lista predefinita
        self.size_listbox = tk.Listbox(
            listbox_container,
            font=('Segoe UI', 12, 'bold'),  # Font con peso bold per leggibilità
            width=8,  # Larghezza in caratteri del widget
            height=4,  # Altezza in righe visibili simultaneamente
            justify='center',  # Allineamento centrale del testo
            relief='flat',  # Stile del bordo piatto per design moderno
            bd=3,  # Spessore del bordo in pixel
            bg=self.colors['bg'],  # Colore di sfondo del widget
            fg=self.colors['text'],  # Colore del testo normale
            selectbackground=self.colors['primary'],  # Colore di sfondo per selezione
            selectforeground='white'  # Colore del testo selezionato
        )
        
        # Popolamento della Listbox con valori predefiniti di cardinalità
        # Array contenente le opzioni di dimensionamento disponibili
        sizes = [10, 20]
        # Iterazione per inserimento sequenziale degli elementi nella lista
        for size in sizes:
            # Inserimento alla fine della lista con conversione a stringa
            self.size_listbox.insert(tk.END, str(size))
        
        # Impostazione della selezione predefinita al primo elemento (indice 0)
        # Garantisce uno stato iniziale coerente dell'interfaccia
        self.size_listbox.selection_set(0)
        # Posizionamento del widget con padding minimale
        self.size_listbox.pack(padx=2, pady=2)
        
        # Binding dell'evento di selezione al metodo di gestione corrispondente
        # Implementa il pattern Observer per la reattività dell'interfaccia
        self.size_listbox.bind('<<ListboxSelect>>', self.on_size_select)
        
        # Inizializzazione della variabile di stato con il valore predefinito
        # Sincronizzazione tra interfaccia e modello dati
        self.array_size = int(self.size_listbox.get(0))
        
        # Sezione dedicata all'input del valore target per la ricerca
        # Frame container per i controlli di inserimento del target
        input_frame = tk.Frame(control_frame, bg=self.colors['card'])
        # Posizionamento laterale con spaziatura orizzontale uniforme
        input_frame.pack(side=tk.LEFT, padx=25)
        
        # Widget Label per l'identificazione del campo di input
        # Utilizza iconografia emoji per migliorare l'usabilità
        tk.Label(
            input_frame,
            text="🎯 Numero da cercare:",
            font=('Segoe UI', 13, 'bold'),  # Tipografia con enfasi per chiarezza
            fg=self.colors['text'],  # Colore del testo per leggibilità ottimale
            bg=self.colors['card']  # Sfondo coerente con il design system
        ).pack()
        
        # Container decorativo per il widget Entry con bordo colorato
        # Implementa il pattern di incapsulamento visivo per coerenza estetica
        entry_container = tk.Frame(input_frame, bg=self.colors['primary'], relief='flat')
        # Posizionamento con spaziatura verticale per separazione visiva
        entry_container.pack(pady=8)
        
        # Widget Entry per l'inserimento del valore target della ricerca
        # Campo di input numerico con validazione implicita
        self.target_entry = tk.Entry(
            entry_container,
            font=('Segoe UI', 16, 'bold'),  # Font di dimensione maggiore per visibilità
            width=12,  # Larghezza in caratteri del campo di input
            justify='center',  # Allineamento centrale del testo inserito
            relief='flat',  # Stile del bordo piatto per design moderno
            bd=3,  # Spessore del bordo in pixel
            bg=self.colors['bg'],  # Colore di sfondo del campo
            fg=self.colors['text']  # Colore del testo inserito
        )
        # Posizionamento con padding minimale per effetto di incapsulamento
        self.target_entry.pack(padx=2, pady=2)
        
        # Sezione contenente i pulsanti di controllo dell'applicazione
        # Frame container per i controlli operativi principali
        button_frame = tk.Frame(control_frame, bg=self.colors['card'])
        # Posizionamento laterale con spaziatura orizzontale
        button_frame.pack(side=tk.LEFT, padx=25)
        
        # Container per il pulsante di ricerca con effetto ombra tridimensionale
        # Implementa il pattern di elevazione visiva per enfasi
        search_container = tk.Frame(button_frame, bg=self.colors['shadow'])
        # Posizionamento laterale con spaziatura tra pulsanti
        search_container.pack(side=tk.LEFT, padx=8)
        
        # Widget Button per l'avvio dell'algoritmo di ricerca binaria
        # Pulsante primario che innesca l'esecuzione dell'algoritmo
        self.search_btn = tk.Button(
            search_container,
            text="🚀 ESEGUI RICERCA",  # Testo con emoji per identificazione immediata
            font=('Segoe UI', 10, 'bold'),  # Font con peso bold per enfasi
            bg=self.colors['success'],  # Colore di sfondo indicativo di azione positiva
            fg='white',  # Colore del testo per contrasto massimo
            command=self.start_search,  # Callback per l'esecuzione dell'algoritmo
            padx=15,  # Padding orizzontale interno per dimensionamento
            pady=8,  # Padding verticale interno per proporzioni
            relief='flat',  # Stile del bordo piatto per design moderno
            bd=0,  # Spessore del bordo nullo
            cursor='hand2'  # Cursore a mano per indicare interattività
        )
        # Posizionamento con padding per effetto di elevazione
        self.search_btn.pack(padx=2, pady=2)
        
        # Container per il pulsante di reset con effetto ombra tridimensionale
        # Implementa coerenza visiva con gli altri controlli
        reset_container = tk.Frame(button_frame, bg=self.colors['shadow'])
        # Posizionamento laterale con spaziatura uniforme
        reset_container.pack(side=tk.LEFT, padx=8)
        
        # Widget Button per la rigenerazione dell'array di dati
        # Pulsante secondario per il reset dello stato dell'applicazione
        self.reset_btn = tk.Button(
            reset_container,
            text="🔄 NUOVO ARRAY",  # Testo con emoji per identificazione funzionale
            font=('Segoe UI', 10, 'bold'),  # Tipografia coerente con altri controlli
            bg=self.colors['warning'],  # Colore di sfondo indicativo di azione di reset
            fg='white',  # Colore del testo per contrasto ottimale
            command=self.generate_array,  # Callback per la rigenerazione dei dati
            padx=15,  # Padding orizzontale per dimensionamento uniforme
            pady=8,  # Padding verticale per proporzioni coerenti
            relief='flat',  # Stile del bordo piatto per design moderno
            bd=0,  # Spessore del bordo nullo
            cursor='hand2'  # Cursore a mano per indicare interattività
        )
        # Posizionamento con padding per effetto di elevazione
        self.reset_btn.pack(padx=2, pady=2)
        

        
        # Sezione principale dedicata alla visualizzazione dell'array
        # Frame container espandibile per la rappresentazione grafica dei dati
        self.array_frame = tk.Frame(self.root, bg=self.colors['bg'])
        # Posizionamento con espansione dinamica per adattamento al contenuto
        self.array_frame.pack(pady=20, expand=True, fill='both')
        
        # Sezione informativa per la visualizzazione dello stato dell'algoritmo
        # Container principale per i messaggi e le statistiche di esecuzione
        info_container = tk.Frame(self.root, bg=self.colors['bg'])
        # Posizionamento con espansione orizzontale e margini laterali
        info_container.pack(pady=25, padx=40, fill='x')
        
        # Implementazione dell'effetto ombra per profondità visiva
        # Frame decorativo per simulare elevazione tridimensionale
        info_shadow = tk.Frame(info_container, bg=self.colors['shadow'], height=8)
        # Espansione orizzontale con margini per effetto di ombreggiatura
        info_shadow.pack(fill='x', padx=8)
        
        # Frame principale contenente le informazioni di stato
        # Container per messaggi di feedback e statistiche algoritmiche
        self.info_frame = tk.Frame(info_container, bg=self.colors['card'], relief='flat', bd=0)
        # Posizionamento con padding interno per spaziatura del contenuto
        self.info_frame.pack(fill='x', pady=(0, 8), ipady=20)
        
        # Widget Label per la visualizzazione del passo corrente dell'algoritmo
        # Componente di feedback primario per l'utente durante l'esecuzione
        self.step_label = tk.Label(
            self.info_frame,
            text="✨ Pronto per iniziare la ricerca! ✨",  # Messaggio di stato iniziale
            font=('Segoe UI', 16, 'bold'),  # Font di dimensione prominente per visibilità
            fg=self.colors['primary'],  # Colore primario per enfasi
            bg=self.colors['card']  # Sfondo coerente con il contenitore
        )
        # Posizionamento con padding verticale per spaziatura
        self.step_label.pack(pady=12)
        
        # Widget Label per la spiegazione dettagliata dell'algoritmo
        # Componente educativo che fornisce contesto teorico durante l'esecuzione
        self.explanation_label = tk.Label(
            self.info_frame,
            text="🎯 La ricerca binaria divide l'array a metà ad ogni passo, eliminando metà degli elementi.",
            font=('Segoe UI', 12),  # Font di dimensione standard per leggibilità
            fg=self.colors['text'],  # Colore del testo per contrasto ottimale
            bg=self.colors['card'],  # Sfondo coerente con il design system
            wraplength=900  # Lunghezza massima della riga per text wrapping automatico
        )
        # Posizionamento con padding asimmetrico per gerarchia visiva
        self.explanation_label.pack(pady=(0, 12))
        
        # Container per la visualizzazione delle statistiche algoritmiche
        # Frame decorativo con colore di accento per enfasi delle metriche
        stats_container = tk.Frame(self.info_frame, bg=self.colors['accent'], relief='flat')
        # Posizionamento con espansione orizzontale e margini laterali
        stats_container.pack(pady=12, padx=50, fill='x')
        
        # Widget Label per la visualizzazione delle metriche di performance
        # Componente che mostra complessità computazionale e statistiche di esecuzione
        self.stats_label = tk.Label(
            stats_container,
            text="📊 Passi: 0 | Complessità: O(log n) | Efficienza: Massima! 🚀",
            font=('Segoe UI', 13, 'bold'),  # Font con peso bold per enfasi delle metriche
            fg=self.colors['text'],  # Colore del testo per leggibilità
            bg=self.colors['accent']  # Sfondo di accento per evidenziazione
        )
        # Posizionamento con padding verticale per spaziatura
        self.stats_label.pack(pady=8)
        
    # Metodo per l'aggiornamento dinamico della velocità di animazione
    # Modifica il parametro temporale per la sincronizzazione delle transizioni visive
    def update_speed(self, value):
        # Conversione del valore di input in numero a virgola mobile
        # Aggiornamento della variabile di delay per controllo temporale
        self.delay = float(value)
    
    # Metodo per il calcolo adattivo del ritardo delle animazioni
    # Implementa una funzione di mapping inversamente proporzionale alla cardinalità dell'array
    def get_animation_delay(self):
        # Parametri di configurazione per il sistema di temporizzazione adattiva
        # Valore di delay di riferimento per array di dimensioni medie
        base_delay = 0.8
        # Soglia inferiore per il ritardo minimo (performance ottimale)
        min_delay = 0.05
        # Soglia superiore per il ritardo massimo (visibilità ottimale)
        max_delay = 1.5
        
        # Algoritmo di calcolo del delay basato sulla cardinalità dell'insieme
        # Implementa una funzione a tratti per ottimizzazione delle performance
        if self.array_size <= 10:
            # Per array di piccole dimensioni: massima visibilità
            delay = max_delay
        elif self.array_size >= 500:
            # Per array di grandi dimensioni: massima performance
            delay = min_delay
        else:
            # Interpolazione logaritmica per transizione fluida tra gli estremi
            # Utilizza la funzione logaritmo naturale per mapping non-lineare
            import math
            # Calcolo del fattore di interpolazione logaritmico
            factor = math.log(self.array_size / 10) / math.log(500 / 10)
            # Applicazione della formula di interpolazione lineare
            delay = max_delay - (max_delay - min_delay) * factor
        
        # Applicazione dei vincoli di dominio per garantire valori validi
        return max(min_delay, min(max_delay, delay))
    
    # Metodo specializzato per il calcolo del ritardo nelle animazioni di ordinamento
    # Implementa una funzione di mapping ottimizzata per algoritmi di sorting
    def get_sort_animation_delay(self):
        # Implementazione di una funzione a tratti per ottimizzazione delle performance
        # Ogni intervallo è calibrato per bilanciare visibilità e velocità di esecuzione
        if self.array_size <= 10:
            # Array di cardinalità minima: priorità alla comprensione visiva
            return 0.15
        elif self.array_size <= 20:
            # Array di piccole dimensioni: bilanciamento tra visibilità e performance
            return 0.1
        elif self.array_size <= 50:
            # Array di dimensioni medie: ottimizzazione per fluidità
            return 0.05
        elif self.array_size <= 100:
            # Array di grandi dimensioni: priorità alle performance
            return 0.02
        elif self.array_size <= 200:
            # Array di dimensioni considerevoli: massimizzazione della velocità
            return 0.01
        else:
            # Array di cardinalità elevata: delay minimale per performance ottimali
            return 0.005
    
    # Metodo di callback per la gestione dell'evento di selezione della dimensione
    # Implementa il pattern Observer per la reattività dell'interfaccia utente
    def on_size_select(self, event):
        # Acquisizione della selezione corrente dal widget Listbox
        # Restituisce una tupla contenente gli indici degli elementi selezionati
        selection = self.size_listbox.curselection()
        # Verifica dell'esistenza di una selezione valida
        if selection:
            # Estrazione del valore selezionato e conversione a intero
            # Aggiornamento della variabile di stato per la cardinalità dell'array
            self.array_size = int(self.size_listbox.get(selection[0]))
        
    # Metodo per la generazione pseudocasuale di un nuovo array di dati
    # Implementa l'algoritmo di campionamento senza ripetizione per diversità degli elementi
    def generate_array(self):
        # Controllo dei semafori per prevenire esecuzioni concorrenti
        # Garantisce l'integrità dello stato durante operazioni asincrone
        if self.searching or self.sorting:
            return
            
        # Generazione di un array non ordinato con distribuzione pseudocasuale
        # Calcolo del valore massimo per garantire varietà numerica adeguata
        max_value = max(100, self.array_size * 2)
        # Utilizzo di random.sample per campionamento senza ripetizione
        # Genera una sequenza di elementi distinti nell'intervallo [1, max_value]
        self.array = random.sample(range(1, max_value), self.array_size)
        # Impostazione dell'invariante di ordinamento a falso
        self.is_sorted = False
        # Invocazione del metodo di rendering per aggiornamento visivo
        self.display_array()
        
        # Reinizializzazione delle variabili di stato dell'algoritmo
        # Reset degli indici di delimitazione del sottointervallo di ricerca
        self.left = 0
        self.right = len(self.array) - 1
        # Reset del flag di localizzazione dell'elemento target
        self.found = False
        
        # Aggiornamento dei messaggi informativi dell'interfaccia utente
        # Configurazione del messaggio di stato per il nuovo array generato
        self.step_label.config(text="✨ Nuovo array NON ordinato generato! ✨")
        # Aggiornamento del messaggio esplicativo per guidare l'utente
        self.explanation_label.config(text="🎯 Array pronto! Clicca su 'ESEGUI RICERCA' per ordinare automaticamente e cercare un numero.")
        # Configurazione delle statistiche con informazioni sulla cardinalità e stato
        self.stats_label.config(text=f"📊 Array di {len(self.array)} elementi | Stato: NON ORDINATO ❌ | Pronto per la ricerca! 🚀")
        
        # Aggiornamento dello stato dei controlli dell'interfaccia
        # Riabilitazione del pulsante di ricerca con testo appropriato
        self.search_btn.config(state='normal', text="🚀 ESEGUI RICERCA")
        
    # Metodo per il rendering visuale dell'array con evidenziazione parametrica degli elementi
    # Implementa algoritmi di visualizzazione adattiva con supporto per animazioni e highlighting
    def display_array(self, highlight_left=-1, highlight_right=-1, highlight_mid=-1, found_index=-1, animate=False):
        # Operazione di garbage collection per i widget esistenti nel frame dell'array
        # Rimozione completa di tutti i componenti figlio per prevenire memory leaks
        for widget in self.array_frame.winfo_children():
            widget.destroy()
            
        # Istanziazione del contenitore principale per l'array con supporto per espansione
        # Configurazione del background secondo il tema cromatico dell'applicazione
        container = tk.Frame(self.array_frame, bg=self.colors['bg'])
        container.pack(expand=True)
        
        # Algoritmo di determinazione del colore del titolo basato sullo stato di ordinamento
        # Mappatura condizionale tra invariante di ordinamento e schema cromatico
        title_bg_color = self.colors['success'] if self.is_sorted else self.colors['warning']
        # Generazione del testo del titolo con indicatori visivi Unicode
        title_text = "📊 ARRAY ORDINATO 📊" if self.is_sorted else "📊 ARRAY NON ORDINATO 📊"
        
        # Creazione del contenitore per il titolo con styling avanzato
        # Configurazione del relief per effetto piatto moderno
        title_container = tk.Frame(container, bg=title_bg_color, relief='flat')
        title_container.pack(pady=(0, 25), padx=200)
        
        # Istanziazione del widget Label per il titolo dell'array
        # Configurazione tipografica con font Segoe UI per consistenza con Windows
        array_title = tk.Label(
            title_container,
            text=title_text,
            font=('Segoe UI', 18, 'bold'),  # Font system-native per ottimizzazione rendering
            fg='white',  # Colore del testo per contrasto ottimale
            bg=title_bg_color  # Background dinamico basato sullo stato
        )
        # Posizionamento con padding simmetrico per bilanciamento visivo
        array_title.pack(pady=8, padx=20)
        
        # Creazione del contenitore principale per l'array con effetti di profondità
        # Implementazione del design pattern Container per organizzazione gerarchica
        array_container = tk.Frame(container, bg=self.colors['bg'])
        array_container.pack(pady=20)
        
        # Implementazione dell'effetto ombra per profondità visiva tridimensionale
        # Utilizzo di un frame dedicato per simulazione dell'ombra proiettata
        shadow_container = tk.Frame(array_container, bg=self.colors['shadow'], height=8)
        shadow_container.pack(fill='x', padx=8)
        
        # Istanziazione del frame principale per contenimento degli elementi dell'array
        # Configurazione con relief flat per design moderno e minimalista
        main_array_frame = tk.Frame(array_container, bg=self.colors['card'], relief='flat')
        main_array_frame.pack(pady=(0, 8), padx=20, ipady=15)
        
        # Creazione del frame dedicato per il rendering degli elementi numerici
        # Separazione logica per gestione indipendente del layout degli elementi
        elements_frame = tk.Frame(main_array_frame, bg=self.colors['card'])
        elements_frame.pack(pady=10)
        
        # Istanziazione del frame per la visualizzazione degli indici posizionali
        # Implementazione di una seconda riga per informazioni di debugging
        indices_frame = tk.Frame(main_array_frame, bg=self.colors['card'])
        indices_frame.pack(pady=(5, 10))
        
        # Creazione del frame per le frecce indicatrici di stato algoritmo
        # Terza riga dedicata per feedback visivo delle operazioni correnti
        arrows_frame = tk.Frame(main_array_frame, bg=self.colors['card'])
        arrows_frame.pack(pady=(0, 5))
        
        # Iterazione attraverso gli elementi dell'array per rendering individuale
        # Implementazione del pattern Iterator per processamento sequenziale
        for i, value in enumerate(self.array):
            # Algoritmo di determinazione dello schema cromatico per ogni elemento
            # Inizializzazione con valori di default per elementi neutri
            color = self.colors['card']  # Colore di background di default
            text_color = self.colors['text']  # Colore del testo per leggibilità ottimale
            border_color = self.colors['shadow']  # Colore del bordo per definizione
            arrow_text = ""  # Stringa vuota per frecce indicatrici
            
            # Controllo prioritario per elemento trovato (massima precedenza visiva)
            if i == found_index:
                color = self.colors['success']  # Verde per successo della ricerca
                text_color = 'white'  # Contrasto massimo per visibilità
                border_color = '#00a085'  # Bordo verde intenso per enfasi
                arrow_text = "🎉"  # Emoji celebrativa per feedback positivo
            # Controllo per elemento mediano nell'algoritmo di ricerca binaria
            elif i == highlight_mid:
                color = self.colors['primary']  # Blu primario per elemento centrale
                text_color = 'white'  # Testo bianco per contrasto ottimale
                border_color = '#5a63e8'  # Bordo blu intenso per evidenziazione
                arrow_text = "👆"  # Freccia verso l'alto per indicazione
            # Controllo per elementi nell'intervallo di ricerca attivo
            elif highlight_left <= i <= highlight_right and highlight_left != -1:
                color = self.colors['warning']  # Arancione per area di ricerca
                text_color = 'white'  # Testo bianco per leggibilità
                border_color = '#e8a23a'  # Bordo arancione per coerenza cromatica
                # Determinazione delle frecce per delimitatori dell'intervallo
                if i == highlight_left:
                    arrow_text = "⬅️"  # Freccia sinistra per limite inferiore
                elif i == highlight_right:
                    arrow_text = "➡️"  # Freccia destra per limite superiore
            
            # Algoritmo di calcolo delle dimensioni responsive per elementi dell'array
            # Determinazione della cardinalità dell'array per scaling adattivo
            array_size = len(self.array)
            
            # Implementazione di una funzione a tratti per dimensionamento ottimale
            # Mappatura tra cardinalità dell'array e parametri di visualizzazione
            if array_size <= 10:
                # Configurazione per array di piccole dimensioni (≤ 10 elementi)
                element_width = 5  # Larghezza massima per leggibilità ottimale
                font_size = 14  # Font size grande per visibilità eccellente
                padx = 2  # Padding orizzontale generoso per spaziatura
                pady = 2  # Padding verticale per separazione visiva
                height = 2  # Altezza doppia per proporzioni bilanciate
            elif array_size <= 20:
                # Configurazione per array di dimensioni medie-piccole (11-20 elementi)
                element_width = 3  # Larghezza ridotta per contenimento
                font_size = 12  # Font size medio-grande per leggibilità
                padx = 1  # Padding ridotto per ottimizzazione spazio
                pady = 1  # Padding verticale minimo
                height = 2  # Mantenimento altezza doppia
            elif array_size <= 50:
                # Configurazione per array di dimensioni medie (21-50 elementi)
                element_width = 3  # Larghezza costante per consistenza
                font_size = 12  # Font size mantenuto per leggibilità
                padx = 1  # Padding minimo per compattezza
                pady = 1  # Padding verticale ridotto
                height = 2  # Altezza doppia preservata
            elif array_size <= 100:
                # Configurazione per array di grandi dimensioni (51-100 elementi)
                element_width = 2  # Larghezza compressa per contenimento
                font_size = 10  # Font size ridotto per adattamento
                padx = 1  # Padding orizzontale minimo
                pady = 1  # Padding verticale preservato
                height = 1  # Altezza singola per compattezza
            elif array_size <= 200:
                # Configurazione per array molto grandi (101-200 elementi)
                element_width = 2  # Larghezza mantenuta per leggibilità minima
                font_size = 8  # Font size piccolo per contenimento
                padx = 0  # Eliminazione padding orizzontale
                pady = 1  # Padding verticale minimo preservato
                height = 1  # Altezza singola per massima compattezza
            elif array_size <= 300:
                # Configurazione per array estremamente grandi (201-300 elementi)
                element_width = 1  # Larghezza minima per contenimento massimo
                font_size = 7  # Font size molto piccolo
                padx = 0  # Eliminazione completa padding orizzontale
                pady = 0  # Eliminazione padding verticale
                height = 1  # Altezza minima
            else:
                # Configurazione per array di dimensioni eccezionali (>300 elementi)
                element_width = 1  # Larghezza minima assoluta
                font_size = 6  # Font size minimo per leggibilità residua
                padx = 0  # Padding nullo per massima densità
                pady = 0  # Padding verticale nullo
                height = 1  # Altezza minima per contenimento estremo
            
            # Creazione del contenitore per elemento con bordo cromatico personalizzato
            # Implementazione del pattern Decorator per aggiunta di bordi colorati
            element_container = tk.Frame(elements_frame, bg=border_color, relief='flat')
            element_container.pack(side=tk.LEFT, padx=padx, pady=pady)
            
            # Istanziazione del widget Label per rappresentazione dell'elemento numerico
            # Configurazione con parametri di styling dinamici calcolati precedentemente
            element = tk.Label(
                element_container,
                text=str(value),  # Conversione del valore numerico a rappresentazione stringa
                font=('Segoe UI', font_size, 'bold'),  # Font system-native con peso bold
                bg=color,  # Background color determinato dall'algoritmo di stato
                fg=text_color,  # Foreground color per contrasto ottimale
                width=element_width,  # Larghezza calcolata dall'algoritmo responsive
                height=height,  # Altezza adattiva basata sulla cardinalità
                relief='flat'  # Relief piatto per design moderno
            )
            # Posizionamento con padding condizionale per ottimizzazione spazio
            element.pack(padx=1 if padx > 0 else 0, pady=1 if pady > 0 else 0)
            
            # Rendering condizionale degli indici posizionali per array di dimensioni moderate
            # Limitazione a 200 elementi per prevenire sovraccarico visivo dell'interfaccia
            if array_size <= 200:
                # Calcolo delle dimensioni per gli indici con coerenza rispetto agli elementi
                index_width = element_width  # Larghezza sincronizzata con elementi
                index_font_size = max(6, font_size - 2)  # Font size ridotto con limite minimo
                index_padx = padx  # Padding orizzontale coerente
                
                # Istanziazione del widget Label per visualizzazione dell'indice posizionale
                # Formato con parentesi quadre per convenzione matematica degli indici
                index_label = tk.Label(
                    indices_frame,
                    text=f"[{i}]",  # Formato standard per indici array con notazione matematica
                    font=('Segoe UI', index_font_size, 'bold'),  # Font ridotto ma leggibile
                    fg=self.colors['text'],  # Colore del testo per leggibilità
                    bg=self.colors['card'],  # Background neutro per non interferire
                    width=index_width  # Larghezza allineata con elementi soprastanti
                )
                # Posizionamento orizzontale con padding sincronizzato
                index_label.pack(side=tk.LEFT, padx=index_padx)
            
            # Rendering condizionale delle frecce indicatrici per array di piccole dimensioni
            # Limitazione a 100 elementi per mantenere chiarezza visiva delle indicazioni
            if array_size <= 100:
                # Istanziazione del widget Label per frecce indicatrici di stato
                # Utilizzo di emoji Unicode per feedback visivo immediato
                arrow_label = tk.Label(
                    arrows_frame,
                    text=arrow_text,  # Testo della freccia determinato dall'algoritmo di stato
                    font=('Segoe UI', max(8, font_size - 2)),  # Font size con limite minimo
                    fg=self.colors['text'],  # Colore del testo per visibilità
                    bg=self.colors['card'],  # Background neutro per coerenza
                    width=element_width  # Larghezza allineata con elementi
                )
                # Posizionamento con padding sincronizzato per allineamento perfetto
                arrow_label.pack(side=tk.LEFT, padx=padx)
            
            # Attivazione condizionale dell'animazione per elementi significativi
            # Applicazione dell'effetto pulse per elementi centrali o trovati
            if animate and (i == highlight_mid or i == found_index):
                # Invocazione del metodo di animazione per feedback visivo dinamico
                self.animate_element_pulse(element)
        
        # Creazione della sezione legenda con design moderno e layout compatto
        # Implementazione di un sistema di documentazione visiva per l'utente
        legend_container = tk.Frame(container, bg=self.colors['bg'])
        legend_container.pack(pady=15)
        
        # Istanziazione del titolo per la sezione legenda
        # Utilizzo di emoji Unicode per miglioramento dell'appeal visivo
        legend_title = tk.Label(
            legend_container,
            text="🎨 LEGENDA COLORI",  # Titolo con emoji per identificazione immediata
            font=('Segoe UI', 12, 'bold'),  # Font di dimensione media con peso bold
            fg=self.colors['text'],  # Colore del testo per leggibilità
            bg=self.colors['bg']  # Background trasparente per integrazione
        )
        # Posizionamento con padding inferiore per separazione dal contenuto
        legend_title.pack(pady=(0, 5))
        
        # Creazione del frame contenitore per gli elementi della legenda
        # Configurazione con background card per distinzione visiva
        legend_frame = tk.Frame(legend_container, bg=self.colors['card'], relief='flat')
        legend_frame.pack(padx=30, pady=3, ipady=8)
        
        # Definizione della struttura dati per gli elementi della legenda
        # Array di tuple contenenti descrizione testuale e colore associato
        legends = [
            ("👆 Elemento centrale (mid)", self.colors['primary']),  # Elemento mediano nell'algoritmo
            ("⚡ Area di ricerca attiva", self.colors['warning']),  # Intervallo di ricerca corrente
            ("🎉 Elemento trovato!", self.colors['success']),  # Elemento target localizzato
            ("💤 Elementi esclusi", self.colors['shadow'])  # Elementi fuori dall'intervallo
        ]
        
        # Iterazione attraverso gli elementi della legenda per rendering individuale
        # Utilizzo di enumerate per accesso sia all'indice che al contenuto
        for i, (text, color) in enumerate(legends):
            # Creazione del contenitore per ogni elemento della legenda
            # Frame individuale per layout orizzontale degli elementi
            legend_item = tk.Frame(legend_frame, bg=self.colors['card'])
            legend_item.pack(side=tk.LEFT, padx=15)
            
            # Implementazione di un indicatore cromatico circolare
            # Sostituzione del quadrato tradizionale con forma geometrica moderna
            color_container = tk.Frame(legend_item, bg=color, width=18, height=18, relief='flat')
            color_container.pack(side=tk.LEFT)
            # Disabilitazione della propagazione per mantenere dimensioni fisse
            color_container.pack_propagate(False)
            
            # Istanziazione del widget Label per il testo descrittivo
            # Configurazione tipografica per leggibilità e coerenza stilistica
            legend_text = tk.Label(
                legend_item,
                text=text,  # Testo descrittivo con emoji per identificazione rapida
                font=('Segoe UI', 10, 'bold'),  # Font di dimensione media con peso bold
                fg=self.colors['text'],  # Colore del testo per leggibilità
                bg=self.colors['card']  # Background neutro per integrazione
            )
            # Posizionamento con padding sinistro per separazione dall'indicatore
            legend_text.pack(side=tk.LEFT, padx=(6, 0))
    
    # Metodo per l'inizializzazione del processo di ricerca binaria
    # Implementa validazione dell'input e gestione automatica dell'ordinamento
    def start_search(self):
        # Controllo dei semafori per prevenire esecuzioni concorrenti
        # Verifica dello stato di ricerca e ordinamento per integrità operazionale
        if self.searching or self.sorting:
            return
        
        # Blocco di gestione delle eccezioni per validazione dell'input utente
        # Tentativo di conversione del valore target da stringa a intero
        try:
            self.target = int(self.target_entry.get())
        except ValueError:
            # Gestione dell'errore di conversione con messagebox informativo
            # Utilizzo di messagebox.showerror per feedback immediato all'utente
            messagebox.showerror("Errore", "Inserisci un numero valido!")
            return
        
        # Verifica dell'invariante di ordinamento dell'array
        # Attivazione automatica dell'ordinamento se necessario per la ricerca binaria
        if not self.is_sorted:
            # Aggiornamento del messaggio di stato per informare l'utente
            self.step_label.config(text="🔄 L'array non è ordinato. Ordino automaticamente prima della ricerca...")
            # Attivazione del semaforo di ordinamento per controllo del flusso
            self.sorting = True
            # Disabilitazione del pulsante di ricerca con aggiornamento del testo
            self.search_btn.config(state='disabled', text="🔄 ORDINAMENTO IN CORSO...")
            self.reset_btn.config(state='disabled')
            
            # Avvia ordinamento in thread separato
            thread = threading.Thread(target=self.auto_sort_and_search)
            thread.daemon = True
            thread.start()
            return
        
        # Se già ordinato, avvia direttamente la ricerca
        self.searching = True
        self.search_btn.config(state='disabled', text="🔍 RICERCA IN CORSO...")
        self.reset_btn.config(state='disabled')
        
        # Avvia ricerca in thread separato
        thread = threading.Thread(target=self.binary_search_animated)
        thread.daemon = True
        thread.start()
    
    def auto_sort_and_search(self):
        # Prima ordina
        self.counting_sort_animated()
        # Poi avvia la ricerca
        self.searching = True
        self.sorting = False
        self.search_btn.config(state='disabled', text="🔍 RICERCA IN CORSO...")
        self.binary_search_animated()
    
    def binary_search_animated(self):
        self.left = 0
        self.right = len(self.array) - 1
        steps = 0
        
        self.root.after(0, lambda: self.step_label.config(
            text=f"🎯 Cerco il numero {self.target} nell'array ordinato ✨"
        ))
        self.root.after(0, lambda: self.explanation_label.config(
            text=f"🚀 Iniziamo con l'intero array! Left=0, Right={len(self.array)-1}. Andiamo a trovare il nostro numero!"
        ))
        
        time.sleep(self.get_sort_animation_delay())
        
        while self.left <= self.right:
            steps += 1
            self.mid = (self.left + self.right) // 2
            
            # Aggiorna display con animazione
            self.root.after(0, lambda: self.display_array(
                highlight_left=self.left,
                highlight_right=self.right,
                highlight_mid=self.mid,
                animate=True
            ))
            
            self.root.after(0, lambda s=steps: self.step_label.config(
                text=f"📍 Passo {s}: Controllo elemento centrale [indice {self.mid}] = {self.array[self.mid]} ✨"
            ))
            
            if self.array[self.mid] == self.target:
                # Trovato con animazione speciale!
                time.sleep(self.get_sort_animation_delay() * 0.5)
                self.root.after(0, lambda: self.display_array(found_index=self.mid, animate=True))
                self.root.after(0, lambda s=steps: self.step_label.config(
                    text=f"🎉✨ TROVATO! ✨🎉 Il numero {self.target} è all'indice {self.mid} dopo {s} passi!"
                ))
                self.root.after(0, lambda: self.explanation_label.config(
                    text=f"🎊 Fantastico! L'elemento centrale {self.array[self.mid]} è esattamente quello che cercavamo! Missione compiuta! 🎊"
                ))
                # Animazione di celebrazione
                self.root.after(0, self.celebrate_found)
                self.found = True
                break
                
            elif self.array[self.mid] < self.target:
                # Cerca nella metà destra
                self.root.after(0, lambda s=steps: self.explanation_label.config(
                    text=f"🔍 Il valore centrale {self.array[self.mid]} è minore di {self.target}. Elimino la metà sinistra e cerco a destra! ➡️"
                ))
                time.sleep(self.get_animation_delay())
                self.left = self.mid + 1
                
            else:
                # Cerca nella metà sinistra
                self.root.after(0, lambda s=steps: self.explanation_label.config(
                    text=f"🔍 Il valore centrale {self.array[self.mid]} è maggiore di {self.target}. Elimino la metà destra e cerco a sinistra! ⬅️"
                ))
                time.sleep(self.get_animation_delay())
                self.right = self.mid - 1
            
            self.root.after(0, lambda s=steps: self.stats_label.config(
                text=f"📊 Passi: {s} | Complessità: O(log n) | Elementi rimanenti: {max(0, self.right - self.left + 1)} | Efficienza: Massima! 🚀"
            ))
            
            time.sleep(self.get_animation_delay())
        
        if not self.found:
            # Non trovato
            self.root.after(0, lambda s=steps: self.step_label.config(
                text=f"❌ Il numero {self.target} non è presente nell'array (dopo {s} passi) ❌"
            ))
            self.root.after(0, lambda: self.explanation_label.config(
                text="🔍 La ricerca è terminata senza trovare l'elemento. L'area di ricerca si è ridotta a zero. Prova con un altro numero!"
            ))
            self.root.after(0, lambda: self.display_array(animate=False))
        
        # Riabilita pulsanti
        self.searching = False
        self.root.after(0, lambda: self.search_btn.config(state='normal', text="🚀 ESEGUI RICERCA"))
        self.root.after(0, lambda: self.reset_btn.config(state='normal'))
    
    def animate_element_pulse(self, element):
        """Animazione di pulsazione per gli elementi evidenziati"""
        def pulse(step=0):
            if step < 6:  # 3 pulsazioni complete
                if step % 2 == 0:
                    # Ingrandisci
                    element.config(font=('Segoe UI', 18, 'bold'))
                else:
                    # Riduci
                    element.config(font=('Segoe UI', 16, 'bold'))
                self.root.after(200, lambda: pulse(step + 1))
        pulse()
    
    def celebrate_found(self):
        """Animazione di celebrazione quando l'elemento è trovato"""
        def flash_colors(step=0):
            if step < 8:  # 4 flash completi
                colors = [self.colors['success'], self.colors['accent'], 
                         self.colors['primary'], self.colors['secondary']]
                color = colors[step % len(colors)]
                
                # Cambia colore del frame info
                self.info_frame.config(bg=color)
                self.step_label.config(bg=color, fg='white')
                
                self.root.after(300, lambda: flash_colors(step + 1))
            else:
                # Ripristina colori originali
                self.info_frame.config(bg=self.colors['card'])
                self.step_label.config(bg=self.colors['card'], fg=self.colors['primary'])
        
        flash_colors()
    
    def animate_button_hover(self, button, enter=True):
        """Animazione hover per i pulsanti"""
        if enter:
            button.config(relief='raised', bd=2)
        else:
            button.config(relief='flat', bd=0)
    
    def setup_button_animations(self):
        """Configura le animazioni hover per i pulsanti"""
        self.search_btn.bind('<Enter>', lambda e: self.animate_button_hover(self.search_btn, True))
        self.search_btn.bind('<Leave>', lambda e: self.animate_button_hover(self.search_btn, False))
        
        self.reset_btn.bind('<Enter>', lambda e: self.animate_button_hover(self.reset_btn, True))
        self.reset_btn.bind('<Leave>', lambda e: self.animate_button_hover(self.reset_btn, False))

    def animate_title(self):
        """Animazione continua per il titolo"""
        def pulse_title():
            current_font = self.root.nametowidget(self.root.winfo_children()[0].winfo_children()[0]).cget('font')
            if 'bold' in str(current_font):
                # Cambia colore gradualmente
                colors = [self.colors['primary'], self.colors['secondary'], 
                         self.colors['success'], self.colors['warning']]
                color_index = (self.animation_step // 20) % len(colors)
                
                title_widget = self.root.nametowidget(self.root.winfo_children()[0].winfo_children()[0])
                title_widget.config(fg=colors[color_index])
                
                self.animation_step += 1
                self.root.after(100, pulse_title)
        
        pulse_title()
    
    def start_counting_sort(self):
        """Avvia l'algoritmo di counting sort con animazioni"""
        if self.sorting or self.searching:
            return
        
        if self.is_sorted:
            messagebox.showinfo("Array già ordinato", "L'array è già ordinato! Puoi procedere con la ricerca binaria.")
            return
        
        self.sorting = True
        self.search_btn.config(state='disabled')
        self.reset_btn.config(state='disabled')
        self.sort_btn.config(state='disabled', text="🎯 ORDINAMENTO...")
        
        # Avvia counting sort in thread separato
        thread = threading.Thread(target=self.counting_sort_animated)
        thread.daemon = True
        thread.start()
    
    def counting_sort_animated(self):
        """Implementazione animata del counting sort"""
        self.root.after(0, lambda: self.step_label.config(
            text="🎯 Iniziamo il COUNTING SORT! Preparati per uno spettacolo incredibile! ✨"
        ))
        self.root.after(0, lambda: self.explanation_label.config(
            text="🚀 Il Counting Sort conta le occorrenze di ogni elemento e poi li ricostruisce in ordine!"
        ))
        
        time.sleep(self.get_sort_animation_delay())
        
        # Fase 1: Trova il valore massimo
        max_val = max(self.array)
        self.root.after(0, lambda: self.step_label.config(
            text=f"📊 Fase 1: Trovato valore massimo = {max_val}! Creiamo l'array di conteggio..."
        ))
        self.root.after(0, lambda: self.explanation_label.config(
            text=f"🔍 Abbiamo bisogno di un array di conteggio di dimensione {max_val + 1} per contare ogni numero!"
        ))
        
        time.sleep(self.get_sort_animation_delay())
        
        # Fase 2: Crea array di conteggio
        count = [0] * (max_val + 1)
        
        self.root.after(0, lambda: self.step_label.config(
            text="📈 Fase 2: Contiamo le occorrenze di ogni elemento! Guarda la magia! ✨"
        ))
        
        # Conta ogni elemento con animazione
        for i, num in enumerate(self.array):
            count[num] += 1
            
            # Evidenzia l'elemento corrente
            self.root.after(0, lambda idx=i: self.display_array_with_highlight(idx, "counting"))
            
            self.root.after(0, lambda n=num, c=count[num]: self.step_label.config(
                text=f"🎯 Elemento {n} trovato! Conteggio aggiornato: {c} occorrenze"
            ))
            self.root.after(0, lambda n=num: self.explanation_label.config(
                text=f"📊 Incrementiamo il contatore per il numero {n}. Ogni numero ha il suo 'cassetto' nell'array di conteggio!"
            ))
            
            time.sleep(self.get_sort_animation_delay() * 0.7)
        
        time.sleep(self.get_sort_animation_delay())
        
        # Fase 3: Ricostruisci l'array ordinato
        self.root.after(0, lambda: self.step_label.config(
            text="🎨 Fase 3: Ricostruiamo l'array ordinato! Ecco dove avviene la magia! ✨"
        ))
        self.root.after(0, lambda: self.explanation_label.config(
            text="🚀 Ora ricostruiamo l'array in ordine, usando i conteggi per sapere quante volte inserire ogni numero!"
        ))
        
        time.sleep(self.get_sort_animation_delay())
        
        sorted_array = []
        for num in range(len(count)):
            for _ in range(count[num]):
                sorted_array.append(num)
                
                # Mostra la ricostruzione progressiva
                self.array = sorted_array + self.array[len(sorted_array):]
                self.root.after(0, lambda idx=len(sorted_array)-1: self.display_array_with_highlight(idx, "building"))
                
                self.root.after(0, lambda n=num, pos=len(sorted_array): self.step_label.config(
                    text=f"🎯 Inserito {n} in posizione {pos-1}! Array in costruzione..."
                ))
                self.root.after(0, lambda: self.explanation_label.config(
                    text="🔧 Stiamo ricostruendo l'array elemento per elemento, in ordine crescente perfetto!"
                ))
                
                time.sleep(self.get_sort_animation_delay() * 0.5)
        
        # Finalizza
        self.array = sorted_array
        self.is_sorted = True
        
        # Animazione finale spettacolare
        self.root.after(0, lambda: self.display_array())
        self.root.after(0, lambda: self.step_label.config(
            text="🎉✨ COUNTING SORT COMPLETATO! ✨🎉 Array perfettamente ordinato!"
        ))
        self.root.after(0, lambda: self.explanation_label.config(
            text="🎊 Fantastico! L'array è ora ordinato e pronto per la ricerca binaria! Il Counting Sort ha una complessità O(n+k)! 🎊"
        ))
        self.root.after(0, lambda: self.stats_label.config(
            text=f"📊 Array di {len(self.array)} elementi | Stato: ORDINATO ✅ | Complessità Counting Sort: O(n+k) | Pronto per ricerca! 🚀"
        ))
        
        # Celebrazione finale
        self.root.after(0, self.celebrate_sorting_complete)
        
        # Riabilita pulsanti
        self.sorting = False
        self.root.after(0, lambda: self.search_btn.config(state='normal', text="🚀 INIZIA RICERCA"))
        self.root.after(0, lambda: self.reset_btn.config(state='normal'))
        self.root.after(0, lambda: self.sort_btn.config(state='normal', text="✅ GIÀ ORDINATO"))
    
    def display_array_with_highlight(self, highlight_index, mode="normal"):
        """Visualizza l'array con evidenziazione speciale per il sorting"""
        # Pulisci il frame
        for widget in self.array_frame.winfo_children():
            widget.destroy()
            
        # Crea container per l'array con animazione
        container = tk.Frame(self.array_frame, bg=self.colors['bg'])
        container.pack(expand=True)
        
        # Titolo array dinamico
        if mode == "counting":
            title_text = "🔍 CONTEGGIO IN CORSO 🔍"
            title_color = self.colors['secondary']
        elif mode == "building":
            title_text = "🎨 RICOSTRUZIONE ARRAY 🎨"
            title_color = self.colors['primary']
        else:
            title_text = "📊 ARRAY IN ELABORAZIONE 📊"
            title_color = self.colors['warning']
        
        title_container = tk.Frame(container, bg=title_color, relief='flat')
        title_container.pack(pady=(0, 25), padx=200)
        
        array_title = tk.Label(
            title_container,
            text=title_text,
            font=('Segoe UI', 18, 'bold'),
            fg='white',
            bg=title_color
        )
        array_title.pack(pady=8, padx=20)
        
        # Container principale per array con ombra
        array_container = tk.Frame(container, bg=self.colors['bg'])
        array_container.pack(pady=20)
        
        # Ombra per l'array
        shadow_container = tk.Frame(array_container, bg=self.colors['shadow'], height=8)
        shadow_container.pack(fill='x', padx=8)
        
        # Frame principale per elementi
        main_array_frame = tk.Frame(array_container, bg=self.colors['card'], relief='flat')
        main_array_frame.pack(pady=(0, 8), padx=20, ipady=15)
        
        # Frame per gli elementi
        elements_frame = tk.Frame(main_array_frame, bg=self.colors['card'])
        elements_frame.pack(pady=10)
        
        # Frame per gli indici
        indices_frame = tk.Frame(main_array_frame, bg=self.colors['card'])
        indices_frame.pack(pady=(5, 10))
        
        for i, value in enumerate(self.array):
            # Determina il colore e lo stile
            if i == highlight_index:
                if mode == "counting":
                    color = self.colors['secondary']
                    text_color = 'white'
                    border_color = '#e85a9d'
                elif mode == "building":
                    color = self.colors['success']
                    text_color = 'white'
                    border_color = '#00a085'
                else:
                    color = self.colors['primary']
                    text_color = 'white'
                    border_color = '#5a63e8'
            elif mode == "building" and i < highlight_index:
                # Elementi già ordinati
                color = self.colors['accent']
                text_color = self.colors['text']
                border_color = '#e8c93a'
            else:
                color = self.colors['card']
                text_color = self.colors['text']
                border_color = self.colors['shadow']
            
            # Container per elemento con bordo colorato
            element_container = tk.Frame(elements_frame, bg=border_color, relief='flat')
            element_container.pack(side=tk.LEFT, padx=3, pady=2)
            
            # Elemento dell'array con stile moderno
            element = tk.Label(
                element_container,
                text=str(value),
                font=('Segoe UI', 16, 'bold'),
                bg=color,
                fg=text_color,
                width=4,
                height=2,
                relief='flat'
            )
            element.pack(padx=2, pady=2)
            
            # Indice con stile elegante
            index_label = tk.Label(
                indices_frame,
                text=f"[{i}]",
                font=('Segoe UI', 11, 'bold'),
                fg=self.colors['text'],
                bg=self.colors['card'],
                width=6
            )
            index_label.pack(side=tk.LEFT, padx=3)
            
            # Animazione per l'elemento evidenziato
            if i == highlight_index:
                self.animate_element_pulse(element)
    
    def celebrate_sorting_complete(self):
        """Animazione di celebrazione per il completamento dell'ordinamento"""
        def flash_colors(step=0):
            if step < 12:  # 6 flash completi
                colors = [self.colors['success'], self.colors['accent'], 
                         self.colors['primary'], self.colors['secondary'],
                         self.colors['warning'], '#ff6b9d']
                color = colors[step % len(colors)]
                
                # Cambia colore del frame info
                self.info_frame.config(bg=color)
                self.step_label.config(bg=color, fg='white')
                self.explanation_label.config(bg=color, fg='white')
                
                self.root.after(200, lambda: flash_colors(step + 1))
            else:
                # Ripristina colori originali
                self.info_frame.config(bg=self.colors['card'])
                self.step_label.config(bg=self.colors['card'], fg=self.colors['primary'])
                self.explanation_label.config(bg=self.colors['card'], fg=self.colors['text'])
        
        flash_colors()

def main():
    root = tk.Tk()
    
    # Configura l'icona e altre proprietà della finestra
    root.resizable(True, True)
    root.minsize(1000, 700)
    
    # Centra la finestra sullo schermo
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - 1200) // 2
    y = (screen_height - 800) // 2
    root.geometry(f"1200x800+{x}+{y}")
    
    app = BinarySearchGUI(root)
    
    # Messaggio di benvenuto
    root.after(1000, lambda: app.step_label.config(
        text="🌟 Benvenuto nel Visualizzatore di Ricerca Binaria! Genera un array e inizia l'esplorazione! 🌟"
    ))
    
    root.mainloop()

if __name__ == "__main__":
    main()