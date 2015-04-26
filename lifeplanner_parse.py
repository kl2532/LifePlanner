# Use the lexer defined by lifeplanner_lex.py
import lifeplanner_lex

# Utilizing the PLY LALR parser generator.
import yacc

# ----TOKEN DECLARATION AND PRECEDENCE----

# Use the tokens from eralex.
tokens = lifeplanner_lex.tokens

# Operator precedence
precedence =    (
                   ('left','PLUS','MINUS'),
                   ('left','TIMES','DIVIDE'),
                   ('left','LEFTPAREN'),
                   ('left','BUILD'),
                   ('left', 'PRINT'),
                   ('right', 'EE'),
                   ('right', 'EQUAL'),
                )

# ----GRAMMAR PRODUCTIONS----

# simple one-line program
# def p_program(p):
#     '''program : day colon newline event build_schedule export_stmt'''
#     p[0] = (p[1], p[2], p[3], p[4], p[5], p[6])

def p_program(p):
    '''program : function_blocks import_stmt schedule_stmts build_schedule export_stmt'''
    p[0] = (p[1], p[2], p[3], p[4])

def p_functionblocks(p):
    '''function_blocks : function_block
                | function_blocks function_block
                | empty'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = (p[1], p[2])

def p_functionblock(p):
    '''function_block : function_declaration expr_block return_statement'''
    p[0] = (p[1], p[2], p[3])
def p_imports(p):
    '''import_stmt : import filename newline
                   | empty'''
    print "p_imports"
    if len(p) == 4:
        p[0] = (p[1], p[2], p[3])
    elif len(p) == 2:
        p[0] = p[1]

def p_schedulestmt(p):
    '''schedule_stmts : day colon newline event_list schedule_stmts_rep
                      | empty'''
    if len(p) == 6:
        p[0] = (p[1], p[2], p[3], p[4], p[5])
    elif len(p) == 2:
        print "p_schedulestmt elif"
        p[0] = p[1]

def p_schedule_stmt_rep(p):
    '''schedule_stmts_rep : schedule_stmts'''
    p[0] = p[1]

def p_day1(p):
    '''day : MONDAY
           | TUESDAY
           | WEDNESDAY
           | THURSDAY
           | FRIDAY
           | SATURDAY
           | SUNDAY
           | date'''
    print "p_day"
    p[0] = p[1]

def p_date(p):
    '''date : num SLASH num year'''
    p[0] = (p[1], p[2]. p[3], p[4])

def p_year(p):
    '''year : SLASH num
            | empty'''
    if len(p) == 3:
        p[0] = (p[1], p[2])
    elif len(p) == 2:
        p[0] = p[1]

def p_events(p):
    '''event_list : event event_list_rep
                  | empty'''
    print "p_events p[1]", p[1]
    if len(p) == 3:
        print "p_events p[2]", p[2]
        p[0] = (p[1], p[2])
    elif len(p) == 2:
        p[0] = p[1]

def p_events_rep(p):
    '''event_list_rep : event_list'''
    p[0] = p[1]
    
def p_event(p):
    '''event : event_title when where who newline tag_line'''
    print "p_event"
    p[0] = (p[1], p[2], p[3], p[4], p[5], p[6])

def p_event_title(p):
    '''event_title : STRING 
                    | USERSTRING'''
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
    if len(p) == 3:
        p[0] = (p[1], p[2])
    elif len(p) == 2:
        p[0] = p[1]

def p_loc(p):
    '''location : strings'''
    print 'p_location', p[1]
    p[0] = p[1]

def p_who(p):
    '''who : with people_list
           | empty'''
    print 'p_who', p[2]
    if len(p) == 3:
        p[0] = (p[1], p[2])
    elif len(p) == 2:
        p[0] = p[1]

def p_plist(p):
    '''people_list : name people_list1'''
    print p[1]
    p[0] = (p[1], p[2])

# def p_plist_rep(p):
#     '''people_list_rep :
#                         | people_list people_list_rep'''
#     if(len(p) == 3):
#         print 'print p[1] ', p[1]
#         print 'print p[2] ', p[2]
#         p[0] = (p[1], p[2])
#     else:
#         print 'empty'

def p_plist1(p):
    '''people_list1 : comma name people_list1
                    | and name
                    | empty'''
    if len(p) == 4:
        p[0] = (p[2], p[3])
    elif len(p) == 3:
        p[0] = (p[1], p[2])
    elif len(p) == 2:
        p[0] = p[1]

def p_tagline(p):
    '''tag_line : tag tag_name newline
                | empty'''
    if len(p) == 4:
        p[0] = (p[1], p[2], p[3])
    elif len(p) == 2:
        p[0] = p[1]

def p_buildstmts(p):
    '''build_schedule : build schedule newline tag_priorities clean'''
    p[0] = (p[1], p[2], p[3], p[4], p[5])

def p_tagp(p):
    '''tag_priorities : tag colon tag_name tag_op tag_name newline tag_priorities
                      | empty'''
    if len(p) == 8:
        p[0] = (p[1], p[2], p[3], p[4], p[5], p[6], p[7])
    elif len(p) == 2:
        p[0] = p[1]
    
def p_tagop(p):
    '''tag_op : LT
              | GT'''
    p[0] = p[1]

#change later
def p_clean(p):
    '''clean : expr newline clean
             | empty'''
    if len(p) == 4:
        p[0] = (p[1], p[2], p[3])
    elif len(p) == 2:
        p[0] = (p[1])

def p_expr_block(p):
    '''expr_block : expr
                    | expr_block expr
                    | empty'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = (p[1], p[2])
        
def p_expr(p):
    '''expr : print_stmt
            | if_stmt
            | while_stmt
            | for_stmt
            | event_stmt
            | comment_stmt
            | assignment_stmt
	    | math_stmt'''
    p[0] = (p[1])

def p_mathstmt1(p):
    '''math_stmt : math_stmt PLUS math_stmt
		 | math_stmt MINUS math_stmt
		 | math_stmt TIMES math_stmt
		 | math_stmt DIVIDE math_stmt'''
    p[0] = (p[1], p[2], p[3])

def p_mathstmt2(p):
    '''math_stmt : LEFTPAREN math_stmt RIGHTPAREN'''
    p[0] = (p[1], p[2], p[3])

def p_mathstmt3(p):
    '''math_stmt : INTEGER
		 | string'''
    p[0] = p[1]

def p_comment_stmt(p): 
    '''comment_stmt : COMMENT strings
                        | empty'''
    if len(p) == 3:
        p[0] = (p[1], p[2])
        
def p_eventstmt(p):
    '''event_stmt : add_stmt
                | cancel_stmt'''
    p[0] = p[1]
    
def p_addstmt(p):
    '''add_stmt : ADD string'''
    p[0] = p[1]
    
def p_cancel_stmt(p):
    '''cancel_stmt : CANCEL string'''
    p[0] = p[1]
    
def p_whilestmt(p):
    '''while_stmt : WHILE bool_expr expr_block END'''
    p[0] = (p[1], p[2], p[3])
    
def p_forstmt(p):
    '''for_stmt : FOR assignment_stmt COMMA bool_expr COMMA math_stmt expr_block END'''
    p[0] = (p[1], p[1], p[3], p[5], p[6])

def p_boolean(p):
    '''bool_expr : bool_expr bool_operator bool_expr 
            | bool_operation 
            | bool_value 
            | value'''
    if len(p) == 4:
        p[0] = (p[1], p[2], p[3])
    else:
        p[0] = (p[1])
        
def p_boolean_opearation(p):
    '''bool_operation : value IN value
                        | value comparison_operator value'''
    p[0] = (p[1], p[2], p[3])

def p_assignmentstmt(p):
   '''assignment_stmt : string EQUAL value'''
   p[0] = (p[1], p[2], p[3])

# gotta add array
def p_value(p):
    '''value : VARIABLE
            | num
            | time
            | day
            | name
            | event
            | tag'''
    p[0] = p[1]


                            
def p_bool_op(p):
    '''bool_operator : AND
                    | OR
                    | NOT'''
    p[0] = p[1]

def p_comp_op(p):
    '''comparison_operator : LT 
                        | GT 
                        | EE 
                        | LE 
                        | GE'''
    p[0] = p[1]
    
def p_bool_value(p):
    '''bool_value : TRUE 
                | FALSE'''
    p[0] = p[1]

def p_ifstmt(p):
    '''if_stmt : if_block elseif_blocks else_block'''
    p[0] = (p[1], p[2], p[3])
    
def p_ifblock(p):
    '''if_block : IF bool_expr expr_block'''
    p[0] = (p[1], p[2], p[3])
    
def p_elseifblocks(p):
    '''elseif_blocks :
                    | elseif_blocks elseif_block
                    | elseif_block'''
    if len(p) == 3:
        p[0] = (p[1], p[2])
    elif len(p) == 2:
        p[0] = p[1]

def p_elseifblock(p):
    '''elseif_block : ELSEIF bool_expr expr_block'''
    p[0] = (p[1], p[1], p[2])

def p_elseblock(p):
    '''else_block :
                    | ELSE expr'''
    if len(p) == 3:
        p[0] = (p[1], p[2])

def p_daymath(p):
    '''day_math : date op date_duration
                | date_duration op date'''
    p[0] = (p[1], p[2], p[3])

def p_timemath(p):
    '''time_math : time op time_duration
                 | time_duration op time'''
    p[0] = (p[1], p[2], p[3])

def p_timeop(p):
    '''op : PLUS
          | MINUS'''
    p[0] = (p[1])
        
def p_printstmt(p):
    '''print_stmt : print quote strings quote'''
    p[0] = (p[1], p[2], p[3], p[4])

def p_datedur(p):
    '''date_duration : num date_unit'''
    p[0] = (p[1], p[2])

def p_dateunit(p):
    '''date_unit : DAY
                 | MONTH
                 | WEEK
                 | YEAR'''
    p[0] = p[1]

def p_timedur(p):
    '''time_duration : num time_unit'''
    p[0] = (p[1], p[2])

def p_timeunit(p):
    '''time_unit : HOUR
                 | MINUTE'''
    p[0] = p[1]

def p_quote(p):
    '''quote : QUOTATION'''
    p[0] = p[1]

def p_exportstmt(p):
    '''export_stmt : export filename
                    | empty'''
    p[0] = (p[1], p[2])
    
def p_filename(p):
    '''filename : string'''
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
    '''and : PPLAND'''
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
    
def p_var_assignmet(p):
    '''var_assign : VARIABLE EQUAL STRING'''
    p[0] = (p[1], p[2], p[3])

def p_function_declaration(p):
    '''function_declaration : type FUNCTION VARIABLE LEFTPAREN parameter_list RIGHTPAREN'''
    p[0] = (p[1], p[2], p[3], p[5])

def p_parameter_list(p):
    '''parameter_list : STRING COMMA parameter_list 
                    | empty'''
    if len(p) == 4:
        p[0] = (p[1], p[2], p[3])

def p_return(p):
    '''return_statement : RETURN value 
                        | empty'''
    if len(p) == 3:
        p[0] = (p[1], p[2])

def p_types(p):
    '''type : NUMTYPE
            | DECTYPE
            | STRTYPE'''
    p[0] = p[1]

def p_error(p):
    print p



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
