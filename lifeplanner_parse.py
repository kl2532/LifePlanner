# Use the lexer defined by lifeplanner-lex.py
import lifeplanner_lex

# Utilizing the PLY LALR parser generator.
import yacc

# ----TOKEN DECLARATION AND PRECEDENCE----

# Use the tokens from eralex.
tokens = lifeplanner_lex.tokens

# Operator precedence
precedence = (
               ('left','PLUS','MINUS'),
               ('left','TIMES','DIVIDE'),
               ('left','LEFTPAREN'),
               ('left','BUILD'),
               ('left', 'PRINT')
)

# ----GRAMMAR PRODUCTIONS----
def p_program(p):
    '''program : expression'''
    p[0] = p[1]

def p_expression(p):
    '''expression : build schedule newline b_stmt'''
    p[0] = (p[1], p[2], p[3], p[4])
   
def p_build(p):
    '''build : BUILD'''
    p[0] = p[1]

def p_schedule(p):
    '''schedule : SCHEDULE'''
    p[0] = p[1]

def p_bstmt(p):
    '''b_stmt : tab print string'''
    p[0] = (p[1], p[2], p[3])

def p_tab(p):
    '''tab : TAB'''
    p[0] = p[1]

def p_print(p):
    '''print : PRINT'''
    p[0] = p[1]

def p_newline(p):
    '''newline : NEWLINE'''
    p[0] = p[1]

# def p_term(p):
#     '''term : constant'''
#     p[0] = ( rt.TERM, p[1] )

# def p_constant(p):
#     '''constant : integer
#                 | decimal
#                 | character
#                 | string'''
#     p[0] = ( rt.CONSTANT, p[1] )

# def p_integer(p):
#     '''integer : INTEGER'''
#     p[0] = ( rt.INTEGER, int(p[1]) )
 
# def p_decimal(p):
#     '''decimal : DECIMAL'''
#     p[0] = ( rt.DECIMAL, float(p[1]) )

# def p_char(p):
#     '''character : CHARACTER'''
#     p[0] = ( rt.CHARACTER, p[1][1])

def p_string(p):
    '''string : STRING'''
    p[0] = p[1]

# def p_indent(p):
#     '''indent : INDENT'''
#     p[0] = p[1]

# def p_rparen(p):
#     '''rparen : RIGHTPAREN'''
#     p[0] = ( rt.RPAREN )

# def p_lparen(p):
#     '''lparen : LEFTPAREN'''
#     p[0] = ( rt.LPAREN )

# ----INITIALIZE PARSER----

yacc.yacc()
data = "build schedule\n\tprint \"Hello World\""
print yacc.parse(data)