import curses
import random
import time

def start_screen(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 0, "Welcome to the Speed Typing Test!")
    stdscr.addstr(2, 0, "Press any key to begin!")
    stdscr.refresh()
    stdscr.getkey()

def load_text():
    with open("text.txt", "r") as f:
        lines = f.readlines()
        return random.choice(lines).strip()

def display_text(stdscr, target, current, wpm=0):
    stdscr.addstr(4, 0, target)
    stdscr.addstr(5, 0, f"WPM: {wpm}")

    for i, char in enumerate(current):
        correct_char = target[i]
        color = curses.color_pair(1)
        if char != correct_char:
            color = curses.color_pair(2)

        stdscr.addstr(4, i, char, color)

def wpm_test(stdscr):
    target_text = load_text()
    current_text = []
    wpm = 0
    start_time = time.time()
    curses.noecho()

    while True:
        time_elapsed = max(time.time() - start_time, 1)
        wpm = round((len(current_text) / time_elapsed) / 5)
        stdscr.clear()
        display_text(stdscr, target_text, current_text, wpm)
        stdscr.refresh()

        key = stdscr.getkey()
        if ord(key) == 27:
            break
        if key in (curses.KEY_BACKSPACE, '\b', '\x7f'):
            if len(current_text) > 0:
                current_text.pop()
        elif len(current_text) < len(target_text):
            current_text.append(key)

def main(stdscr):
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)

    start_screen(stdscr)
    while True:
        wpm_test(stdscr)
        stdscr.addstr(6, 0, "You completed the text! Press any key to continue...")
        key = stdscr.getkey()
        if ord(key) == 27:
            break

curses.wrapper(main)
