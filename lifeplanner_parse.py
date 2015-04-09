# Use the lexer defined by lifeplanner_lex.py
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
    '''program : import_stmt schedule_stmts build_schedule export_stmt'''
    p[0] = (p[1], p[2], p[3], p[4])

def p_imports(p):
    '''import_stmt : import string newline
                   | empty'''
    if (len(p) == 4):
        p[0] = (p[1], p[2], p[3])
    elif (len(p) == 2):
        p[0] = p[1]

def p_schedulestmt(p):
    '''schedule_stmts : day colon newline event_list schedule_stmts
                      | empty'''
    if (len(p) == 6):
        p[0] = (p[1], p[2], p[3], p[4], p[5])
    elif (len(p) == 2):
        p[0] = p[1]

def p_day1(p):
    '''day : MONDAY'''
    p[0] = p[1]
def p_day2(p):
    '''day : TUESDAY'''
    p[0] = p[1]
def p_day3(p):
    '''day : WEDNESDAY'''
    p[0] = p[1]
def p_day4(p):
    '''day : THURSDAY'''
    p[0] = p[1]
def p_day5(p):
    '''day : FRIDAY'''
    p[0] = p[1]
def p_day6(p):
    '''day : SATURDAY'''
    p[0] = p[1]
def p_day7(p):
    '''day : SUNDAY'''
    p[0] = p[1]
def p_day8(p):
    '''day : time'''
    p[0] = p[1]

def p_events(p):
    '''event_list : event event_list
                  | empty'''
    if (len(p) == 3):
        p[0] = (p[1], p[2])
    elif (len(p) == 2):
        p[0] = p[1]

def p_event(p):
    '''event : event_title when where who newline tag_line'''
    p[0] = (p[1], p[2], p[3], p[4], p[5], p[6])

def p_eventname(p):
    '''event_title: strings'''
    p[0] = p[1]

def p_when(p):
    '''when : from time to time'''
    p[0] = (p[1], p[2], p[3], p[4])

def p_time(p):
    '''time : num num colon num num meridian
            | num colon num num meridian'''
    if (len(p) == 7):
        p[0] = (p[1], p[2], p[3], p[4], p[5], p[6])
    elif (len(p) == 6):
        p[0] = (p[1], p[2], p[3], p[4], p[5])

def p_where(p):
    '''where : at location
             | empty'''
    if (len(p) == 3):
        p[0] = (p[1], p[2])
    elif (len(p) == 2):
        p[0] = p[1]

def p_loc(p):
    '''location : strings'''
    p[0] = p[1]

def p_at(p):
    '''at : AT'''
    p[0] = p[1]

def p_num(p):
    '''num : NUM'''
    p[0] = p[1]

def p_meridian1(p):
    '''meridian : AM'''
    p[0] = p[1]

def p_meridian2(p):
    '''meridian : PM'''
    p[0] = p[1]

def p_from(p):
    '''from : FROM'''
    p[0] = p[1]

def p_to(p):
    '''to : TO'''
    p[0] = p[1]

def p_colon(p):
    '''colon : COLON'''
    p[0] = p[1]

def p_build(p):
    '''build : BUILD'''
    p[0] = p[1]

def p_schedule(p):
    '''schedule : SCHEDULE'''
    p[0] = p[1]

def p_bstmt(p):
    '''b_stmt : tab print string'''
    p[0] = ('print', p[1], p[2], p[3])

def p_strings(p):
    '''strings : string strings
               | empty'''
    if (len(p) == 3 ):
        p[0] = (p[1], p[2])
    elif (len(p) == 3):
        p[0] = p[1]

def p_empty(p):
    '''empty :'''
    pass

def p_tab(p):
    '''tab : TAB'''
    p[0] = p[1]

def p_import(p):
    '''import : IMPORT'''
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
tree = yacc.parse(data)

import sys

python_translation = ""

for line in tree:
    if line[0]=='print':
        for i in range(len(line) - 1, -1, -1):
            if line[i] == 'print':
                python_translation +=  ''.join(line[i+1:]).strip('\"')
                break

with open("calendar.py", "w") as f:
    f.write(python_translation)
