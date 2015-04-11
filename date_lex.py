import lex

tokens = ('AM', 'PM', 'NUM', 'COLON', 'FROM', 
            'TO', 'STRING',) 
reserved = {
    'from' : 'FROM',
    'to' : 'TO',
    'AM' : 'AM',
    'PM' : 'PM' }

t_AM = r'(AM)'
t_PM = r'(PM)'
t_NUM = r'[\-]?[0-9]+'
t_COLON = r'\:'
t_FROM = r'(from)'
t_TO = r'(to)'
t_ignore = ' '

def t_STRING(t):
    r'[a-zA-Z]+'
    if t.value in reserved:
        t.type = reserved[t.value]
    return t

#t_STRING = r'^([a-zA-Z]+)$'
#t_USERSTRING = r'[a-zA-Z]+'
def t_error(t):
    print t.type, " ",t.value
lex = lex.lex()
