import lex

# ----DELINEATION OF KEYWORDS AND TOKENS----

tokens = [
    'INTEGER','DECIMAL','STRING', #'CHARACTER', 
    'PLUS','MINUS','DIVIDE', 'TIMES', 
    'NEWLINE', 'LEFTPAREN', 'COLON', 'COMMA', 'RIGHTPAREN', 'COMMENT', 
    'PPLAND', 'SLASH', 'VARIABLE', 'USERSTRING',
    'EE', 'GE', 'LE', 'EQUAL', 'GT', 'LT', 'QUOTATION',
    'NUMTYPE', 'DECTYPE', 'STRTYPE',
    ]

reserved = {
    'from' : 'FROM',
    'to' : 'TO',
    'at' : 'AT',
    'with' : 'WITH',
    'AM' : 'AM',
    'PM' : 'PM', 
    'Monday' : 'MONDAY',
    'Tuesday' : 'TUESDAY',
    'Wednesday' : 'WEDNESDAY',
    'Thursday' : 'THURSDAY',
    'Friday': 'FRIDAY', 
    'Saturday': 'SATURDAY', 
    'Sunday': 'SUNDAY', 
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
    'tag' : 'TAG',
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
    'January' : 'JAN',
    'February' : 'FEB',
    'March' : 'MAR',
    'April' : 'APR',
    'May' : 'MAY',
    'June' : 'JUN',
    'July' : 'JUL',
    'August' : 'AUG',
    'September' : 'SEP',
    'October' : 'OCT',
    'November' : 'NOV',
    'December' : 'DEC',
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
    'function' : 'FUNCTION'
    }

tokens = tokens + reserved.values()

# ----REGULAR EXPRESSION PATTERNS---

# Regular expression patterns for whitespace
t_ignore = ' \t'

# Keywords

# Time
t_MONDAY = r'(Monday)'
t_TUESDAY = r'(Tuesday)'
t_WEDNESDAY = r'(Wednesday)'
t_THURSDAY = r'(Thursday)'
t_FRIDAY = r'(Friday)'
t_SATURDAY = r'(Saturday)'
t_SUNDAY = r'(Sunday)'
t_JAN = 'January'
t_FEB = 'February'
t_MAR = 'March'
t_APR = 'April'
t_MAY = 'May'
t_JUN = 'June'
t_JUL = 'July'
t_AUG = 'August'
t_SEP = 'September'
t_OCT = 'October'
t_NOV = 'November'
t_DEC = 'December'
t_MINUTE = r'(minute) | (minutes)'
t_HOUR = r'(hour) | (hours)'
t_DAY = r'(day) | (days)'
t_WEEK = r'(week) | (weeks)'
t_MONTH = r'(month) | (months)'
t_YEAR = r'(year) | (years)'
t_AM = r'(AM)'
t_PM = r'(PM)'


t_BUILD = r'(build)'
t_SCHEDULE = r'(schedule)'
t_PRINT = r'(print)'
t_IMPORT = r'(import)'
t_FROM = r'(from)'
t_EXPORT = r'(export)'
t_TAG = r'(tag)'

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

#Control Sequences
t_IF = r'(if)'
t_ELSEIF = r'(elseif)'
t_ELSE = r'(else)'
t_FOR = r'(for)'
t_WHILE = r'(while)'
t_RETURN = r'(return)'
t_END = r'(end)'

#Add/Cancel Events
t_ADD = r'(add)'
t_CANCEL = r'(cancel)'

# Punctuation
t_NEWLINE = r'\n'
t_LEFTPAREN  = r'\('
t_RIGHTPAREN = r'\)'
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
# t_USERSTRING(t) = r'\"[a-zA-Z0-9_]*\"'

def t_VARIABLE(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value in reserved:
        t.type = reserved[t.value]
    return t

def t_STRING(t):
    r'[a-zA-Z0-9_]+'
    if t.value in reserved:
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
# def t_NEWLINE(t):
#      r'\n'
#      t.lexer.lineno +=1
#      return t             


# ----ERROR HANDLING----

# If an error is found, attempt to recover by skipping the invalid character.

def t_error(t):
    t.lexer.skip(1)

# def t_error(t):
#     print t.type, " ",t.value

# Lex the input.
lexer = lex.lex()
