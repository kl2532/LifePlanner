import date_lex
import yacc

tokens = date_lex.tokens

start = 'program'

def p_program(p):
    '''program : string when'''
    p[0] = (p[1], p[2])
    
def p_when(p):
    '''when : from time to time'''
    p[0] = (p[1], p[2], p[3], p[4])

def p_time(p):
    '''time : num colon num meridian'''
    p[0] = (p[1], p[2], p[3], p[4])

def p_meridian(p):
    '''meridian : AM 
               | PM'''
    p[0] = p[1]

def p_num(p):
    '''num : NUM'''
    p[0] = p[1]

def p_colon(p):
    '''colon : COLON'''
    p[0] = p[1]

def p_from(p):
    '''from : FROM'''
    p[0] = p[1]

def p_to(p):
    '''to : TO'''
    p[0] = p[1]

def p_string(p):
    '''string : STRING'''
    p[0] = p[1]

def p_error(p):
    print p.type, " ", p.value

# def p_user_strings(p):
#    '''user_strings : USERSTRING user_string_rep'''
#    print 'p_strings p[1]', p[1]
#    print 'p_strings p[2]', p[2]
#    p[0] = (p[1], p[2])
   
# def p_user_string_rep(p):
#    '''user_string_rep : 
#    			    | user_strings user_string_rep'''
#    if(len(p) == 3):
#    	print 'print p[1] ', p[1]
#    	print 'print p[2] ', p[2]
#    	p[0] = (p[1], p[2])
#    else:
#    	print 'empty'
     
yacc.yacc()
data = "PLT from 4:25PM to 5:30PM"
tree = yacc.parse(data)
print tree
