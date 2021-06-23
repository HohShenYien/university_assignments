with open("tmp.txt", "r") as file:
    for line in file.readlines():
        if "class_profile.html" in line:
            print(line.replace("class_profile.html", "class_profile_2.html"), end="")
        else:
            print(line, end="")