class Person:
	def __init__(self, firstName, lastName, idNumber):
		self.firstName = firstName
		self.lastName = lastName
		self.idNumber = idNumber
	def printPerson(self):
		print("Name:", self.lastName + ",", self.firstName)
		print("ID:", self.idNumber)

class Student(Person):
    #   Class Constructor
    #   
    #   Parameters:
    #   firstName - A string denoting the Person's first name.
    #   lastName - A string denoting the Person's last name.
    #   id - An integer denoting the Person's ID number.
    #   scores - An array of integers denoting the Person's test scores.
    #
    def __init__(self, firstName, lastName, id, scores) :
        Person.__init__(self, firstName, lastName, id)
        self.scores = scores

    #   Function Name: calculate
    #   Return: A character denoting the grade.
    #
    def calculate(self) :
        sum = 0
        for score in self.scores:
            sum += score
        avg_score = sum / len(self.scores)
        if (avg_score >= 90 and avg_score <= 100) :
            return 'O'
        elif (avg_score >= 80 and avg_score < 90) :
            return 'E'
        elif (avg_score >= 70 and avg_score < 80) :
            return 'A'
        elif (avg_score >= 55 and avg_score < 70) :
            return 'P'
        elif (avg_score >= 40 and avg_score < 55) :
            return 'D'
        elif (avg_score < 40) :
            return 'T'

line = input().split()
firstName = line[0]
lastName = line[1]
idNum = line[2]
numScores = int(input()) # not needed for Python
scores = list( map(int, input().split()) )
s = Student(firstName, lastName, idNum, scores)
s.printPerson()
print("Grade:", s.calculate())