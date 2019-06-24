import random
import sys
import os


class Test():
    def __init__(self, casos=random.randint(1, 10),
                 processes=random.randint(2, 10)):
        self.casos = casos
        self.processes = processes
        self.path = os.path.dirname(os.path.relpath(__file__))
        self.generate()

    def generate(self):
        if self.path:
            print("Error:\tCurrent path is not appropriated path for tests")
            sys.exit(1)
        for __ in range(self.casos):
            files = list(filter(lambda file:
                                (file.split('.')[-1] == "txt"),
                                os.listdir()))
            indice = len(files)
            with open("test{}.txt".format(indice), 'w') as file:
                for y in range(self.processes):
                    pid = y + 1
                    begin = random.randint(0, 10)
                    execute = random.randint(1, 20)
                    pages = random.randint(1, 10)
                    offset = random.randint(10, 60)
                    start = round(pages/2, 0) + execute + begin
                    deadline = random.randint(start, start + offset)
                    priority = random.randint(1, 30)
                    file.write("{} {} {} {} {} {}\n"
                                .format(pid, begin, execute,
                                        pages, deadline, priority))
        print("[ OK ]\t{} test files generated with {} processes each"
              .format(self.casos, self.processes))


if __name__ == "__main__":
    parameters = ["-n", "-p", "-r"]
    help_parameter = "--help"
    if not any(parameter in sys.argv for parameter in parameters):
        arguments = ["-n (number of files)",
                     "-p (number of processes in each file)",
                     "-r (for complete randomness)"]
        print("Usage: python test-generator.py [OPTIONS]")
        print(*arguments, sep='\n')
        sys.exit(help_parameter not in sys.argv)
    else:
        has_n = False
        has_p = False
        error = False
        if "-n" in sys.argv:
            try:
                casos = int(sys.argv[sys.argv.index("-n") + 1])
                has_n = True
            except ValueError:
                has_n = False
                error = True
        if "-p" in sys.argv:
            try:
                processes = int(sys.argv[sys.argv.index("-p") + 1])
                has_p = True
            except ValueError:
                has_p = False
                error = True
        if has_n and has_p:
            Test(casos, processes)
        elif not has_n and has_p:
            Test(processes=processes)
        elif has_n and not has_p:
            Test(casos=casos)
        elif ("-r" in sys.argv and len(sys.argv) == 2) or error:
            Test()
