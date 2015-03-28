import ply.lex as lex

# ----DELINEATION OF KEYWORDS AND TOKENS----

tokens = (
    'INTEGER','DECIMAL','CHARACTER', 'STRING', 
    'PLUS','MINUS','DIVIDE',
    'TIMES', 'NEWLINE', 'LEFTPAREN',
    'RIGHTPAREN', 'BUILD', 'PRINT'
)

# ----REGULAR EXPRESSION PATTERNS---

# Regular expression patterns for basic 
# constants (integer, decimal, character)
t_INTEGER    = r'[\-]?[0-9]+'
t_DECIMAL    = r'[\-]?[0-9]+\.[0-9]*'
t_CHARACTER  = r'(\'[^\']\')'
t_STRING     = r'(\"[^\"]*\")'

# Regular expression patterns for arithmetic
# operators.
t_PLUS       = r'\+'
t_MINUS	     = r'\-'
t_TIMES      = r'\*'
t_DIVIDE    = r'/'

t_ignore = ' \t'

# Regular expression patterns for multi-use
# tokens.
t_LEFTPAREN  = r'\('
t_RIGHTPAREN = r'\)'
t_BUILD = r'(build schedule)'
t_PRINT = r'(print)'

def t_NEWLINE(t):       # When a \n is found,
    r'\n'               # increment the line
    t.lexer.lineno +=1  # number of the lexer.
    return t            # This way, line count
                        # and errors can be
                        # reported precisely.

# ----ERROR HANDLING----

# If an error is found, attempt to recover by
# skipping the invalid character.

def t_error(t):
    t.lexer.skip(1)

# Lex the input.
lexer = lex.lex()