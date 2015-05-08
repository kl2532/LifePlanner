import yacc
import sys
import datetime as dt
event_count = 0
all_events = []

def translate(tree):
	if tree[0] != 'program':
		sys.stderr.write('Invalid program')
		sys.exit(1)
	return 'import datetime as dt\nimport time\nimport event as e\nimport ourCalendar as c\nfrom dateutil import tz\n' + \
		'\ndef get_event(name, var_all_events):\n' + \
		'\tfor event in var_all_events:\n' + \
		'\t\tif event[\'event_title\'] == name:\n' + \
		'\t\t\treturn event\n\n' + \
		'cal = c.ourCalendar()\n\n' + \
		dir_to_func['program'](tree[1:], 0)

def parse_program(tree, num_tabs):
	#print "parse_program tree: ", str(tree)
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

def parse_function_block(tree, num_tabs):
	pass

def parse_function_declaration(tree, num_tabs):
	code = ''
	i = 0
	while i < num_tabs:
		code += '\t'
		i += 1
	code += 'def ' + dir_to_func['variable'](tree[0][1], num_tabs) + '('
	params = dir_to_func['parameter_list'](tree[1], num_tabs)
	x = params.split()
	params = x[0]
	for i in range(1, len(x)):
		params += ', ' + x[i]
	code += params + '):\n'
	return code

def parse_import_stmt(tree, num_tabs):
	code = 'orig_event_dict = cal.readCalendar(\'' + str(dir_to_func['filename'](tree[1][1:], num_tabs)) + '\')\n'
	code += 'for orig_e in orig_event_dict:\n'
	code += '\te_name = orig_e[\'event_title\']\n'
	code += '\te_to = orig_e[\'to\']\n'
	code += '\te_from = orig_e[\'from\']\n'
	code += '\te_at = orig_e[\'at\']\n'
	code += '\te_with = orig_e[\'with\']\n'
	code += '\torig_event = e.Event(e_name, e_from, e_to, e_at, e_with)\n'
	code += '\tcal.addEvent(orig_event.create_string_event())\n'
	return code

def parse_filename(tree, num_tabs):
	return tree[0][1]

def parse_schedule_stmts(tree, num_tabs):
	# print "\nparse_schedule_stmts tree: ", str(tree)
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
	print 'parse_expr tree: ', str(tree)
	code = ''
	#done
	if tree[0][0] == 'print_stmt':
		code += dir_to_func['print_stmt'](tree[0][1:], num_tabs) + '\n'
	#done
	if tree[0][0] == 'if_stmt':
		code += dir_to_func['if_stmt'](tree[0][1:], num_tabs) + '\n'
	#done
	if tree[0][0] == 'while_stmt':
		code += dir_to_func['while_stmt'](tree[0][1:], num_tabs) + '\n'
	if tree[0][0] == 'for_stmt':
		code += dir_to_func['for_stmt'](tree[0][1:], num_tabs) + '\n'
	#done
	if tree[0][0] == 'event_stmt':
		code += dir_to_func['event_stmt'](tree[0][1:], num_tabs) + '\n'
	#done
	if tree[0][0] == 'comment_stmt':
		code += dir_to_func['comment_stmt'](tree[0][1:], num_tabs)
	#done
	if tree[0][0] == 'assignment_stmt':
		code += dir_to_func['assignment_stmt'](tree[0][1:], num_tabs) + '\n'
	#done
	if tree[0][0] == 'math_stmt':
		code += dir_to_func['math_stmt'](tree[0][1:], num_tabs) + '\n'
	#done
	if tree[0][0] == 'time_math':
		code += dir_to_func['time_math'](tree[0][1:], num_tabs) + '\n'
	if tree[0][0] == 'day_math':
		code += dir_to_func['day_math'](tree[0][1:], num_tabs) + '\n'
	#done
	if tree[0][0] == 'func':
		code += dir_to_func['func'](tree[0][1:], num_tabs) + '\n'
	if tree[0][0] == 'time_range':
		code += dir_to_func['time_range'](tree[0][1:], num_tabs) + '\n'
	return code

def parse_func(tree, num_tabs):
	code = ''
	i = 0
	while i < num_tabs:
		code += '\t'
		i += 1
	code += dir_to_func['variable'](tree[0][1], num_tabs) + '('
	params = dir_to_func['parameter_list'](tree[1], num_tabs)
	x = params.split()
	params = x[0]
	for i in range(1, len(x)):
		params += ', ' + x[i]
	code += params + ')\n'
	return code

def parse_parameter_list(tree, num_tabs):
	print '\nparams: ' + str(tree)
	#['parameter_list', 'a', ['parameter_list', 'b', ['parameter_list', 'c', ['parameter_list', 'd', ['parameter_list', 'e', ['parameter_list', None]]]]]]
	params = ''
	if tree[1]:
		params += tree[1]
		return params + ' ' + parse_parameter_list(tree[2], num_tabs)
	return ''
# import datetime
# from datetime import timedelta
# datetime.datetime(2015, 5, 7) + timedelta(days= 3)
# datetime.datetime(2015, 5, 7, 2, 0) + timedelta(hours= 2)

def parse_day_math(tree, num_tabs):
	pass

def parse_time_math(tree, num_tabs):
	print 'parse_time_math: ', str(tree)
	code = ''
	if tree[0][0] == 'time':
		hour, minute = dir_to_func['time_elements'](tree[0][1:], num_tabs)
		code += 'dt.datetime.combine(dt.date.today(), dt.time(' + hour + ',' + minute + '))'
	if tree[1][0] == 'op':
		code += dir_to_func['op'](tree[1][1:], num_tabs)
	if tree[2][0] == 'time_duration':
		code += dir_to_func['time_duration'](tree[2][1:], num_tabs)
	return '(' + code + ').time()'

def parse_time_duration(tree, num_tabs):
	if tree[0][0] == 'num':
		num = dir_to_func['num'](tree[0][1:], num_tabs)
	if tree[1][0] == 'time_unit':
		unit = dir_to_func['time_unit'](tree[1][1:], num_tabs)
	return 'dt.timedelta(' + unit + '=' + num + ')'

def parse_time_unit(tree, num_tabs):
	return tree[0]

def parse_op(tree, num_tabs):
	return tree[0]

def parse_event_stmt(tree, num_tabs):
	print "parse_event_stmt: ", str(tree)
	if tree[0][0] == 'cancel_stmt':
		return dir_to_func['cancel_stmt'](tree[0][1:], num_tabs)
	if tree[0][0] == 'update_stmt':
		return dir_to_func['update_stmt'](tree[0][1:], num_tabs)
	if tree[0][0] == 'add_stmt':
		return dir_to_func['add_stmt'](tree[0][1:], num_tabs)
	if tree[0][0] == 'remove_stmt':
		return dir_to_func['remove_stmt'](tree[0][1:], num_tabs)
	return 'event_stmt'

def parse_remove_stmt(tree, num_tabs):
	tabs = ''
	i = 0
	while i < num_tabs:
		tabs += '\t'
		i += 1
	code = tabs + 'for event in var_all_events:\n\t' + \
	tabs + 'if event[\'event_title\'] == \'' + dir_to_func['strings'](tree[1][1], num_tabs) + '\':\n\t\t' + \
	tabs + 'event[\'with\'].remove(\''+dir_to_func['strings'](tree[0][1], num_tabs)+'\')'
	return code

def parse_add_stmt(tree, num_tabs):
	tabs = ''
	i = 0
	while i < num_tabs:
		tabs += '\t'
		i += 1
	code = tabs + 'for event in var_all_events:\n\t' + \
	tabs + 'if event[\'event_title\'] == \'' + dir_to_func['strings'](tree[1][1], num_tabs) + '\':\n\t\t' + \
	tabs + 'event[\'with\'].append(\''+dir_to_func['strings'](tree[0][1], num_tabs)+'\')'
	return code

def parse_update_stmt(tree, num_tabs):
	tabs = ''
	i = 0
	while i < num_tabs:
		tabs += '\t'
		i += 1
	code = tabs + 'for event in var_all_events:\n\t' + \
	tabs + 'if event[\'event_title\'] == \'' + dir_to_func['strings'](tree[0][1], num_tabs) + '\':\n\t\t'
	
	if tree[1] == 'from' or tree[1] == 'to':
		code += tabs + 'date = str(event[\''+ tree[1]+'\'].date())\n\t\t'
		code += tabs + 'time = ' + dir_to_func['variable'](tree[2][1], num_tabs) + '\n\t\t'
		code += tabs + 'new_when = date + \' \' + time\n\t\t'
		code += tabs + 'event[\''+tree[1]+'\'] = dt.datetime.strptime(new_when, \'%m-%d-%Y %I:%M %p\')\n'
	if tree[1] == 'at':
		code += tabs + 'event[\'' + tree[1] + '\'] = ' + dir_to_func['variable'](tree[2][1], num_tabs)
	return code

def parse_cancel_stmt(tree, num_tabs):
	tabs = ''
	j = 0
	while(j < num_tabs):
		tabs = '\t'
		j += 1
	code = tabs + 'for i in range(len(var_all_events)):\n\t' + tabs + \
	'event = var_all_events[i]\n\t' + tabs + \
	'if event[\'event_title\'] == \'' + dir_to_func['strings'](tree[1][1], num_tabs) + '\':\n\t\t' + tabs + \
	'var_all_events.pop(i)'

	return code

def parse_assignment_stmt(tree, num_tabs):
	code = ''
	i = 0
	while i < num_tabs:
		code += '\t'
		i += 1
	if tree[0][0] == 'variable':
		code += dir_to_func['variable'](tree[0][1], num_tabs) + ' = '
	if tree[2][0] == 'value':
		code += dir_to_func['value'](tree[2][1], num_tabs)
	return code

def parse_math_stmt(tree, num_tabs):
	print 'math tree: ', tree
	label = tree[0]
	if len(tree) == 4:
		first = tree[1]
		op = tree[2]
		second = tree[3]
		if type(first) == list and type(second) == list and \
			len(first) > 0 and len(second) > 0:
			if label == 'math_plus' or label == 'math_minus' or\
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
	print 'Invalid Math Stmt: ', tree
	return -1

def parse_variable(tree, num_tabs):
	if type(tree) is list:
		return str(tree[1])
	return str(tree)

def parse_value(tree, num_tabs):
	print 'parse_value tree: ' + str(tree)
	label = tree[0]
	if label in \
	['variable', 'num', 'time', 'date', 'event', 'tag', 'time_math', 'access']:
		return dir_to_func[label](tree[1:], num_tabs)
	if 'math_' in label:
		return dir_to_func['math_stmt'](tree[:], num_tabs)
	else:
		return 'in parse_value'

def parse_access(tree, num_tabs):
	print '\nparse_access: ' + str(tree)
	code = 'get_event(\'' + dir_to_func['strings'](tree[0][1], num_tabs) + '\', var_all_events)[\'' + tree[1] + '\']'
	return code

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
	code = 'try:\n\tevent_dict\nexcept NameError:\n\tpass\nelse:\n'
	code += '\tfor ev in event_dict:\n'
	code += '\t\te_name = ev[\'event_title\']\n'
	code += '\t\te_to = ev[\'to\']\n'
	code += '\t\te_from = ev[\'from\']\n'
	code += '\t\te_at = ev[\'at\']\n'
	code += '\t\te_with = ev[\'with\']\n'
	code += '\t\tev_event = e.Event(e_name, e_from, e_to, e_at, e_with)\n'
	code += '\t\tcal.addEvent(ev_event.create_string_event())\n'
	return \
	code + 'cal.write_file(\'' + str(dir_to_func['filename'](tree[1][1:], num_tabs)) + '\')'

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
	hour, minute = dir_to_func['time_elements'](tree[1][1:], num_tabs)
	create_time = 'time' + str(event_count) + ' = ' + \
		'dt.time(' + hour + ',' + minute + ')'
	create_dt = 'from_dt' + str(event_count) + ' = ' + \
		'dt.datetime.combine( date' + str(event_count) + \
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
	hour, minute = dir_to_func['time_elements'](tree[3][1:], num_tabs)
	create_time = 'time' + str(event_count) + ' = ' + \
		'dt.time(' + hour + ',' + minute + ')'
	create_dt = 'to_dt' + str(event_count) + ' = ' + \
		'dt.datetime.combine( date' + str(event_count) + \
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
	# print 'getmeridian: ', str(tree)
	if len(tree) != 4 or tree[3][0] != 'meridian':
		return -1 
	return dir_to_func['meridian'](tree[3][1:], num_tabs)

def parse_time(tree, num_tabs):
	# print 'parse_time: ', str(tree)
	hour, minute = dir_to_func['time_elements'](tree, num_tabs)
	code = 'dt.time(' + hour + ',' + minute + ')'
	return code

def parse_time_elements(tree, num_tabs):
	# print "parse_time_elements: ", str(tree)
	if len(tree) != 4:
		sys.stderr.write('Invalid time input')
		sys.exit(1)
	hour = tree[0][1]
	minute = tree[2][1]
	print hour, minute
	if getmeridian(tree, num_tabs) == 'PM':
		hour = str(int(hour) + 12)
	return hour, minute
	
def parse_where(tree, num_tabs):
	if not tree[0]:
		return ''
	if len(tree) != 2 or tree[0][1] != 'at' or tree[1][0] != 'location': 
		sys.stderr.write('Invalid location for event')
		sys.exit(1)
	event_location = dir_to_func['location'](tree[1][1:], num_tabs)
	return 'event_dict' + str(event_count) + '[\"at\"] = ' + event_location


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
			code += 'pp_list' + str(event_count) + '.append(\'' + dir_to_func['name'](branch[1], num_tabs) + '\')\n'
		if branch[0] == 'comma':
			code += dir_to_func['comma'](branch[1:], num_tabs)
		if branch[0] == 'and':
			code += 'pp_list' + str(event_count) + '.append(\'' + dir_to_func['name'](branch[2][1], num_tabs) + '\')\n'
	code += 'event_dict' + str(event_count) + '[\"with\"] = pp_list' + str(event_count)
	return code

def parse_name(tree, num_tabs):
	return tree[1]

def parse_comma(tree, num_tabs):
	code = ''
	for branch in tree:
		if branch[0] == 'name':
			code += 'pp_list' + str(event_count) + '.append(\'' + dir_to_func['name'](branch[1], num_tabs) + '\')\n'
		if branch[0] == 'comma':
			code += dir_to_func['comma'](branch[1:], num_tabs)
		if branch[0] == 'and':
			code += 'pp_list' + str(event_count) + '.append(\'' + dir_to_func['name'](branch[2][1], num_tabs) + '\')\n'
	return code

def parse_while_stmt(tree, num_tabs):
	# print "parse_while_stmt: ", str(tree)
	if tree[0] != 'while':
		return -1
	code = 'while '
	if tree[1][0] == 'bool_expr':
		code += dir_to_func['bool_expr'](tree[1][1:], num_tabs) + ":\n"
	if tree[2][0] == 'expr_block':
		code += dir_to_func['expr_block'](tree[2][1:], num_tabs+1)
	return code

def parse_bool_expr(tree, num_tabs):
	print '\nparse_bool_expr: ', str(tree)
	code = ''
	if tree[0]:
		if tree[0][0] == 'bool_operation':
			code += dir_to_func['bool_operation'](tree[0][1:], num_tabs)
		if tree[0] == 'bool_operation':
			code += dir_to_func['bool_operation'](tree[1:], num_tabs)
		if tree[0][0] == 'bool_value':
			code += dir_to_func['bool_value'](tree[0][1], num_tabs)
		if tree[0] == 'bool_value':
			code += dir_to_func['bool_value'](tree[1], num_tabs)
		if tree[0] == 'not':
			code += 'not ' + dir_to_func['bool_expr'](tree[1][1], num_tabs)
		if tree[0][0] == 'bool_expr':
			code += dir_to_func['bool_expr'](tree[0][1], num_tabs) + ' ' + dir_to_func['bool_operator'](tree[1][1], num_tabs) + ' ' + dir_to_func['bool_expr'](tree[2][1], num_tabs)
	return code

def parse_bool_operation(tree, num_tabs):
	print 'parse_bool_operation: ', str(tree)
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
			code += '\'' + dir_to_func['value'](tree[0][1], num_tabs) + '\' in '
		if tree[2][0] == 'value':
			code += dir_to_func['value'](tree[2][1], num_tabs)
	return code

def parse_bool_value(tree, num_tabs):
	return tree

def parse_comparison_operator(tree, num_tabs):
	# print 'parse_comparison_operator: ', str(tree)
	return tree

def parse_if_stmt(tree, num_tabs):
	code = ''
	if len(tree) > 0:
		for item in tree:
			if len(item) > 1:
				#print '\nitem: ', item
				#print '\nitem[1:], ', item[1:]
				code += dir_to_func[item[0]](item[1:], num_tabs)
			else:
				print "error in ", item
	return code 

def parse_if_block(tree, num_tabs):
	print '\n if_block: ' + str(tree)
	if len(tree) == 3 and len(tree[1]) > 1 \
		and tree[1][0] == 'bool_expr' and len(tree[2]) > 1\
		and tree[2][0] == 'expr_block':
		code = 'if ' + dir_to_func[tree[1][0]](tree[1][1:], num_tabs) \
			+ ':\n' + dir_to_func[tree[2][0]](tree[2][1:], num_tabs + 1)
		return code
	else:
		print 'error in if statement: ', tree[1]
	return -1

def parse_else_block(tree, num_tabs):
	if not tree[0]:
		return ''
	print 'else: ', tree
	if len(tree) == 2 and tree[1][0] == 'expr_block':
		return 'else:\n' + dir_to_func[tree[1][0]](tree[1][1:], num_tabs + 1)
	return -1
	
def parse_elseif_blocks(tree, num_tabs):
	print 'else if blocks tree: ', tree
	if not tree[0]:
		return ''
	if len(tree) == 2 and len(tree[0]) > 1 and len(tree[1]) > 1\
		and tree[0][0] == 'elseif_block' and tree[1][0] == 'elseif_blocks_rep':
		return dir_to_func[tree[0][0]](tree[0][1:], num_tabs) + \
			dir_to_func[tree[1][0]](tree[1][1:], num_tabs)
	print 'error in elseif blocks'
	return -1
		
def parse_elseif_block(tree, num_tabs):
	print 'else if tree: ', tree
	if not tree[0]:
		return ''
	if len(tree) == 3 and len(tree[1]) > 1 and len(tree[2]) > 1\
		and tree[1][0] == 'bool_expr' and tree[2][0] == 'expr_block':
		return 'elif ' + dir_to_func[tree[1][0]](tree[1][1:], num_tabs) + \
			':\n' + dir_to_func[tree[2][0]](tree[2][1:], num_tabs + 1)
	print 'error in elseif block'
	return -1

def parse_elseif_blocks_rep(tree, num_tabs):
	print 'elseif rep tree: ', tree
	if not tree[0]:
		return ''
	if len(tree) == 1 and len(tree[0]) > 1 and tree[0][0] == 'elseif_blocks':
		return dir_to_func[tree[0][0]](tree[0][1:], num_tabs)
	print 'error in else if rep'
	return -1

def parse_tag_line(tree, num_tabs):
	return ''

def parse_for_stmt(tree, num_tabs):
	print 'parse_for_stmt: ', str(tree)
	# ['for', 
	# ['assignment_stmt', ['variable', 'i'], '=', ['value', ['math_int', '0']]], 
	# ['bool_expr', ['bool_operation', ['value', ['math_var', ['variable', 'i']]], ['comparison_operator', '<'], ['value', ['math_int', '3']]]], 
	# ['assignment_stmt', ['variable', 'i'], '=', ['value', ['math_plus', ['math_var', ['variable', 'i']], '+', ['math_int', '1']]]], 
	# ['expr_block', ['expr', ['print_stmt', ['print', 'print'], ['quote', '"'], ['strings', 'hello'], ['quote', '"']]], ['expr_block_rep', ['expr_block', None]]]
	# ]
	if tree[0] != 'for':
		return -1
	code = ''
	if tree[1][0] == 'assignment_stmt':
		code += dir_to_func['assignment_stmt'](tree[1][1:], num_tabs) + '\n'
	if tree[2][0] == 'bool_expr':
		code += 'while ' + dir_to_func['bool_expr'](tree[2][1:], num_tabs) + ':\n'
	if tree[3][0] == 'assignment_stmt':
		increment = dir_to_func['assignment_stmt'](tree[3][1:], num_tabs+1)
	if tree[4][0] == 'expr_block':
		code += dir_to_func['expr_block'](tree[4][1:], num_tabs+1)
	code += increment
	return code
	
def parse_date_duration(tree, num_tabs):
	pass
			
def parse_return_stmt(tree, num_tabs):
	pass
	
def parse_and(tree, num_tabs):
	pass

# def parse_year(tree, num_tabs):
# 	pass
		
def parse_tag_priorities(tree, num_tabs):
	return 'tag priorities'
	
def parse_comment_stmt(tree, num_tabs):
	return ''
	
def parse_function_declaration(tree, num_tabs):
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

def parse_import(tree, num_tabs):
	pass

def parse_bool_operator(tree, num_tabs):
	return tree

def parse_with(tree, num_tabs):
	pass

def parse_date_unit(tree, num_tabs):
	pass

def parse_string_rep(tree, num_tabs):
	pass

def parse_schedule(tree, num_tabs):
	pass

def parse_num(tree, num_tabs):
	return tree[0]

def parse_to(tree, num_tabs):
	pass

def parse_tag_name(tree, num_tabs):
	pass

def parse_print(tree, num_tabs):
	pass

def parse_at(tree, num_tabs):
	pass

def parse_type(tree, num_tabs):
	pass

dir_to_func = {
	'program' : parse_program,
	'function_block' : parse_function_block,
	'function_blocks' : parse_function_blocks,
	'import_stmt' : parse_import_stmt,
	'schedule_stmts' : parse_schedule_stmts,
	'date' : parse_date,
	#'year' : parse_year,
	'event_list' : parse_event_list,
	'event' : parse_event,
	'when' : parse_when,
	'time' : parse_time,
	'time_elements' : parse_time_elements,
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
	'update_stmt' : parse_update_stmt,
	'remove_stmt' : parse_remove_stmt,
	'function' : parse_func,
	'elseif_blocks_rep' : parse_elseif_blocks_rep,
	'access' : parse_access
}

