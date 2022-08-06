import tkinter as t
import pandas as pd

######################  CONSTANTS  ####################
BACKGROUND_COLOR = "#B1DDC6"
CARD_FRONT = './images/card_front.png'
CARD_BACK = './images/card_back.png'
IMG_RIGHT = './images/right.png'
IMG_WRONG = './images/wrong.png'
data_file = './data/french_words.csv'
font1 = ("Times New Roman", 30, 'italic')
font2 = ("Times New Roman", 45, 'bold')

################ GLOBAL VARIABLES  ##############
i = 0
flips = 0

################  FILE READ  ##################
df = pd.read_csv(data_file)
data_dict = df.to_dict()

################  FLIP CARD  ##################
def flip_card():
    global i, flips
    if(i < len(data_dict['French'])):
        # Updating card information appropriately.
        if(flips%2 == 0):
            card.itemconfig(card_side, image=cb)
            card.itemconfig(card_lang, text='English', font=font1, fill='white')
            card.itemconfig(card_word, text=data_dict['English'][i], font=font2, fill='white')
            i += 1
        else:
            card.itemconfig(card_side, image=cf)
            card.itemconfig(card_lang, text='French', font=font1, fill='black')
            card.itemconfig(card_word, text=data_dict['French'][i], font=font2, fill='black')
        flips += 1
        # Recursive call every 3 seconds.
        window.after(3000, flip_card)
    else:
        print('DONE!!!!!!!!!!')

#################  UI SETUP  ###################
# Set up window.
window = t.Tk()
window.title('Flash Cards For French')
window.config(bg=BACKGROUND_COLOR, padx=100, pady=50)

# Set up canvas.
card = t.Canvas(width=800, height=526)
cf = t.PhotoImage(file=CARD_FRONT)
cb = t.PhotoImage(file=CARD_BACK)
card_side = card.create_image(400, 261, image=cf)
card_lang = card.create_text(400, 150, text='French', font=font1)
card_word = card.create_text(400, 250, text=data_dict['French'][i], font=font2, fill='black')
card.config(bg=BACKGROUND_COLOR, highlightthickness=0)
# GRID --> (3 columns X 2 rows)
card.pack()
# Flip the card every 3 seconds.
window.after(3000, flip_card)


# Keep the window displayed.
window.mainloop()
