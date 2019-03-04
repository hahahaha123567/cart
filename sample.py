class Sample(object):

    def __init__(self, hasHouse, married, income, hasLoan):
        self.hasHouse = hasHouse
        self.married = married
        self.income = income
        self.hasLoan = hasLoan
        
    def print(self):
        print(self.hasHouse, self.married, self.income, self.hasLoan)
