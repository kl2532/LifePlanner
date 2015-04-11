import lex

# ----DELINEATION OF KEYWORDS AND TOKENS----

tokens = (
    'STRING',)

# ----REGULAR EXPRESSION PATTERNS---

# Regular expression patterns
# for whitespace
t_ignore = ' \t'

t_STRING = r'[a-zA-Z]+'


# Lex the input.
lexer = lex.lex()
