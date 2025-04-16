questions = ( "1.How many planets do we have in Solar System?",
              "2.What is the gravitational force at Earth?", 
              "3.What is the speed of the light?", 
              "4.What is the highest payed job currently?", 
              "5.Who is richest person of 2024?", 
              "6.Who invented lamp?", 
              "7.Which of the following is the first 8 digits of Pi?")

options = (("A. 10", "B. 11", "C. 9", "D. 8"),
           ("A. 11 m/s^2", "B. 9.8 m/s^2", "C. 10 m/s^2", "D. 8 m/s^2"),
           ("A. 3*10^8 m/s", "B. 3*10^4 km/s", "C. 4*10^7 m/s", "D. 3.5*10^9 m/s"),
           ("A. Doctor", "B. Software engineer", "C. Teacher", "D. Pilot"),
           ("A. Elon Musk", "B. Murk Zuckerberg", "C. Warren Buffet", "D. Jeff Besoz"),
           ("A. Sir Isaac Newton", "B. Nicola Tesla", "C. Albert Einstein", "D. Thomas Edison"),
           ("A. 3.1476893", "B. 3.1410935", "C. 3.1415926", "D. 3.1445673"))

answers = ("D", "B", "A", "B", "A", "D", "C")
valid_answers = ["A", "B", "C", "D"]

guesses = []
score = 0
question_num = 0

print()
print("-------------Quiz--------------")
print("Answer the following questions. 1 point for each question")

for question in questions:
    print("-------------------------------")
    print(question)
    for option in options[question_num]:
        print(option)

    while True:
        if guess in valid_answers:
            guess = str(input("Choose an option: ").upper())
            guesses.append(guess)
            break
        else:
            print(f"{guess} is NOT an option. Please choose an option A, B, C, or D.")
            print("Choose and option: ")
    question_num += 1

print()
print("Correct answers:", end="")
for answer in answers:
    print(answer, end=" ")
print("Your answers:", end="")
for guess in guesses:
    print(guess, end="")
print(f"Your score is {score} out of 7")



