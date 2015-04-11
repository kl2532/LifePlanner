import lex

tokens = ('AM', 'PM', 'NUM', 'COLON', 'FROM', 'TO', 'STRING',) 
t_AM = r'(AM)'
t_PM = r'(PM)'
t_NUM = r'[\-]?[0-9]+'
t_COLON = r'\:'
t_FROM = r'(from)'
t_TO = r'(to)'
t_ignore = ' '
t_STRING = r'^([a-zA-Z]+)$'
#t_USERSTRING = r'[a-zA-Z]+'
lex = lex.lex()
