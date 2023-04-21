# http://fractalworld.xaoc.ru/L-system_collection
import argparse
import json
import turtle


class LSystem:
    def __init__(self, *, start="", rules={}):
        self.__result = start
        self.__rules = rules
        self.__iteration = 0

    def step(self):
        results = []
        for variable in self.__result:
            # ignore consts
            r = self.__rules[variable] if self.__rules.get(variable) else variable
            results.append(r)
        results = "".join(results)
        self.__result = results
        self.__iteration += 1
        return self

    def iterate(self, count=1):
        for _ in range(count):
            self.step()
        return self

    @property
    def result(self):
        return self.__result


class Turtle:
    def __init__(self, *, cmds="", start_angle=0, loops=1, rules={}):
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
                if not self.__rules.get(symbol):
                    continue

                cmd = self.__rules.get(symbol)
                var = None
                if ":" in self.__rules[symbol]:
                    cmd, var = cmd.split(":")
                    cmd = cmd.lower()
                    if var.isdigit():
                        var = float(var)

                match cmd:
                    case "forward":
                        turtle.forward(var)
                    case "left":
                        turtle.left(var)
                    case "right":
                        turtle.right(var)
                    case "push_angle":
                        self.__angles.append(turtle.heading())
                    case "pop_angle":
                        turtle.setheading(self.__angles.pop())
                    case "push_all":
                        self.__stack.append((turtle.xcor(), turtle.ycor(), turtle.heading()))
                    case "pop_all":
                        x, y, a = self.__stack.pop()
                        turtle.setpos(x, y)
                        turtle.setheading(a)
                    case other:
                        print(f"unknown command: {other}")

        if savename:
            ts = turtle.getscreen()
            ts.getcanvas().postscript(file="{}.eps".format(savename))
            return

        turtle.mainloop()


def execute_model(filename, *, savename=None, iterations=None):
    with open(filename, "r") as jsf:
        data = json.load(jsf)
    if iterations:
        data["iterations"] = iterations
    result = LSystem(start=data["axiom"], rules=data["generate_rules"]).iterate(data["iterations"]).result
    Turtle(cmds=result, start_angle=data["start_angle"], rules=data["draw_rules"]).run(savename=savename)


def main():
    parser = argparse.ArgumentParser(description="Draw L System model")
    parser.add_argument("-m", metavar="model", type=str, default=None, help="input model file")
    parser.add_argument("-i", metavar="iterations", type=int, default=None, help="number of iterations")
    parser.add_argument("-o", metavar="output", type=str, default=None, help="name for output eps file")
    args = parser.parse_args()

    if not args.m:
        parser.print_help()
        return

    execute_model(args.m, savename=args.o, iterations=args.i)


if __name__ == "__main__":
    main()
