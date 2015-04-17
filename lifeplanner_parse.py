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
# def p_program(p):
#     '''program : day colon newline event build_schedule export_stmt'''
#     p[0] = (p[1], p[2], p[3], p[4], p[5], p[6])

def p_program(p):
    '''program : import_stmt schedule_stmts build_schedule export_stmt'''
    p[0] = (p[1], p[2], p[3], p[4])

def p_imports(p):
    '''import_stmt : import strings newline
                   | empty'''
    print "p_imports"
    if (len(p) == 4):
        p[0] = (p[1], p[2], p[3])
    elif (len(p) == 2):
        p[0] = p[1]

def p_schedulestmt(p):
    '''schedule_stmts : day colon newline event
                      | empty'''
    if (len(p) == 5):
        p[0] = (p[1], p[2], p[3], p[4])
    elif (len(p) == 2):
        print "p_schedulestmt elif"
        p[0] = p[1]

def p_schedule_stmt_rep(p):
    '''schedule_stmts_rep : 
                            | schedule_stmts schedule_stmts_rep'''
    if(len(p) == 3):
        print 'print p[1] ', p[1]
        print 'print p[2] ', p[2]
        p[0] = (p[1], p[2])
    else:
        print 'empty'

def p_day1(p):
    '''day : MONDAY'''
    print "p_day1"
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
#def p_day8(p):
#    '''day : time'''
#    p[0] = p[1]

def p_events(p):
    '''event_list : event event_list_rep
                  | empty'''
    print "p_events p[1]", p[1]
    if (len(p) == 3):
        print "p_events p[2]", p[2]
        p[0] = (p[1], p[2])
    elif (len(p) == 2):
        p[0] = p[1]

def p_events_rep(p):
    '''event_list_rep : 
                        | event_list event_list_rep'''
    if(len(p) == 3):
        print 'print p[1] ', p[1]
        print 'print p[2] ', p[2]
        p[0] = (p[1], p[2])
    else:
        print 'empty'

def p_event(p):
    '''event : event_title when where who newline tag_line'''
    print "p_event"
    p[0] = (p[1], p[2], p[3], p[4], p[5], p[6])

def p_event_title(p):
    '''event_title : strings'''
    print "p_eventname", p[1]
    p[0] = p[1]

def p_when(p):
    '''when : from time to time'''
    print "p_when", p[1]
    p[0] = (p[1], p[2], p[3], p[4])

def p_time(p):
    '''time : num colon num meridian'''
    p[0] = (p[1], p[2], p[3], p[4])
    print "p_time", p[0]

def p_where(p):
    '''where : at location
             | empty'''
    print 'p_where'
    if (len(p) == 3):
        p[0] = (p[1], p[2])
    elif (len(p) == 2):
        p[0] = p[1]

def p_loc(p):
    '''location : strings'''
    print 'p_location', p[1]
    p[0] = p[1]

def p_who(p):
    '''who : with people_list
           | empty'''
    print 'p_who', p[2]
    if (len(p) == 3):
        p[0] = (p[1], p[2])
    elif (len(p) == 2):
        p[0] = p[1]

def p_plist(p):
    '''people_list : name'''
    print p[1]
    p[0] = p[1]

# def p_plist_rep(p):
#     '''people_list_rep :
#                         | people_list people_list_rep'''
#     if(len(p) == 3):
#         print 'print p[1] ', p[1]
#         print 'print p[2] ', p[2]
#         p[0] = (p[1], p[2])
#     else:
#         print 'empty'

# def p_plist1(p):
#     '''people_list1 : comma name people_list1
#                     | and people_list1
#                     | empty'''
#     if (len(p) == 4):
#         p[0] = (p[1], p[2], p[3])
#     elif (len(p) == 3):
#         p[0] = (p[1], p[2])
#     elif (len(p) == 2):
#         p[0] = p[1]

def p_tagline(p):
    '''tag_line : tag tag_name newline
                | empty'''
    if (len(p) == 4):
        p[0] = (p[1], p[2], p[3])
    elif (len(p) == 2):
        p[0] = p[1]

def p_buildstmts(p):
    '''build_schedule : build schedule newline'''# tag_priorities clean'''
    p[0] = (p[1], p[2], p[3])#, p[4], p[5])

#change later
def p_tagp(p):
    '''tag_priorities : empty'''
    p[0] = p[1]

#change later
def p_clean(p):
    '''clean : empty'''
    p[0] = p[1]

#change
def p_exportstmt(p):
    '''export_stmt : export'''
    p[0] = p[1]

def p_export(p):
    '''export : EXPORT'''
    p[0] = p[1]

def p_tagname(p):
    '''tag_name : strings'''
    p[0] = p[1]

def p_tag(p):
    '''tag : TAG'''
    p[0] = p[1]

def p_name(p):
    '''name : strings'''
    p[0] = p[1]

def p_and(p):
    '''and : AND'''
    p[0] = p[1]

def p_comma(p):
    '''comma : COMMA'''
    p[0] = p[1]

def p_with(p):
    '''with : WITH'''
    print 'p_with', p[1]
    p[0] = p[1]

def p_at(p):
    '''at : AT'''
    print 'p_at', p[1]
    p[0] = p[1]

def p_num(p):
    '''num : INTEGER'''
    print 'p_num', p[1]
    p[0] = p[1]

def p_meridian(p):
    '''meridian : AM
                | PM'''
    print 'p_meridian', p[1]
    p[0] = p[1]

def p_from(p):
    '''from : FROM'''
    print 'p_from', p[1]
    p[0] = p[1]

def p_to(p):
    '''to : TO'''
    print 'p_to', p[1]
    p[0] = p[1]

def p_colon(p):
    '''colon : COLON'''
    print "p_colon", p[1]
    p[0] = p[1]

def p_build(p):
    '''build : BUILD'''
    p[0] = p[1]

def p_schedule(p):
    '''schedule : SCHEDULE'''
    p[0] = p[1]

def p_string(p):
    '''string : STRING'''
    p[0] = p[1]

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

def p_empty(p):
    'empty :'
    pass

def p_import(p):
    '''import : IMPORT'''
    p[0] = p[1]

def p_print(p):
    '''print : PRINT'''
    p[0] = p[1]

def p_newline(p):
    '''newline : NEWLINE'''
    print "p_newline"
    p[0] = p[1]

# def p_error(p):
#     print p.type, " ", p.value

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

# def p_string(p):
#     '''string : STRING'''
#     print 'hello', p[1]
#     p[0] = p[1]

# def p_indent(p):
#     '''indent : INDENT'''
#     p[0] = p[1]

# def p_rparen(p):
#     '''rparen : RIGHTPAREN'''
#     p[0] = ( rt.RPAREN )

# def p_lparen(p):
#     '''lparen : LEFTPAREN'''
#     p[0] = ( rt.LPAREN )

# def p_user_strings(p):
#    '''user_strings : USERSTRING user_string_rep'''
#    print 'p_strings p[1]', p[1]
#    print 'p_strings p[2]', p[2]
#    p[0] = (p[1], p[2])
   
# def p_user_string_rep(p):
#    '''user_string_rep : 
#                   | user_strings user_string_rep'''
#    if(len(p) == 3):
#       print 'print p[1] ', p[1]
#       print 'print p[2] ', p[2]
#       p[0] = (p[1], p[2])
#    else:
#       print 'empty'

# ----INITIALIZE PARSER----

yacc.yacc()
data = "Monday:\nPLT from 4:13PM to 4:20PM at Mudd with Aho\nbuild schedule\nexport"
print data
tree = yacc.parse(data)
print tree

#import sys

#python_translation = ""

#for line in tree:
#    if line[0]=='print':
#        for i in range(len(line) - 1, -1, -1):
#            if line[i] == 'print':
#                python_translation +=  ''.join(line[i+1:]).strip('\"')
#                break

#with open("calendar.py", "w") as f:
#    f.write(python_translation)
