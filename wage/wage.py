from datetime import datetime, timedelta

WAGES = [
    { 'weekday': 'MO', 'lower': timedelta(hours=0, minutes=0), 'upper': timedelta(hours=9, minutes=0), 'amount': 25},
    { 'weekday': 'MO', 'lower': timedelta(hours=9, minutes=1), 'upper': timedelta(hours=18,minutes=0), 'amount': 15},
    { 'weekday': 'MO', 'lower': timedelta(hours=18,minutes=1), 'upper': timedelta(hours=24,minutes=0), 'amount': 20},
    { 'weekday': 'TU', 'lower': timedelta(hours=0, minutes=0), 'upper': timedelta(hours=9, minutes=0), 'amount': 25},
    { 'weekday': 'TU', 'lower': timedelta(hours=9, minutes=1), 'upper': timedelta(hours=18,minutes=0), 'amount': 15},
    { 'weekday': 'TU', 'lower': timedelta(hours=18,minutes=1), 'upper': timedelta(hours=24,minutes=0), 'amount': 20},
    { 'weekday': 'WE', 'lower': timedelta(hours=0, minutes=0), 'upper': timedelta(hours=9, minutes=0), 'amount': 25},
    { 'weekday': 'WE', 'lower': timedelta(hours=9, minutes=1), 'upper': timedelta(hours=18,minutes=0), 'amount': 15},
    { 'weekday': 'WE', 'lower': timedelta(hours=18,minutes=1), 'upper': timedelta(hours=24,minutes=0), 'amount': 20},
    { 'weekday': 'TH', 'lower': timedelta(hours=0, minutes=0), 'upper': timedelta(hours=9, minutes=0), 'amount': 25},
    { 'weekday': 'TH', 'lower': timedelta(hours=9, minutes=1), 'upper': timedelta(hours=18,minutes=0), 'amount': 15},
    { 'weekday': 'TH', 'lower': timedelta(hours=18,minutes=1), 'upper': timedelta(hours=24,minutes=0), 'amount': 20},
    { 'weekday': 'FR', 'lower': timedelta(hours=0, minutes=0), 'upper': timedelta(hours=9, minutes=0), 'amount': 25},
    { 'weekday': 'FR', 'lower': timedelta(hours=9, minutes=1), 'upper': timedelta(hours=18,minutes=0), 'amount': 15},
    { 'weekday': 'FR', 'lower': timedelta(hours=18,minutes=1), 'upper': timedelta(hours=24,minutes=0), 'amount': 20},
    { 'weekday': 'SA', 'lower': timedelta(hours=0, minutes=0), 'upper': timedelta(hours=9, minutes=0), 'amount': 30},
    { 'weekday': 'SA', 'lower': timedelta(hours=9, minutes=1), 'upper': timedelta(hours=18,minutes=0), 'amount': 20},
    { 'weekday': 'SA', 'lower': timedelta(hours=18,minutes=1), 'upper': timedelta(hours=24,minutes=0), 'amount': 25},
    { 'weekday': 'SU', 'lower': timedelta(hours=0, minutes=0), 'upper': timedelta(hours=9, minutes=0), 'amount': 30},
    { 'weekday': 'SU', 'lower': timedelta(hours=9, minutes=1), 'upper': timedelta(hours=18,minutes=0), 'amount': 20},
    { 'weekday': 'SU', 'lower': timedelta(hours=18,minutes=1), 'upper': timedelta(hours=24,minutes=0), 'amount': 25},
]

class Worktime():
    def __init__(self, weekday, lower, upper):
        self.weekday = weekday
        self.lower = lower
        self.upper = upper
    
    def get_amount(self):
        ranges = [w for w in WAGES if w['weekday']==self.weekday]
        acum = 0
        for r in ranges:
            dif = timedelta(hours=0, minutes=0)
            if r['lower'] < self.upper <= r['upper']:
                if self.lower < r['lower']:
                    dif = self.upper - r['lower']
                elif r['lower'] < self.lower <= r['upper']:
                    dif = self.upper - self.lower
            elif self.upper > r['upper']:
                if self.lower < r['lower']:
                    dif = r['upper'] - r['lower']
                elif r['lower'] < self.lower <= r['upper']:
                    dif = r['upper'] - self.lower
            worked_hours = (dif.seconds / 3600) 
            acum = acum + worked_hours * r['amount']
        return acum
        
            

def get_timedelta(v):
    try:
        return timedelta(hours = int(v[0:2]), minutes=int(v[3:5]))
        
    except ValueError:
        print(f"There is an error in worktime. Please check input {v}")
        return timedelta(0)

def calculate_wage(line):
    try:
        values = line.split("=")[1].split(",")
        
        wage = 0
        for v in values:
            weekday = v[0:2]

            lower = get_timedelta(v[2:7])
            upper = get_timedelta(v[8:13])
            
            if lower > upper:
                raise ValueError
            worktime = Worktime(weekday, lower, upper)
            wage = wage + worktime.get_amount()
        return wage
    except IndexError:
        print(f"Line has a wrong format. Name should be separated with '=' and days with '-'. Please check the input: {line}")
        return 0
    except ValueError:
        print((f"You can't have a 'from' time higher than 'to' time: {line}"))



def calculate_wage_for_file(filename):
    try:
        with open(filename, "r") as file:
            lines = file.readlines()
            output = []
            for line in lines:
                name = line.split("=")[0]
                
                result = round(calculate_wage(line),2)
                text_result = f"The amount to pay to {name} is: {result} USD"
                output.append(text_result)
                print(text_result)
        return output
    except FileNotFoundError:
        print("File does not exist")


if __name__ == "__main__":
    import sys
    if len(sys.argv) == 1:
        print("Please give a filename")
        exit()

    calculate_wage_for_file(sys.argv[1])