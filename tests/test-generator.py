import random
import sys
import os
class Test():
    def __init__(self, casos=random.randint(1,10),
                 processes=random.randint(2, 10)):
        self.casos = casos
        self.processes = processes
        self.generate()
                
    def generate(self):
        for i in range(self.casos):    
            files = list(filter(lambda file: 
                                (file.split('.')[-1] == "txt"),
                                os.listdir()))
            indice = len(files)
            with open("test{}.txt".format(indice), 'w') as file:
                for y in range(self.processes):
                    pid = y+1
                    begin = random.randint(0, 10) 
                    execute = random.randint(1, 20)
                    pages = random.randint(1, 10)
                    offset = max(random.randint(20, 50), 
                                random.randint(10, 60))
                    deadline = random.randint(execute, execute + offset)
                    priority = random.randint(1, 30)
                    file.write("{} {} {} {} {} None False {}\n"
                                .format(pid, begin, execute,
                                        pages, deadline, priority))
        print("[ OK ]\t{} test files generated with {} processes each" 
              .format(self.casos, self.processes))
    


if __name__ == "__main__":
    parameters = ["-n", "-p", "-r"]
    help_parameter = "--help"
    if not any(parameter in sys.argv for parameter in parameters):
        print("Usage: python test-generator.py\nUse one or more of these arguments\n-n (number of files)\n-p (number of processes in each file)\n-r (complete random)")
        sys.exit(not help_parameter in sys.argv)
    else:   
        has_n = False
        has_p = False

        if "-n" in sys.argv:
            casos = int(sys.argv[sys.argv.index("-n") + 1])
            has_n = True
            
        if "-p" in sys.argv:
            processes = int(sys.argv[sys.argv.index("-p") + 1])
            has_p = True
            
        if has_n and has_p:
            Test(casos, processes)
        elif "-r" in sys.argv and len(sys.argv) == 2:
            Test()
        elif not has_n and has_p:
            Test(processes=processes)
        elif has_n and not has_p:
            Test(casos=casos)
