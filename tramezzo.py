import sys

import lexer
import parser

scopes = [{}]
functions = {}


class ReturnValue(Exception):
    def __init__(self, value):
        self.value = value

def create_scope():
    scopes.append({})


def destroy_scope():
    if len(scopes) > 1:
        scopes.pop()


def get_var(name):
    for scope in reversed(scopes):
        if name in scope:
            return scope[name]

    raise NameError(f"Variabile non definita: {name}")


def set_var(name, value):
    scopes[-1][name] = value


def formatta(valore):
    if isinstance(valore, bool):
        return "vero" if valore else "falso"

    if isinstance(valore, float):
        if valore == int(valore):
            return str(int(valore))
        return str(valore).replace(".", ",")

    if isinstance(valore, list):
        return "[" + ", ".join(formatta(v) for v in valore) + "]"

    return str(valore)


def evaluate(node, functions):
    tipo = node[0]

    if tipo == "NUMERO" or tipo == "STRINGA":
        return node[1]

    elif tipo == "VERO":
        return True

    elif tipo == "FALSO":
        return False

    elif tipo == "VAR":
        return get_var(node[1])

    elif tipo == "INSERISCI":
        prompt = evaluate(node[1], functions) if node[1] is not None else ""
        return input(prompt)

    elif tipo == "LUNGHEZZA":
        return len(evaluate(node[1], functions))

    elif tipo == "LISTA":
        if node[1] == None:
            return []
        return [evaluate(element, functions) for element in node[1]]

    elif tipo == "ACCESS":
        indice = evaluate(node[1], functions)
        lista = evaluate(node[2], functions)

        return lista[indice]

    elif tipo == "CALL":
        nome = node[1]
        argomenti = node[2]

        if nome not in functions:
            raise NameError(f"Funzione non definita: {nome}")

        parametri, corpo = functions[nome]

        if len(argomenti) != len(parametri):
            raise TypeError(
                f"{nome} richiede {len(parametri)} argomenti, "
                f"ma ne sono stati forniti {len(argomenti)}"
            )

        valori = [
            evaluate(argomento, functions)
            for argomento in argomenti
        ]

        create_scope()

        try:
            for parametro, valore in zip(parametri, valori):
                set_var(parametro, valore)

            for statement in corpo:
                execute(statement, functions)

            return None

        except ReturnValue as result:
            return result.value

        finally:
            destroy_scope()

    elif tipo == "UNARY":
        operator = node[1]
        value = evaluate(node[2], functions)

        if operator == "MENO":
            return -value

        elif operator == "NON":
            return not value

    elif tipo == "BINOP":
        operator = node[1]

        left = evaluate(node[2], functions)

        if operator == "E":
            return left and evaluate(node[3], functions)

        elif operator == "O":
            return left or evaluate(node[3], functions)

        right = evaluate(node[3], functions)

        if operator == "PIU":
            return left + right

        elif operator == "MENO":
            return left - right

        elif operator == "PER":
            return left * right

        elif operator == "DIVISO":
            return left / right

        elif operator == "MODULO":
            return left % right

        elif operator == "POTENZA":
            return left ** right

        elif operator == "MAGGIORE":
            return left > right

        elif operator == "MINORE":
            return left < right

        elif operator == "MAGGIORE_UGUALE":
            return left >= right

        elif operator == "MINORE_UGUALE":
            return left <= right

        elif operator == "UGUALE_A":
            return left == right

        elif operator == "NON_UGUALE_A":
            return left != right

    raise SyntaxError(f"Espressione sconosciuta: {tipo}")


# EXECUTION

def execute(node, functions):
    tipo = node[0]

    if tipo == "PROGRAMMA":
        for statement in node[1]:
            execute(statement, functions)

    elif tipo == "SIA":
        nome = node[1]
        valore = evaluate(node[2], functions)

        set_var(nome, valore)

    elif tipo == "RITORNA":
        value = evaluate(node[1], functions)
        raise ReturnValue(value)

    elif tipo == "FUNZIONE":
        nome = node[1]
        parametri = node[2]
        corpo = node[3]

        functions[nome] = (parametri, corpo)

    elif tipo == "STAMPA":
        valore = evaluate(node[1], functions)
        print(formatta(valore))

    elif tipo == "SE":
        condition = evaluate(node[1], functions)

        if condition:
            for statement in node[2]:
                execute(statement, functions)

        elif node[3] is not None:
            for statement in node[3]:
                execute(statement, functions)

    elif tipo == "MENTRE":
        while evaluate(node[1], functions):
            for statement in node[2]:
                execute(statement, functions)

    elif tipo == "PEROGNI":
        nome = node[1][1]
        elementi = evaluate(node[2], functions)

        for elemento in elementi:
            set_var(nome, elemento)

            for statement in node[3]:
                execute(statement, functions)
    elif tipo == "CALL_STMT":
        evaluate(node[1], functions)

with open(sys.argv[1], "r") as programma:
    if not sys.argv[1].endswith(".tmz"):
        raise NameError(f"Nome file invalido {sys.argv[1]}: i file devono terminare in .tmz")
    programma = programma.read()
    parser.tokens = lexer.tokenize_source(programma)
    ast = parser.parse_program()

    execute(ast, functions)
