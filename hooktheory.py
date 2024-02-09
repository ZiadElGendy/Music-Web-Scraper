import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
def main():
    is_quit = False
    user_input = input("Press G to generate a chord progression\nPress Q to quit the program\n").upper()
    while not is_quit:
        match user_input:
            case "G":
                print("Generating chord progression, please wait...")
                res = generate_chord_progression()
                print("Generated chord progression:")
                print(res)
                user_input = input("Press G to generate a chord progression\nPress Q to quit the program\n").upper()

            case "Q":
                is_quit = True

            case _:
                print("Invalid input")


def generate_chord_progression():
    url = 'https://www.hooktheory.com/trends'
    driver = webdriver.Chrome()
    driver.get(url)
    driver.implicitly_wait(10)

    chord_progression_result = []
    is_finished = False
    count = 0

    while not is_finished:
        print(f"Count: {count}")
        print(f"Results: {chord_progression_result}")
        time.sleep(3)
        chord_info = get_chord_info(driver, count)
        if chord_info[1].__contains__("100%") or len(chord_info[1]) == 0:
            driver.quit()
            return chord_progression_result
        selected_chord = select_random_chord(chord_info[0], chord_info[1])
        if selected_chord[0] != "Other":
            chord_progression_result.append(selected_chord[0])
            count += 1
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
        print(parts)
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
    print(f"Selected chord: {selected_chord}")
    index = chords.index(selected_chord)
    return [selected_chord, index]


if __name__ == "__main__":
    main()