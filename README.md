# Tramezzo

## Sintassi

### Variabili

Le variabili vengono dichiarate utilizzando la parola chiave `sia`.

```text
sia x = 10
sia nome = "Mario"
```

### Output

Utilizza `stampa` per visualizzare un valore.

```text
stampa "Ciao, mondo!"
stampa 10 + 5
```

### Condizioni

Le istruzioni condizionali utilizzano `se`, `allora` e `altrimenti`.

```text
sia x = 10

se x > 5 allora
    stampa "Maggiore di 5"
altrimenti
    stampa "Minore o uguale a 5"
```

### Liste

Le liste vengono create utilizzando `lista con`.

```text
sia numeri = lista con 1, 2, 3, 4, 5
```

Si può creare una lista vuota utilizzando la parola chiave `nulla`.
```text
sia lista_vuota = lista con nulla
```

È possibile accedere ai singoli elementi utilizzando `da`.

```text
stampa 0 da numeri
```

È anche possibile ottenere la lunghezza di una lista utilizzando `lunghezza`.
```text
stampa lunghezza numeri
```
#### Matrice

a seguire è la sintassi per implementare le matrici.
```text
sia x = lista con (lista con 1,2,3), (lista con 4,5,6), (lista con 7,8,9)

sia riga = 1 da x
stampa 1 da riga # stampa 5

# oppure

sia num = 1 da (1 da x)
stampa num # stampa 5
```

### Cicli

Per iterare sugli elementi di una lista si utilizza `perogni`.

```text
perogni numero in numeri allora
    stampa numero
```

È inoltre possibile utilizzare `mentre` per creare cicli condizionali.

```text
sia x = 0

mentre x < 5 allora
    stampa x
    sia x = x + 1
```

### Funzioni

Le funzioni vengono dichiarate utilizzando `funzione`, mentre i parametri vengono introdotti con `con`.

```text
funzione somma con a, b
    ritorna a + b

sia risultato = somma con 10, 20
stampa risultato
```

### Input

Utilizza `inserisci` per ricevere dati dall'utente.

```text
stampa "Come ti chiami?"
sia nome = inserisci "io mi chiamo: "

stampa nome
```

### Commenti

per aggiungere commenti al codice basta aggiungere un `#`.

```text
se x % 2 == 0 allora # x è pari
    stampa "maggiore di 5"
```

commenti multilinee si aprono con `#-` e chiudono con `-#`.

```text
#-
lista non deve contenere 0
0, 1, 2
3, 4, 5
-#
perogniqualvolta numero in lista allora
    se lista con numero == 0 allora
    lista con numero += 1
```
