from tkinter import *
import math 
from pygame import mixer

mixer.init()

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#228B22"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
REP = 1
TIMER = "00:00"

# ---------------------------- TIMER RESET ------------------------------- # 
def rest_timer():
    window.after_cancel(TIMER)
    label1.config(text="TIME", fg=GREEN)
    canvas.itemconfig(timer_text, text="00:00")
    global REP
    REP = 1
    label2.config(text="")

# ---------------------------- TIMER MECHANISM ------------------------------- #
def start_timer():
    global REP
    global TIMER
    window.after_cancel(TIMER)

    work_sec = WORK_MIN * 60
    short_sec = SHORT_BREAK_MIN * 60
    long_sec = LONG_BREAK_MIN * 60

    if REP % 8 == 0:
        countdown(long_sec)
        label1.config(text="L-BREAK", fg=PINK)
    elif REP % 2 == 0:
        countdown(short_sec)
        label1.config(text="BREAK", fg=GREEN)
    else:
        countdown(work_sec)
        label1.config(text="WORK", fg=RED)

    REP += 1

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- # 
def countdown(count):
    count_min = math.floor(count / 60)
    count_sec = count % 60

    time_format = f"{count_min:02d}:{count_sec:02d}"
    canvas.itemconfig(timer_text, text=time_format)

    if count > 0:
        global TIMER
        TIMER = window.after(1000, countdown, count - 1)
    else:
        try:
            alarm_sound = mixer.Sound("alarm.wav")  
            alarm_sound.play()
        except Exception as e:
            print(f"Error playing sound: {e}")
        start_timer()
        label2.config(text="✓" * (REP // 2))

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("POMODORO")
window.config(pady=50, padx=100, bg=YELLOW)
window.resizable(False, FALSE)

label1 = Label(text="TIME", font=(FONT_NAME, 35, "bold"), bg=YELLOW, fg=GREEN)
label1.grid(column=1, row=0)

button1 = Button(text="START", font=(FONT_NAME, 15, "bold"), bg=YELLOW, fg=RED, bd=0, command=start_timer)
button1.grid(column=0, row=2)

button2 = Button(text="RESET", font=(FONT_NAME, 15, "bold"), bg=YELLOW, fg=RED, bd=0, command=rest_timer)
button2.grid(column=2, row=2)

label2 = Label(font=(FONT_NAME, 20), bg=YELLOW, fg=GREEN)
label2.grid(column=1, row=3)

canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file="./img/tomato.png")
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 25, "bold"))
canvas.grid(column=1, row=1)

window.mainloop()
mixer.quit()
