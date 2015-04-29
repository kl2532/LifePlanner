import yacc


def translate(tree):
	if tree[0] != 'program':
		return -1
	return dir_to_func['program'](tree[1:], 0)

def parse_program(tree, num_tabs):
	if len(tree) != 5:
		return -1
	if tree[0][0] != 'function_blocks':
		return -1
	if tree[1][0] != 'import_stmt':
		return -1
	if tree[2][0] != 'schedule_stmts':
		return -1
	if tree[3][0] != 'build_schedule':
		return -1
	if tree[4][0] != 'export_stmt':
		return -1
	return \
	dir_to_func['function_blocks'](tree[0][1:], 0) + '\n' + \
	dir_to_func['import_stmt'](tree[1][1:], 0) + '\n' + \
	dir_to_func['schedule_stmts'](tree[2][1:], 0) + '\n' + \
	dir_to_func['build_schedule'](tree[3][1:], 0) + '\n' + \
	dir_to_func['export_stmt'](tree[4][1:], 0)

def parse_function_blocks(tree, num_tabs):
	return 'function_blocks'

def parse_import_stmt(tree, num_tabs):
	return 'readCalendar(%s)' %tree[1]

def parse_schedule_stmts(tree, num_tabs):
	if len(tree) != 4:
		return -1
	if tree[0][0] != 'day':
		return -1
	if tree[1][0] != 'colon':
		return -1
	if tree[2][0] != 'event_list':
		return -1
	if tree[3][0] != 'schedule_stmts_rep':
		return -1
	return \
	dir_to_func['day'](tree[0][1:], 0) + '\n' + \
	dir_to_func['colon'](tree[1][1:], 0) + '\n' + \
	dir_to_func['event_list'](tree[2][1:], 0) + '\n' + \
	dir_to_func['schedule_stmts_rep'](tree[3][1:], 0)
	
def parse_build_schedule(tree, num_tabs):
	return 'build_schedule'

def parse_export_stmt(tree, num_tabs):
	return 'export_stmt'

def parse_function_block(tree, num_tabs):
	pass

def parse_comma(tree, num_tabs):
	pass

def parse_else_block(tree, num_tabs):
	pass
	
def parse_elseif_blocks(tree, num_tabs):
	pass
	
def parse_people_list(tree, num_tabs):
	pass
	
def parse_cancel_stmt(tree, num_tabs):
	pass
	
def parse_tag_line(tree, num_tabs):
	pass
	
def parse_print_stmt(tree, num_tabs):
	pass
	
def parse_bool_expr(tree, num_tabs):
	pass

def parse_for_stmt(tree, num_tabs):
	pass
	
def parse_bool_operation(tree, num_tabs):
	pass
	
def parse_if_stmt(tree, num_tabs):
	pass
	
def parse_name(tree, num_tabs):
	pass
	
def parse_date_duration(tree, num_tabs):
	pass
	
def parse_if_block(tree, num_tabs):
	pass
	
def parse_parameter_list(tree, num_tabs):
	pass
	
def parse_event_list(tree, num_tabs):
	pass
	
def parse_return_stmt(tree, num_tabs):
	pass
	
def parse_elseif_block(tree, num_tabs):
	pass
	
def parse_and(tree, num_tabs):
	pass
	
def parse_time_math(tree, num_tabs):
	pass
	
def parse_day_math(tree, num_tabs):
	pass
	
def parse_math_stmt(tree, num_tabs):
	pass

def parse_year(tree, num_tabs):
	pass
	
def parse_event(tree, num_tabs):
	pass
	
def parse_tag_priorities(tree, num_tabs):
	pass
	
def parse_comment_stmt(tree, num_tabs):
	pass
	
def parse_when(tree, num_tabs):
	pass

def parse_add_stmt(tree, num_tabs):
	pass
	
def parse_who(tree, num_tabs):
	pass
	
def parse_date(tree, num_tabs):
	pass
	
def parse_expr_block(tree, num_tabs):
	pass
	
def parse_function_declaration(tree, num_tabs):
	pass
	
def parse_time_duration(tree, num_tabs):
	pass
	
def parse_where(tree, num_tabs):
	pass
	
def parse_while_stmt(tree, num_tabs):
	pass
	
def parse_clean(tree, num_tabs):
	pass
	
def parse_time(tree, num_tabs):
	pass
	
def parse_strings(tree, num_tabs):
	pass
	
dir_to_func = {
	'program' : parse_program,
	'function_block' : parse_function_block,
	'function_blocks' : parse_function_blocks,
	'import_stmt' : parse_import_stmt,
	'schedule_stmts' : parse_schedule_stmts,
	'date' : parse_date,
	'year' : parse_year,
	'event_list' : parse_event_list,
	'event' : parse_event,
	'when' : parse_when,
	'time' : parse_time,
	'where' : parse_where,
	'who' : parse_who,
	'people_list' : parse_people_list,
	'comma' : parse_comma,
	'and' : parse_and,
	'tag_line' : parse_tag_line,
	'build_schedule' : parse_build_schedule,
	'tag_priorities' : parse_tag_priorities,
	'clean' : parse_clean,
	'expr_block' : parse_expr_block,
	'math_stmt' : parse_math_stmt,
	'comment_stmt' : parse_comment_stmt,
	'add_stmt' : parse_add_stmt,
	'cancel_stmt' : parse_cancel_stmt,
	'while_stmt' : parse_while_stmt,
	'for_stmt' : parse_for_stmt,
	'bool_expr' : parse_bool_expr,
	'bool_operation' : parse_bool_operation,
	'if_stmt' : parse_if_stmt,
	'if_block' : parse_if_block,
	'elseif_blocks' : parse_elseif_blocks,
	'elseif_block' : parse_elseif_block,
	'else_block' : parse_else_block,
	'day_math' : parse_day_math,
	'time_math' : parse_time_math,
	'print_stmt' : parse_print_stmt,
	'date_duration' : parse_date_duration,
	'time_duration' : parse_time_duration,
	'export_stmt' : parse_export_stmt,
	'name' : parse_name,
	'strings' : parse_strings,
	'function_declaration' : parse_function_declaration,
	'parameter_list' : parse_parameter_list,
	'return_stmt' : parse_return_stmt,
	'day' : parse_day,
}

