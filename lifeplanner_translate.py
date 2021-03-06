# Libraries
import yacc
import sys
import datetime as dt

#Global Variables
event_count = 0
all_events = []
get_event = '\ndef get_event(name, var_all_events):\n' + \
		'\tfor event in var_all_events:\n' + \
		'\t\tif event[\'event_title\'] == name:\n' + \
		'\t\t\treturn event'

#Start by translating program!
def translate(tree):
	try:
		if tree[0] != 'program':
			sys.stderr.write('Invalid program')
			sys.exit(1)
		return 'import datetime as dt\nimport time\nimport event as e\n' + \
			'import ourCalendar as c\n' + get_event + '\n' + \
			'cal = c.ourCalendar()\n\n' + 'var_all_events = []' + '\n' + dir_to_func['program'](tree[1:], 0)
	except:
		print 'Invalid program; Error: ', sys.exc_info()[0], ' From parsed tree: ', tree 
		sys.exit(1)

def parse_program(tree, num_tabs):
	try:
		if len(tree) != 5:
			sys.stderr.write('Invalid program start')
			sys.exit(1)
		if tree[0][0] != 'function_blocks':
			sys.stderr.write('Invalid function blocks')
			sys.exit(1)
		if tree[1][0] != 'import_stmt':
			sys.stderr.write('Invalid import statement')
			sys.exit(1)
		if tree[2][0] != 'schedule_stmts':
			sys.stderr.write('Invalid schedule')
			sys.exit(1)
		if tree[3][0] != 'build_schedule':
			sys.stderr.write('Invalid building of schedule')
			sys.exit(1)
		if tree[4][0] != 'export_stmt':
			sys.stderr.write('Invalid export statement')
			sys.exit(1)
		entire_prog = ''

		if tree[0][1]:
			entire_prog += dir_to_func['function_blocks'](tree[0][1:], num_tabs) \
			+ '\n' 
		if tree[1][1]:
			entire_prog += dir_to_func['import_stmt'](tree[1][1:], num_tabs) \
			+ '\n'
		if tree[2][1]:
			entire_prog += dir_to_func['schedule_stmts'](tree[2][1:], num_tabs) + '\n'
		if tree[3][1]:
			entire_prog += dir_to_func['build_schedule'](tree[3][1:], num_tabs) \
			+ '\n'
		if tree[4][1]:
			entire_prog += dir_to_func['export_stmt'](tree[4][1:], num_tabs)
		return entire_prog
	except:
		print 'Invalid program format; Error: ', sys.exc_info()[0], ' From parsed tree: ', tree 
		sys.exit(1)


def parse_function_blocks(tree, num_tabs):
	try:
		code = ''
		for f_block in tree:
			if f_block == None:
				return code
			code += parse_function_block(f_block[1:], num_tabs)
		return code
	except:
		print 'Invalid function blocks; Error: ', sys.exc_info()[0], ' From parsed tree: ', tree 
		sys.exit(1)


def parse_function_block(tree, num_tabs):
	try:
		code = parse_function_declaration(tree[0][2:], num_tabs)
		code += parse_expr_block(tree[1][1:], num_tabs+1)
		return code
	except:
		print 'Invalid function block; Error: ', sys.exc_info()[0], ' From parsed tree: ', tree 
		sys.exit(1)

def parse_function_declaration(tree, num_tabs):
	try:	
		code = ''
		i = 0
		while i < num_tabs:
			code += '\t'
			i += 1
		code += 'def ' + dir_to_func['variable'](tree[0][1], num_tabs) + '('
		params = dir_to_func['parameter_list'](tree[1], num_tabs)
		if params != '':
			x = params.split()
			params = x[0]
			for i in range(1, len(x)):
				params += ', ' + x[i]
		code += params + '):\n'
		return code
	except:
		print 'Invalid function declaration; Error: ', sys.exc_info()[0], ' From parsed tree: ', tree 
		sys.exit(1)

def parse_return_stmt(tree, num_tabs):
	try:
		code = '\t'*num_tabs
		code += 'return ' + parse_value(tree[1][1], num_tabs) + '\n\n'
		return code
	except:
		print 'Invalid return statement; Error: ', sys.exc_info()[0], ' From parsed tree: ', tree 
		sys.exit(1)

def parse_import_stmt(tree, num_tabs):
	try:
		code = 'orig_event_dict = cal.read_calendar(\'' 
		code += str(dir_to_func['filename'](tree[1][1:], num_tabs)) + '\')\n'
		code += 'for orig_e in orig_event_dict:\n'
		code += '\te_name = orig_e[\'event_title\']\n'
		code += '\te_to = orig_e[\'to\']\n'
		code += '\te_from = orig_e[\'from\']\n'
		code += '\te_at = orig_e[\'at\']\n'
		code += '\te_with = orig_e[\'with\']\n'
		code += '\te_uid = orig_e[\'uid\']\n'
		code += '\tvar_all_events.append(orig_e)\n'
		return code
	except:
		print 'Invalid import statement; Error: ', sys.exc_info()[0], ' From parsed tree: ', tree 
		sys.exit(1)

def parse_filename(tree, num_tabs):
	try:
		return tree[0][1]
	except:
		print 'Invalid file name; Error: ', sys.exc_info()[0], ' From parsed tree: ', tree 
		sys.exit(1)

def parse_schedule_stmts(tree, num_tabs):
	try:
		if len(tree) != 4:
			sys.stderr.write('Invalid schedule list')
			sys.exit(1)
		if tree[0][0] != 'date':
			sys.stderr.write('Date not found')
			sys.exit(1)
		if tree[1][0] != 'colon':
			sys.stderr.write('Colon not found')
			sys.exit(1)
		if tree[2][0] != 'event_list':
			sys.stderr.write('Event list not found')
			sys.exit(1)
		if tree[3][0] != 'schedule_stmts_rep':
			sys.stderr.write('Invalid schedule list')
			sys.exit(1)
		month, day, year = dir_to_func['date'](tree[0][1:], num_tabs)
		code = dir_to_func['event_list'](tree[2][1:], 0, month, day, year) + '\n' 
		if tree[3][1][1]:
			code += dir_to_func['schedule_stmts_rep'](tree[3][1:], num_tabs)
		return code
	except:
		print 'Invalid schedule statements; Error: ', sys.exc_info()[0], ' From parsed tree: ', tree 
		sys.exit(1)

def parse_schedule_stmts_rep(tree, num_tabs):
	try:
		if tree and tree[0][0] == 'schedule_stmts':
			return dir_to_func['schedule_stmts'](tree[0][1:], num_tabs)
		return ''
	except:
		print 'Invalid repetition of schedule statements; Error: ', sys.exc_info()[0], ' From parsed tree: ', tree 
		sys.exit(1)

def parse_build_schedule(tree, num_tabs):
	try:
		if len(tree) != 3:
			sys.stderr.write('Invalid build schedule')
			sys.exit(1)
		if tree[0][0] != 'build':
			sys.stderr.write('Build not found')
			sys.exit(1)
		if tree[1][0] != 'schedule':
			sys.stderr.write('Schedule not found')
			sys.exit(1)
		if tree[2] and tree[2][0] != 'clean':
			sys.stderr.write('Build schedule body not found')
			sys.exit(1)
		code = ''
		if tree[2][1]:
			code += dir_to_func['clean'](tree[2][1:], num_tabs)
		return code
	except:
		print 'Invalid build schedule; Error: ', sys.exc_info()[0], ' From parsed tree: ', tree 
		sys.exit(1)

def parse_clean(tree, num_tabs):
	try:
		if tree[0][0] != 'expr_block':
			sys.stderr.write('Expression block not found')
			sys.exit(1)
		code = ''
		if tree[0][1][1]:
			code += dir_to_func['expr_block'](tree[0][1:], num_tabs) + '\n'
		return code
	except:
		print 'Invalid segment after build schedule; Error: ', sys.exc_info()[0], ' From parsed tree: ', tree 
		sys.exit(1)

def parse_expr_block(tree, num_tabs):
	try:
		if not tree[0]:
			return ''
		if tree[0][0] != 'expr':
			sys.stderr.write('Expression not found')
			sys.exit(1)
		code = ''
		code += dir_to_func['expr'](tree[0][1:], num_tabs)
		if tree[1][1][1]:
			code += dir_to_func['expr_block_rep'](tree[1][1:], num_tabs) + '\n'
		return code
	except:
		print 'Invalid expression block; Error: ', sys.exc_info()[0], ' From parsed tree: ', tree 
		sys.exit(1)

def parse_expr_block_rep(tree, num_tabs):
	try:
		if tree and tree[0][0] == 'expr_block':
			return dir_to_func['expr_block'](tree[0][1:], num_tabs)
		return ''
	except:
		print 'Invalid repetition of expression block; Error: ', sys.exc_info()[0], ' From parsed tree: ', tree 
		sys.exit(1)

def parse_expr(tree, num_tabs):
	try:
		code = ''
		label = tree[0][0]
		code += dir_to_func[label](tree[0][1:], num_tabs) 
		if label != 'return_stmt' and label != 'plan_stmt':
			code += '\n'
		return code
	except:
		print 'Invalid expression; Error: ', sys.exc_info()[0], ' From parsed tree: ', tree 
		sys.exit(1)

def parse_func(tree, num_tabs):
	try:
		code = ''
		i = 0
		while i < num_tabs:
			code += '\t'
			i += 1
		code += dir_to_func['variable'](tree[0][1], num_tabs) + '('
		params = dir_to_func['parameter_list'](tree[1], num_tabs)
		if params != '':
			x = params.split()
			params = x[0]
			for i in range(1, len(x)):
				params += ', ' + x[i]
		code += params + ')\n'
		return code
	except:
		print 'Invalid function; Error: ', sys.exc_info()[0], ' From parsed tree: ', tree 
		sys.exit(1)

def parse_parameter_list(tree, num_tabs):
	try:
		params = ''
		if tree[1]:
			params += tree[1]
			return params + ' ' + parse_parameter_list(tree[2], num_tabs)
		return ''
	except:
		print 'Invalid parameter list; Error: ', sys.exc_info()[0], ' From parsed tree: ', tree 
		sys.exit(1)

def parse_day_math(tree, num_tabs):
	pass

def parse_time_math(tree, num_tabs):
	try:
		code = ''
		if tree[0][0] == 'time':
			hour, minute = dir_to_func['time_elements'](tree[0][1:], num_tabs)
			code += 'dt.datetime.combine(dt.date.today(), dt.time(' + hour + ',' \
				+ minute + '))'
		if tree[0][0] == 'variable':
			code += 'dt.datetime.combine(dt.date.today(), ' + dir_to_func['variable'](tree[0][1:], num_tabs) + ')'
		if tree[1][0] == 'op':
			code += dir_to_func['op'](tree[1][1:], num_tabs)
		if tree[2][0] == 'time_duration':
			code += dir_to_func['time_duration'](tree[2][1:], num_tabs)
		return '(' + code + ').time()'
	except:
		print 'Invalid time math statement; Error: ', sys.exc_info()[0], ' From parsed tree: ', tree 
		sys.exit(1)

def parse_time_duration(tree, num_tabs):
	try:
		if tree[0][0] == 'num':
			num = dir_to_func['num'](tree[0][1:], num_tabs)
		if tree[1][0] == 'time_unit':
			unit = dir_to_func['time_unit'](tree[1][1:], num_tabs)
		return 'dt.timedelta(' + unit + '=' + num + ')'
	except:
		print 'Invalid time duration; Error: ', sys.exc_info()[0], ' From parsed tree: ', tree 
		sys.exit(1)

def parse_time_unit(tree, num_tabs):
	try:
		return tree[0]
	except:
		print 'Invalid time unit; Error: ', sys.exc_info()[0], ' From parsed tree: ', tree 
		sys.exit(1)

def parse_op(tree, num_tabs):
	try:
		if tree[0] == 'add':
			return '+'
		return '-'
	except:
		print 'Invalid operation; Error: ', sys.exc_info()[0], ' From parsed tree: ', tree 
		sys.exit(1)

def parse_event_stmt(tree, num_tabs):
	try:
		if tree[0][0] == 'cancel_stmt':
			return dir_to_func['cancel_stmt'](tree[0][1:], num_tabs)
		if tree[0][0] == 'update_stmt':
			return dir_to_func['update_stmt'](tree[0][1:], num_tabs)
		if tree[0][0] == 'add_stmt':
			return dir_to_func['add_stmt'](tree[0][1:], num_tabs)
		if tree[0][0] == 'remove_stmt':
			return dir_to_func['remove_stmt'](tree[0][1:], num_tabs)
		return 'event_stmt'
	except:
		print 'Invalid event statement; Error: ', sys.exc_info()[0], ' From parsed tree: ', tree 
		sys.exit(1)

def parse_remove_stmt(tree, num_tabs):
	try:
		tabs = ''
		i = 0
		while i < num_tabs:
			tabs += '\t'
			i += 1
		code = tabs + 'for event in var_all_events:\n\t' + tabs \
			+ 'if event[\'event_title\'] == \'' \
			+ dir_to_func['strings'](tree[1][1], num_tabs) \
			+ '\':\n\t\t' + tabs + 'event[\'with\'].remove(\'' \
			+ dir_to_func['strings'](tree[0][1], num_tabs) + '\')'
		return code
	except:
		print 'Invalid remove statement; Error: ', sys.exc_info()[0], ' From parsed tree: ', tree 
		sys.exit(1)

def parse_add_stmt(tree, num_tabs):
	try:
		tabs = ''
		i = 0
		while i < num_tabs:
			tabs += '\t'
			i += 1
		code = tabs + 'for event in var_all_events:\n\t' \
			+ tabs + 'if event[\'event_title\'] == \'' \
			+ dir_to_func['strings'](tree[1][1], num_tabs) + '\':\n\t\t' + tabs \
			+ 'event[\'with\'].append(\'' \
			+ dir_to_func['strings'](tree[0][1], num_tabs) + '\')'
		return code
	except:
		print 'Invalid add statement; Error: ', sys.exc_info()[0], ' From parsed tree: ', tree 
		sys.exit(1)

def parse_update_stmt(tree, num_tabs):
	try:
		tabs = ''
		i = 0
		while i < num_tabs:
			tabs += '\t'
			i += 1
		code = tabs + 'for event in var_all_events:\n\t' + \
			tabs + 'if event[\'event_title\'] == \'' + \
			dir_to_func['strings'](tree[0][1], num_tabs) + '\':\n\t\t'
		if tree[1] == 'from' or tree[1] == 'to':
			code += tabs + 'date = str(event[\''+ tree[1] + '\'].date())\n\t\t'
			code += tabs + 'time = ' \
				+ dir_to_func['variable'](tree[2][1], num_tabs) + '\n\t\t'
			code += tabs \
				+ 'new_when = date + \' \' + time.strftime("%I:%M %p")\n\t\t'
			code += tabs + 'event[\'' + tree[1] \
				+ '\'] = dt.datetime.strptime(new_when, \'%Y-%m-%d %I:%M %p\')\n'
		if tree[1] == 'at':
			code += tabs + 'event[\'' + tree[1] + '\'] = ' \
				+ dir_to_func['variable'](tree[2][1], num_tabs)
		return code
	except:
		print 'Invalid update statement; Error: ', sys.exc_info()[0], ' From parsed tree: ', tree 
		sys.exit(1)

def parse_cancel_stmt(tree, num_tabs):
	try:
		code = '\t' * num_tabs + 'for i in range(len(var_all_events)):\n\t' + '\t' * num_tabs + \
		'event = var_all_events[i]\n\t' + '\t' * num_tabs + \
		'if event[\'event_title\'] == \'' + \
		dir_to_func['strings'](tree[1][1], num_tabs) + '\':\n\t\t' + '\t' * num_tabs + \
		'if \'uid\' in event:\n\t\t\t' + '\t' * num_tabs + \
		'var_all_events[i][\'cancel\'] = True\n\t\t' + '\t' * num_tabs + \
		'else:\n\t\t\t' + '\t' * num_tabs + \
		'var_all_events.pop(i)\n\t\t' + '\t' * num_tabs + 'break\n'
		return code
	except:
		print 'Invalid cancel statement; Error: ', sys.exc_info()[0], ' From parsed tree: ', tree 
		sys.exit(1)

def parse_assignment_stmt(tree, num_tabs):
	try:
		code = ''
		code += '\t' * num_tabs
		if tree[0][0] == 'variable':
			code += dir_to_func['variable'](tree[0][1], num_tabs) + ' = '
			code += dir_to_func[tree[2][0]](tree[2][1], num_tabs)
		return code
	except:
		print 'Invalid assignment statement; Error: ', sys.exc_info()[0], ' From parsed tree: ', tree 
		sys.exit(1)

def parse_math_stmt(tree, num_tabs):
	try:
		label = tree[0]
		if len(tree) == 4:
			first = tree[1]
			op = tree[2]
			second = tree[3]
			if type(first) == list and type(second) == list and \
				len(first) > 0 and len(second) > 0:
				if label == 'math_plus' or label == 'math_minus' or \
					label == 'math_div' or label == 'math_mult':
						first_label = first[0]
						if 'math_' in first[0]:
							first_label = 'math_stmt'
						second_label = second[0]
						if 'math_' in second[0]:
							second_label = 'math_stmt'
						return dir_to_func[first_label](first, num_tabs) + op \
						+ dir_to_func[second_label](second, num_tabs)
			elif label == 'math_paren' and type(op) == list and \
				len(op) > 0:
					mid_label = op[0]
					if 'math_' in op[0]:
						mid_label = 'math_stmt'
					return first + dir_to_func[mid_label](op, num_tabs) + second
		elif len(tree) == 2:
			if label == 'math_int':
				return tree[1]
			elif label == 'math_var':
				return tree[1][1]
		sys.stderr.write('Invalid math statement')
		sys.exit(1)
	except:
		print 'Invalid math statement; Error: ', sys.exc_info()[0], ' From parsed tree: ', tree 
		sys.exit(1)

def parse_variable(tree, num_tabs):
	try:
		if type(tree) is list:
			if tree[0] == 'variable':
				return str(tree[1])
			else:
				return str(tree[0])
		return str(tree)
	except:
		print 'Invalid variable; Error: ', sys.exc_info()[0], ' From parsed tree: ', tree 
		sys.exit(1)

def parse_value(tree, num_tabs):
	try:
		label = tree[0]
		if label in \
		['bool_value', 'user_string', 'variable', 'num', 'time', 'date', \
		'event', 'tag', 'time_math', 'access', 'func', 'str_stmt']:
			return dir_to_func[label](tree[1:], num_tabs)
		if label[0:4] == 'math':
			return dir_to_func['math_stmt'](tree, num_tabs)
		else:
			sys.stderr.write('Error in parse_value: ' + str(tree))
			sys.exit(1)
	except:
		print 'Invalid value; Error: ', sys.exc_info()[0], ' From parsed tree: ', tree 
		sys.exit(1)

def parse_access(tree, num_tabs):
	try:
		code = 'get_event(\'' + dir_to_func['strings'](tree[0][1], num_tabs) + \
			'\', var_all_events)[\'' + tree[1] + '\']'
		return code
	except:
		print 'Invalid access statement; Error: ', sys.exc_info()[0], ' From parsed tree: ', tree 
		sys.exit(1)

def parse_user_string(tree, num_tabs):
	try:
		return tree[0]
	except:
		print 'Invalid user string; Error: ', sys.exc_info()[0], ' From parsed tree: ', tree 
		sys.exit(1)

def parse_print_stmt(tree, num_tabs):
	try:
		tabs = '\t' * num_tabs
		code = ''
		if len(tree) == 2 and len(tree[0]) > 0 and tree[0][0] == 'print' and \
		len(tree[1]) > 0:
			print_item = dir_to_func[tree[1][0]](tree[1][1:], num_tabs)
			str_print_item = print_item
			if len(print_item) < 2 or print_item[0] != '"' or print_item[len(print_item) - 1] != '"':
				str_print_item = '"' + print_item.replace('"', '\\"') + '"'
			str_print_item = str_print_item.replace('\n', '\\n')
			code += tabs + 'printed = False\n' +\
				tabs + 'str_print_item = ' + str_print_item + '\n' +\
				tabs + 'for elem in var_all_events:\n' + \
				tabs + '\tif elem["event_title"] == str_print_item:\n' +\
				tabs + '\t\telem.pop(\'uid\', None)\n' +\
				tabs + '\t\tprint elem\n' +\
				tabs + '\t\tprinted = True\n' + \
				tabs + 'if not printed:\n' +\
				tabs + '\tprint ' + print_item + '\n'
			return code
		else:
			sys.stderr.write('Print statement incorrect')
			sys.exit(1)
	except:
		print 'Invalid print statement; Error: ', sys.exc_info()[0], ' From parsed tree: ', tree 
		sys.exit(1)

def parse_strings(tree, num_tabs):
	try:
		code = ""
		for string in tree:
			if string:
				code += string
		return code
	except:
		print 'Invalid strings; Error: ', sys.exc_info()[0], ' From parsed tree: ', tree 
		sys.exit(1)

def parse_export_stmt(tree, num_tabs):
	try:
		if len(tree) != 2:
			sys.stderr.write('Invalid export')
			sys.exit(1)
		if tree[0][0] != 'export':
			sys.stderr.write('Export not found')
			sys.exit(1)
		if tree[1][0] != 'filename':
			sys.stderr.write('Filename not found')
			sys.exit(1)
		code = 'try:\n\tvar_all_events\nexcept NameError:\n\tpass\nelse:\n'
		code += '\tfor ev in var_all_events:\n'
		code += '\t\te_name = ev[\'event_title\']\n'
		code += '\t\te_to = ev[\'to\']\n'
		code += '\t\te_from = ev[\'from\']\n'
		code += '\t\tif \'at\' in ev:\n'
		code += '\t\t\te_at = ev[\'at\']\n'
		code += '\t\telse:\n'
		code += '\t\t\te_at = \'\'\n'
		code += '\t\tif \'with\' in ev:\n'
		code += '\t\t\te_with = ev[\'with\']\n'
		code += '\t\telse:\n'
		code += '\t\t\te_with = \'\'\n'
		code += '\t\tif \'cancel\' in ev:\n'
		code += '\t\t\te_cancel = True\n'
		code += '\t\telse:\n'
		code += '\t\t\te_cancel = False\n'
		code += '\t\tif \'uid\' in ev:\n'
		code += '\t\t\te_uid = ev[\'uid\']\n'
		code += '\t\telse:\n'
		code += '\t\t\te_uid = None\n'
		code += '\t\tev_event = e.Event(e_name, e_from, e_to, e_at, e_with, e_uid, e_cancel)\n'
		code += '\t\tcal.add_event(ev_event.create_string_event())\n'
		return code + 'cal.write_file(\'' + \
			str(dir_to_func['filename'](tree[1][1:], num_tabs)) + '\')'
	except:
		print 'Invalid export statement; Error: ', sys.exc_info()[0], ' From parsed tree: ', tree 
		sys.exit(1)

def parse_date(tree, num_tabs):
	try:
		month = tree[0][1]
		day = tree[1][1]
		year = tree[2][1]
		if len(month) > 2:
			sys.stderr.write('Month cannot be more than 2 digits')
			sys.exit(1)
		if len(day) > 2:
			sys.stderr.write('Day cannot be more than 2 digits')
			sys.exit(1)
		if len(year) != 4:
			if len(year) == 2:
				year = '20' + year
			else:
				sys.stderr.write('Year cannot be more than 4 digits')
				sys.exit(1)
		return month, day, year
	except:
		print 'Invalid date; Error: ', sys.exc_info()[0], ' From parsed tree: ', tree 
		sys.exit(1)

def parse_event_list(tree, num_tabs, month, day, year):
	try:
		if not tree[0]:
			return ''
		if tree[0][0] != 'event':
			return -1
		if tree[1][0] and tree[1][0] != 'event_list_rep':
			return -1 
		code = dir_to_func['event'](tree[0][1:], num_tabs, month, day, year) + '\n'
		if tree[1][0]:
			code += dir_to_func['event_list_rep'](tree[1][1:], num_tabs, month, \
				day, year)
		return code + '\n' 
	except:
		print 'Invalid event list; Error: ', sys.exc_info()[0], ' From parsed tree: ', tree 
		sys.exit(1)

def parse_event_list_rep(tree, num_tabs, month, day, year=None):
	try:
		if tree and tree[0][0] == 'event_list':
			return dir_to_func['event_list'](tree[0][1:], num_tabs, month, day, \
				year)
		return ''
	except:
		print 'Invalid repetition of event list; Error: ', sys.exc_info()[0], ' From parsed tree: ', tree 
		sys.exit(1)

def parse_event(tree, num_tabs, month, day, year):
	try:
		if tree[0][0] != 'event_title':
			sys.stderr.write('Event title not found')
			sys.exit(1)
		if tree[1][0] != 'when':
			sys.stderr.write('Time not found')
			sys.exit(1)
		if tree[2][0] != 'where':
			sys.stderr.write('Location not found')
			sys.exit(1)
		if tree[3][0] != 'who':
			sys.stderr.write('People list not found')
			sys.exit(1)
		global event_count
		event_initial = 'event_dict' + str(event_count) + ' = {}\n'
		modify_event = dir_to_func['event_title'](tree[0][1:], num_tabs) \
			+ '\n' + dir_to_func['when'](tree[1][1:], num_tabs, month, day, year) \
			+ '\n' 
		if tree[2][1]:
			modify_event += dir_to_func['where'](tree[2][1:], num_tabs) +'\n'
		if tree[3][1]:
			modify_event += dir_to_func['who'](tree[3][1:], num_tabs) + '\n'
		add_event = 'var_all_events.append(event_dict' + str(event_count) + ')\n'
		event_count += 1
		return event_initial + modify_event + add_event 
	except:
		print 'Invalid event; Error: ', sys.exc_info()[0], ' From parsed tree: ', tree 
		sys.exit(1)

def parse_event_title(tree, num_tabs):
	try:
		event_title = tree[0][1]
		global event_count
		return 'event_dict' + str(event_count) + '[\"event_title\"] = ' + '"' + \
		event_title + '"' 
	except:
		print 'Invalid event title; Error: ', sys.exc_info()[0], ' From parsed tree: ', tree 
		sys.exit(1)

def parse_when(tree, num_tabs, month, day, year):
	try:
		if len(tree) != 4:
			sys.stderr.write('Time given invalid')
			sys.exit(1)
		if tree[0][0] != 'from':
			sys.stderr.write('Start time keyword not found')
			sys.exit(1)
		if tree[1][0] != 'time':
			sys.stderr.write('Start time not found')
			sys.exit(1)
		if tree[2][0] != 'to':
			sys.stderr.write('End time keyword not found')
			sys.exit(1)
		if tree[3][0] != 'time':
			sys.stderr.write('End time not found')
			sys.exit(1)
		code = ''
		global event_count
		create_day = 'date' + str(event_count) + ' = ' + \
			'dt.date(' + year + ',' + month + ',' + day + ')'
		hour, minute = dir_to_func['time_elements'](tree[1][1:], num_tabs)
		create_time = 'time' + str(event_count) + ' = ' + \
			'dt.time(' + hour + ',' + minute + ')'
		create_dt = 'from_dt' + str(event_count) + ' = ' + \
			'dt.datetime.combine( date' + str(event_count) + \
			', time' + str(event_count) +  ')'
		add_dt = 'event_dict' + str(event_count) + '[\"from\"] = ' + 'from_dt' + \
		str(event_count) 
		code += create_day + '\n' + create_time + '\n' + \
			create_dt + '\n' + add_dt + '\n'
		meridian1 = getmeridian(tree[1][1:], num_tabs)
		meridian2 = getmeridian(tree[3][1:], num_tabs)
		if meridian1 == 'PM' and meridian2 == 'AM':
			first_day = dt.date(int(float(year)), int(float(month)), \
				int(float(day)))
			first_day += dt.timedelta(days=1)
			year = first_day.year
			month = first_day.month
			day = first_day.day
			create_day = 'date' + str(event_count) + ' = ' + \
			'dt.date(' + year + ',' + month + ',' + day + ')'
		hour, minute = dir_to_func['time_elements'](tree[3][1:], num_tabs)
		create_time = 'time' + str(event_count) + ' = ' + \
			'dt.time(' + hour + ',' + minute + ')'
		create_dt = 'to_dt' + str(event_count) + ' = ' + \
			'dt.datetime.combine( date' + str(event_count) + \
			', time' + str(event_count) +  ')'
		add_dt = 'event_dict' + str(event_count) + '[\"to\"] = ' + 'to_dt' + \
		str(event_count)
		code += create_day + '\n' + create_time + '\n' + \
				create_dt + '\n' + add_dt
		return code
	except:
		print 'Invalid event time; Error: ', sys.exc_info()[0], ' From parsed tree: ', tree 
		sys.exit(1)

def parse_meridian(tree, num_tabs):
	try:
		if len(tree) != 1:
			sys.stderr.write('Invalid meridian')
			sys.exit(1)
		return tree[0]
	except:
		print 'Invalid time meridian; Error: ', sys.exc_info()[0], ' From parsed tree: ', tree 
		sys.exit(1)

def getmeridian(tree, num_tabs):
	try:
		if len(tree) != 4 or tree[3][0] != 'meridian':
			sys.stderr.write('Invalid meridian')
			sys.exit(1)
		return dir_to_func['meridian'](tree[3][1:], num_tabs)
	except:
		print 'Invalid time merdian; Error: ', sys.exc_info()[0], ' From parsed tree: ', tree 
		sys.exit(1)

def parse_time(tree, num_tabs):
	try:
		hour, minute = dir_to_func['time_elements'](tree, num_tabs)
		code = 'dt.time(' + hour + ',' + minute + ')'
		return code
	except:
		print 'Invalid time; Error: ', sys.exc_info()[0], ' From parsed tree: ', tree 
		sys.exit(1)

def parse_time_elements(tree, num_tabs):
	try:
		if len(tree) != 4:
			sys.stderr.write('Invalid time input')
			sys.exit(1)
		hour = tree[0][1]
		minute = tree[2][1]
		if getmeridian(tree, num_tabs) == 'PM' and hour != '12':
			hour = str(int(hour) + 12)
		elif hour == '12' and getmeridian(tree, num_tabs) == 'AM':
			hour = '0'
		return hour, minute
	except:
		print 'Invalid time minute or hour; Error: ', sys.exc_info()[0], ' From parsed tree: ', tree 
		sys.exit(1)
	
def parse_where(tree, num_tabs):
	try:
		if not tree[0]:
			return ''
		if len(tree) != 2 or tree[0][1] != 'at' or tree[1][0] != 'location': 
			sys.stderr.write('Invalid location for event')
			sys.exit(1)
		event_location = dir_to_func['location'](tree[1][1:], num_tabs)
		return 'event_dict' + str(event_count) + '[\"at\"] = \'' + \
		event_location + '\''
	except:
		print 'Invalid location for event; Error: ', sys.exc_info()[0], ' From parsed tree: ', tree 
		sys.exit(1)


def parse_location(tree, num_tabs):
	try:
		if len(tree) != 1:
			sys.stderr.write('Invalid location')
			sys.exit(1)
		return tree[0][1]
	except:
		print 'Invalid location; Error: ', sys.exc_info()[0], ' From parsed tree: ', tree 
		sys.exit(1)

def parse_who(tree, num_tabs):
	try:
		if len(tree) != 2 or tree[0][1] != 'with' or tree[1][0] != 'people_list':
			sys.stderr.write('Invalid who for event')
			sys.exit(1)
		pp_list = 'pp_list' + str(event_count)  + '= []\n' \
		+ dir_to_func['people_list'](tree[1][1:], num_tabs)
		return pp_list
	except:
		print 'Invalid list of people for event; Error: ', sys.exc_info()[0], ' From parsed tree: ', tree 
		sys.exit(1)

def parse_people_list(tree, num_tabs):
	try:
		code = ''
		for branch in tree:
			if branch[0] == 'name':
				code += 'pp_list' + str(event_count) + '.append(\'' + \
					dir_to_func['name'](branch[1], num_tabs) + '\')\n'
			if branch[0] == 'comma':
				code += dir_to_func['comma'](branch[1:], num_tabs)
			if branch[0] == 'and':
				code += 'pp_list' + str(event_count) + '.append(\'' + \
					dir_to_func['name'](branch[2][1], num_tabs) + '\')\n'
		code += 'event_dict' + str(event_count) + '[\"with\"] = pp_list' + \
		str(event_count)
		return code
	except:
		print 'Invalid people list; Error: ', sys.exc_info()[0], ' From parsed tree: ', tree 
		sys.exit(1)

def parse_name(tree, num_tabs):
	try:
		return tree[1]
	except:
		print 'Invalid name; Error: ', sys.exc_info()[0], ' From parsed tree: ', tree 
		sys.exit(1)

def parse_comma(tree, num_tabs):
	try:
		code = ''
		for branch in tree:
			if branch[0] == 'name':
				code += 'pp_list' + str(event_count) + '.append(\'' + \
					dir_to_func['name'](branch[1], num_tabs) + '\')\n'
			if branch[0] == 'comma':
				code += dir_to_func['comma'](branch[1:], num_tabs)
			if branch[0] == 'and':
				code += 'pp_list' + str(event_count) + '.append(\'' + \
					dir_to_func['name'](branch[2][1], num_tabs) + '\')\n'
		return code
	except:
		print 'Invalid comma in repetition of people list; Error: ', sys.exc_info()[0], ' From parsed tree: ', tree 
		sys.exit(1)

def parse_while_stmt(tree, num_tabs):
	try:
		if tree[0] != 'while':
			sys.stderr.write('Invalid while')
			sys.exit(1)
		code = '\t' * num_tabs + 'while '
		if tree[1][0] == 'bool_expr':
			code += dir_to_func['bool_expr'](tree[1][1:], num_tabs) + ":\n"
		if tree[2][0] == 'expr_block':
			code += dir_to_func['expr_block'](tree[2][1:], num_tabs+1)
		return code
	except:
		print 'Invalid while statement; Error: ', sys.exc_info()[0], ' From parsed tree: ', tree 
		sys.exit(1)

def parse_bool_expr(tree, num_tabs):
	try:
		code = ''
		if tree[0]:
			if tree[0][0] == 'bool_operation':
				code += dir_to_func['bool_operation'](tree[0][1:], num_tabs)
			elif tree[0] == 'bool_operation':
				code += dir_to_func['bool_operation'](tree[1:], num_tabs)
			elif tree[0][0] == 'bool_value':
				code += dir_to_func['bool_value'](tree[0][1], num_tabs)
			elif tree[0] == 'bool_value':
				code += dir_to_func['bool_value'](tree[1], num_tabs)
			elif tree[0] == 'not':
				code += 'not ' + dir_to_func['bool_expr'](tree[1][1:], num_tabs)
			elif tree[0][0] == 'bool_expr':
				code += dir_to_func['bool_expr'](tree[0][1], num_tabs) + \
				' ' + dir_to_func['bool_operator'](tree[1][1], num_tabs) +\
				' ' + dir_to_func['bool_expr'](tree[2][1:], num_tabs)
			elif tree[0] == 'bool_expr':
				code += dir_to_func['bool_expr'](tree[1], num_tabs)+ ' ' 
			elif tree[0] == 'value':
				code += dir_to_func['value'](tree[1], num_tabs)
			elif tree[0][0] == 'value':
				code += dir_to_func['value'](tree[0][1], num_tabs)
			elif tree[0] == '(':
				code += '(' + dir_to_func['bool_expr'](tree[1][1:], num_tabs) + ')'
			else:
				sys.stderr.write('Invalid bool expr: ' + str(tree))
				sys.exit(1)
		return code
	except:
		print 'Invalid boolean expression; Error: ', sys.exc_info()[0], ' From parsed tree: ', tree 
		sys.exit(1)

def get_item_code(item, num_tabs):
	return ''

def parse_bool_operation(tree, num_tabs):
	try:
		code = ''
		if tree[1][0] == 'comparison_operator':
			if tree[0][0] == 'value':
				code += dir_to_func['value'](tree[0][1], num_tabs)
			if tree[1][0] == 'comparison_operator':
				code += dir_to_func['comparison_operator'](tree[1][1], num_tabs)
			if tree[2][0] == 'value':
				code += dir_to_func['value'](tree[2][1], num_tabs)
		if tree[1] == 'in':
			if tree[0][0] == 'value':
				code += '\'' + dir_to_func['value'](tree[0][1], num_tabs) + \
				'\' in '
			if tree[2][0] == 'value':
				code += dir_to_func['value'](tree[2][1], num_tabs)
		return code
	except:
		print 'Invalid boolean operation; Error: ', sys.exc_info()[0], ' From parsed tree: ', tree 
		sys.exit(1)

def parse_bool_value(tree, num_tabs):
	try:
		if type(tree) == list:
			return tree[0]
		else:
			return tree
	except:
		print 'Invalid boolean value; Error: ', sys.exc_info()[0], ' From parsed tree: ', tree 
		sys.exit(1)

def parse_comparison_operator(tree, num_tabs):
	return tree

def parse_if_stmt(tree, num_tabs):
	try:
		code = ''
		if len(tree) > 0:
			for item in tree:
				if len(item) > 1:
					code += dir_to_func[item[0]](item[1:], num_tabs)
				else:
					print "Invalid if statement. Error in", item
		return code 
	except:
		print 'Invalid if statement; Error: ', sys.exc_info()[0], ' From parsed tree: ', tree 
		sys.exit(1)

def parse_if_block(tree, num_tabs):
	try:
		if len(tree) == 3 and len(tree[1]) > 1 \
			and tree[1][0] == 'bool_expr' and len(tree[2]) > 1\
			and tree[2][0] == 'expr_block':
			code = '\t' * num_tabs + 'if ' + \
				dir_to_func[tree[1][0]](tree[1][1:], num_tabs) + \
				':\n' + dir_to_func[tree[2][0]](tree[2][1:], num_tabs + 1)
			return code
		else:
			print 'Invalid if block: ', str(tree[1])
		sys.exit(1)
	except:
		print 'Invalid if block; Error: ', sys.exc_info()[0], ' From parsed tree: ', tree 
		sys.exit(1)

def parse_else_block(tree, num_tabs):
	try:
		if not tree[0]:
			return ''
		if len(tree) == 2 and tree[1][0] == 'expr_block':
			return '\t' * num_tabs + 'else:\n' + \
			dir_to_func[tree[1][0]](tree[1][1:], num_tabs + 1)
		print 'Invalid else block: ', str(tree)
		sys.exit(1)
	except:
		print 'Invalid else block, Error: ', sys.exc_info()[0], ' From parsed tree: ', tree 
		sys.exit(1)
	
def parse_elseif_blocks(tree, num_tabs):
	try:
		if not tree[0]:
			return ''
		if len(tree) == 2 and len(tree[0]) > 1 and len(tree[1]) > 1 and \
			tree[0][0] == 'elseif_block' and tree[1][0] == 'elseif_blocks_rep':
			return dir_to_func[tree[0][0]](tree[0][1:], num_tabs) + \
				dir_to_func[tree[1][0]](tree[1][1:], num_tabs)
		print 'Invalid elseif blocks: ', str(tree)
		sys.exit(1)
	except:
		print 'Invalid elseif block; Error: ', sys.exc_info()[0], ' From parsed tree: ', tree 
		sys.exit(1)
			
def parse_elseif_block(tree, num_tabs):
	try:
		if not tree[0]:
			return ''
		if len(tree) == 3 and len(tree[1]) > 1 and len(tree[2]) > 1\
			and tree[1][0] == 'bool_expr' and tree[2][0] == 'expr_block':
			return '\t' * num_tabs + 'elif ' + \
				dir_to_func[tree[1][0]](tree[1][1:], num_tabs) + \
				':\n' + dir_to_func[tree[2][0]](tree[2][1:], num_tabs + 1)
		print 'Invalid elseif block: ', str(tree)
		sys.exit(1)
	except:
		print 'Invalid elseif block; Error: ', sys.exc_info()[0], ' From parsed tree: ', tree 
		sys.exit(1)

def parse_elseif_blocks_rep(tree, num_tabs):
	try:
		if not tree[0]:
			return ''
		if len(tree) == 1 and len(tree[0]) > 1 and tree[0][0] == 'elseif_blocks':
			return dir_to_func[tree[0][0]](tree[0][1:], num_tabs)
		print 'Invalid repetition of else if: ', str(tree)
		sys.exit(1)
	except:
		print 'Invalid repetition of else if; Error: ', sys.exc_info()[0], ' From parsed tree: ', tree 
		sys.exit(1)

def parse_for_stmt(tree, num_tabs):
	try:
		if tree[0] != 'for':
			return -1
		code = ''
		if tree[1][0] == 'assignment_stmt':
			code += dir_to_func['assignment_stmt'](tree[1][1:], num_tabs) + '\n'
		if tree[2][0] == 'bool_expr':
			code += '\t'*num_tabs + 'while ' + dir_to_func['bool_expr'](tree[2][1:], num_tabs) \
			+ ':\n'
		if tree[3][0] == 'assignment_stmt':
			increment = dir_to_func['assignment_stmt'](tree[3][1:], num_tabs+1)
		if tree[4][0] == 'expr_block':
			code += dir_to_func['expr_block'](tree[4][1:], num_tabs+1)
		code += increment
		return code
	except:
		print 'Invalid for statement; Error: ', sys.exc_info()[0], ' From parsed tree: ', tree 
		sys.exit(1)

def parse_bool_operator(tree, num_tabs):
	return tree
	
def parse_comment_stmt(tree, num_tabs):
	return ''

def parse_num(tree, num_tabs):
	try:
		return tree[0]
	except:
		print 'Invalid number; Error: ', sys.exc_info()[0], ' From parsed tree: ', tree 
		sys.exit(1)

def parse_newline(tree, num_tabs):
	return '\n'

def parse_str_stmt(tree, num_tabs):
	try:
		code = ''
		for item in tree:
			if item:
				code += dir_to_func[item[0]](item[1:], num_tabs) + " + "
		return code[:len(code) - 3]
	except:
		print 'Invalid concatenation of strings; Error: ', sys.exc_info()[0], ' From parsed tree: ', tree 
		sys.exit(1)

def parse_plan_stmt(tree, num_tabs):
	try:
		code = ''
		if len(tree) == 2 and tree[0][0] == 'date':
			month, day, year = dir_to_func['date'](tree[0][1:], num_tabs)
			tabs = '\t' * num_tabs
			code = tabs + dir_to_func['event'](tree[1][1:], num_tabs, month, day, year)
			code = code.replace('\n', '\n' + tabs)
			return code
		sys.stderr.write('Invalid plan statement')
		sys.exit(1)
	except:
		print 'Invalid plan statement; Error: ', sys.exc_info()[0], ' From parsed tree: ', tree 
		sys.exit(1)

def parse_string(tree, num_tabs):
	try:
		return tree[0]
	except:
		print 'Invalid string; Error: ', sys.exc_info()[0], ' From parsed tree: ', tree 
		sys.exit(1)


def parse_colon(tree, num_tabs):
	return ':'

#No translations required! :)
def parse_date_duration(tree, num_tabs):
	pass

def parse_date_unit(tree, num_tabs):
	pass

def parse_string_rep(tree, num_tabs):
	pass

def parse_at(tree, num_tabs):
	pass

def parse_print(tree, num_tabs):
	pass

def parse_type(tree, num_tabs):
	pass

def parse_import(tree, num_tabs):
	pass

def parse_export(tree, num_tabs):
	pass

def parse_and(tree, num_tabs):
	pass

def parse_year(tree, num_tabs):
	pass

def parse_from(tree, num_tabs):
	pass

def parse_to(tree, num_tabs):
	pass

def parse_with(tree, num_tabs):
	pass

def parse_build(tree, num_tabs):
	pass

def parse_schedule(tree, num_tabs):
	pass



dir_to_func = {
	'program' : parse_program,
	'function_block' : parse_function_block,
	'function_blocks' : parse_function_blocks,
	'import_stmt' : parse_import_stmt,
	'schedule_stmts' : parse_schedule_stmts,
	'date' : parse_date,
	'event_list' : parse_event_list,
	'event' : parse_event,
	'when' : parse_when,
	'time' : parse_time,
	'time_elements' : parse_time_elements,
	'where' : parse_where,
	'who' : parse_who,
	'people_list' : parse_people_list,
	'comma' : parse_comma,
	'build_schedule' : parse_build_schedule,
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
	'expr_block_rep' : parse_expr_block_rep,
	'expr' : parse_expr,
	'event_stmt' : parse_event_stmt,
	'value' : parse_value,
	'variable' : parse_variable,
	'bool_operator' : parse_bool_operator,
	'comparison_operator' : parse_comparison_operator,
	'bool_value' : parse_bool_value,
	'op' : parse_op,
	'time_unit' : parse_time_unit,
	'filename' : parse_filename,
	'and' : parse_and,
	'comma' : parse_comma,
	'num' : parse_num,
	'meridian' : parse_meridian,
	'newline' : parse_newline,
	'assignment_stmt' : parse_assignment_stmt,
	'update_stmt' : parse_update_stmt,
	'remove_stmt' : parse_remove_stmt,
	'func' : parse_func,
	'elseif_blocks_rep' : parse_elseif_blocks_rep,
	'access' : parse_access,
	'user_string' : parse_user_string,
	'str_stmt' : parse_str_stmt,
	'plan_stmt' : parse_plan_stmt,
	'date_duration' : parse_date_duration,
	'date_unit' : parse_date_unit,
	'string' : parse_string,
	'string_rep' : parse_string_rep,
	'at' : parse_at,
	'print' : parse_print,
	'type' : parse_type,
	'colon' : parse_colon,
	'import' : parse_import,
	'export' : parse_export,
	'and' : parse_and,
	'year' : parse_year,
	'from' : parse_from,
	'to' : parse_to,
	'with' : parse_with,
	'build' : parse_build,
	'schedule' : parse_schedule,
}

