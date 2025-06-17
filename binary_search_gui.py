import tkinter as tk
from tkinter import ttk, messagebox
import time
import threading
import random
import math

class BinarySearchGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Visualizzatore Ricerca Binaria")
        self.root.geometry("1200x900")
        self.root.configure(bg='#faf8f3')  # Sfondo chiaro crema
        
        # Variabili per l'algoritmo
        self.array = []
        self.target = 0
        self.left = 0
        self.right = 0
        self.mid = 0
        self.found = False
        self.searching = False
        self.sorting = False
        self.is_sorted = False
        self.delay = 1.5  # secondi
        self.array_size = 10  # Dimensione predefinita array
        
        # Colori tema chiaro crema
        self.colors = {
            'bg': '#faf8f3',           # Crema chiaro
            'primary': '#6b73ff',       # Blu elegante
            'secondary': '#ff6b9d',     # Rosa acceso
            'success': '#00d4aa',       # Verde acqua
            'warning': '#ffb347',       # Arancione caldo
            'text': '#2d3748',          # Grigio scuro
            'card': '#ffffff',          # Bianco puro
            'shadow': '#e2e8f0',        # Grigio chiaro per ombre
            'accent': '#ffd93d',        # Giallo dorato
            'gradient_start': '#667eea', # Inizio gradiente
            'gradient_end': '#764ba2'    # Fine gradiente
        }
        
        # Variabili per animazioni
        self.animation_step = 0
        self.pulse_direction = 1
        
        self.setup_ui()
        self.setup_button_animations()
        self.generate_array()
        self.animate_title()
        
    def setup_ui(self):
        # Titolo principale
        title_frame = tk.Frame(self.root, bg=self.colors['bg'])
        title_frame.pack(pady=20)
        
        # Titolo con effetto gradiente simulato
        title_label = tk.Label(
            title_frame,
            text="🔍 VISUALIZZATORE RICERCA BINARIA 🔍",
            font=('Segoe UI', 28, 'bold'),
            fg=self.colors['primary'],
            bg=self.colors['bg']
        )
        title_label.pack()
        
        # Sottotitolo elegante
        subtitle_label = tk.Label(
            title_frame,
            text="✨ Impara come funziona l'algoritmo di ricerca! ✨",
            font=('Segoe UI', 14, 'italic'),
            fg=self.colors['text'],
            bg=self.colors['bg']
        )
        subtitle_label.pack(pady=(8, 0))
        
        # Linea decorativa
        separator = tk.Frame(title_frame, height=3, bg=self.colors['primary'])
        separator.pack(fill='x', padx=100, pady=10)
        
        # Frame controlli con ombra
        control_container = tk.Frame(self.root, bg=self.colors['bg'])
        control_container.pack(pady=25)
        
        # Ombra per il frame controlli
        shadow_frame = tk.Frame(control_container, bg=self.colors['shadow'], height=5)
        shadow_frame.pack(fill='x', padx=5)
        
        control_frame = tk.Frame(control_container, bg=self.colors['card'], relief='flat', bd=0)
        control_frame.pack(fill='x', padx=20, pady=(0, 5), ipady=15)
        
        # Frame per selezione dimensione array
        size_frame = tk.Frame(control_frame, bg=self.colors['card'])
        size_frame.pack(side=tk.LEFT, padx=25)
        
        tk.Label(
            size_frame,
            text="📏 Elementi array:",
            font=('Segoe UI', 13, 'bold'),
            fg=self.colors['text'],
            bg=self.colors['card']
        ).pack()
        
        # Listbox per selezione dimensione
        listbox_container = tk.Frame(size_frame, bg=self.colors['primary'], relief='flat')
        listbox_container.pack(pady=8)
        
        self.size_listbox = tk.Listbox(
            listbox_container,
            font=('Segoe UI', 12, 'bold'),
            width=8,
            height=4,
            justify='center',
            relief='flat',
            bd=3,
            bg=self.colors['bg'],
            fg=self.colors['text'],
            selectbackground=self.colors['primary'],
            selectforeground='white'
        )
        
        # Aggiungi opzioni predefinite (solo 10 e 20)
        sizes = [10, 20]
        for size in sizes:
            self.size_listbox.insert(tk.END, str(size))
        
        # Seleziona 10 come default
        self.size_listbox.selection_set(0)
        self.size_listbox.pack(padx=2, pady=2)
        
        # Bind per aggiornare la dimensione quando selezionata
        self.size_listbox.bind('<<ListboxSelect>>', self.on_size_select)
        
        # Aggiorna array_size con il valore selezionato di default
        self.array_size = int(self.size_listbox.get(0))
        
        # Input per il numero da cercare con stile moderno
        input_frame = tk.Frame(control_frame, bg=self.colors['card'])
        input_frame.pack(side=tk.LEFT, padx=25)
        
        tk.Label(
            input_frame,
            text="🎯 Numero da cercare:",
            font=('Segoe UI', 13, 'bold'),
            fg=self.colors['text'],
            bg=self.colors['card']
        ).pack()
        
        # Container per entry con bordo colorato
        entry_container = tk.Frame(input_frame, bg=self.colors['primary'], relief='flat')
        entry_container.pack(pady=8)
        
        self.target_entry = tk.Entry(
            entry_container,
            font=('Segoe UI', 16, 'bold'),
            width=12,
            justify='center',
            relief='flat',
            bd=3,
            bg=self.colors['bg'],
            fg=self.colors['text']
        )
        self.target_entry.pack(padx=2, pady=2)
        
        # Pulsanti con stile moderno e ombra
        button_frame = tk.Frame(control_frame, bg=self.colors['card'])
        button_frame.pack(side=tk.LEFT, padx=25)
        
        # Pulsante ricerca con effetto 3D
        search_container = tk.Frame(button_frame, bg=self.colors['shadow'])
        search_container.pack(side=tk.LEFT, padx=8)
        
        self.search_btn = tk.Button(
            search_container,
            text="🚀 ESEGUI RICERCA",
            font=('Segoe UI', 10, 'bold'),
            bg=self.colors['success'],
            fg='white',
            command=self.start_search,
            padx=15,
            pady=8,
            relief='flat',
            bd=0,
            cursor='hand2'
        )
        self.search_btn.pack(padx=2, pady=2)
        
        # Pulsante reset con effetto 3D
        reset_container = tk.Frame(button_frame, bg=self.colors['shadow'])
        reset_container.pack(side=tk.LEFT, padx=8)
        
        self.reset_btn = tk.Button(
            reset_container,
            text="🔄 NUOVO ARRAY",
            font=('Segoe UI', 10, 'bold'),
            bg=self.colors['warning'],
            fg='white',
            command=self.generate_array,
            padx=15,
            pady=8,
            relief='flat',
            bd=0,
            cursor='hand2'
        )
        self.reset_btn.pack(padx=2, pady=2)
        

        
        # Frame per l'array
        self.array_frame = tk.Frame(self.root, bg=self.colors['bg'])
        self.array_frame.pack(pady=20, expand=True, fill='both')
        
        # Frame per le informazioni con design moderno
        info_container = tk.Frame(self.root, bg=self.colors['bg'])
        info_container.pack(pady=25, padx=40, fill='x')
        
        # Ombra per info frame
        info_shadow = tk.Frame(info_container, bg=self.colors['shadow'], height=8)
        info_shadow.pack(fill='x', padx=8)
        
        self.info_frame = tk.Frame(info_container, bg=self.colors['card'], relief='flat', bd=0)
        self.info_frame.pack(fill='x', pady=(0, 8), ipady=20)
        
        # Etichette informative con stile elegante
        self.step_label = tk.Label(
            self.info_frame,
            text="✨ Pronto per iniziare la ricerca! ✨",
            font=('Segoe UI', 16, 'bold'),
            fg=self.colors['primary'],
            bg=self.colors['card']
        )
        self.step_label.pack(pady=12)
        
        self.explanation_label = tk.Label(
            self.info_frame,
            text="🎯 La ricerca binaria divide l'array a metà ad ogni passo, eliminando metà degli elementi.",
            font=('Segoe UI', 12),
            fg=self.colors['text'],
            bg=self.colors['card'],
            wraplength=900
        )
        self.explanation_label.pack(pady=(0, 12))
        
        # Frame per statistiche con design accattivante
        stats_container = tk.Frame(self.info_frame, bg=self.colors['accent'], relief='flat')
        stats_container.pack(pady=12, padx=50, fill='x')
        
        self.stats_label = tk.Label(
            stats_container,
            text="📊 Passi: 0 | Complessità: O(log n) | Efficienza: Massima! 🚀",
            font=('Segoe UI', 13, 'bold'),
            fg=self.colors['text'],
            bg=self.colors['accent']
        )
        self.stats_label.pack(pady=8)
        
    def update_speed(self, value):
        self.delay = float(value)
    
    def get_animation_delay(self):
        """Calcola il delay delle animazioni inversamente proporzionale al numero di elementi"""
        base_delay = 0.8  # Delay base in secondi
        min_delay = 0.05  # Delay minimo
        max_delay = 1.5   # Delay massimo
        
        # Calcola delay inversamente proporzionale
        if self.array_size <= 10:
            delay = max_delay
        elif self.array_size >= 500:
            delay = min_delay
        else:
            # Interpolazione logaritmica per una transizione più fluida
            import math
            factor = math.log(self.array_size / 10) / math.log(500 / 10)
            delay = max_delay - (max_delay - min_delay) * factor
        
        return max(min_delay, min(max_delay, delay))
    
    def get_sort_animation_delay(self):
        """Calcola il delay per le animazioni di ordinamento (leggermente più lento)"""
        if self.array_size <= 10:
            return 0.15  # Più lento per array piccoli per vedere meglio
        elif self.array_size <= 20:
            return 0.1   # Rallentato per vedere l'animazione
        elif self.array_size <= 50:
            return 0.05
        elif self.array_size <= 100:
            return 0.02
        elif self.array_size <= 200:
            return 0.01
        else:
            return 0.005  # Ancora veloce ma non troppo
    
    def on_size_select(self, event):
        """Gestisce la selezione della dimensione dell'array"""
        selection = self.size_listbox.curselection()
        if selection:
            self.array_size = int(self.size_listbox.get(selection[0]))
        
    def generate_array(self):
        if self.searching or self.sorting:
            return
            
        # Genera array NON ordinato casuale
        max_value = max(100, self.array_size * 2)  # Assicura varietà di numeri
        self.array = random.sample(range(1, max_value), self.array_size)
        self.is_sorted = False
        self.display_array()
        
        # Reset variabili
        self.left = 0
        self.right = len(self.array) - 1
        self.found = False
        
        self.step_label.config(text="✨ Nuovo array NON ordinato generato! ✨")
        self.explanation_label.config(text="🎯 Array pronto! Clicca su 'ESEGUI RICERCA' per ordinare automaticamente e cercare un numero.")
        self.stats_label.config(text=f"📊 Array di {len(self.array)} elementi | Stato: NON ORDINATO ❌ | Pronto per la ricerca! 🚀")
        
        # Aggiorna stato pulsanti
        self.search_btn.config(state='normal', text="🚀 ESEGUI RICERCA")
        
    def display_array(self, highlight_left=-1, highlight_right=-1, highlight_mid=-1, found_index=-1, animate=True):
        # Pulisci il frame
        for widget in self.array_frame.winfo_children():
            widget.destroy()
            
        # Crea container per l'array con animazione
        container = tk.Frame(self.array_frame, bg=self.colors['bg'])
        container.pack(expand=True)
        
        # Titolo array con stile elegante
        title_bg_color = self.colors['success'] if self.is_sorted else self.colors['warning']
        title_text = "📊 ARRAY ORDINATO 📊" if self.is_sorted else "📊 ARRAY NON ORDINATO 📊"
        
        title_container = tk.Frame(container, bg=title_bg_color, relief='flat')
        title_container.pack(pady=(0, 25), padx=200)
        
        array_title = tk.Label(
            title_container,
            text=title_text,
            font=('Segoe UI', 18, 'bold'),
            fg='white',
            bg=title_bg_color
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
        
        # Frame per le frecce indicatrici
        arrows_frame = tk.Frame(main_array_frame, bg=self.colors['card'])
        arrows_frame.pack(pady=(0, 5))
        
        for i, value in enumerate(self.array):
            # Determina il colore e lo stile
            color = self.colors['card']
            text_color = self.colors['text']
            border_color = self.colors['shadow']
            arrow_text = ""
            
            if i == found_index:
                color = self.colors['success']
                text_color = 'white'
                border_color = '#00a085'
                arrow_text = "🎉"
            elif i == highlight_mid:
                color = self.colors['primary']
                text_color = 'white'
                border_color = '#5a63e8'
                arrow_text = "👆"
            elif highlight_left <= i <= highlight_right and highlight_left != -1:
                color = self.colors['warning']
                text_color = 'white'
                border_color = '#e8a23a'
                if i == highlight_left:
                    arrow_text = "⬅️"
                elif i == highlight_right:
                    arrow_text = "➡️"
            
            # Calcola dimensioni elemento per renderli sempre tutti visibili
            array_size = len(self.array)
            
            # Calcola larghezza e font size in base al numero di elementi
            if array_size <= 10:
                element_width = 5
                font_size = 14
                padx = 2
                pady = 2
                height = 2
            elif array_size <= 20:
                element_width = 3
                font_size = 12
                padx = 1
                pady = 1
                height = 2
            elif array_size <= 50:
                element_width = 3
                font_size = 12
                padx = 1
                pady = 1
                height = 2
            elif array_size <= 100:
                element_width = 2
                font_size = 10
                padx = 1
                pady = 1
                height = 1
            elif array_size <= 200:
                element_width = 2
                font_size = 8
                padx = 0
                pady = 1
                height = 1
            elif array_size <= 300:
                element_width = 1
                font_size = 7
                padx = 0
                pady = 0
                height = 1
            else:
                element_width = 1
                font_size = 6
                padx = 0
                pady = 0
                height = 1
            
            # Container per elemento con bordo colorato
            element_container = tk.Frame(elements_frame, bg=border_color, relief='flat')
            element_container.pack(side=tk.LEFT, padx=padx, pady=pady)
            
            # Elemento dell'array con stile moderno
            element = tk.Label(
                element_container,
                text=str(value),
                font=('Segoe UI', font_size, 'bold'),
                bg=color,
                fg=text_color,
                width=element_width,
                height=height,
                relief='flat'
            )
            element.pack(padx=1 if padx > 0 else 0, pady=1 if pady > 0 else 0)
            
            # Indice con stile elegante (solo se ci sono meno di 200 elementi)
            if array_size <= 200:
                index_width = element_width
                index_font_size = max(6, font_size - 2)
                index_padx = padx
                
                index_label = tk.Label(
                    indices_frame,
                    text=f"[{i}]",
                    font=('Segoe UI', index_font_size, 'bold'),
                    fg=self.colors['text'],
                    bg=self.colors['card'],
                    width=index_width
                )
                index_label.pack(side=tk.LEFT, padx=index_padx)
            
            # Freccia indicatrice (solo se ci sono meno di 100 elementi)
            if array_size <= 100:
                arrow_label = tk.Label(
                    arrows_frame,
                    text=arrow_text,
                    font=('Segoe UI', max(8, font_size - 2)),
                    fg=self.colors['text'],
                    bg=self.colors['card'],
                    width=element_width
                )
                arrow_label.pack(side=tk.LEFT, padx=padx)
            
            # Animazione di entrata per i nuovi elementi
            if animate and (i == highlight_mid or i == found_index):
                self.animate_element_pulse(element)
        
        # Legenda con design moderno e compatto
        legend_container = tk.Frame(container, bg=self.colors['bg'])
        legend_container.pack(pady=15)
        
        # Titolo legenda
        legend_title = tk.Label(
            legend_container,
            text="🎨 LEGENDA COLORI",
            font=('Segoe UI', 12, 'bold'),
            fg=self.colors['text'],
            bg=self.colors['bg']
        )
        legend_title.pack(pady=(0, 5))
        
        legend_frame = tk.Frame(legend_container, bg=self.colors['card'], relief='flat')
        legend_frame.pack(padx=30, pady=3, ipady=8)
        
        legends = [
            ("👆 Elemento centrale (mid)", self.colors['primary']),
            ("⚡ Area di ricerca attiva", self.colors['warning']),
            ("🎉 Elemento trovato!", self.colors['success']),
            ("💤 Elementi esclusi", self.colors['shadow'])
        ]
        
        for i, (text, color) in enumerate(legends):
            legend_item = tk.Frame(legend_frame, bg=self.colors['card'])
            legend_item.pack(side=tk.LEFT, padx=15)
            
            # Cerchio colorato invece di quadrato
            color_container = tk.Frame(legend_item, bg=color, width=18, height=18, relief='flat')
            color_container.pack(side=tk.LEFT)
            color_container.pack_propagate(False)
            
            legend_text = tk.Label(
                legend_item,
                text=text,
                font=('Segoe UI', 10, 'bold'),
                fg=self.colors['text'],
                bg=self.colors['card']
            )
            legend_text.pack(side=tk.LEFT, padx=(6, 0))
    
    def start_search(self):
        if self.searching or self.sorting:
            return
        
        try:
            self.target = int(self.target_entry.get())
        except ValueError:
            messagebox.showerror("Errore", "Inserisci un numero valido!")
            return
        
        # Controlla se l'array è ordinato e ordina automaticamente se necessario
        if not self.is_sorted:
            self.step_label.config(text="🔄 L'array non è ordinato. Ordino automaticamente prima della ricerca...")
            # Avvia ordinamento e poi ricerca
            self.sorting = True
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