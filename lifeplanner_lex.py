import lex

# ----DELINEATION OF KEYWORDS AND TOKENS----

tokens = (
    'INTEGER','DECIMAL','CHARACTER', 'STRING', 
    'PLUS','MINUS','DIVIDE',
    'TIMES', 'NEWLINE', 'LEFTPAREN', 'COLON',
    'RIGHTPAREN', 'BUILD', 'PRINT', 'TAB', 'SCHEDULE', 'EXPORT', 'IMPORT'
    'MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY', 'SUNDAY', 'AM', 'PM',
    'TO', 'WITH', 'FROM', 'AT', 'TAG')

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

# Regular expression patterns
# for whitespace
t_NEWLINE = r'\n'

# Regular expression patterns for multi-use
# tokens.

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
t_EXPORT = r'(export)'
t_TAG = r'(tag)'
t_AT = r'(at)'
t_FROM = r'(from)'
t_TO = r'(to)'
t_WITH = r'(with)'

# Time Meridian
t_AM = r'(AM)'
t_PM = r'(PM)'
t_ignore = r' \t'

# Punctuation
t_LEFTPAREN  = r'\('
t_RIGHTPAREN = r'\)'
t_COLON = r'\:'


# def t_NEWLINE(t):       # When a \n is found,
#     r'\n'               # increment the line
#     t.lexer.lineno +=1  # number of the lexer.
#     return t            # This way, line count
#                         # and errors can be
#                         # reported precisely.

# ----ERROR HANDLING----

# If an error is found, attempt to recover by
# skipping the invalid character.

def t_error(t):
    t.lexer.skip(1)

# Lex the input.
lexer = lex.lex()