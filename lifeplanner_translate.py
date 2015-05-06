import yacc
import sys
import datetime as dt
event_count = 0
all_events = []

def translate(tree):
	if tree[0] != 'program':
		return -1
	return 'import datetime as dt\n' + \
		dir_to_func['program'](tree[1:], 0)

def parse_program(tree, num_tabs):
	#print "parse_program tree: ", str(tree)
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
	entire_prog = ''

	if tree[0][1]:
		entire_prog += dir_to_func['function_blocks'](tree[0][1:], num_tabs) + '\n' 
	if tree[1][1]:
		entire_prog += dir_to_func['import_stmt'](tree[1][1:], num_tabs) + '\n'
	if tree[2][1]:
		entire_prog += 'var_all_events = []' + '\n' + dir_to_func['schedule_stmts'](tree[2][1:], num_tabs) + '\n'
	print "\ntree[3][1]: ", tree[3][1]
	if tree[3][1]:
		entire_prog += dir_to_func['build_schedule'](tree[3][1:], num_tabs) + '\n'
	if tree[4][1]:
		entire_prog += dir_to_func['export_stmt'](tree[4][1:], num_tabs)
	return entire_prog

def parse_function_blocks(tree, num_tabs):
	return 'function_blocks'
	#need to finish translating

def parse_import_stmt(tree, num_tabs):
	return 'readCalendar(' + str(dir_to_func['filename'](tree[1][1:], num_tabs)) + ')'

def parse_filename(tree, num_tabs):
	return tree[0][1]

def parse_schedule_stmts(tree, num_tabs):
	# print "\nparse_schedule_stmts tree: ", str(tree)
	if len(tree) != 4:
		return -1
	if tree[0][0] != 'date':
		return -1
	if tree[1][0] != 'colon':
		return -1
	if tree[2][0] != 'event_list':
		return -1
	if tree[3][0] != 'schedule_stmts_rep':
		return -1
	month, day, year = dir_to_func['date'](tree[0][1:], num_tabs)
	code = dir_to_func['event_list'](tree[2][1:], 0, month, day, year) + '\n' 

	if tree[3][1][1]:
		code += dir_to_func['schedule_stmts_rep'](tree[3][1:], num_tabs)
	return code

def parse_schedule_stmts_rep(tree, num_tabs):
	if tree and tree[0][0] == 'schedule_stmts':
		return dir_to_func['schedule_stmts'](tree[0][1:], num_tabs)
	return ''

def parse_build_schedule(tree, num_tabs):
	print "parse_build_schedule tree: ", tree
	# return "hello"
	if len(tree) != 4:
		return -1
	if tree[0][0] != 'build':
		return -1
	if tree[1][0] != 'schedule':
		return -1
	if tree[2] and tree[2][0] != 'tag_priorities':
		return -1
	if tree[3] and tree[3][0] != 'clean':
		return -1
	code = ''
	if tree[2][1]:
		code += dir_to_func['tag_priorities'](tree[2][1:], num_tabs) + '\n' 
	if tree[3][1]:
		code += dir_to_func['clean'](tree[3][1:], num_tabs)
	return code

def parse_clean(tree, num_tabs):
	# print "parse_clean: ", str(tree)
	# parse_clean:  [['expr_block', ['expr', ['print_stmt', ['print', 'print'], ['variable', 'hello']]], ['expr_block_rep', ['expr_block', None]]], 
					# ['clean', None]]
	if tree[0][0] != 'expr_block':
		return -1
	code = ''
	# print "\ntree[0][1][1]: ", tree[0][1][1]
	if tree[0][1][1]:
		code += dir_to_func['expr_block'](tree[0][1:], num_tabs) + '\n'
	return code

def parse_expr_block(tree, num_tabs):
	# print "parse_expr_block tree: ", str(tree)
	# parse_expr_block tree:  [['expr', ['print_stmt', ['print', 'print'], ['variable', 'hello']]], ['expr_block_rep', ['expr_block', None]]]
	if tree[0][0] != 'expr':
		return -1
	code = ''
	code += dir_to_func['expr'](tree[0][1:], num_tabs)
	# print "tree[1]: ", tree[1]
	if tree[1][1][1]:
		code += dir_to_func['expr_block_rep'](tree[1][1:], num_tabs) + '\n'
	return code

def parse_expr_block_rep(tree, num_tabs):
	# print "parse_expr_block_rep: ", str(tree)
	#parse_expr_block_rep:  [['expr', ['print_stmt', ['print', 'print'], ['variable', 'var']]], ['expr_block_rep', ['expr_block', None]]]
	if tree and tree[0][0] == 'expr_block':
		return dir_to_func['expr_block'](tree[0][1:], num_tabs)
	return ''
# [['expr_block', 0,0
# ['expr', ['print_stmt', ['print', 'print'], ['quote', '"'], ['strings', 'hello world'], ['quote', '"']]], 0,1
# ['expr_block_rep', ['expr_block', ['expr', ['print_stmt', ['print', 'print'], ['variable', 'var']]], ['expr_block_rep', ['expr_block', None]]]] 0,2
# ], ['clean', None]] 1


def parse_expr(tree, num_tabs):
	# print 'parse_expr tree: ', str(tree)
	# parse_expr tree:  [['print_stmt', ['print', 'print'], ['variable', 'hello']]]
	code = ''
	if tree[0][0] == 'print_stmt':
		code += dir_to_func['print_stmt'](tree[0][1:], num_tabs) + '\n'
	if tree[0][0] == 'if_stmt':
		code += dir_to_func['if_stmt'](tree[0][1:], num_tabs) + '\n'
	if tree[0][0] == 'while_stmt':
		code += dir_to_func['while_stmt'](tree[0][1:], num_tabs) + '\n'
	if tree[0][0] == 'for_stmt':
		code += dir_to_func['for_stmt'](tree[0][1:], num_tabs) + '\n'
	if tree[0][0] == 'event_stmt':
		code += dir_to_func['event_stmt'](tree[0][1:], num_tabs) + '\n'
	if tree[0][0] == 'comment_stmt':
		code += dir_to_func['comment_stmt'](tree[0][1:], num_tabs)
	if tree[0][0] == 'assignment_stmt':
		code += dir_to_func['assignment_stmt'](tree[0][1:], num_tabs) + '\n'
	if tree[0][0] == 'math_stmt':
		code += dir_to_func['math_stmt'](tree[0][1:], num_tabs) + '\n'
	if tree[0][0] == 'time_math':
		code += dir_to_func['time_math'](tree[0][1:], num_tabs) + '\n'
	if tree[0][0] == 'day_math':
		code += dir_to_func['day_math'](tree[0][1:], num_tabs) + '\n'
	if tree[0][0] == 'func':
		code += dir_to_func['func'](tree[0][1:], num_tabs) + '\n'
	if tree[0][0] == 'time_range':
		code += dir_to_func['time_range'](tree[0][1:], num_tabs) + '\n'
	return code

def parse_assignment_stmt(tree, num_tabs):
	print "\nparse_assignment_stmt: ", str(tree)
	#parse_assignment_stmt:  [['variable', 'i'], '=', ['value', ['math_stmt', '0']]]
	code = ''
	if tree[0][0] == 'variable':
		code += dir_to_func['variable'](tree[0][1], num_tabs) + ' = '
	if tree[2][0] == 'value':
		code += dir_to_func['value'](tree[2][1], num_tabs)
	return code

def parse_math_stmt(tree, num_tabs):
	print '\nparse_math_stmt' + str(tree)
	if len(tree) == 1:
	    return str(tree[0])
	elif tree[0] == '(':
	    return '(' + parse_math_stmt(tree[1]) + ')'
	elif tree[1] in ('+', '-', '*', '/'):
	    return parse_math_stmt(tree[0]) + str(tree[1]) \
	    + parse_math_stmt(tree[2])
	else:
		print 'Bad math statement'
		return -1

def parse_variable(tree, num_tabs):
	print "parse_variable: ", str(tree)
	return str(tree)

def parse_value(tree, num_tabs):
	print 'parse_value tree: ' + str(tree)
	label = tree[0]
	if label in \
	['variable', 'num', 'time', 'date', 'event', 'tag', 'math_stmt']:
		return dir_to_func[label](tree[1:], num_tabs)
	else:
		return -1

def parse_print_stmt(tree, num_tabs):
	# print "\nparse_print_stmt tree: ", str(tree)
	#parse_print_stmt tree:  [['print', 'print'], ['variable', 'hello']]
	#parse_print_stmt tree:  [['print', 'print'], ['quote', '"'], ['strings', 'hello world'], ['quote', '"']]
	if tree[0][0] != 'print':
		return -1
	code = ''
	i = 0
	while i < num_tabs:
		code += '\t'
		i += 1
	if tree[1][0] == 'variable':
		code += 'print ' + dir_to_func['variable'](tree[1][1], num_tabs)
	if tree[1][0] == 'quote':
		code += 'print \"' + dir_to_func['strings'](tree[2][1], num_tabs) + '\"'
	return code

def parse_strings(tree, num_tabs):
	return tree

def parse_export_stmt(tree, num_tabs):
	if len(tree) != 2:
		return -1
	if tree[0][0] != 'export':
		return -1
	if tree[1][0] != 'filename':
		return -1
	return \
	'export_cal(' + \
	str(dir_to_func['filename'](tree[1][1:], num_tabs)) + ')'
	
def parse_date(tree, num_tabs):
	month = tree[0][1]
	day = tree[1][1]
	year = tree[2][1]
	if len(month) > 2:
		sys.stderr.write('Month cannot be more than 2 digits')
	if len(day) > 2:
		sys.stderr.write('Day cannot be more than 2 digits')
	if len(year) != 4:
		if len(year) == 2:
			year = '20' + year
		else:
			sys.stderr.write('Year cannot be more than 4 digits')
	return month, day, year

def parse_event_list(tree, num_tabs, month, day, year):
	# if len(tree) != 2:
	# 	return -1
	print
	print 'event' + str(tree)
	print
	if not tree[0]:
		return ''
	if tree[0][0] != 'event':
		return -1
	if tree[1][0] and tree[1][0] != 'event_list_rep':
		return -1 
	code = dir_to_func['event'](tree[0][1:], num_tabs, month, day, year) + '\n'
	if tree[1][0]:
		code += dir_to_func['event_list_rep'](tree[1][1:], num_tabs, month, day, year)
	return \
	code + '\n' 

def parse_event_list_rep(tree, num_tabs, month, day, year=None):
	print tree
	print
	if tree and tree[0][0] == 'event_list':
		print tree[0][1:]
		print
		return dir_to_func['event_list'](tree[0][1:], num_tabs, month, day, year)
	return ''

def parse_event(tree, num_tabs, month, day, year):
	# event[['event', ['event_title', ('strings', 'PLT')], ['when', ('from', 'from'), ['time', ('num', '4'), ('colon', ':'), ('num', '00'), ('meridian', 'PM')], ('to', 'to'), ['time', ('num', '9'), ('colon', ':'), ('num', '00'), ('meridian', 'PM')]], ('where', None), ('who', None), ('tag_line', None)], ['event_list_rep', ['event_list', ['event', ['event_title', ('strings', 'Dinner')], ['when', ('from', 'from'), ['time', ('num', '9'), ('colon', ':'), ('num', '00'), ('meridian', 'PM')], ('to', 'to'), ['time', ('num', '10'), ('colon', ':'), ('num', '00'), ('meridian', 'PM')]], ('where', None), ('who', None), ('tag_line', None)], ['event_list_rep', ['event_list', None]]]]]

	# if len(tree) != 4:
	# 	return -1
	if tree[0][0] != 'event_title':
		return -1
	if tree[1][0] != 'when':
		return -1
	if tree[2][0] != 'where':
		return -1
	if tree[3][0] != 'who':
		return -1
	# if tree[4][0] != 'tag_line':
	# 	return -1

	global event_count
	event_initial = 'event_dict' + str(event_count) + ' = {}\n'
	modify_event = dir_to_func['event_title'](tree[0][1:], num_tabs) \
		+ '\n' + dir_to_func['when'](tree[1][1:], num_tabs, month, day, year) \
		+ '\n' 
	if tree[2][1]:
		modify_event += dir_to_func['where'](tree[2][1:], num_tabs) +'\n'
	if tree[3][1]:
		modify_event += dir_to_func['who'](tree[3][1:], num_tabs) + '\n'
	if tree[4]:
		modify_event += dir_to_func['tag_line'](tree[4][1:], num_tabs)
	add_event = 'var_all_events.append(event_dict' + str(event_count) + ')'
	event_count += 1
	return event_initial + modify_event + add_event 

def parse_event_title(tree, num_tabs):
	event_title = tree[0][1]
	global event_count
	return 'event_dict' + str(event_count) + '[\"event_title\"] = ' + '"' +event_title + '"' 

def parse_when(tree, num_tabs, month, day, year):
	if len(tree) != 4:
		return -1
	if tree[0][0] != 'from':
		return -1
	if tree[1][0] != 'time':
		return -1
	if tree[2][0] != 'to':
		return -1
	if tree[3][0] != 'time':
		return -1
	code = ''
	global event_count
	create_day = 'date' + str(event_count) + ' = ' + \
		'dt.date(' + year + ',' + month + ',' + day + ')'
	hour, minute = dir_to_func['time'](tree[1][1:], num_tabs)
	create_time = 'time' + str(event_count) + ' = ' + \
		'dt.time(' + hour + ',' + minute + ')'
	create_dt = 'from_dt' + str(event_count) + ' = ' + \
		'dt.datetime_combine( date' + str(event_count) + \
		', time' + str(event_count) +  ')'
	add_dt = 'event_dict' + str(event_count) + '[\"from\"] = ' + 'from_dt' + str(event_count) 
	code += create_day + '\n' + create_time + '\n' + \
		create_dt + '\n' + add_dt + '\n'
	meridian1 = getmeridian(tree[1][1:], num_tabs)
	meridian2 = getmeridian(tree[3][1:], num_tabs)
	if meridian1 == 'PM' and meridian2 == 'AM':
		first_day = dt.date(int(float(year)), int(float(month)), int(float(day)))
		first_day += dt.timedelta(days=1)
		year = first_day.year
		month = first_day.month
		day = first_day.day
		create_day = 'date' + str(event_count) + ' = ' + \
		'dt.date(' + year + ',' + month + ',' + day + ')'
	hour, minute = dir_to_func['time'](tree[3][1:], num_tabs)
	create_time = 'time' + str(event_count) + ' = ' + \
		'dt.time(' + hour + ',' + minute + ')'
	create_dt = 'to_dt' + str(event_count) + ' = ' + \
		'dt.datetime_combine( date' + str(event_count) + \
		', time' + str(event_count) +  ')'
	add_dt = 'event_dict' + str(event_count) + '[\"to\"] = ' + 'to_dt' + str(event_count)
	code += create_day + '\n' + create_time + '\n' + \
			create_dt + '\n' + add_dt
	return code


def parse_meridian(tree, num_tabs):
	if len(tree) != 1:
		sys.stderr.write('Invalid meridian')
		sys.exit(1)
	return tree[0]

def getmeridian(tree, num_tabs):
	if len(tree) != 4 or tree[3] != 'meridian':
		return -1 
	return dir_to_func['meridian'](tree[3][1:], num_tabs)

def parse_time(tree, num_tabs):
	if len(tree) != 4:
		sys.stderr.write('Invalid time input')
		sys.exit(1)
	hour = tree[0][1]
	minute = tree[2][1]
	print hour, minute
	if getmeridian(tree, num_tabs) == 'PM':
		hour = str(float(hour) + 12)
	return hour, minute

	
def parse_where(tree, num_tabs):
	if not tree[0]:
		return ''
	if len(tree) != 2 or tree[0][1] != 'at' or tree[1][0] != 'location': 
		sys.stderr.write('Invalid location for event')
		sys.exit(1)
	event_location = dir_to_func['location'](tree[1][1:], num_tabs)
	return 'event_dict' + str(event_count) + '[\"location\"] = ' + event_location


def parse_location(tree, num_tabs):
	if len(tree) != 1:
		print tree
		sys.stderr.write('Invalid location')
		sys.exit(1)
	return tree[0][1]

def parse_who(tree, num_tabs):
	if len(tree) != 2 or tree[0][1] != 'with' or tree[1][0] != 'people_list':
		sys.stderr.write('Invalid who for event')
		sys.exit(1)
	pp_list = dir_to_func['people_list'](tree[1][1:], num_tabs)
	return pp_list

def parse_people_list(tree, num_tabs):
	# if len(tree) != 2 or tree[0][1] != 'people_list' or tree[1][0] != 'name':
	# 	sys.stderr.write('Invalid person for event')
	# 	sys.exit(1)	
	code = 'pp_list' + str(event_count)  + '= []\n'
	for branch in tree:
		if branch[0] == 'name':
			code += 'pp_list' + str(event_count) + '.append(' + dir_to_func['name'](branch[1], num_tabs) + ')\n'
		if branch[0] == 'comma':
			code += dir_to_func['comma'](branch[1:], num_tabs)
		if branch[0] == 'and':
			code += 'pp_list' + str(event_count) + '.append(' + dir_to_func['name'](branch[2][1], num_tabs) + ')\n'
	code += 'event_dict' + str(event_count) + '[\"with\"] = ppl_list' + str(event_count)
	return code

def parse_name(tree, num_tabs):
	return tree[1]

def parse_comma(tree, num_tabs):
	code = ''
	for branch in tree:
		if branch[0] == 'name':
			code += 'pp_list' + str(event_count) + '.append(' + dir_to_func['name'](branch[1], num_tabs) + ')\n'
		if branch[0] == 'comma':
			code += dir_to_func['comma'](branch[1:], num_tabs)
		if branch[0] == 'and':
			code += 'pp_list' + str(event_count) + '.append(' + dir_to_func['name'](branch[2][1], num_tabs) + ')\n'
	return code



def parse_function_block(tree, num_tabs):
	pass

def parse_else_block(tree, num_tabs):
	pass
	
def parse_elseif_blocks(tree, num_tabs):
	pass
	
def parse_cancel_stmt(tree, num_tabs):
	pass
	
def parse_tag_line(tree, num_tabs):
	return ''
	
def parse_bool_expr(tree, num_tabs):
	pass

def parse_for_stmt(tree, num_tabs):
	pass
	
def parse_bool_operation(tree, num_tabs):
	pass
	
def parse_if_stmt(tree, num_tabs):
	pass
	
def parse_date_duration(tree, num_tabs):
	pass
	
def parse_if_block(tree, num_tabs):
	pass
	
def parse_parameter_list(tree, num_tabs):
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

def parse_year(tree, num_tabs):
	pass
		
def parse_tag_priorities(tree, num_tabs):
	return 'tag priorities'
	
def parse_comment_stmt(tree, num_tabs):
	return ''

def parse_add_stmt(tree, num_tabs):
	pass
	
def parse_function_declaration(tree, num_tabs):
	pass
	
def parse_time_duration(tree, num_tabs):
	pass
	
def parse_while_stmt(tree, num_tabs):
	pass

def parse_and(tree, num_tabs):
	pass

def parse_string(tree, num_tabs):
	pass

def parse_colon(tree, num_tabs):
	pass

def parse_from(tree, num_tabs):
	pass

def parse_newline(tree, num_tabs):
	pass

def parse_build(tree, num_tabs):
	pass

def parse_tag_op(tree, num_tabs):
	pass

def parse_tag(tree, num_tabs):
	pass

def parse_export(tree, num_tabs):
	pass

def parse_time_unit(tree, num_tabs):
	pass

def parse_import(tree, num_tabs):
	pass


def parse_bool_operator(tree, num_tabs):
	pass

def parse_with(tree, num_tabs):
	pass

def parse_date_unit(tree, num_tabs):
	pass


def parse_string_rep(tree, num_tabs):
	pass

def parse_schedule(tree, num_tabs):
	pass

def parse_bool_value(tree, num_tabs):
	pass

def parse_num(tree, num_tabs):
	return tree[0]

def parse_to(tree, num_tabs):
	pass

def parse_tag_name(tree, num_tabs):
	pass

def parse_event_stmt(tree, num_tabs):
	pass

def parse_print(tree, num_tabs):
	pass

def parse_at(tree, num_tabs):
	pass

def parse_type(tree, num_tabs):
	pass

def parse_comparison_operator(tree, num_tabs):
	pass

def parse_op(tree, num_tabs):
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
	'date' : parse_date,
	'schedule_stmts_rep' : parse_schedule_stmts_rep,
	'event_list_rep' : parse_event_list_rep,
	'event_title' : parse_event_title,
	'location' : parse_location,
	'tag_op' : parse_tag_op,
	'expr_block_rep' : parse_expr_block_rep,
	'expr' : parse_expr,
	'event_stmt' : parse_event_stmt,
	'value' : parse_value,
	'variable' : parse_variable,
	'bool_operator' : parse_bool_operator,
	'comparison_operator' : parse_comparison_operator,
	'bool_value' : parse_bool_value,
	'op' : parse_op,
	'date_unit' : parse_date_unit,
	'time_unit' : parse_time_unit,
	'filename' : parse_filename,
	'export' : parse_export,
	'tag_name' : parse_tag_name,
	'tag' : parse_tag,
	'and' : parse_and,
	'comma' : parse_comma,
	'with' : parse_with,
	'at' : parse_at,
	'num' : parse_num,
	'meridian' : parse_meridian,
	'from' : parse_from,
	'to' : parse_to,
	'colon' : parse_colon,
	'build' : parse_build,
	'schedule' : parse_schedule,
	'string' : parse_string,
	'string_rep' : parse_string_rep,
	'import' : parse_import,
	'print' : parse_print,
	'newline' : parse_newline,
	'type' : parse_type,
	'assignment_stmt' : parse_assignment_stmt,
}

