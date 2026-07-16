from datetime import datetime

def execute(argument: dict):
    now = datetime.now()
    return now.strftime("%d-%n-%Y %I:%M:%S %p")

if __name__ == "__main":
    print("Time tool \n")
    print(execute({}))