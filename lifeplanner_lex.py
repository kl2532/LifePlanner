import lex

# ----DELINEATION OF KEYWORDS AND TOKENS----

tokens = (
    'INTEGER','DECIMAL','STRING', 'NUM', #'CHARACTER', 
    'PLUS','MINUS','DIVIDE', 'TIMES', 
    'NEWLINE', 'LEFTPAREN', 'COLON', 'COMMA', 'RIGHTPAREN', 
    'BUILD', 'PRINT', 'TAB', 'SCHEDULE', 'EXPORT', 'IMPORT',
    'MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY', 
    'SUNDAY', 
    'AM', 'PM', 'TO', 'WITH', 'FROM', 'AT', 'TAG', 'AND',
    )

reserved = {
    'from' : 'FROM',
    'to' : 'TO',
    'AM' : 'AM',
    'PM' : 'PM' }


# ----REGULAR EXPRESSION PATTERNS---

# Regular expression patterns for whitespace
t_NEWLINE = r'\n'

# Regular expression patterns for multi-use tokens.

# Keywords
t_MONDAY = r'(Monday)'
t_TUESDAY = r'(Tuesday)'
t_WEDNESDAY = r'(Wednesday)'
t_THURSDAY = r'(Thursday)'
t_FRIDAY = r'(Friday)'
t_SATURDAY = r'(Saturday)'
t_SUNDAY = r'(Sunday)'
t_BUILD = r'(build)'
t_SCHEDULE = r'(schedule)'
t_PRINT = r'(print)'
t_IMPORT = r'(import)'
t_FROM = r'(from)'
t_EXPORT = r'(export)'
t_TAG = r'(tag)'
t_AT = r'(at)'
t_TO = r'(to)'
t_WITH = r'(with)'
t_AND = r'(and)'
t_COMMA = r'\,'
# Time Meridian
t_AM = r'(AM)'
t_PM = r'(PM)'
t_ignore = ' \t'
# t_PLT = r'(PLT)'

# Punctuation
t_LEFTPAREN  = r'\('
t_RIGHTPAREN = r'\)'
t_COLON = r'\:'

# Regular expression patterns for basic constants 
# (integer, decimal, character, ...)
t_NUM 		= r'[\-]?[0-9]+'
t_INTEGER	= r'[\-]?[0-9]+'
t_DECIMAL	= r'[\-]?[0-9]+\.[0-9]*'
# t_CHARACTER  = r'(\'[^\']\')'
# t_STRING     = r'(\"[^\"]+\")'
# t_STRING = r'[a-zA-Z]+'
# t_STRING = r'(^[A-Za-z]+$)'
# t_STRING = r'^([a-zA-Z]+)$'
# t_USERSTRING = r'[a-zA-Z]+'

def t_STRING(t):
    r'[a-zA-Z]+'
    if t.value in reserved:
        t.type = reserved[t.value]
    return t

# Regular expression patterns for arithmetic operators.
t_PLUS		= r'\+'
t_MINUS		= r'\-'
t_TIMES		= r'\*'
t_DIVIDE	= r'/'

# def t_NEWLINE(t):       # When a \n is found,
#      r'\n'               # increment the line
#      t.lexer.lineno +=1  # number of the lexer.
#      return t            # This way, line count
#                         # and errors can be
#                         # reported precisely.


# ----ERROR HANDLING----

# If an error is found, attempt to recover by skipping the invalid character.

def t_error(t):
    t.lexer.skip(1)

# def t_error(t):
#     print t.type, " ",t.value

# Lex the input.
lexer = lex.lex()
