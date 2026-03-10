import os
import requests
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('GITHUB_TOKEN')
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}
REPO = "Anthos87/AccFactory"
URL = f"https://api.github.com/repos/{REPO}/issues"

def update_issue(issue_number, title, body):
    res = requests.patch(f"{URL}/{issue_number}", headers=HEADERS, json={"title": title, "body": body})
    if res.status_code == 200:
        print(f"Issue #{issue_number} updated: {res.json()['html_url']}")
    else:
        print(f"Error updating issue #{issue_number}: {res.status_code} - {res.text}")

master_body = """### Obiettivo
Realizzare l'MVP di una piattaforma e-commerce focalizzata sull'esperienza utente nel processo di navigazione del catalogo e nell'acquisto tramite carrello.

### Requisiti di Business
#### 1. Catalogo Prodotti
- Gli utenti devono poter visualizzare una **griglia o lista di prodotti**.
- Ogni prodotto deve mostrare: immagine, titolo, descrizione breve, prezzo e disponibilità.
- Possibilità di filtrare (es. per categoria) e ricercare i prodotti tramite testo libero.

#### 2. Gestione Carrello
- Gli utenti devono poter aggiungere uno o più prodotti al carrello dalla pagina di dettaglio o prettamente dal catalogo.
- Nel carrello, deve essere possibile modificare le quantità o rimuovere un articolo.
- Il carrello deve mostrare il riepilogo dei costi (subtotale, tasse stimate, totale).
- Il carrello deve essere persistente (es. tramite sessione o local storage per utenti Guest).

#### 3. Processo di Check-out (Bozza MVP)
- Riepilogo ordine prima della conferma finale.
- Mock del sistema di pagamento per simulare un flusso E2E completo."""

backend_body = """**Assegnato a:** `backend_agent`

### Descrizione Tecnica e Funzionale
L'agente di backend è responsabile di implementare le API necessarie per supportare le funzionalità di Catalogo e Carrello descritte nella Master Issue. I servizi devono essere robusti, documentati e coperti da test.

### Requisiti Architetturali e di Sviluppo
#### 1. Progettazione API (`api_contract.md`)
- Definire i contratti OpenAPI per tutti gli endpoint esposti, garantendo che l'interfaccia sia documentata e chiara per il Front-End fin dall'inizio.

#### 2. Gestione Catalogo (Endpoint di Lettura)
- `GET /api/products`: Restituisce la lista dei prodotti. Deve supportare la paginazione, i filtri per categoria e la ricerca testuale (`?q=...&category=...&page=...`).
- `GET /api/products/{id}`: Restituisce il dettaglio completo di un singolo prodotto comprensivo di metadata.

#### 3. Gestione Carrello (Risorsa e Sessione)
- `GET /api/cart/{session_id}`: Recupera lo stato attuale del carrello per una specifica sessione utente anonima o registrata.
- `POST /api/cart/{session_id}/items`: Aggiunge un prodotto al carrello. Deve processare il Payload (`product_id`, `quantity`) e validare la disponibilità d'inventario (mockata).
- `PUT /api/cart/{session_id}/items/{item_id}`: Aggiorna la quantità di uno specifico articolo, riverificando l'inventario e ri-calcolando il totale.
- `DELETE /api/cart/{session_id}/items/{item_id}`: Rimuove il prodotto dal carrello e aggiorna lo stato.

#### 4. Qualità del Codice e Testing
- Sviluppare all'interno della cartella `/server`.
- Scrivere **Unit Test e Integration Test** per ogni endpoint. Devono essere garantiti test case di successo (200, 201) e test case d'errore (400, 404, 500), confermando il corretto fault-tolerance (es. aggiungere item inesistente).
- Le risposte API devono essere in formato JSON standardizzato (JSend layout preferibile)."""

frontend_body = """**Assegnato a:** `frontend_agent`

### Descrizione Tecnica e Funzionale
L'agente di frontend è incaricato di creare le interfacce utente per l'MVP, garantendo una User Experience (UX) fluida, moderna, responsive e capace di incrementare conversion rate e l'ingaggio utente, usando React/Next.js.

### Requisiti Architetturali e di Sviluppo
#### 1. Layout e Navigazione Strutturale
- Implementare il layout principale con **Header** (che include il contatore real-time degli item nel carrello) e **Footer** istituzionale.
- Il design system deve essere basato su **Tailwind CSS**.

#### 2. Esperienza Catalogo Utente
- Sviluppare una **Product Grid** responsive (CSS Grid/Flexbox) che consumi attivamente l'endpoint `GET /api/products`.
- Implemetare **Product Card** eleganti e funzionali:
  - Call-To-Action primarie e secondarie ("Dettaglio", "Aggiungi al Carrello").
  - Hover effects per evidenziare l'interattività e lazy loading delle immagini.
- Fornire gli strumenti di filtro e la search bar, implementando tecniche per evitare sovraccarico di rete (Debouncing).

#### 3. Gestione Stato Carrello e Interazioni API
- Introdurre e configurare un Global State Manager (Context API / Redux) per mantenere reattivo l'intero portale in relazione ai cambiamenti del carrello.
- Invocare i servizi REST (POST, PUT, DELETE su `/api/cart/...`). Fornire sempre un adeguato Feedback all'utente, gestendo gli "UI Loading State" ed eventuali Alert d'errore (Toast Notifications), garantendo una User-Journey non interruttiva.

#### 4. UI/UX Carrello (Modal o Off-Canvas)
- Progettare la schermata/Flyout del Carrello, calcolando dinamicamente a client i subtotali in real-time all'aggiunta/rimozione.
- Fornire selettori di quantità reattivi che effettuano chiamate `PUT` dirette in background.

#### 5. Guidelines di Qualità
- Creare i componenti UI modularizzati dentro `/client`.
- Evitare div-soup, utilizzare semantica HTML5 completa e curare l'accessibilità base (a11y aria-label)."""

print("Updating Master Task...")
update_issue(1, "Sviluppo MVP E-commerce [Epic]", master_body)

print("Updating Backend Task...")
update_issue(2, "Task Backend: Sviluppo API e Unit Test per Catalogo e Carrello", backend_body)

print("Updating Frontend Task...")
update_issue(3, "Task Frontend: Sviluppo Interfacce UX/UI React per Catalogo e Carrello", frontend_body)
