from memory_handler import *
from light_datastructures import *
from quadruple import *
from figures import *

win = None #GraphWin("LIGHT", 500, 500)
fig_dict = {}

def execute_operator(argument, quad, index):

	switcher = {
		0	: 	plus,
		1	: 	minus,
		2	: 	times,
		3	:	over,
		4	:	lessThan,
		5	:	greaterThan,
		6	:	lessEqThan,
		7	: 	greaterEqThan,
		8	:	equals,
		9	:	notEqual,
		10	:	_and,
		11	:	_or,
		14	:	equal,
		15	:	gotof,
		16	:	gotot,
		17	:	goto,
		18	:	ret,
		19	:	_return,
		20	:	gosub,
		21	:	era,
		22	:	param,
		23	:	_print,
		24	:	end,	
		25	:	alloc,
		26	:	eqarr,
		27	:	newfig,
		28	:	addv,
		29	:	addc,
		30	:	adds,
		31	:	wsize,
		32	:	cam,
		33	:	move,
		34	:	rst,
		35 	:	wait

	}
	# Get the function from switcher dictionary
	func = switcher.get(argument, lambda: "nothing")
	# Execute the function
	return func(quad, index)

def plus(quad, index):
	MemoryHandler.binary_operator(quad)

def minus(quad, index):
	MemoryHandler.binary_operator(quad)

def times(quad, index):
	MemoryHandler.binary_operator(quad)

def over(quad, index):
	MemoryHandler.division(quad)

def lessThan(quad, index):
	MemoryHandler.binary_operator(quad)

def greaterThan(quad, index):
	MemoryHandler.binary_operator(quad)

def lessEqThan(quad, index):
	MemoryHandler.binary_operator(quad)

def greaterEqThan(quad, index):
	MemoryHandler.binary_operator(quad)

def equals(quad, index):
	MemoryHandler.binary_operator(quad)

def notEqual(quad, index):
	MemoryHandler.binary_operator(quad)

def _and(quad, index):
	MemoryHandler.and_or_operator(quad)

def _or(quad, index):
	MemoryHandler.and_or_operator(quad)

def equal(quad, index):
	MemoryHandler.assign_operator(quad)

def gotof(quad, index):
	index = MemoryHandler.gotof(quad, index)
	return index

def gotot(quad, index):
	index = MemoryHandler.gotot(quad, index)
	return index

def goto(quad, index):
	index = MemoryHandler.goto(quad)
	return index

def ret(quad, index):
	index = MemoryHandler.ret_operator()
	return index

def _return(quad, index):
	index = MemoryHandler.return_operator(quad)
	return index

def gosub(quad, index):
	index = MemoryHandler.gosub(quad, index)
	return index

def era(quad, index):
	MemoryHandler.era_operator(quad) 

def param(quad, index):
	MemoryHandler.param_operator(quad)

def _print(quad, index):
	MemoryHandler._print(quad)

def end(quad, index):
	print "> PROGRAM EXECUTION DONE"

def alloc(quad, index):
	MemoryHandler.allocate_array_space(quad)

def eqarr(quad, index):
	MemoryHandler.get_array_value(quad)

def newfig(quad, index):
	MemoryHandler.set_new_fig(quad)

def addv(quad, index):
	obj_temp = MemoryHandler.get_fig(quad.result)
	MemoryHandler.add_vertex_fig(quad, obj_temp)
	#MemoryHandler.set_fig(obj_temp, quad)

def addc(quad, index):
	obj_temp = MemoryHandler.get_fig(quad.result)
	MemoryHandler.add_color_fig(quad, obj_temp)
	#MemoryHandler.set_fig(obj_temp, quad)
	
def adds(quad, index):
	obj_temp = MemoryHandler.get_fig(quad.result)
	MemoryHandler.add_size_fig(quad, obj_temp)
	#MemoryHandler.set_fig(obj_temp, quad)

def wsize(quad, index):

	width = MemoryHandler.get_address_value(quad.right_operand)
	height = MemoryHandler.get_address_value(quad.result)

	global win
	win = GraphWin("LIGHT", width, height)

def move(quad, index):
	#obj_temp = MemoryHandler.get_fig(quad.result)
	fig = fig_dict[quad.result]
	x = MemoryHandler.get_address_value(quad.left_operand)
	y = MemoryHandler.get_address_value(quad.right_operand)
	fig.move(x, y)

def rst(quad, index):
	obj_temp = MemoryHandler.get_fig(quad.result)
	obj_temp.reset()

def wait(quad, index):
	MemoryHandler.wait(quad)

def cam(quad, index):
	obj_temp = MemoryHandler.get_fig(quad.result)

	type = abs(quad.result) // 1000

	if type == 6 : #Line
		x = Line(obj_temp.getPointsList())
		x.setFill(obj_temp.getColor())
		x.draw(win)
		fig_dict[quad.result] = x

	elif type == 7 : #triangle
		x = Polygon(obj_temp.getPointsList())
		x.setFill(obj_temp.getColor())
		x.draw(win)
		fig_dict[quad.result] = x


	elif type == 8 : #square
		x = Rectangle(obj_temp.getPoints())
		x.setFill(obj_temp.getColor())
		x.draw(win)
		fig_dict[quad.result] = x


	elif type == 9 : #rectangle
		x = Rectangle(obj_temp.getPoints())
		x.setFill(obj_temp.getColor())
		x.draw(win)
		fig_dict[quad.result] = x


	elif type == 10 : #polygon
		x = Polygon(obj_temp.getPointsList())
		x.setFill(obj_temp.getColor())
		x.draw(win)
		fig_dict[quad.result] = x


	elif type == 12 : #circle
		x = Circle(obj_temp.getPointCenter(), obj_temp.radius)
		x.setFill(obj_temp.getColor())
		x.draw(win)
		fig_dict[quad.result] = x

	else:
		pass

def RUN_AT_LIGHTSPEED():
	MemoryHandler.init_class_vars() # Supah weird hack...
	quads = Quadruples.quad_list
	print "\nVIRTUAL MACHINE ==============================="
	QuadIterator(0, quads)

	raw_input("Press enter to exit")
	#win.getMouse() # Pause to view result
	win.close()
	print "> PROGRAM EXIT"

def QuadIterator(index, quads):

	while(index < len(quads)):
		op = quads[index].operator
		print("\n> EXECUTION LINE: {}, Quad: {}".format(index, quads[index].get_list()))
		new_index = execute_operator(op, quads[index], index)
		index = new_index if new_index else (index + 1)
