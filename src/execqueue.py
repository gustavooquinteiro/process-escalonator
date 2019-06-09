class ExecQueue:
    queue = []
    
    @staticmethod
    def enqueue(data):
        queue.append(data)

    @staticmethod
    def getQueue():
        return queue