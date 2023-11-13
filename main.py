import curses 
import random 
import time

def start_screen(stdscr):
    stdscr.clear() 
    max_y, max_x = stdscr.getmaxyx()

    welcome_text = "Welcome to the Speed Typing Test!"
    welcome_x = max_x // 2 - len(welcome_text) // 2  

    middle_text = "Press any key to begin!"
    middle_x = max_x // 2 - len(middle_text) // 2  

    stdscr.addstr(max_y // 2, welcome_x, welcome_text)  
    stdscr.addstr(max_y // 2 + 2, middle_x, middle_text) 
    stdscr.refresh() 
    stdscr.getch()



def load_text(): 
    with open("text.txt", "r") as f:
        lines = f.readlines() 
        return random.choice(lines).strip() 

def display_text(stdscr, target, current, wpm=0):
    max_y, max_x = stdscr.getmaxyx()
    text_length = len(target)

    start_y = max_y // 2
    start_x = max_x // 2 - text_length // 2

    stdscr.addstr(start_y, start_x, target)
    stdscr.addstr(start_y + 1, 0, f"WPM: {wpm}")

    for i, char in enumerate(current):
        if i < text_length:
            correct_char = target[i]
            color = curses.color_pair(1)
            if char != correct_char:
                color = curses.color_pair(2)

            stdscr.addstr(start_y, start_x + i, char, color)


def wpm_test(stdscr):
    target_text = load_text() 
    current_text = []
    wpm = 0
    start_time = time.time()
    curses.noecho()

    while True:
        time_elapsed = max(time.time() - start_time, 1)
        wpm = round(((len(current_text) / 5) / (time_elapsed / 60))  / 5)
        stdscr.clear()
        display_text(stdscr, target_text, current_text, wpm)
        stdscr.refresh()

        if "".join(current_text) == target_text:
            stdscr.nodelay(False)
            break
        try:
            key = stdscr.getkey()
        except: continue

        if ord(key) == 27: 
            break

        if key in ("KEY_BACKSPACE", '\b', "\x7f"):
            if len(current_text) > 0:
                current_text.pop()
        elif len(current_text) < len(target_text):
            current_text.append(key)

def main(stdscr): #orchestrates the whole process
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)

    start_screen(stdscr)
    while True:
        wpm_test(stdscr)
        stdscr.addstr(6, 0, "You completed the text! Press any key to continue...")
        key = stdscr.getch()
        if key == 27:  # ESC key
            break

curses.wrapper(main) #executes the main function using curses for terminal-based interaction
