# Use the lexer defined by lifeplanner_lex.py
import string_lex

# Utilizing the PLY LALR parser generator.
import yacc

# ----TOKEN DECLARATION AND PRECEDENCE----

# Use the tokens from eralex.
tokens = string_lex.tokens

def p_strings(p):
    'strings : STRING string_rep'
    print 'p_strings p[1]', p[1]
    print 'p_strings p[2]', p[2]
    p[0] = (p[1], p[2])
def p_string_rep(p):
    '''string_rep : 
    			    | strings string_rep'''
    if(len(p) == 3):
    	print 'print p[1] ', p[1]
    	print 'print p[2] ', p[2]
    	p[0] = (p[1], p[2])
    else:
    	print 'empty'

yacc.yacc()
data = "hello world"
# data = "Monday:\nPLT from 4:13PM to 4:14PM at Mudd with Aho\nbuild schedule\nexport"
print data
print "END"
tree = yacc.parse(data)
print tree