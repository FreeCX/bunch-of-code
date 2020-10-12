# http://fractalworld.xaoc.ru/L-system_collection
import argparse
import turtle
import json


class LSystem:
    def __init__(self, *, start='', rules={}):
        self.__result = start
        self.__rules = rules
        self.__iteration = 0

    def step(self):
        results = []
        for variable in self.__result:
            # ignore consts
            r = self.__rules[variable] if self.__rules.get(variable) else variable
            results.append(r)
        results = ''.join(results)
        self.__result = results
        self.__iteration += 1
        return self

    def iterate(self, count=1):
        for _ in range(count):
            self.step()
        return self

    def result(self):
        return self.__result


class Turtle:
    def __init__(self, *, cmds='', start_angle=0, loops=1, rules={}):
        self.__cmds = cmds
        self.__rules = rules
        self.__angles = []
        self.__stack = []
        self.__loops = loops
        turtle.reset()
        turtle.degrees()
        turtle.left(start_angle)

    def run(self, savename=None):
        turtle.speed(0)
        turtle.hideturtle()
        for _ in range(self.__loops):
            for symbol in self.__cmds:
                if self.__rules.get(symbol):
                    if ':' in self.__rules[symbol]:
                        cmd, var = self.__rules.get(symbol).split(':')
                        cmd, var = cmd.lower(), float(var) if var.isdigit() else None
                    else:
                        cmd = self.__rules.get(symbol)
                        var = None
                else:
                    continue
                if cmd == 'forward':
                    turtle.forward(var)
                elif cmd == 'left':
                    turtle.left(var)
                elif cmd == 'right':
                    turtle.right(var)
                elif cmd == 'push_angle':
                    self.__angles.append(turtle.heading())
                elif cmd == 'pop_angle':
                    turtle.setheading(self.__angles.pop())
                elif cmd == 'push_all':
                    self.__stack.append((turtle.xcor(), turtle.ycor(), turtle.heading()))
                elif cmd == 'pop_all':
                    x, y, a = self.__stack.pop()
                    turtle.setpos(x, y)
                    turtle.setheading(a)
        if savename:
            ts = turtle.getscreen()
            ts.getcanvas().postscript(file='{}.eps'.format(savename))
        else:
            turtle.mainloop()


def execute_model(filename, *, savename=None, iterations=None):
    with open(filename, 'r') as jsf:
        data = json.load(jsf)
    if iterations:
        data['iterations'] = iterations
    result = LSystem(start=data['axiom'], rules=data['generate_rules']).iterate(data['iterations']).result()
    Turtle(cmds=result, start_angle=data['start_angle'], rules=data['draw_rules']).run(savename=savename)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Draw L System model')
    parser.add_argument('-m', metavar='model', type=str, default=None, help='input model file')
    parser.add_argument('-i', metavar='iterations', type=int, default=None, help='number of iterations')
    parser.add_argument('-o', metavar='output', type=str, default=None, help='name for output eps file')
    args = parser.parse_args()
    if args.m:
        execute_model(args.m, savename=args.o, iterations=args.i)
    else:
        parser.print_help()
