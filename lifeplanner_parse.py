# Use the lexer defined by lifeplanner_lex.py
import lifeplanner_lex
import lifeplanner_translate as trans

# Utilizing the PLY LALR parser generator.
import yacc

# ----TOKEN DECLARATION AND PRECEDENCE----

# Use the tokens from eralex.
tokens = lifeplanner_lex.tokens

# Operator precedence
precedence =    (
                    ('left','PLUS','MINUS'),
                    ('left','TIMES','SLASH'),
                    ('left','LEFTPAREN'),
                    ('left','BUILD'),
                    ('left', 'PRINT'),
                    ('right', 'EE'),
                    ('right', 'EQUAL'),
                )
# All programs must start with the program production
start = 'program'

# ----- Grammar productions-----

def p_program(p):
    '''program : function_blocks import_stmt schedule_stmts build_schedule export_stmt whatever'''
    p[0] = ['program', p[1], p[2], p[3], p[4], p[5]]

# ----- Production for functions -----
def p_functionblocks(p):
    '''function_blocks : function_block function_blocks
                    | empty'''
    if len(p) == 3:
        p[0] = ['function_blocks', p[1], p[2][1]]
    else:
        p[0] = ['function_blocks', None]

def p_functionblock(p):
    '''function_block : function_declaration expr_block newline'''
    p[0] = ['function_block', p[1], p[2]]

def p_function_declaration(p):
    '''function_declaration : FUNCTION function_name LEFTPAREN parameter_list RIGHTPAREN newline'''
    p[0] = ['function_declaration', p[1], p[2], p[4]]

def p_function_name(p):
    '''function_name : variable'''
    p[0] = ['function_name', p[1][1]]

def p_parameter_list(p):
    '''parameter_list : STRING parameter_list 
                    | INTEGER parameter_list 
                    | DECIMAL parameter_list
                    | USERSTRING parameter_list
                    | COMMA STRING parameter_list
                    | COMMA INTEGER parameter_list
                    | COMMA DECIMAL parameter_list
                    | COMMA USERSTRING parameter_list
                    | empty'''
    if len(p) == 3:
        p[0] = ['parameter_list', p[1], p[2]]
    elif len(p) == 4:
        p[0] = ['parameter_list', p[2], p[3]]
    elif len(p) == 2:
        p[0] = ['parameter_list', None]

def p_return(p):
    '''return_stmt : RETURN value newline'''
    if len(p) == 4:
        p[0] = ['return_stmt', p[1], p[2]]
    else:
        p[0] = ['return_stmt', None]

# --- Production for Import Statements -----
def p_imports(p):
    '''import_stmt : import filename newline
                   | empty'''
    if len(p) == 4:
        p[0] = ['import_stmt', p[1], p[2]]
    else:
        p[0] = ['import_stmt', None]

# ----- Productions for Creating a Schedule -----
def p_schedulestmt(p):
    '''schedule_stmts : date colon newline event_list schedule_stmts_rep
                      | empty'''
    if len(p) == 6:
        p[0] = ['schedule_stmts', p[1], p[2], p[4], p[5]]
    else:
        p[0] = ['schedule_stmts', None]

def p_schedule_stmt_rep(p):
    '''schedule_stmts_rep : schedule_stmts'''
    p[0] = ['schedule_stmts_rep', p[1]]

def p_date(p):
    '''date : num SLASH num SLASH num'''
    p[0] = ['date', p[1], p[3], p[5]]

def p_events(p):
    '''event_list : event event_list_rep
                  | empty'''
    if len(p) == 3:
        p[0] = ['event_list', p[1], p[2]]
    else:
        p[0] = ['event_list', None]

def p_events_rep(p):
    '''event_list_rep : event_list'''
    p[0] = ['event_list_rep', p[1]]
    
def p_event(p):
    '''event : event_title when where who newline'''
    p[0] = ['event', p[1], p[2], p[3], p[4]]

def p_event_title(p):
    '''event_title : strings event_title_rep'''
    title = p[1][1]
    if p[2]:
        p[1][1] += ' ' + p[2]
    p[0] = ['event_title', p[1]]

def p_event_title_rep(p):
    '''event_title_rep : strings event_title_rep
                        | num event_title_rep
                        | empty'''
    if len(p) == 3:
        first = p[1]
        if p[1]:
            first = p[1][1]
        p[0] = first
        second  = p[2]
        if p[2]:
            second = p[2]
            if type(second) == list:
                second = p[2][1]
            p[0] = first + ' ' +second


def p_when(p):
    '''when : from time to time'''
    p[0] = ['when', p[1], p[2], p[3], p[4]]

def p_time(p):
    '''time : num colon num meridian'''
    p[0] = ['time', p[1], p[2], p[3], p[4]]

def p_where(p):
    '''where : at location
             | empty'''
    if len(p) == 3:
        p[0] = ['where', p[1], p[2]]
    else:
        p[0] = ['where', None]

def p_loc(p):
    '''location : strings'''
    p[0] = ['location', p[1]]

def p_who(p):
    '''who : with people_list
           | empty'''
    if len(p) == 3:
        p[0] = ['who', p[1], p[2]]
    else:
        p[0] = ['who', None]

def p_plist(p):
    '''people_list : name people_list1'''
    p[0] = ['people_list', p[1], p[2]]

def p_plist1(p):
    '''people_list1 : comma name people_list1
                    | comma and name
                    | and name
                    | empty'''
    if len(p) == 4:
        p[0] = ['comma', p[2], p[3]]
    elif len(p) == 3:
        p[0] = ['and', p[1], p[2]]
    elif len(p) == 2:
        p[0] = ['people_list1', None]

# ----- Production for Modifying the Schedule -----
def p_buildstmts(p):
    '''build_schedule : build schedule newline clean'''
    p[0] = ['build_schedule', p[1], p[2], p[4]]

def p_clean(p):
    '''clean : expr_block
             | empty'''
    if len(p) == 2:
        p[0] = ['clean', p[1]]
    else:
        p[0] = ['clean', None]

def p_expr_block(p):
    '''expr_block : expr expr_block_rep
                    | empty'''
    if len(p) == 3:
        p[0] = ['expr_block', p[1], p[2]]
    else:
        p[0] = ['expr_block', None]

def p_expr_block_rep(p):
    '''expr_block_rep : expr_block'''
    p[0] = ['expr_block_rep', p[1]]
        
def p_expr(p):
    '''expr : print_stmt newline
            | if_stmt
            | while_stmt newline
            | for_stmt newline
            | event_stmt newline
            | comment_stmt newline
            | assignment_stmt newline
	        | math_stmt newline
            | time_math newline
            | day_math newline
            | func newline
            | time_range newline
            | str_stmt newline
            | plan_stmt
            | return_stmt'''
    p[0] = ['expr', p[1]]

def p_func(p):
    '''func : variable LEFTPAREN parameter_list RIGHTPAREN'''
    p[0] = ['func', p[1], p[3]]

def p_comment_stmt(p): 
    '''comment_stmt : COMMENT strings'''
    if len(p) == 3:
        p[0] = ['comment_stmt', p[1], p[2]]
    else:
        p[0] = ['comment_stmt', None]
        
def p_eventstmt(p):
    '''event_stmt : add_stmt
                | cancel_stmt
                | update_stmt
                | remove_stmt'''
    p[0] = ['event_stmt', p[1]]

def p_updatestmt(p):
    '''update_stmt : UPDAT strings FROM variable
                    | UPDAT strings TO variable
                    | UPDAT strings AT variable'''
    p[0] = ['update_stmt', p[2], p[3], p[4]]


def p_planstmt(p):
    '''plan_stmt : PLAN date colon event'''
    p[0] = ['plan_stmt', p[2], p[4]]

def p_addstmt(p):
    '''add_stmt : ADD strings TO strings'''
    p[0] = ['add_stmt', p[2], p[4]]

def p_removestmt(p):
    '''remove_stmt : REMOVE strings FROM strings'''
    p[0] = ['remove_stmt', p[2], p[4]]
    
def p_cancel_stmt(p):
    '''cancel_stmt : CANCEL strings'''
    p[0] = ['cancel_stmt', p[1], p[2]]
    
def p_whilestmt(p):
    '''while_stmt : WHILE bool_expr newline expr_block END'''
    p[0] = ['while_stmt', p[1], p[2], p[4]]

def p_timerange(p):
    '''time_range : FROM date TO date newline expr_block END'''
    p[0] = ['time_range', p[1], p[2], p[3], p[4], p[6]]
    
def p_forstmt(p):
    '''for_stmt : FOR assignment_stmt COMMA bool_expr COMMA assignment_stmt newline expr_block END'''
    p[0] = ['for_stmt', p[1], p[2], p[4], p[6], p[8]]

def p_boolean(p):
    '''bool_expr : bool_expr bool_operator bool_expr 
            | bool_operation 
            | bool_value 
            | value
            | NOT bool_expr
            | LEFTPAREN bool_expr RIGHTPAREN'''
    if len(p) == 4:
        p[0] = ['bool_expr', p[1], p[2], p[3]]
    elif len(p) == 3:
        p[0] = ['bool_expr', p[1], p[2]]
    elif len(p) == 2:
        p[0] = ['bool_expr', p[1]]
        
def p_boolean_opearation(p):
    '''bool_operation : value IN value
                        | value comparison_operator value'''
    p[0] = ['bool_operation', p[1], p[2], p[3]]

def p_assignmentstmt(p):
   '''assignment_stmt : variable EQUAL value'''
   p[0] = ['assignment_stmt', p[1], p[2], p[3]]

def p_value(p):
    '''value : variable
            | num
            | time
            | date
            | user_string
            | event
            | math_stmt
            | time_math
            | day_math
            | func
            | access
            | bool_value
            | str_stmt'''
    p[0] = ['value', p[1]]

def p_access(p):
    '''access : strings LBRACKET TO RBRACKET
            | strings LBRACKET FROM RBRACKET
            | strings LBRACKET WITH RBRACKET
            | strings LBRACKET AT RBRACKET'''
    p[0] = ['access', p[1], p[3]]

def p_variable(p):
    '''variable : STRING'''
    p[0] = ['variable', p[1]]
                            
def p_bool_op(p):
    '''bool_operator : AND
                    | OR'''
    p[0] = ['bool_operator', p[1]]

def p_comp_op(p):
    '''comparison_operator : LT 
                        | GT 
                        | EE 
                        | LE 
                        | GE
                        | BEFORE
                        | AFTER'''
    p[0] = ['comparison_operator', p[1]]
    
def p_bool_value(p):
    '''bool_value : TRUE 
                | FALSE'''
    p[0] = ['bool_value', p[1]]

def p_ifstmt(p):
    '''if_stmt : if_block elseif_blocks else_block'''
    p[0] = ['if_stmt', p[1], p[2], p[3]]
    
def p_ifblock(p):
    '''if_block : IF bool_expr newline expr_block END newline'''
    p[0] = ['if_block', p[1], p[2], p[4]]
    
def p_elseifblocks(p):
    '''elseif_blocks : empty
                    | elseif_block elseif_blocks_rep'''
    if len(p) == 3:
        p[0] = ['elseif_blocks', p[1], p[2]]
    elif len(p) == 2:
        if p[1]:
            p[0] = ['elseif_blocks', p[1]]
        else:
            p[0] = ['elseif_blocks', None]

def p_elseifblocksrep(p):
    '''elseif_blocks_rep : elseif_blocks'''
    p[0] = ['elseif_blocks_rep', p[1]]

def p_elseifblock(p):
    '''elseif_block : ELSEIF bool_expr newline expr_block END newline'''
    p[0] = ['elseif_block', p[1], p[2], p[4]]

def p_elseblock(p):
    '''else_block : empty
                    | ELSE newline expr_block END newline'''
    if len(p) == 6:
        p[0] = ['else_block', p[1], p[3]]
    else:
        p[0] = ['else_block', None]

def p_daymath(p):
    '''day_math : date op date_duration
                | date_duration op date'''
    p[0] = ['day_math', p[1], p[2], p[3]]

def p_timemath(p):
    '''time_math : time op time_duration
                 | variable op time_duration'''
    p[0] = ['time_math', p[1], p[2], p[3]]

def p_timeop(p):
    '''op : ADD
          | SUBTRACT'''
    p[0] = ['op', p[1]]
        
def p_printstmt(p):
    '''print_stmt : print user_string
                  | print variable
                  | print num
                  | print bool_value
                  | print math_stmt
                  | print bool_expr
                  | print func
                  | print str_stmt'''
    p[0] = ['print_stmt', p[1], p[2]]

def p_datedur(p):
    '''date_duration : num date_unit'''
    p[0] = ['date_duration', p[1], p[2]]

def p_dateunit(p):
    '''date_unit : DAY
                 | MONTH
                 | WEEK
                 | YEAR'''
    p[0] = ['date_unit', p[1]]

def p_timedur(p):
    '''time_duration : num time_unit'''
    p[0] = ['time_duration', p[1], p[2]]

def p_timeunit(p):
    '''time_unit : HOUR
                 | MINUTE'''
    p[0] = ['time_unit', p[1]]

def p_stringstmt(p):
    '''str_stmt : var_str PLUS var_str str_stmt_rep'''
    p[0] = ['str_stmt', p[1], p[3], p[4]]

def p_str_var(p):
    '''var_str : string
                | user_string'''
    p[0] = p[1]

def p_strstmt_rep(p):
    '''str_stmt_rep : PLUS var_str str_stmt_rep
                    | empty'''
    if len(p) == 4:
        p[0] = ['str_stmt_rep', p[2], p[3]]

def p_mathstmt1(p):
    '''math_stmt : math_stmt PLUS math_stmt
         | math_stmt MINUS math_stmt
         | math_stmt TIMES math_stmt
         | math_stmt SLASH math_stmt
         | LEFTPAREN math_stmt RIGHTPAREN'''
    if p[2] == '+':
        p[0] = ['math_plus', p[1], p[2], p[3]]
    elif p[2] == '-':
        p[0] = ['math_minus', p[1], p[2], p[3]]
    elif p[2] == '*':
        p[0] = ['math_mult', p[1], p[2], p[3]]
    elif p[2] == '/':
        p[0] = ['math_div', p[1], p[2], p[3]]
    else:
        p[0] = ['math_paren', p[1], p[2], p[3]]

def p_mathstmt3(p):
    '''math_stmt : INTEGER
                  | variable'''
    if not type(p[1]) == list:
        p[0] = ['math_int', p[1]]
    else:
        p[0] = ['math_var', p[1]]

def p_quote(p):
    '''quote : QUOTATION'''
    p[0] = ['quote', p[1]]

def p_exportstmt(p):
    '''export_stmt : export filename
                    | empty'''
    if len(p) == 3:
        p[0] = ['export_stmt', p[1], p[2]]
    else:
        p[0] = ['export_stmt', None]
    
def p_filename(p):
    '''filename : string'''
    p[0] = ['filename', p[1]]

def p_export(p):
    '''export : EXPORT'''
    p[0] = ['export', p[1]]

def p_name(p):
    '''name : strings'''
    p[0] = ['name', p[1]]

def p_and(p):
    '''and : AND'''
    p[0] = ['and', p[1]]

def p_comma(p):
    '''comma : COMMA'''
    p[0] = ['comma', p[1]]

def p_end(p):
    '''whatever : newline whatever
                | empty'''
    pass

def p_with(p):
    '''with : WITH'''
    p[0] = ['with', p[1]]

def p_at(p):
    '''at : AT'''
    p[0] = ['at', p[1]]

def p_num(p):
    '''num : INTEGER'''
    p[0] = ['num', p[1]]

def p_meridian(p):
    '''meridian : AM
                | PM'''
    p[0] = ['meridian', p[1]]

def p_from(p):
    '''from : FROM'''
    p[0] = ['from', p[1]]

def p_to(p):
    '''to : TO'''
    p[0] = ['to', p[1]]

def p_colon(p):
    '''colon : COLON'''
    p[0] = ['colon', p[1]]

def p_build(p):
    '''build : BUILD'''
    p[0] = ['build', p[1]]

def p_schedule(p):
    '''schedule : SCHEDULE'''
    p[0] = ['schedule', p[1]]

def p_user_string(p):
    '''user_string : USERSTRING'''
    p[0] = ['user_string', p[1]]

def p_string(p):
    '''string : STRING'''
    p[0] = ['string', p[1]]

def p_strings(p):
    '''strings : STRING string_rep'''
    str_list = ""
    for string in p[2][1:]:
        if string:
            if string[0] == 'strings':
                str_list = str_list + ' ' + str(string[1])
            else:
                str_list = str_list + " " + str(string)
    p[0] = ['strings', p[1] + str_list]

def p_string_rep(p):
    '''string_rep : strings
                    | empty'''
    p[0] = ['string_rep', p[1]]

def p_empty(p):
    '''empty :'''
    pass

def p_import(p):
    '''import : IMPORT'''
    p[0] = ['import', p[1]]

def p_print(p):
    '''print : PRINT'''
    p[0] = ['print', p[1]]

def p_newline(p):
    '''newline : NEWLINE'''
    p[0] = ['newline', p[1]]

def p_types(p):
    '''type : NUMTYPE
            | DECTYPE
            | STRTYPE'''
    p[0] = ['type', p[1]]

def p_error(p):
    print 'Unexpected Error in Parser with token: ', p

# ----INITIALIZE PARSER----
yacc.yacc()
import sys

#Read source program
data = ''
with open(sys.argv[1], 'r') as f:
    data = f.read()
#Parse source program
tree = yacc.parse(data)

#Write translation to file
with open('translation.py', 'w') as f:
    f.write(trans.translate(tree))