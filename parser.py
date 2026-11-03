tokens = []
pos = 0

def current():
    if pos >= len(tokens):
        return None
    return tokens[pos]

def advance():
    global pos

    token = current()
    pos += 1
    return token

def expect(expected):
    token = current()

    if token != expected:
        raise SyntaxError(f"Atteso {expected}, trovato {token}")

    return advance()

def parse_unary():
    if current() == "MENO":
        advance()
        operand = parse_unary()
        return ("UNARY", "MENO", operand)

    if current() == "NON":
        advance()
        operand = parse_unary()
        return ("UNARY", "NON", operand)

    return parse_primary()

def parse_primary():
    token = current()

    if isinstance(token, tuple) and token[0] == "NUMERO":
        advance()
        return ("NUMERO", token[1])

    if isinstance(token, tuple) and token[0] == "STRINGA":
        advance()
        return ("STRINGA", token[1])

    if isinstance(token, tuple) and token[0] == "IDENTIFICATORE":
        if pos + 1 < len(tokens) and tokens[pos + 1] == "CON":
            return parse_call()

        advance()
        return ("VAR", token[1])

    if token == "VERO":
        advance()
        return ("VERO",)

    if token == "FALSO":
        advance()
        return ("FALSO",)

    if token == "NULLA":
        advance()
        return ("NULLA", None)

    if token == "LISTA":
        return parse_list()

    if token == "INSERISCI":
        return parse_input()

    if token == "LUNGHEZZA":
        return parse_len()

    if token == "PARENTESI_S":
        advance()

        expr = parse_expression()

        expect("PARENTESI_D")

        return expr

    raise SyntaxError("Espressione non valida")

def parse_factor():
    left = parse_access()

    while current() in ("PER", "POTENZA", "DIVISO", "MODULO"):
        operator = advance()
        right = parse_access()

        left = ("BINOP", operator, left, right)

    return left

def parse_term():
    left = parse_factor()

    while current() in ("PIU", "MENO"):
        operator = advance()
        right = parse_factor()

        left = ("BINOP", operator, left, right)

    return left

def parse_expression():
    left = parse_and()

    while current() == "O":
        operator = advance()
        right = parse_and()

        left = ("BINOP", operator, left, right)

    return left

def parse_and():
    left = parse_comparison()

    while current() == "E":
        operator = advance()
        right = parse_comparison()

        left = ("BINOP", operator, left, right)

    return left

def parse_comparison():
    left = parse_term()

    while current() in (
        "MAGGIORE",
        "MINORE",
        "MAGGIORE_UGUALE",
        "MINORE_UGUALE",
        "UGUALE_A",
        "NON_UGUALE_A"
    ):
        operator = advance()
        right = parse_term()

        left = ("BINOP", operator, left, right)

    return left

def parse_list():
    expect("LISTA")
    expect("CON")

    elements = []

    elements.append(parse_expression())

    if elements[0][1] == None:
        return ("LISTA", None)

    while current() == "VIRGOLA":
        advance()
        elements.append(parse_expression())

    return ("LISTA", elements)

def parse_block():
    expect("NEWLINE")
    expect("INDENT")

    statements = []

    while current() != "DEDENT" and current() is not None:
        if current() == "NEWLINE":
            advance()
            continue

        statements.append(parse_statement())

    expect("DEDENT")

    return statements

def parse_declaration():
    expect("SIA")

    name = current()

    if not isinstance(name, tuple) or name[0] != "IDENTIFICATORE":
        raise SyntaxError("Nome della variabile atteso")

    advance()

    expect("UGUALE")

    value = parse_expression()

    expect("NEWLINE")

    return ("SIA", name[1], value)

def parse_function():
    expect("FUNZIONE")

    name = current()
    if not isinstance(name, tuple) or name[0] != "IDENTIFICATORE":
        raise SyntaxError("Nome della funzione atteso")

    advance()
    expect("CON")

    parameters = []
    token = current()

    if isinstance(token, tuple) and token[0] == "IDENTIFICATORE":
        parameters.append(token[1])
        advance()

        while current() == "VIRGOLA":
            advance()

            token = current()
            if not isinstance(token, tuple) or token[0] != "IDENTIFICATORE":
                raise SyntaxError("Parametro atteso dopo la virgola")

            parameters.append(token[1])
            advance()

    body = parse_block()

    return ("FUNZIONE", name[1], parameters, body)

def parse_call():
    name = current()
    if not isinstance(name, tuple) or name[0] != "IDENTIFICATORE":
        raise SyntaxError("Nome della funzione atteso")

    advance()

    expect("CON")

    arguments = []

    if current() not in ("NEWLINE", "PARENTESI_D", None):
        arguments.append(parse_expression())

        while current() == "VIRGOLA":
            advance()
            arguments.append(parse_expression())

    return ("CALL", name[1], arguments)

def parse_print():
    expect("STAMPA")

    value = parse_expression()

    expect("NEWLINE")

    return ("STAMPA", value)

def parse_input():
    expect("INSERISCI")

    prompt = None

    token = current()
    if isinstance(token, tuple) and token[0] == "STRINGA":
        prompt = parse_primary()

    return ("INSERISCI", prompt)

def parse_len():
    expect("LUNGHEZZA")

    value = parse_unary()

    return ("LUNGHEZZA", value)

def parse_if():
    expect("SE")

    condition = parse_expression()

    expect("ALLORA")

    body = parse_block()

    otherwise = None

    if current() == "ALTRIMENTI":
        advance()
        otherwise = parse_block()

    return ("SE", condition, body, otherwise)

def parse_foreach():
    expect("PEROGNI")

    nome = current()

    if not isinstance(nome, tuple) or nome[0] != "IDENTIFICATORE":
        raise SyntaxError("Nome della variabile atteso")


    advance()
    expect("IN")

    lista = current()
    if not isinstance(lista, tuple) or lista[0] != "IDENTIFICATORE":
        raise SyntaxError("Nome della lista atteso")

    advance()
    expect("ALLORA")

    body = parse_block()

    return ("PEROGNI", ("VAR", nome[1]), ("VAR", lista[1]), body)

def parse_access():
    node = parse_unary()

    while current() == "DA":
        advance()
        lista = parse_unary()

        node = ("ACCESS", node, lista)

    return node

def parse_while():
    expect("MENTRE")

    cond = parse_expression()

    expect("ALLORA")

    body = parse_block()

    return ("MENTRE", cond, body)

def parse_return():
    expect("RITORNA")

    expr = parse_expression()

    expect("NEWLINE")

    return ("RITORNA", expr)

def parse_statement():
    token = current()

    if isinstance(token, tuple) and token[0] == "IDENTIFICATORE":
        if pos + 1 < len(tokens) and tokens[pos + 1] == "CON":
            node = parse_call()
            expect("NEWLINE")
            return ("CALL_STMT", node)

        raise SyntaxError(f"Istruzione sconosciuta: {token[1]}")

    elif token == "SIA":
        return parse_declaration()

    elif token == "STAMPA":
        return parse_print()

    elif token == "SE":
        return parse_if()

    elif token == "PEROGNI":
        return parse_foreach()

    elif token == "MENTRE":
        return parse_while()

    elif token == "RITORNA":
        return parse_return()

    elif token == "FUNZIONE":
        return parse_function()

    else:
        raise SyntaxError(f"Istruzione sconosciuta: {token}")

def parse_program():
    statements = []

    while current() is not None:
        if current() == "NEWLINE":
            advance()
            continue

        statements.append(parse_statement())

    return ("PROGRAMMA", statements)
