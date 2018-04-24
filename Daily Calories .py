import ui, appex, os, json, console
from copy import deepcopy

fields = {
	'f1':{'state':'inactive', 'num': 330},
	'f2':{'state':'inactive', 'num': 250},
	'f3':{'state':'inactive', 'num': 350},
	'f4':{'state':'inactive', 'num': 250},
	'f5':{'state':'inactive', 'num': 350},
	'f6':{'state':'inactive', 'num': 250},
	'f7':{'state':'inactive', 'num': 250},
}

totals = {
	'eaten':0,
	'total':2030,
}

fields_default = deepcopy(fields)
totals_default = deepcopy(totals)

def reset(sender):
	for i in totals:
			v[i].text = str(totals[i])
			v[i].text = str(totals[i])
	for f in fields:
			sender.superview[f].state = 'inactive'
			#fields_default[f]['state']
			sender.superview[f].title = str(fields_default[f]['num'])
			sender.superview[f].tint_color = (0, 0, 0, 1)
			sender.superview[f].image = None
			#save totals dict to file
			with open('.totals.txt', 'w') as f_totals:
				json.dump(totals, f_totals)
			#save fields dict to file
			with open('.fields.txt', 'w') as f_fields:
				json.dump(fields, f_fields)
		
def toggle_field(sender):
	
	eaten = sender.superview['eaten']
	
	def activate():
		sender.tint_color = (0, 0, 255, 1)
		for f in fields:
			if fields[f]['state'] == 'active':
				fields[f]['state'] = 'inactive'
			if sender.superview[f].state == 'active':
				sender.superview[f].state = 'inactive'
				sender.superview[f].tint_color = (0, 0, 0, 1)
		sender.state = 'active'
		fields[sender.name]['state'] = 'active'
		#save fields dict to file
		with open('.fields.txt', 'w') as f:
			json.dump(fields, f)
		
	def deactivate():
		sender.tint_color = (0, 0, 0, 1)
		sender.image = None
		sender.state = 'inactive'
		fields[sender.name]['state'] = 'inactive'
		eaten.text = str(int(eaten.text) - int(sender.title))
		#update totals dict with eaten
		totals['eaten'] = int(eaten.text)
		#save totals dict to file
		with open('.totals.txt', 'w') as f_totals:
			json.dump(totals, f_totals)
		#save fields dict to file
		with open('.fields.txt', 'w') as f_fields:
			json.dump(fields, f_fields)
		
	def lock():
		sender.tint_color = (0, 0, 0, 1)
		sender.image = ui.Image('iob:ios7_locked_24')
		sender.state = 'locked'
		fields[sender.name]['state'] = 'locked'
		eaten.text = str(int(sender.title) + int(eaten.text))
		#update totals dict with eaten
		totals['eaten'] = int(eaten.text)
		#save totals dict to file
		with open('.totals.txt', 'w') as f_totals:
			json.dump(totals, f_totals)
		#save fields dict to file
		with open('.fields.txt', 'w') as f_fields:
			json.dump(fields, f_fields)
		
	if sender.state == 'inactive':
		activate()
	elif sender.state == 'active':
		lock() 
	elif sender.state == 'locked':
		deactivate()


def button_tapped(sender):
	
	total = sender.superview['total']
	eaten = sender.superview['eaten']
	active_dict = ''
	active = ''
	
	for f in fields:
		if fields[f]['state'] == 'active':
			active_dict = fields[f]
		if sender.superview[f].state == 'active':
			active = sender.superview[f]
				
	def maths(title):
		symbol = title[0:1]
		number = int(title[1:4])
		if symbol =='+':
			#update number on button 
			active.title = str(int(active.title) + number)
			#update daily total label
			total.text = str(int(total.text) + number)
			#update field dict number 
			active_dict['num'] = (int(active_dict['num']) + number)
			#update totals dict
			totals['total'] = (totals['total'] + number)
			#save totals dict to file
			with open('.totals.txt', 'w') as f_totals:
				json.dump(totals, f_totals)
			#save fields dict to file
			with open('.fields.txt', 'w') as f_fields:
				json.dump(fields, f_fields)
			
		elif symbol == '-':
			#update field number 
			active.title = str(int(active.title) - number)
			#update total
			total.text = str(int(total.text) - number)
			#update field dict number
			active_dict['num'] = (int(active_dict['num']) - number)
			#update totals dict
			totals['total'] = (totals['total'] - number)
			#save totals dict to file
			with open('.totals.txt', 'w') as f_totals:
				json.dump(totals, f_totals)
			#save fields dict to file
			with open('.fields.txt', 'w') as f_fields:
				json.dump(fields, f_fields)
	
	try:
		maths(sender.title)
	except AttributeError:
		pass
	except TypeError:
		pass


v = ui.load_view()

appex.set_widget_view(v)


def restoreState():
	
	with open('.totals.txt') as f_totals:
		totals = json.load(f_totals)
		
		for i in totals:
			v[i].text = str(totals[i])
			v[i].text = str(totals[i])
	
	with open('.fields.txt') as f_fields:
		fields = json.load(f_fields)
	
	for f in fields:
		v[f].state = fields[f]['state']
		if v[f].state == 'inactive':
			v[f].tint_color = (0, 0, 0, 1)
			v[f].image = None
		elif v[f].state == 'active':
			v[f].tint_color = (0, 0, 255, 1)
		elif v[f].state == 'locked':
			v[f].tint_color = (0, 0, 0, 1)
			v[f].image = ui.Image('iob:ios7_locked_24')
			v[f].title = str(fields[f]['num'])
			
restoreState()
