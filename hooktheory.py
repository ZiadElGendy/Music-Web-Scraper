import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


def main():
    is_quit = False
    scale = ["C", "major"]
    user_input = input(
        f"Press G to generate a chord progression\nPress Q to quit the program\nPress S to change the scale\nCurrent scale: {scale[0]} {scale[1]}\n").upper()
    while not is_quit:
        match user_input:
            case "G":
                print("Generating chord progression, please wait...")
                res = generate_chord_progression(scale[0], scale[1])
                print("Generated chord progression:")
                print(res)
                user_input = input(
                    f"Press G to generate a chord progression\nPress Q to quit the program\nPress S to change the scale\nCurrent scale: {scale[0]} {scale[1]}\n").upper()

            case "Q":
                is_quit = True

            case "S":
                scale = select_scale()
                user_input = input(
                    f"Press G to generate a chord progression\nPress Q to quit the program\nPress S to change the scale\nCurrent scale: {scale[0]} {scale[1]}\n").upper()

            case _:
                print("Invalid input")


def select_scale():
    root = input("Type in the desired root note, alternatively type in 'Rel' for roman numeral notation\n").upper()

    match root:
        case "C#":
            root = "Db"
        case "DB":
            root = "Db"
        case "D#":
            root = "Eb"
        case "EB":
            root = "Eb"
        case "GB":
            root = "F#"
        case "AB":
            root = "Ab"
        case "G#":
            root = "Ab"
        case "BB":
            root = "Bb"
        case "A#":
            root = "Bb"
        case "REL":
            root = "Rel"

    while root not in ["C", "Db", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B", "Rel"]:
        print("Invalid input, try again.\n")
        root = input("Type in the desired root note, alternatively type in 'Rel' for roman numeral notation\n")

    mode = input("Type in the desired mode (Major, Minor, Dorian, Phrygian, Lydian, Mixolydian, Locrian)\n").lower()
    while mode not in ["major", "minor", "dorian", "phrygian", "lydian", "mixolydian", "locrian"]:
        print("Invalid input, try again.\n")
        mode = input("Type in the desired mode (Major, Minor, Dorian, Phrygian, Lydian, Mixolydian, Locrian)\n").lower()

    return [root, mode]


def generate_chord_progression(root, mode):
    url = f'https://www.hooktheory.com/trends#key={root}&scale={mode}'
    options = Options()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    driver.implicitly_wait(10)

    chord_progression_result = []
    is_finished = False
    count = 0

    while not is_finished:
        chord_info = get_chord_info(driver, count)

        if len(chord_info[1]) == 0:
            driver.quit()
            return chord_progression_result

        selected_chord = select_random_chord(chord_info[0], chord_info[1])
        if selected_chord[0] != "Other":
            chord_progression_result.append(selected_chord[0])
            count += 1
        if chord_info[1].__contains__("100%"):
            driver.quit()
            return chord_progression_result

        clickable = chord_info[2][selected_chord[1]]
        clickable.click()


def get_chord_info(driver, count):
    chord_elements = driver.find_elements(By.TAG_NAME, "foreignObject")
    chord_info = [chord.text for chord in chord_elements]
    chord_info = chord_info[count:]
    chords = []
    percentages = []
    for item in chord_info:
        parts = item.split()
        chords.append(parts[0])
        percentages.append(parts[1])
    return [chords, percentages, chord_elements[count:]]


def select_random_chord(chords, percentages):
    population = []
    for element, weight in zip(chords, percentages):
        weight_float = float(weight.rstrip('%'))
        weight_int = int(weight_float * 100)
        population.extend([element] * weight_int)

    selected_chord = random.choice(population)
    index = chords.index(selected_chord)
    return [selected_chord, index]


if __name__ == "__main__":
    main()
