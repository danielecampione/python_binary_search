# 🔍 Visualizzatore Ricerca Binaria

Un'applicazione Python con interfaccia grafica che mostra in modo interattivo e comprensibile come funziona l'algoritmo di ricerca binaria.

## 🚀 Come Eseguire l'Applicazione

### Prerequisiti
- Python 3.x installato sul sistema
- Tkinter (incluso di default con Python)

### Esecuzione
```bash
python binary_search_gui.py
```

Oppure su Windows:
```bash
py binary_search_gui.py
```

## Schermata catturata

![Png](https://i.ibb.co/Rps9sCXG/Immagine-2025-06-25-231519.png)


## 🎯 Caratteristiche dell'Applicazione

### Interface Utente
- **Design moderno**: Interfaccia scura e accattivante con colori vivaci
- **Controlli intuitivi**: Pulsanti grandi e chiari per ogni azione
- **Slider velocità**: Regola la velocità dell'animazione da 0.5 a 3 secondi
- **Input semplice**: Campo di testo per inserire il numero da cercare

### Visualizzazione dell'Algoritmo
- **Array colorato**: Ogni elemento è rappresentato da un riquadro colorato
- **Animazioni fluide**: L'algoritmo procede passo dopo passo con delay configurabile
- **Codifica colori**:
  - 🟦 **Blu**: Elemento centrale (mid) attualmente esaminato
  - 🟨 **Giallo**: Area di ricerca attiva (da left a right)
  - 🟩 **Verde**: Elemento trovato!
  - ⬜ **Grigio**: Elementi non più considerati

### Spiegazioni Educative
- **Descrizioni passo-passo**: Ogni operazione è spiegata in linguaggio semplice
- **Statistiche in tempo reale**: Mostra il numero di passi e gli elementi rimanenti
- **Complessità algoritmica**: Visualizza la complessità O(log n)
- **Messaggi informativi**: Spiegazioni chiare per principianti assoluti

## 🧠 Come Funziona la Ricerca Binaria

### Principio Base
La ricerca binaria è un algoritmo di ricerca che funziona **solo su array ordinati**. Il principio è semplice:

1. **Dividi**: Guarda l'elemento centrale dell'array
2. **Confronta**: 
   - Se è quello che cerchi → **TROVATO!**
   - Se è più piccolo → cerca nella metà destra
   - Se è più grande → cerca nella metà sinistra
3. **Ripeti**: Continua fino a trovare l'elemento o esaurire le possibilità

### Vantaggi
- **Velocità**: Molto più veloce della ricerca lineare
- **Efficienza**: Elimina metà degli elementi ad ogni passo
- **Complessità**: O(log n) invece di O(n)

### Esempio Pratico
Se hai un array di 1000 elementi:
- **Ricerca lineare**: fino a 1000 confronti
- **Ricerca binaria**: massimo 10 confronti!

## 🎮 Come Usare l'Applicazione

1. **Avvia l'applicazione**: Esegui il file Python
2. **Osserva l'array**: Viene generato automaticamente un array ordinato casuale
3. **Inserisci un numero**: Scrivi il numero che vuoi cercare
4. **Regola la velocità**: Usa lo slider per impostare la velocità dell'animazione
5. **Inizia la ricerca**: Clicca "🚀 INIZIA RICERCA"
6. **Osserva l'algoritmo**: Guarda come procede passo dopo passo
7. **Genera nuovo array**: Clicca "🔄 NUOVO ARRAY" per ricominciare

## 🎨 Dettagli Tecnici

### Struttura del Codice
- **Classe principale**: `BinarySearchGUI` gestisce tutta l'interfaccia
- **Threading**: La ricerca avviene in un thread separato per non bloccare l'UI
- **Animazioni**: Aggiornamenti dell'interfaccia sincronizzati con l'algoritmo
- **Gestione eventi**: Controlli reattivi e validazione input

### Funzionalità Avanzate
- **Generazione array casuale**: Array ordinati di 15 elementi casuali
- **Validazione input**: Controllo errori per input non validi
- **Stato dell'applicazione**: Disabilitazione controlli durante la ricerca
- **Messaggi informativi**: Feedback costante all'utente

## 🎓 Valore Educativo

Questa applicazione è perfetta per:
- **Studenti**: Capire visivamente come funziona la ricerca binaria
- **Insegnanti**: Strumento didattico per spiegare algoritmi
- **Principianti**: Introduzione ai concetti di algoritmi e complessità
- **Curiosi**: Chiunque voglia vedere "in azione" un algoritmo famoso

### Concetti Insegnati
- Algoritmi di ricerca
- Complessità computazionale
- Importanza dell'ordinamento
- Strategia "divide et impera"
- Efficienza algoritmica

## 🔧 Personalizzazioni Possibili

- Modificare la dimensione dell'array
- Cambiare i colori del tema
- Aggiungere suoni alle animazioni
- Implementare altri algoritmi di ricerca
- Aggiungere modalità di confronto

---

**Buon divertimento nell'esplorare il mondo degli algoritmi! 🚀**
