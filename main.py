'''
This is the driver class. It creates a scheduler object and accepts

'''

from Scheduler import Scheduler


class Main:

    @staticmethod
    def main():
        s = Scheduler()
        s.search()


if __name__ == "__main__":
    Main.main()