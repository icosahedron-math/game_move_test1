import keyboard

from random import randint
from colorama import Fore
from time import sleep
from os import system, name

UNIT = f'{Fore.BLUE}@'
ENEMY = f'{Fore.RED}@'
BOX = ' '
WALL = f'{Fore.GREEN}#'
TELEPORT = f'{Fore.CYAN}#'

def red_moving(rows):
    c = 0
    if randint(0,1) == 0:
        w = -1
    else:
        w = 1
    if randint(0,1) == 0:
        # w_move
        for row in rows:
            try:   
                ind = row.index(ENEMY)
            except ValueError:
                pass
            else:
                try:
                    if ind+w <= -1:
                        pass
                    if rows[c][ind+w] not in(WALL, UNIT, TELEPORT):
                        rows[c][ind], rows[c][ind+w] = rows[c][ind+w], rows[c][ind]
                    return rows
                except IndexError:
                    pass
            c+=1
    else:
        # h_move
        for row in rows:
            try:   
                ind = row.index(ENEMY)
            except ValueError:
                pass
            else:
                try:
                    if ind+w <= -1:
                        pass
                    if rows[c+w][ind] not in(WALL, UNIT, TELEPORT):
                        rows[c][ind], rows[c+w][ind] = rows[c+w][ind], rows[c][ind]
                    return rows
                except IndexError:
                    pass
            c+=1


class Commands():
    def w_move(self, rows, w):
        c = 0
        for row in rows:
            try:
                ind = row.index(UNIT)
            except ValueError:
                pass
            else:
                try:
                    if ind+w <= -1:
                        pass
                    else:
                        rows = red_moving(rows)
                        if rows[c][ind+w] == WALL:
                            break
                        if rows[c][ind+w] == ENEMY:
                            rows[c][ind+w] = BOX
                            while True:
                                x = randint(0,len(rows)-1)
                                y = randint(0,len(row)-1)
                                if rows[x][y] not in(WALL, UNIT, TELEPORT):
                                    rows[x][y] = ENEMY
                                    break
                            self.kill_count+=1
                        if rows[c][ind+w] == TELEPORT:
                            while True:
                                x = randint(0,len(rows)-1)
                                y = randint(0,len(row)-1)
                                if rows[x][y] not in(WALL, TELEPORT, ENEMY):
                                    rows[c][ind], rows[x][y] = rows[x][y], rows[c][ind]
                                    self.x = y-1
                                    self.y = x-1
                                    return rows, self.x, self.y
                        rows[c][ind], rows[c][ind+w] = rows[c][ind+w], rows[c][ind]
                        self.x = self.x + w
                    return rows, self.x
                except IndexError:
                    pass
            c+=1

    def h_move(self, rows, w):
        c = 0
        for row in rows:
            try:
                ind = row.index(UNIT)
            except ValueError:
                pass
            else:
                try:
                    if c-w <= -1:
                        pass
                    else:
                        rows = red_moving(rows)
                        if rows[c-w][ind] == WALL:
                            break
                        if rows[c-w][ind] == ENEMY:
                            rows[c-w][ind] = BOX
                            while True:
                                x = randint(0,len(rows)-1)
                                y = randint(0,len(row)-1)
                                if rows[x][y] not in(WALL, UNIT, TELEPORT):
                                    rows[x][y] = ENEMY
                                    break
                            self.kill_count+=1
                        if rows[c-w][ind] == TELEPORT:
                            while True:
                                x = randint(0,len(rows)-1)
                                y = randint(0,len(row)-1)
                                if rows[x][y] not in(WALL, TELEPORT, ENEMY):
                                    rows[c][ind], rows[x][y] = rows[x][y], rows[c][ind]
                                    self.x = y-1
                                    self.y = x-1
                                    return rows, self.x, self.y
                        rows[c][ind], rows[c-w][ind] = rows[c-w][ind], rows[c][ind]
                        self.y = self.y - w
                    return rows, self.y
                except IndexError:
                    pass
            c+=1


def get_map(row_len, walls_procent):
    rows = []
    for __ in range(row_len):
                row = []
                for _ in range(row_len*2):
                    if __ == 0:
                        row.append(WALL)
                    elif __ == row_len-1:
                        row.append(WALL)
                    else:
                        if _ == 0:
                            row.append(WALL)
                        elif _ == row_len*2-1:
                            row.append(WALL)
                        else:
                            if randint(0, walls_procent) == 0:
                                row.append(WALL)
                            else:
                                row.append(BOX)
                rows.append(row)
    rows[1][1] = UNIT
    while True:
        x = randint(0,len(rows)-1)
        y = randint(0,len(row)-1)
        if rows[x][y] not in(WALL, UNIT):
            rows[x][y] = ENEMY
            break
    for _ in range(2):
        while True:
            x = randint(0,len(rows)-1)
            y = randint(0,len(row)-1)
            if rows[x][y] not in(WALL, UNIT, ENEMY, TELEPORT):
                rows[x][y] = TELEPORT
                break
    return rows
    

class Main(Commands):
    def __init__(self) -> None:
        print(f'{Fore.GREEN}World maker')
        try:
            self.row_len = int(input(f'{Fore.BLUE}Map size (5-20)= {Fore.GREEN}'))
            self.row_len += 3
            if self.row_len <= 5:
                self.row_len = 5
            elif self.row_len >= 21:
                self.row_len = 20
            print(1)
        except:
            self.row_len = 20
        try:
            self.walls_procent = int(input(f'{Fore.BLUE}Wals procent (1-9)= {Fore.GREEN}'))
            if self.walls_procent <= 1:
                self.walls_procent = 1
            elif self.walls_procent >= 9:
                self.walls_procent = 9
            self.walls_procent%=10
        except:
            self.walls_procent = 7
        self.kill_count = 0
        self.x = 0
        self.y = 0
        self.red_move = 0
        self.move_count = 0
        self.move_to_jump = 30
        self.active = 'right'
        self.rows = get_map(self.row_len, self.walls_procent)
        self.left = f'{Fore.MAGENTA}left'
        self.right = f'{Fore.LIGHTMAGENTA_EX}right'
        self.down = f'{Fore.MAGENTA}down'
        self.up = f'{Fore.MAGENTA}up'
        
    
    def worker(self, com: str):
        # analysis and work command
        if com in ('shift', 'space'):
            if self.active == 'left':
                com = 'left'
                self.w_move(self.rows, -3)
            elif self.active == 'right':
                com = 'right'
                self.w_move(self.rows, 3)
            elif self.active == 'down':
                com = 'down'
                self.h_move(self.rows, -3)
            elif self.active == 'up':
                com = 'up'
                self.h_move(self.rows, 3)
            sleep(0.05)
        if com in ('r', 'к'):
            self.x = 1
            self.y = 1
            self.rows = get_map(self.row_len, self.walls_procent)
        if com in ('right', 'd', 'в'):
            com = 'right'
            self.w_move(self.rows, 1)
        if com in ('left', 'a', 'ф'):
            com = 'left'
            self.w_move(self.rows, -1)
        if com in ('down', 's', 'ы'):
            com = 'down'
            self.h_move(self.rows, -1)
        if com in ('up', 'w', 'ц'):
            com = 'up'
            self.h_move(self.rows, 1)
        for i in ('left','right','down','up'):
            if i == com:
                self.active = i
                exec(f'self.{i} = \'{Fore.LIGHTMAGENTA_EX}{i}\'')
            else:
                exec(f'self.{i} = \'{Fore.MAGENTA}{i}\'')


    def interface(self):
        while True:
            # make interface
            interf = (
                f"{Fore.CYAN}{'='*(self.row_len*2)}\n"
                f"{Fore.BLUE}x = {Fore.MAGENTA}{str(self.x)}\n"
                f"{Fore.BLUE}y = {Fore.MAGENTA}{str(self.y)}\n"
                f"{Fore.BLUE}Kills = {Fore.MAGENTA}{str(self.kill_count)}\n"
                f"{Fore.BLUE}Move count = {Fore.MAGENTA}{str(self.move_count)}\n"
                f"{Fore.BLUE}Move to jump = {Fore.MAGENTA}{str(self.move_to_jump)}\n"
                f"{Fore.CYAN}{'='*(self.row_len*2)}\n"
                f"{self.left} {self.right} {self.down} {self.up}"
            )
            # draw map
            rows_map = ''
            for i in self.rows:
                for ii in i:
                    rows_map+=ii
                rows_map+='\n'
            # clear ritual
            if name == "posix":
                system('clear')
            elif name in ("nt", "dos", "ce"):
                system(f'CLS')
            print(rows_map)
            print(interf)

            # get command
            while True:
                com = keyboard.read_key()
                if com in ('shift', 'space'):
                    if self.move_to_jump == f'{Fore.GREEN}JUMP!':
                        self.move_to_jump = 30
                        self.worker(com)
                        self.move_count += 1
                        self.red_move = self.move_count%2
                        break
                if com in ('right', 'd', 'в', 'left', 'a', 'ф', 'down', 's', 'ы', 'up', 'w', 'ц', 'r', 'к'):
                    self.worker(com)
                    self.red_move = self.move_count%2
                    self.move_count += 1
                    if self.move_to_jump != f'{Fore.GREEN}JUMP!':
                        self.move_to_jump -= 1
                        if self.move_to_jump == 0:
                            self.move_to_jump = f'{Fore.GREEN}JUMP!'
                    break


if __name__ == '__main__':
    main = Main()
    main.interface()

