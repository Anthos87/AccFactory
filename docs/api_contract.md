openapi: 3.0.0
info:
  title: MVP E-commerce API
  description: Contratto API per il Catalogo Prodotti e la Gestione Carrello
  version: 1.0.0
servers:
  - url: http://localhost:8000/api
    description: Server di Sviluppo

paths:
  /products:
    get:
      summary: Lista Prodotti
      description: Restituisce l'intero catalogo prodotti con supporto alla paginazione.
      parameters:
        - name: page
          in: query
          schema:
            type: integer
            default: 1
        - name: category
          in: query
          schema:
            type: string
        - name: q
          in: query
          description: Testo per la ricerca libera
          schema:
            type: string
      responses:
        '200':
          description: Lista dei prodotti.
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/Product'

  /products/{id}:
    get:
      summary: Dettaglio Prodotto
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          description: Dati completi del prodotto.
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Product'

  /cart/{session_id}:
    get:
      summary: Recupera il carrello
      parameters:
        - name: session_id
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          description: Stato attuale del carrello.
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Cart'

  /cart/{session_id}/items:
    post:
      summary: Aggiunge item al carrello
      parameters:
        - name: session_id
          in: path
          required: true
          schema:
            type: string
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                product_id:
                  type: string
                quantity:
                  type: integer
      responses:
        '201':
          description: Item aggiunto al carrello.

  /cart/{session_id}/items/{item_id}:
    put:
      summary: Aggiorna quantità
      parameters:
        - name: session_id
          in: path
          required: true
          schema:
            type: string
        - name: item_id
          in: path
          required: true
          schema:
            type: string
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                quantity:
                  type: integer
      responses:
        '200':
          description: Quantità aggiornata.
    delete:
      summary: Rimuove item
      parameters:
        - name: session_id
          in: path
          required: true
          schema:
            type: string
        - name: item_id
          in: path
          required: true
          schema:
            type: string
      responses:
        '204':
          description: Item rimosso.

components:
  schemas:
    Product:
      type: object
      properties:
        id:
          type: string
        title:
          type: string
        description:
          type: string
        price:
          type: number
        availability:
          type: boolean
        image_url:
          type: string
    CartItem:
      type: object
      properties:
        id:
          type: string
        product:
          $ref: '#/components/schemas/Product'
        quantity:
          type: integer
    Cart:
      type: object
      properties:
        session_id:
          type: string
        items:
          type: array
          items:
            $ref: '#/components/schemas/CartItem'
        subtotal:
          type: number
        tax:
          type: number
        total:
          type: number
