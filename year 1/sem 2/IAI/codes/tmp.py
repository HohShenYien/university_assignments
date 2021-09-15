import scan_symptom

def get_knowledge():
    # This function will read all the knowledge into dictionaries
    symptom_nutrient = {}
    symptom_avoid = {}
    nutrient_food = {}
    with open("symptoms-to_eat.txt", "r") as file:
        for line in file.readlines():
            tmp = line.strip().split("|")
            symptoms = tmp[0].split("/")
            nutrients = tmp[1].split("/")
            for symptom in symptoms:
                if symptom in ["AIDS", "HIV"]:
                    # special case
                    symptom_nutrient[symptom] = (symptom, nutrients)
                    continue
                # Process the symptom name
                symptom_nutrient[scan_symptom.lemmatize(symptom.lower())] = (symptom, nutrients)

    with open("symptoms-not_to_eat.txt", "r") as file:
        for line in file.readlines():
            tmp = line.strip().split("|")
            symptoms = tmp[0].split("/")
            food = tmp[1].split("/")
            for symptom in symptoms:
                if symptom in ["AIDS", "HIV"]:
                    # special case
                    symptom_avoid[symptom] = (symptom, food)
                    continue
                # Process the symptom name
                symptom_avoid[scan_symptom.lemmatize(symptom.lower())] = (symptom, food)

    with open("nutrient-food.txt", "r") as file:
        for line in file.readlines():
            tmp = line.strip().split("|")
            nutrients = tmp[0].split("/")
            food = tmp[1].split("/")
            for nutrient in nutrients:
                # Process the symptom name
                nutrient_food[nutrient] = food
    
    return symptom_nutrient, symptom_avoid, nutrient_food

symptom_nutrient, symptom_avoid, nutrient_food = get_knowledge()
for _, value in symptom_nutrient.items():
    for tmp in value[1]:
        try:
            nutrient_food[tmp]
        except:
            print(f"{value[0]}.", end="")
            print(f"--{tmp}--")
