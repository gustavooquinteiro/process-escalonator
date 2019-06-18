import random
import sys
import os

casos = 1
processes = random.randint(2, 30) 

def generate(casos, processes):
    for i in range(casos):    
        files = list(filter(lambda file: 
                            (file.split('.')[-1] == "txt"),
                            os.listdir()))
        indice = len(files)
        with open("test{}.txt".format(indice), 'w') as file:
            for y in range(processes):
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
    print("[ OK ]\t{} test files generated" .format(casos))
    


if __name__ == "__main__":
    parameters = ["-n", "-p"]
    if not any(parameter in sys.argv for parameter in parameters):
        print("Usage: python test-generator.py -n (number of files) -p (number of processes in each file)")
        sys.exit(1)
    else:
        if "-n" in sys.argv:
            casos = int(sys.argv[sys.argv.index("-n") + 1])
        if "-p" in sys.argv:
            processes = int(sys.argv[sys.argv.index("-p") + 1])
        generate(casos, processes)
    
        
            
