from tkinter import *
import pandas
import json

BACKGROUND_COLOR = "#B1DDC6"

# ---------------------------- WORDS MANAGER ------------------------------- #
data = pandas.read_csv("data/german_words.csv")
english_words = (data["English"])
german_words = (data["German"])
reps = 0
counter = 6
unknown_words = 0
guessed_words = 0
is_created = False


def new_english_word():
    global reps
    canvas.create_image(400, 263, image=card_back_img)
    canvas.create_text(400, 150, text="English", font=("Ariel", 40, "italic"))
    canvas.create_text(400, 263, text=f"{english_words[reps]}", font=("Ariel", 60, "bold"))


def new_german_word():
    global reps
    canvas.create_image(400, 263, image=card_front_img)
    canvas.create_text(400, 150, text="German", font=("Ariel", 40, "italic"))
    canvas.create_text(400, 263, text=f"{german_words[reps]}", font=("Ariel", 60, "bold"))


def increase_points():
    global guessed_words
    guessed_words += 1
    known_words_label = Label(text=f'{guessed_words}/100', font=('Arial', 50), background=BACKGROUND_COLOR)
    known_words_label.grid(column=0, row=2, columnspan=11)

# ---------------------------- COUNTER MANAGER ------------------------------- #


def count_down():
    global counter
    if counter > 0:
        counter -= 1
        timer_label.config(text=str(counter))
        window.after(1000, count_down)


def reset_counter():
    global counter
    counter = 6
# ---------------------------- BUTTONS FUNCTIONS ------------------------------- #


def disable_button():
    correct_button.config(state="disabled")
    wrong_button.config(state="disabled")


def enable_button():
    correct_button.config(state="normal")
    wrong_button.config(state="normal")


def known_word():
    global reps
    reps += 1
    increase_points()
    game()


def unknown_word():
    global reps
    global is_created
    global unknown_words
    unknown_words += 1
    actual_english_words = english_words[reps]
    actual_german_words = german_words[reps]
    word_to_json = {
        reps: {
            "english": actual_english_words,
            "german": actual_german_words,
        }
    }
    try:
        if unknown_words == 1 and not is_created:
            with open("words_to_learn.json", "w") as data_file:
                json.dump(word_to_json, data_file, indent=4)
            is_created = True
        else:
            with open("words_to_learn.json", "r") as data_file:
                words_to_learn = json.load(data_file)
    except FileNotFoundError:
        with open("words_to_learn.json", "w") as data_file:
            json.dump(word_to_json, data_file, indent=4)
    else:
        words_to_learn.update(word_to_json)

        with open("words_to_learn.json", "w") as data_file:
            json.dump(words_to_learn, data_file, indent=4)
    finally:
        reps += 1
        game()


# ---------------------------- GAME ------------------------------- #
def game():
    global counter
    if reps == 100:
        canvas.create_image(400, 263, image=card_front_img)
        canvas.create_text(400, 150, text="GAME OVER", font=("Ariel", 40, "italic"))
        canvas.create_text(400, 263, text=f"YOU WENT THROUGH \n       ALL WORDS!!", font=("Ariel", 30, "bold"))
        canvas.create_text(400, 400, text="WORDS THAT YOU DON'T KNOW,YOU CAN \nFIND IN THE FILE words_to_learn.json",
                           font=("Ariel", 20, "bold"))
        disable_button()
    else:
        counter = 6
        disable_button()
        new_german_word()
        count_down()
        window.after(5000, new_english_word)
        window.after(5001, enable_button)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Flashy")
ico = PhotoImage(file='images/flash-card.png')
window.iconphoto(False, ico)
window.resizable(False, False)
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
canvas.create_image(400, 263, image=card_front_img)
canvas.grid(row=0, column=0, columnspan=2)
card_title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))

# Timer
timer_label = Label(text='5', font=('Arial', 50), background=BACKGROUND_COLOR)
timer_label.grid(column=0, row=1, columnspan=11)
# Known_words
guessed_words_label = Label(text=f'{guessed_words}/100', font=('Arial', 50), background=BACKGROUND_COLOR)
guessed_words_label.grid(column=0, row=2, columnspan=11)

# Wrong Button
wrong_image = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_image, highlightthickness=0, command=unknown_word)
wrong_button.grid(row=1, column=0)
# Correct Button
correct_image = PhotoImage(file="images/right.png")
correct_button = Button(image=correct_image, highlightthickness=0, command=known_word)
correct_button.grid(row=1, column=1)

game()
window.mainloop()
