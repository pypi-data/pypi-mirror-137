import os


class Logger():
    def __init__(self, fname):
        path, _ = os.path.split(fname)
        os.makedirs(path, exist_ok=True)

        self.logger = open(fname, 'w')

    def log(self, string):
        self.logger.write(string+'\n')
        self.logger.flush()
        print(string)

    def __call__(self, string):
        self.log(string)

    def close(self):
        self.logger.close()
