import curses #text based user interface buat terminal
import random #pilih line random dari text.txt
import time #buat ngukur wpm

def start_screen(stdscr):
    stdscr.clear() #clears the entire screen
    max_y, max_x = stdscr.getmaxyx() #ngambil panjang dan lebar maximum dari layar

    welcome_text = "Welcome to the Speed Typing Test!"
    welcome_x = max_x // 2 - len(welcome_text) // 2 #makes sure that the welcome text is in the center 

    middle_text = "Press any key to begin or 'q' to exit."
    middle_x = max_x // 2 - len(middle_text) // 2  #biar instruksinya ditengah

    stdscr.addstr(max_y // 2, welcome_x, welcome_text)  #welcome text di print di posisi yang sdh dihitung
    stdscr.addstr(max_y // 2 + 2, middle_x, middle_text) #instruksi di print di posisi yang sdh dihitung
    stdscr.refresh() 
    stdscr.getch() #nunggu usernya pencet sesuatu, klo blm, program gk akan lanjut

def load_text(): 
    with open("text.txt", "r") as f: #ngebuka file namanya tet.txt dalam read mode
        lines = f.readlines() #ngescan seluruh baris, dan membuat list yg elemennya tiap baris, ie {line 1, line 2, etc}
        return random.choice(lines).strip() #pilih satu line secara random

def display_text(stdscr, target, current, wpm=0):
    max_y, max_x = stdscr.getmaxyx() #ngambil maksimum panjang dan lebar layar
    text_length = len(target)

    start_y = max_y // 2 #text yg mau diketik harus tepat ditengah
    start_x = max_x // 2 - text_length // 2

    stdscr.addstr(start_y, start_x, target) #text diluarkan di posisi yang sudah dihitung
    stdscr.addstr(start_y + 1, 0, f"WPM: {wpm}") #wpm di tarok dibawah text.

    for i, char in enumerate(current):
        """
enumerate artinya mengambil index dan character tiap elemen di list
index = 0,1,2. character = huruf2nya
loopnya berjalan untuk tiap character di string, dan tiap iterasi bakal dihitung sebgai index x
tulisannya i, char karena dia menugaskan tiap character untuk index2 tertentu
        """
        if i < text_length: #iterasi bakal selesai kalau i = text_length, berarti sdh lewat semua
            correct_char = target[i] 
            '''
target itu kalimat yang harus ditulis dari text.txt
correct_char adalah karakter dari index tertentu di target
            '''
            color = curses.color_pair(1) #pair 1 hijau, kalau benar munculnya hijau
            if char != correct_char:
                color = curses.color_pair(2) #pair 2 merah, kalau charnya yg diketik user salah/ beda dgn char yg di target text, munculnya warna merah

            stdscr.addstr(start_y, start_x + i, char, color) #text muncul di screen

def is_exit_key(key):
    return key.lower() == 'q'

def wpm_test(stdscr):
    target_text = load_text()  #target textnya itu random line dari text.txt
    current_text = [] #list yg menyimpan input user
    wpm = 0 #wpm awalnya 0
    start_time = time.time() #waktu mulai dhitung

    while True:
        curses.echo()  #echo biar user input langsung muncul di layar pas diketik
        time_elapsed = max(time.time() - start_time, 1)
        
        word_count = len("".join(current_text).split()) #ngehitung jumlah karakter yg diketik
        wpm = round((word_count / (time_elapsed / 60))) #ngehitung wppm berdasarkan karakter yg ditulis dan waktu yg udah ke record

        stdscr.clear()
        display_text(stdscr, target_text, current_text, wpm)
        stdscr.refresh()

        if "".join(current_text) == target_text: #kalau user udah ketik semua kalimat yg hrs diketik dgn benar, loopnya break
            curses.noecho()  
            stdscr.nodelay(False)
            break
        try:
            key = stdscr.getkey()
        except:
            continue

        if is_exit_key(key): #kalau user ngetik q, berarti keluar.
            curses.noecho() #q nya gak muncul, karena noecho
            return 'q'

        curses.noecho()

        if key in ("KEY_BACKSPACE", '\b', "\x7f"): #kalau backspace dipencet
            if len(current_text) > 0: #cek, ada karakter atau enggak di current text
                current_text.pop()
        elif len(current_text) < len(target_text): #kalau keynya bukan backspace
            current_text.append(key)

def main(stdscr): 
    curses.start_color() #Initialize color support di terminal
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)#warna hijau di background hitam
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)

    start_screen(stdscr) #start_screen function di panggil buat menunjukkan welcome screen
    
    while True:
        result = wpm_test(stdscr) #fungsi wpm_test dipanggil
        
        if result == 'q': #kalau q dipencet, langsung break
            break
        
        stdscr.addstr(6, 0, "You completed the text! Press 'c' to continue or 'q' to exit.")
        
        while True:
            key = stdscr.getch()
            if key == ord('c'):
                break
            elif key == ord('q'):
                stdscr.addstr(6, 0, "You pressed 'q'. Press any key to exit.")
                stdscr.getch()
                return

curses.wrapper(main)

