from chesswar import Board
from player_models import *
from score_heuristics import *
import curses
from curses import wrapper
import time
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
# import time
# import glob
import os
# import shutil

p1, p2, piece1, piece2 = 'AI AlphaBeta', 'AI Minimax', 'bishop', 'knight'
flag = False

def choose_piece(stdscr, win, n):
    pieces = ['bishop', 'knight', 'rook', 'queen']
    flag = False
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    YELLOW = curses.color_pair(3)

    while not flag:
        win.clear()
        for i in range(len(pieces)):
            win.addstr(i+5, 20, f'{i+1} : {pieces[i]}', YELLOW)
        win.refresh()

        win.addstr(1, 0, f"Select Player {n} piece: ")
        win.refresh()
        val = ""
        while True:
            key = chr(stdscr.getch())
            if(key == '\n'):
                break
            val += key
            win.addstr(key)
            win.refresh()
        try:
            pl1 = pieces[int(val)-1]
            flag = True
        except:
            win.clear()
            win.addstr("Invalid choice, please choose again!")
            win.refresh()
    return pl1

def choose_player(stdscr, win, n):
    players = ['Human', 'Random', 'AI AlphaBeta', 'AI Minimax']
    flag = False
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    YELLOW = curses.color_pair(3)

    while not flag:
        win.clear()
        for i in range(len(players)):
            win.addstr(i+5, 20, f'{i+1} : {players[i]}', YELLOW)
        win.refresh()

        win.addstr(0, 0, f"Select Player {n} : ")
        win.refresh()
        val = ""
        while True:
            key = chr(stdscr.getch())
            if(key == '\n'):
                break
            val += key
            win.addstr(key)
            win.refresh()
        try:
            pl1 = players[int(val)-1]
            flag = True
        except:
            val = "Invalid choice, please choose again!"
            stdscr.refresh()
    return pl1

def main(stdscr):
    global p1, p2, piece1, piece2, flag
    stdscr.clear()

    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
    CYAN_TEXT = curses.color_pair(1)
    
    stdscr.addstr(2, 55, "Chess Piece Wars", CYAN_TEXT | curses.A_BOLD)
    stdscr.refresh()
    time.sleep(1)

    begin_x = 3; begin_y = 3
    height = 23; width = 40
    try:
        win = curses.newwin(height, width, begin_y, begin_x)
    except curses.error:
        raise RuntimeError("Inadequate terminal size, please resize to atleast 80x80 (Preferably open a fullscreen terminal) !")

    piece1 = choose_piece(stdscr, win, 1)
    piece2 = choose_piece(stdscr, win, 2)

    players_dict = {'AI AlphaBeta' : AlphaBetaPlayer(), 'AI Minimax' : MinimaxPlayer(), 'Human' : HumanPlayer(), 'Random' : RandomPlayer()}
    
    p1 = choose_player(stdscr, win, 1)
    p2 = choose_player(stdscr, win, 2)
    player1 = players_dict[p1]
    player2 = players_dict[p2]
    win.clear()
    stdscr.clear()
    
    stdscr.addstr(2, 55, "Chess Piece Wars", CYAN_TEXT | curses.A_BOLD)

    stdscr.addstr(5, 5, f"Player 1 : {p1} ({piece1})")
    stdscr.addstr(6, 5, f"Player 2 : {p2} ({piece2})")
    stdscr.refresh()
    time.sleep(1)

    begin_x = 10; begin_y = 10
    height = 40; width = 60
    try:
        win2 = curses.newwin(height, width, begin_y, begin_x)
    except curses.error:
        RuntimeError("Inadequate terminal size, please resize to atleast 80x80 (Preferably open a fullscreen terminal) !")


    if (p1 == 'Human' or p2 == 'Human'):
        stdscr.addstr(2, 55, "Chess Piece Wars", CYAN_TEXT | curses.A_BOLD)

        stdscr.addstr(5, 5, f"Player 1 : {p1} ({piece1})")
        stdscr.addstr(6, 5, f"Player 2 : {p2} ({piece2})")
        stdscr.refresh()
        time.sleep(1)

        begin_x = 10; begin_y = 10
        height = 40; width = 60
        win2 = curses.newwin(height, width, begin_y, begin_x)

        
        game = Board(player1, player2, player_1_piece=piece1, player_2_piece=piece2)

        game.apply_move((0, 0))
        game.apply_move((6, 6))

        win2.clear()
        win2.addstr(0, 0, game.to_string())
        win2.refresh()
        time.sleep(3)

        assert(player1 == game.active_player)

        winner, history, outcome = game.play(print_steps=True, stdscr=win2)
        win2.addstr("\n\nWinner: {}\nOutcome: {}".format('Player1' if (winner==player1) else 'Player2', outcome))
        win2.refresh()

        stdscr.addstr(40, 2, "Press any key to exit", curses.A_REVERSE)
        stdscr.refresh()

        stdscr.getch()

        print("\nWinner: {}\nOutcome: {}".format('Player1' if (winner==player1) else 'Player2', outcome))
        print(game.to_string())
        print("Move history:\n{!s}".format(history))
    else:
        flag = True
        game = Board(player1, player2, player_1_piece=piece1, player_2_piece=piece2)

        game.apply_move((0, 0))
        game.apply_move((6, 6))
        winner, history, outcome = game.play(time_limit=500)

wrapper(main)

if flag:
    # chrome_options = Options()
    # prefs = {
    #     "download.prompt_for_download": False,
    #     "download.directory_upgrade": True,
    #     "safebrowsing.enabled": True
    # }

    # chrome_options.add_experimental_option("prefs", prefs)
    # browser = webdriver.Chrome(chrome_options=chrome_options)
    browser = webdriver.Chrome()

    browser.get('https://toonme.com/')
    wait = WebDriverWait(browser, 600)

    image_number = 11266
    end_number = 12515

    while image_number <= end_number:
        browser.get('https://cyantarantula.github.io/StaleMate/')

        upload_btn = wait.until((ec.presence_of_element_located((By.CLASS_NAME, 'file-field-hidden'))))
        upload_btn.send_keys("D:/temp2/temp2/face/" + str(image_number) + ".png")

        try: 
            print("here1")
            toon_type_btn = wait.until((ec.presence_of_element_located((By.CLASS_NAME, "collage__tab_tab210622"))))
            toon_type_btn.click()

            print("here2")

            list_of_files_png = glob.glob('C:/Users/hp/Downloads/*.png')
            old_latest_file_png = max(list_of_files_png, key=os.path.getctime)

            list_of_files_jpeg = glob.glob('C:/Users/hp/Downloads/*.jpeg')
            old_latest_file_jpeg = max(list_of_files_jpeg, key=os.path.getctime)
            
            list_of_all_files = glob.glob('C:/Users/hp/Downloads/*')
            any_old_latest_file = max(list_of_all_files, key=os.path.getctime)

            download_btn = wait.until((ec.presence_of_element_located((By.CLASS_NAME, "btn-upload-foto-result"))))
            download_btn.click()
            time.sleep(7)

            while True:       
                print("here3") 
                list_of_files_png = glob.glob('C:/Users/hp/Downloads/*.png')
                new_latest_file_png = max(list_of_files_png, key=os.path.getctime)

                list_of_files_jpeg = glob.glob('C:/Users/hp/Downloads/*.jpeg')
                new_latest_file_jpeg = max(list_of_files_jpeg, key=os.path.getctime)


                list_of_all_files = glob.glob('C:/Users/hp/Downloads/*')
                any_new_latest_file = max(list_of_all_files, key=os.path.getctime)

                if old_latest_file_png != new_latest_file_png:
                    print(new_latest_file_png)
                    try:
                        shutil.move(str(new_latest_file_png), 'D:/temp2/temp2/toon/' + str(image_number) + '.png')
                    except:
                        print("71")
                        break
                    
                    time.sleep(0.5)
                    print("74")
                    break

                elif old_latest_file_jpeg != new_latest_file_jpeg:
                    print(new_latest_file_jpeg)
                    try:
                        shutil.move(str(new_latest_file_jpeg), 'D:/temp2/temp2/toon/' + str(image_number) + '.jpeg')
                    except:
                        print("82")
                        break
                    
                    time.sleep(0.5)
                    print("86")
                    break

                
                elif (any_old_latest_file != any_new_latest_file):
                    print(any_new_latest_file)
                    print("92")
                    break


                    
        except:
            print("error")
            pass

        image_number += 1