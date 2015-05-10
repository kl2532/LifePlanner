import lex
import re

# ----DELINEATION OF KEYWORDS AND TOKENS----

tokens = [
    'INTEGER','DECIMAL','STRING',
    'PLUS','MINUS','DIVIDE', 'TIMES', 
    'NEWLINE', 'LEFTPAREN', 'COLON', 'COMMA', 'RIGHTPAREN', 'COMMENT', 
    'PPLAND', 'SLASH', 'USERSTRING',
    'EE', 'GE', 'LE', 'EQUAL', 'GT', 'LT', 'QUOTATION',
    'NUMTYPE', 'DECTYPE', 'STRTYPE', 'LBRACKET', 'RBRACKET', 'USERSTRING'
    ]

reserved = {
    'from' : 'FROM',
    'to' : 'TO',
    'at' : 'AT',
    'with' : 'WITH',
    'AM' : 'AM',
    'PM' : 'PM', 
    'build' : 'BUILD',
    'schedule' : 'SCHEDULE',
    'export' : 'EXPORT',
    'import' : 'IMPORT',
    'True' : 'TRUE',
    'False' : 'FALSE',
    'before': 'BEFORE',
    'after': 'AFTER',
    'end': 'END',
    'print' : 'PRINT',
    'schedule' : 'SCHEDULE',
    'export' : 'EXPORT',
    'import' : 'IMPORT',
    'minute' : 'MINUTE',
    'minutes' : 'MINUTE',
    'hour' : 'HOUR',
    'hours' : 'HOUR',
    'day' : 'DAY',
    'days' : 'DAY',
    'week' : 'WEEK',
    'weeks' : 'WEEK',
    'month': 'MONTH',
    'months': 'MONTH',
    'year' : 'YEAR',
    'years': 'YEAR',
    'append' : 'APPEND',
    'remove' : 'REMOVE',
    'length': 'LENGTH',
    'in' : 'IN',
    'length': 'LENGTH',
    'if' : 'IF',
    'elseif' : 'ELSEIF',
    'else': 'ELSE', 
    'for' : 'FOR',
    'while' : 'WHILE',
    'return' : 'RETURN', 
    'add' : 'ADD', 
    'cancel' : 'CANCEL',
    'and' : 'AND',
    'not' : 'NOT',
    'or' : 'OR',
    'function' : 'FUNCTION',
    'before' : 'BEFORE',
    'after' : 'AFTER',
    'update' : 'UPDAT',
    'subtract' : 'SUBTRACT',
    'plan' : 'PLAN'
    }

tokens = tokens + reserved.values()

# ----REGULAR EXPRESSION PATTERNS---

# Regular expression patterns for whitespace
t_ignore = ' \t'

# Keywords

# Time
t_MINUTE = r'(minute) | (minutes)'
t_HOUR = r'(hour) | (hours)'
t_DAY = r'(day) | (days)'
t_WEEK = r'(week) | (weeks)'
t_MONTH = r'(month) | (months)'
t_YEAR = r'(year) | (years)'
t_AM = r'(AM)'
t_PM = r'(PM)'

# Special keywords
t_BUILD = r'(build)'
t_SCHEDULE = r'(schedule)'
t_PRINT = r'(print)'
t_IMPORT = r'(import)'
t_FROM = r'(from)'
t_EXPORT = r'(export)'
t_PLAN = r'(plan)'

#Parts of events
t_AT = r'(at)'
t_TO = r'(to)'
t_WITH = r'(with)'

#Booleans
t_TRUE = r'(True)'
t_FALSE = r'(False)'

#Boolean Operators
t_AND = r'(and)'
t_OR = r'(or)'
t_NOT = r'(not)'

#Time comparisons
t_BEFORE = r'(before)'
t_AFTER = r'(after)'

#Array functions
t_APPEND = r'(append)'
t_REMOVE = r'(remove)'
t_LENGTH = r'(length)'
t_IN = r'(in)'
t_UPDAT = r'(update)'

#Control Sequences
t_IF = r'(if)'
t_ELSEIF = r'(elif)'
t_ELSE = r'(else)'
t_FOR = r'(for)'
t_WHILE = r'(while)'
t_RETURN = r'(return)'
t_END = r'(end)'

#Add/Cancel Events
t_ADD = r'(add)'
t_CANCEL = r'(cancel)'
t_SUBTRACT = r'(subtract)'

# Punctuation
t_LEFTPAREN  = r'\('
t_RIGHTPAREN = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_COLON = r'\:'
t_COMMA = r'\,'
t_COMMENT = r'\:\)'
t_PPLAND = r'\(&\)'
t_QUOTATION = '\"'
t_SLASH = r'/'

# Keywords
t_FUNCTION = r'function'
t_NUMTYPE = r'number'
t_DECTYPE = r'decimal'
t_STRTYPE = r'string'

# Regular expression patterns for basic constants 
# (integer, decimal, character, ...)
t_INTEGER   = r'[\-]?[0-9]+'
t_DECIMAL   = r'[\-]?[0-9]+\.[0-9]*'

# Strings - user string has quotes around it and is chosen
# over the reserved words, string has no quotes and is
# not prefered over the reserved words
def t_USERSTRING(t):
    r'\"[^\""]+\"'
    return t

def t_STRING(t):
    r'[a-zA-Z0-9_]*[.]?[a-zA-Z0-9_]+'
    int_re = re.compile('[\-]?[0-9]+')
    dec_re = re.compile('[\-]?[0-9]+\.[0-9]*')
    if int_re.match(t.value):
        t.type = 'INTEGER'
    elif dec_re.match(t.value):
        t.type = 'DECIMAL'
    elif t.value in reserved:
        t.type = reserved[t.value]
    return t

# Regular expression patterns for arithmetic operators.
t_PLUS      = r'\+'
t_MINUS     = r'\-'
t_TIMES     = r'\*'
t_DIVIDE    = r'/'
t_LT        = r'<'
t_GT        = r'>'
t_EQUAL     = r'='
t_LE        = r'<='
t_GE        = r'>='
t_EE        = r'=='

# When a \n is found, increment the line number of the lexer.
# This way, line count and errors can be reported.
def t_NEWLINE(t):
     r'\n'
     t.lexer.lineno +=1
     return t             


# ----ERROR HANDLING----

# If an error is found, attempt to recover by skipping the invalid character.

def t_error(t):
    t.lexer.skip(1)
    print 'Error in line %d. Invalid character: ' % t.lexer.lineno
    print '\ntype: ' + t.type + ',    value: ' + t.value

# Lex the input.
lexer = lex.lex()
