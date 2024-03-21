def create_database():
    with open("mpls\mpls_home.txt", "r") as file:
        lines = file.readlines()
        with open("database.txt", "a") as database_file:
            for line in lines:
                print(line.strip())
                for i in range(1,6):
                    print(i)
                    advice = input().replace("\n", " ")
                    result = "### Question: Give me Advice on the folling mpl error: " + line.strip() + "### Answer: " + advice + "\n"
                    database_file.write(result)

def fix_questions():
    with open("database.txt", "r") as file:
        lines = file.readlines()
        with open("database_fixed.txt", "w") as database_file:
            for line in lines:
                    database_file.write(line.replace("### Question: ", "### Question: Give me Advice on the folling mpl error: "))

def create_validation():
    with open("database.txt", "r") as file:
        lines = file.readlines()
        with open("validation.txt", "w") as database_file:
            for i in range(len(lines)):
                if i % 5 == 0:
                    database_file.write(lines[i])
create_validation()