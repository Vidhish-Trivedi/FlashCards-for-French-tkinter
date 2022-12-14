import tkinter as t
import pandas as pd

######################  CONSTANTS  ####################
BACKGROUND_COLOR = "#B1DDC6"
CARD_FRONT = './images/card_front.png'
CARD_BACK = './images/card_back.png'
IMG_RIGHT = './images/right.png'
IMG_WRONG = './images/wrong.png'
data_file = './data/french_words.csv'
font1 = ("Times New Roman", 40, 'italic')
font2 = ("Times New Roman", 60, 'bold')

################ GLOBAL VARIABLES  ##############
i = 0
flips = 0
list_known = []
clk = None

################  FILE READ  ##################
# Try to open file with previous learning progress, if exists.
try:
    file_test = open('./data/to_learn.csv')
# Incase of exception, open default data_file and create a new file to save progress.
except FileNotFoundError:
    df = pd.read_csv(data_file)
    with open('./data/to_learn.csv', mode='w') as file:
        file.write('French,English\n')
else:
    df = pd.read_csv('./data/to_learn.csv')
finally:
    data_dict = df.to_dict()

################  FLIP CARD  ##################
def flip_card(seconds):
    global i, flips, list_known, clk
    if(i < len(data_dict['French'])):
        # Updating card information appropriately.
        if(data_dict['French'][i] == 'False'):
            i += 1
            if(flips%2 == 0):
                flips += 1
            else:
                flips += 2
            window.after_cancel(clk)
            clk = window.after(1, flip_card, 3)
        else:
            if(flips%2 == 0):
                card.itemconfig(card_side, image=cb)
                card.itemconfig(card_lang, text='English', font=font1, fill='#141E61')
                card.itemconfig(card_word, text=data_dict['English'][i], font=font2, fill='#141E61')
                i += 1
                flips += 1
            elif(flips%2 == 1):
                card.itemconfig(card_side, image=cf)
                card.itemconfig(card_lang, text='French', font=font1, fill='black')
                card.itemconfig(card_word, text=data_dict['French'][i], font=font2, fill='black')
                flips += 1
            else:
                pass
            if(i >= len(data_dict['French'])):
                i = 0
                flips = 0
            # Recursive call every 3 seconds.
            clk = window.after(seconds*1000, flip_card, seconds)
    else:
        print('DONE!!!!!!!!!!')

###########  TICK MARK BUTTON  #################
def known_word():  ########################################  DEBUG. list_known.append(i)
    global clk, data_dict
    data_dict['French'][i] = 'False'
    data_dict['English'][i] = 'False'
    window.after_cancel(clk)
    clk = window.after(1, flip_card, 3)

###########  CROSS MARK BUTTON  ################
def unknown_word():
    global clk, i, data_dict

    ###########  WRITE TO FILE  ###########
    # Filter out keys with values != False, these are the words to learn.
    with open('./data/to_learn.csv', mode='a') as file:
        file.write(f"{data_dict['French'][i]},{data_dict['English'][i]}\n")

    window.after_cancel(clk)
    clk = window.after(1, flip_card, 3)

#################  UI SETUP  ###################
# Set up window.
window = t.Tk()
window.title('Flash Cards For French')
window.config(bg=BACKGROUND_COLOR, padx=50, pady=50)

# Set up canvas.
card = t.Canvas(width=800, height=526)
cf = t.PhotoImage(file=CARD_FRONT)
cb = t.PhotoImage(file=CARD_BACK)
card_side = card.create_image(400, 263, image=cf)
card_lang = card.create_text(400, 150, text='French', font=font1)
card_word = card.create_text(400, 250, text=data_dict['French'][i], font=font2, fill='black')
card.config(bg=BACKGROUND_COLOR, highlightthickness=0)
# GRID --> (2 columns X 2 rows)
card.grid(column=0, row=0, columnspan=2)
# Flip the card every 3 seconds.
clk = window.after(3000, flip_card, 3)

# Button for wrong (cross).
img_wrong = t.PhotoImage(file=IMG_WRONG)
b_wrong = t.Button(image=img_wrong, highlightthickness=0, bg=BACKGROUND_COLOR, border=0, command=unknown_word)
b_wrong.grid(column=0, row=1)

# Button for right (tick).
img_right = t.PhotoImage(file=IMG_RIGHT)
b_right = t.Button(image=img_right, highlightthickness=0, bg=BACKGROUND_COLOR, border=0, command=known_word)
b_right.grid(column=1, row=1)

# Keep the window displayed.
window.mainloop()

# TODO: Bug when clicking cross button (when card displays
#       English word), writes the next (not current) word
#       to the to_learn.csv file.
