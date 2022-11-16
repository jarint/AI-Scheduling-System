'''
This is the driver class. It creates a scheduler object and accepts

'''

from Scheduler import Scheduler


class Main:

    def main(self):
        s = Scheduler()
        s.start()


if __name__ == "__main__":
    Main.main()