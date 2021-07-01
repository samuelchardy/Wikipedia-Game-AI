lines = []
path = input()

for i in range(100):
    try:
        filename = path + str(i)+".csv"
        file = open(filename, "r")
        lines.append(file.readline())
        file.close()
    except:
        print("Error on line: " + str(i))

file = open("full.csv", "w")
file.writelines(lines)
file.close()