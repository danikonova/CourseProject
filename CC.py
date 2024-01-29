import os
from tkinter import *
import random
import time
import copy
from tkinter import messagebox, ttk

# ---------------------------------------- Глобально --------------------------------------
fa = None
file_name = 'registry.txt'

bg_color = 'gray10'
fg_color = 'bisque'
menu_fg = "snow"

def load_images():  # загружаем изображения шашек
    global pieces
    img1 = PhotoImage(file="w.png")
    img2 = PhotoImage(file="wq.png")
    img3 = PhotoImage(file="b.png")
    img4 = PhotoImage(file="bq.png")
    pieces = [0, img1, img2, img3, img4]

# ------------------------------------------------ Шифрование ---------------------------------------------------------
def cesar(txt):
    code = 0
    for ch in txt:
        code += ord(ch)
    code += 128
    return code

def encrypt(txt, code):
    result = ""
    for c in txt:
        result += chr(ord(c) + code)
    return result

def decrypt(txt, code):
    result = ""
    for c in txt:
        result += chr(ord(c) - code)
    return result

current_user = None

# ---------------------------------------- Игра --------------------------------------------
WIDTH = 792
HEIGHT = 792
ROWS = 12
COLUMNS = 12
mx = 66
my = 66

# ------------------------------------------------ GUI -------------------------------------
class SampleApp(Tk):
    def __init__(self):
        Tk.__init__(self)

        self.title('Канадские шашки')
        # self.geometry(str(WIDTH) + 'x' + str(HEIGHT))
        self.resizable(0, 0)
        self.configure(bg=bg_color)

        global user, password
        user = StringVar()
        password = StringVar()
        user.set('a')

        menubar = MenuBar(self)
        self.config(menu=menubar)

        self._frame = None
        self.switch_frame(Login_page)

    def switch_frame(self, frame_class):
        global new_frame
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack(anchor='center')

    def switch_window(self, window_class):
        global new_window
        new_window = window_class(self)
        # self.withdraw()


# ------------------------------------------------ Меню ------------------------------------
class MenuBar(Menu):
    def __init__(self, parent):
        Menu.__init__(self, parent)

        self.add_cascade(label="Регистрация", command=lambda: parent.switch_frame(Sign_up_page))
        self.add_cascade(label="Сменить аккаунт", command=lambda: parent.switch_frame(Login_page))
        self.add_cascade(label="Играть", command=lambda: parent.switch_window(Game_page))
        self.add_separator()
        self.add_cascade(label="Выход", command=lambda: parent.destroy())


# ---------------------------------------------- Логин ------------------------------------
class Login_page(Frame, Menu):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.config(bg=bg_color)
        # self.pack(expand=True)

        global fa
        fa = Login_page

        style1 = ttk.Style()
        style1.configure('TLabel', background=bg_color, foreground=fg_color, font='Calibri 20')

        global user, password, current_user
        user = StringVar()
        password = StringVar()

        frame1 = Frame(self, bg=bg_color)
        frame1.grid(row=0, column=0)

        ttk.Label(frame1, text='ВХОД', style='login.TLabel').grid(row=0, column=1, pady=(150, 5), padx=(8, 0))

        frame3 = Frame(self, bg=bg_color)
        frame3.grid(row=1, column=0)
        ttk.Label(frame3, text='ИМЯ ПОЛЬЗОВАТЕЛЯ', style='TLabel').grid(row=1, column=0, pady=(50, 10))
        ttk.Label(frame3, text='ПАРОЛЬ ', style='TLabel').grid(row=2, column=0, )
        ttk.Entry(frame3, textvariable=user, width=30).grid(row=1, column=2, pady=(50, 10), padx=(20, 10))
        p = ttk.Entry(frame3, textvariable=password, width=30)
        p.grid(row=2, column=2, padx=(12, 2))
        p.config(show='*')
        self.x = 1

        style = ttk.Style()
        style.configure('a.TButton', background=fg_color, borderwidth=35)

        frame2 = Frame(self, bg=bg_color)
        frame2.grid(row=2, column=0, pady=35)
        ttk.Button(frame2, text='Регистрация', command=lambda: master.switch_frame(Sign_up_page),
                   style='a.TButton').pack(side=LEFT, padx=8)
        ttk.Button(frame2, text='Вход', command=lambda: self.enter(master), style='a.TButton').pack(side=RIGHT, padx=8)

    def enter(self, master):
        global current_user
        if os.path.isfile(file_name):
            with open(file_name, 'r', encoding='utf-16') as f:
                data = f.readlines()
                flag = False
                for line in data:
                    if line[0:line.find(' ')] == user.get():
                        p = decrypt(line[line.find(' ') + 1:len(line) - 1], cesar(user.get()))
                        if p == password.get():
                            current_user = user.get()
                            flag = True
                        break
            if flag:
                messagebox.showinfo("Давайте играть!", f"Приветствую, {current_user}!")
                master.switch_window(Game_page)
            else:
                messagebox.showerror("Ошибка", "Имя пользователя или пароль введены неверно")
                user.set('')
                password.set('')
        else:
            messagebox.showerror("Ошибка", "Имя пользователя или пароль введены неверно")
            user.set('')
            password.set('')


class Sign_up_page(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)
        Frame.configure(self, bg=bg_color)
        global fa
        fa = Sign_up_page

        global newuser, newpassword
        newuser = StringVar()
        newpassword = StringVar()

        frame1 = Frame(self, bg=bg_color)
        frame1.grid(row=0, column=0)
        # frame = Frame(self, bg=bg_color).grid(row=0, column=2)
        style = ttk.Style()
        style.configure('TButton', background='slateblue', borderwidth=30)

        Style1 = ttk.Style()
        Style1.configure('TLabel', background=bg_color, foreground='slateblue', font='Calibri 20')
        ttk.Label(frame1, text='РЕГИСТРАЦИЯ', style='login.TLabel').grid(row=0, column=1, pady=(150, 5), padx=(8, 0))

        frame3 = Frame(self, bg=bg_color)
        frame3.grid(row=1, column=0)
        ttk.Label(frame3, text='ИМЯ ПОЛЬЗОВАТЕЛЯ', style='TLabel').grid(row=1, column=0, pady=(50, 10))
        ttk.Label(frame3, text='ПАРОЛЬ ', style='TLabel').grid(row=2, column=0)
        ttk.Entry(frame3, textvariable=newuser, width=30).grid(row=1, column=2, pady=(50, 10), padx=(20, 10))
        p = ttk.Entry(frame3, textvariable=newpassword, width=30)
        p.grid(row=2, column=2, padx=(20, 10))
        p.config(show="")
        self.x = 2

        frame2 = Frame(self, bg=bg_color)
        frame2.grid(row=2, column=0, pady=35)
        ttk.Button(frame2,
                   text='Зарегистрироваться',
                   command=lambda: self.sign_up(master),
                   style='TButton').grid(row=0, column=0)

        (ttk.Button(frame2, text='Назад',
                   command=lambda: master.switch_frame(Login_page),
                   style='TButton').grid(row=0, column=1, padx=20))
    def sign_up(self, master):
        new_user = newuser.get()

        if new_user == '':
            messagebox.showerror('Ошибка ввода', 'Введите действительное имя пользователя')
        else:
            if newpassword.get() == '':
                messagebox.showerror('Ошибка ввода', 'Поле ввода пароля не может быть пустым.')
            else:
                if not os.path.isfile(file_name):
                    with open(file_name, 'w', encoding='utf-16') as f:
                        pass

                with open(file_name, 'r', encoding='utf-16') as f:
                    existing_users = [line.split()[0] for line in f]

                if new_user in existing_users:
                    messagebox.showerror('Ошибка', 'Пользователь с таким именем уже существует.')
                else:
                    with open(file_name, 'a', encoding='utf-16') as f:
                        res = new_user + ' ' + encrypt(newpassword.get(), cesar(new_user)) + '\n'
                        f.write(res)

                    messagebox.showinfo('Успешно', 'Аккаунт был успешно добавлен\nПожалуйста, войдите в систему')
                    master.switch_frame(Login_page)
   
# --------------------------------------- Игра ---------------------------------------------
comp_moves_f_list = ()  # конечный список ходов компьютера
deep_mind = 2  # количество предсказываемых компьютером ходов
k_res = 0  
o_res = 0
pos1_x = -1  # клетка не задана

def on_close(window):
    # window.deiconify()
    window.destroy()

class Game_page():

    moveable = True  # определение хода игрока(да)

    def __init__(self, master):
        game_window = Toplevel(master)
        # Frame.__init__(self, master)
        # Frame.configure(self, bg=bg_color)
        game_window.title("Канадские шашки")
        game_window.resizable(0, 0)
        game_window.wm_attributes("-topmost", 1)
        game_window.protocol("WM_DELETE_WINDOW", lambda window=game_window: on_close(window))
        # global fa
        # fa = Game_page

        global board
        board = Canvas(game_window, width=WIDTH, height=HEIGHT, bg="white")
        board.pack()

        load_images()  # здесь загружаем изображения шашек

        self.new_game()  # начинаем новую игру
        self.draw_board(-1, -1, -1, -1)  # рисуем игровое поле
        board.bind("<Motion>", self.mouse_pos_from)  # движение мышки по полю
        board.bind("<Button-1>", self.mouse_pos_to)  # нажатие левой кнопки

    def new_game(self):  # начинаем новую игру
        global scene
        scene = [[0 for _ in range(ROWS)] for _ in range(COLUMNS)]

        for row in range(ROWS):
            for col in range(COLUMNS):
                if row < (ROWS - 2) / 2 and (row + col) % 2 == 1:
                    scene[row][col] = 3
                if row >= (ROWS + 2) / 2 and (row + col) % 2 == 1:
                    scene[row][col] = 1

    def draw_board(self, x_pos_1, y_pos_1, x_pos_2, y_pos_2):  # рисуем игровое поле
        global pieces
        global scene
        global red_frame, green_frame
        k = WIDTH / ROWS
        x = 0
        board.delete('all')
        red_frame = board.create_rectangle(-5, -5, -5, -5, outline="red", width=12)
        green_frame = board.create_rectangle(-5, -5, -5, -5, outline="green", width=12)

        while x < WIDTH:  # рисуем доску
            y = k
            while y < HEIGHT:
                board.create_rectangle(x, y, x + k, y + k, fill="black")
                y += 2 * k
            x += 2 * k
        x = k
        while x < WIDTH:  # рисуем доску
            y = 0
            while y < HEIGHT:
                board.create_rectangle(x, y, x + k, y + k, fill="black")
                y += 2 * k
            x += 2 * k

        for y in range(ROWS):  # рисуем стоячие шашки
            for x in range(COLUMNS):
                z = scene[y][x]
                if z:
                    if (x_pos_1, y_pos_1) != (x, y):  # стоячие шашки?
                        board.create_image(x * k, y * k, anchor=NW, image=pieces[z])
        # рисуем активную шашку
        z = scene[y_pos_1][x_pos_1]
        if z:  # ???
            board.create_image(x_pos_1 * k, y_pos_1 * k, anchor=NW, image=pieces[z], tag='ani')
        # вычисление коэф. для анимации
        kx = 1 if x_pos_1 < x_pos_2 else -1
        ky = 1 if y_pos_1 < y_pos_2 else -1
        for i in range(abs(x_pos_1 - x_pos_2)):  # анимация перемещения шашки
            for j in range(33):
                board.move('ani', 0.03 * k * kx, 0.03 * k * ky)
                board.update()  # обновление
                time.sleep(0.01)

    def message(self, s):
        z = 'Игра завершена'
        if s == 1:
            i = messagebox.askyesno(title=z, message='Вы победили!\nНажми "Да" что бы начать заново.', icon='info')
        if s == 2:
            i = messagebox.askyesno(title=z, message='Вы проиграли!\nНажми "Да" что бы начать заново.', icon='info')
        if s == 3:
            i = messagebox.askyesno(title=z, message='Ходов больше нет.\nНажми "Да" что бы начать заново.', icon='info')
        self.new_game()
        self.draw_board(-1, -1, -1, -1)  # рисуем игровое поле
        self.moveable = True  # ход игрока доступен

    def mouse_pos_from(self, event):  # выбор клетки для хода 1
        x, y = event.x // mx, event.y // my  # вычисляем координаты клетки
        board.coords(green_frame, x * mx, y * my, x * mx + mx, y * my + my)  # рамка в выбранной клетке

    def mouse_pos_to(self, event):  # выбор клетки для хода 2
        global pos1_x, pos1_y, pos2_x, pos2_y

        x, y = event.x // mx, event.y // my  # вычисляем координаты клетки
        if scene[y][x] == 1 or scene[y][x] == 2:  # проверяем шашку игрока в выбранной клетке
            board.coords(red_frame, x * mx, y * my, x * mx + mx, y * my + my)  # рамка в выбранной клетке
            pos1_x, pos1_y = x, y
        else:
            if pos1_x != -1:  # клетка выбрана
                pos2_x, pos2_y = x, y
                if self.moveable:  # ход игрока?
                    self.player_move()
                    if not self.moveable:
                        time.sleep(0.5)
                        self.comp_move()  # передаём ход компьютеру
                pos1_x = -1  # клетка не выбрана
                board.coords(red_frame, -5, -5, -5, -5)  # рамка вне поля

    def comp_move(self):  # !!!

        global comp_moves_f_list
        self.check_comp_move(1, (), [])
        if comp_moves_f_list:  # проверяем наличие доступных ходов
            count_moves = len(comp_moves_f_list)  # количество ходов
            t_move = random.randint(0, count_moves - 1)  # случайный ход
            len_move = len(comp_moves_f_list[t_move])  # длина хода
            for i in range(len_move - 1):
                # выполняем ход
                self.turn(1, comp_moves_f_list[t_move][i][0], comp_moves_f_list[t_move][i][1],
                     comp_moves_f_list[t_move][1 + i][0], comp_moves_f_list[t_move][1 + i][1])
            comp_moves_f_list = []  # очищаем список ходов
            self.moveable = True  # ход игрока доступен

        # определяем победителя
        comp_scores, player_scores = self.check()
        if not player_scores:
            self.message(2)
        elif not comp_scores:
            self.message(1)
        elif self.moveable and not self.player_moves_list():
            self.message(3)
        elif not self.moveable and not self.comp_moves_list():
            self.message(3)

    def comp_moves_list(self):  # составляем список ходов компьютера
        moves_list = self.check_comp_mandatory_moves([])  # здесь проверяем обязательные ходы
        if not moves_list:
            moves_list = self.check_left_comp_moves([])  # здесь проверяем оставшиеся ходы
        return moves_list

    def check_comp_move(self, tur, n_list, moves_list):  # !!!
        global scene
        global comp_moves_f_list
        global best_res, k_res, o_res
        if not moves_list:  # если список ходов пустой...
            moves_list = self.comp_moves_list()  # заполняем

        if moves_list:
            k_scene = copy.deepcopy(scene)  # копируем поле
            for ((pos1_x, pos1_y), (pos2_x, pos2_y)) in moves_list:  # проходим все ходы по списку
                t_list = self.turn(0, pos1_x, pos1_y, pos2_x, pos2_y)
                if t_list:  # если существует ещё ход
                    self.check_comp_move(tur, (n_list + ((pos1_x, pos1_y),)), t_list)
                else:
                    self.check_player_move(tur, [])
                    if tur == 1:
                        t_res = o_res / k_res
                        if not (comp_moves_f_list):  # записыаем если пустой
                            comp_moves_f_list = (n_list + ((pos1_x, pos1_y), (pos2_x, pos2_y)),)
                            best_res = t_res  # сохряняем наилучший результат
                        else:
                            if t_res == best_res:
                                comp_moves_f_list = comp_moves_f_list + (n_list + ((pos1_x, pos1_y), (pos2_x, pos2_y)),)
                            if t_res > best_res:
                                comp_moves_f_list = ()
                                comp_moves_f_list = (n_list + ((pos1_x, pos1_y), (pos2_x, pos2_y)),)
                                best_res = t_res  # сохряняем наилучший результат
                        o_res = 0
                        k_res = 0

                scene = copy.deepcopy(k_scene)  # возвращаем поле
        else:  # ???
            comp_scores, player_scores = self.check()  # подсчёт результата хода
            o_res += (comp_scores - player_scores)
            k_res += 1

    def player_moves_list(self):  # составляем список ходов игрока
        moves_list = self.check_player_mandatory_moves([])  # здесь проверяем обязательные ходы
        if not moves_list:
            moves_list = self.check_left_player_moves([])  # здесь проверяем оставшиеся ходы
        return moves_list

    def check_player_move(self, tur, moves_list):
        global scene, k_res, o_res
        global deep_mind
        if not moves_list:
            moves_list = self.player_moves_list()

        if moves_list:  # проверяем наличие доступных ходов
            k_scene = copy.deepcopy(scene)  # копируем поле
            for ((pos1_x, pos1_y), (pos2_x, pos2_y)) in moves_list:
                t_list = self.turn(0, pos1_x, pos1_y, pos2_x, pos2_y)
                if t_list:  # если существует ещё ход
                    self.check_player_move(tur, t_list)
                else:
                    if tur < deep_mind:
                        self.check_comp_move(tur + 1, (), [])
                    else:
                        comp_scores, player_scores = self.check()  # подсчёт результата хода
                        o_res += (comp_scores - player_scores)
                        k_res += 1

                scene = copy.deepcopy(k_scene)  # возвращаем поле
        else:  # доступных ходов нет
            comp_scores, player_scores = self.check()  # подсчёт результата хода
            o_res += (comp_scores - player_scores)
            k_res += 1

    def check(self):  # подсчёт шашек на поле
        global scene
        score_player = 0
        score_comp = 0
        for i in range(ROWS):
            for j in scene[i]:
                if j == 1: score_player += 1
                if j == 2: score_player += 3
                if j == 3: score_comp += 1
                if j == 4: score_comp += 3
        return score_comp, score_player

    def player_move(self):
        global pos1_x, pos1_y, pos2_x, pos2_y

        self.moveable = False  # считаем ход игрока выполненным
        moves_list = self.player_moves_list()
        if moves_list:
            if ((pos1_x, pos1_y), (pos2_x, pos2_y)) in moves_list:  # проверяем ход на соответствие правилам игры
                t_list = self.turn(1, pos1_x, pos1_y, pos2_x, pos2_y)  # если всё хорошо, делаем ход
                if t_list:  # если есть ещё ход той же шашкой
                    self.moveable = True  # считаем ход игрока невыполненным
            else:
                self.moveable = True  # считаем ход игрока невыполненным
        board.update()  # !!!обновление

    def turn(self, flag, pos1_x, pos1_y, pos2_x, pos2_y):
        global scene
        if flag: self.draw_board(pos1_x, pos1_y, pos2_x, pos2_y)  # рисуем игровое поле
        # превращение
        if pos2_y == 0 and scene[pos1_y][pos1_x] == 1:
            scene[pos1_y][pos1_x] = 2
        # превращение
        if pos2_y == ROWS - 1 and scene[pos1_y][pos1_x] == 3:
            scene[pos1_y][pos1_x] = 4
        # делаем ход
        scene[pos2_y][pos2_x] = scene[pos1_y][pos1_x]
        scene[pos1_y][pos1_x] = 0

        # рубим шашку игрока
        kx = ky = 1
        if pos1_x < pos2_x: kx = -1
        if pos1_y < pos2_y: ky = -1
        x_pos, y_pos = pos2_x, pos2_y
        while (pos1_x != x_pos) or (pos1_y != y_pos):
            x_pos += kx
            y_pos += ky
            if scene[y_pos][x_pos] != 0:
                scene[y_pos][x_pos] = 0
                if flag: self.draw_board(-1, -1, -1, -1)  # рисуем игровое поле
                # проверяем ход той же шашкой...
                if scene[pos2_y][pos2_x] == 3 or scene[pos2_y][pos2_x] == 4:  # ...компьютера
                    return self.check_comp_moves([], pos2_x, pos2_y)  # возвращаем список доступных ходов
                elif scene[pos2_y][pos2_x] == 1 or scene[pos2_y][pos2_x] == 2:  # ...игрока
                    return self.check_player_moves([], pos2_x, pos2_y)  # возвращаем список доступных ходов
        if flag: self.draw_board(pos1_x, pos1_y, pos2_x, pos2_y)  # рисуем игровое поле

    def check_comp_mandatory_moves(self, moves_list):  # проверка наличия обязательных ходов
        for y in range(COLUMNS):  # сканируем всё поле
            for x in range(ROWS):
                moves_list = self.check_comp_moves(moves_list, x, y)
        return moves_list

    def check_comp_moves(self, move_list, x, y):
        if scene[y][x] == 3:  # шашка
            for ix, iy in (-1, -1), (-1, 1), (1, -1), (1, 1):
                if 0 <= y + iy + iy < COLUMNS and 0 <= x + ix + ix < ROWS:
                    if scene[y + iy][x + ix] == 1 or scene[y + iy][x + ix] == 2:
                        if scene[y + iy + iy][x + ix + ix] == 0:
                            move_list.append(((x, y), (x + ix + ix, y + iy + iy)))  # запись хода в конец списка
        if scene[y][x] == 4:  # шашка с короной
            for ix, iy in (-1, -1), (-1, 1), (1, -1), (1, 1):
                isCorrect = 0  # определение правильности хода
                for i in range(1, COLUMNS):
                    if 0 <= y + iy * i < COLUMNS and 0 <= x + ix * i < ROWS:
                        if isCorrect == 1:
                            move_list.append(((x, y), (x + ix * i, y + iy * i)))  # запись хода в конец списка
                        if scene[y + iy * i][x + ix * i] == 1 or scene[y + iy * i][x + ix * i] == 2:
                            isCorrect += 1
                        if scene[y + iy * i][x + ix * i] == 3 or scene[y + iy * i][x + ix * i] == 4 or isCorrect == 2:
                            if isCorrect > 0: move_list.pop()  # удаление хода из списка
                            break
        return move_list

    def check_left_comp_moves(self, moves_list):  # проверка наличия остальных ходов
        for y in range(COLUMNS):  # сканируем всё поле
            for x in range(ROWS):
                if scene[y][x] == 3:  # шашка
                    for ix, iy in (-1, 1), (1, 1):
                        if 0 <= y + iy < COLUMNS and 0 <= x + ix < ROWS:
                            if scene[y + iy][x + ix] == 0:
                                moves_list.append(((x, y), (x + ix, y + iy)))  # запись хода в конец списка
                            if scene[y + iy][x + ix] == 1 or scene[y + iy][x + ix] == 2:
                                if 0 <= y + iy * 2 < COLUMNS and 0 <= x + ix * 2 < ROWS:
                                    if scene[y + iy * 2][x + ix * 2] == 0:
                                        moves_list.append(((x, y),
                                                           (x + ix * 2, y + iy * 2)))  # запись хода в конец списка
                if scene[y][x] == 4:  # шашка с короной
                    for ix, iy in (-1, -1), (-1, 1), (1, -1), (1, 1):
                        isCorrect = 0  # определение правильности хода
                        for i in range(1, COLUMNS):
                            if 0 <= y + iy * i < COLUMNS and 0 <= x + ix * i < ROWS:
                                if scene[y + iy * i][x + ix * i] == 0:
                                    moves_list.append(((x, y), (x + ix * i, y + iy * i)))  # запись хода в конец списка
                                if scene[y + iy * i][x + ix * i] == 1 or scene[y + iy * i][x + ix * i] == 2:
                                    isCorrect += 1
                                if scene[y + iy * i][x + ix * i] == 3 or scene[y + iy * i][
                                    x + ix * i] == 4 or isCorrect == 2:
                                    break
        return moves_list

    def check_player_mandatory_moves(self, moves_list):  # проверка наличия обязательных ходов
        moves_list = []  # список ходов
        for y in range(COLUMNS):  # сканируем всё поле
            for x in range(ROWS):
                moves_list = self.check_player_moves(moves_list, x, y)
        return moves_list

    def check_player_moves(self, moves_list, x, y):
        if scene[y][x] == 1:  # шашка
            for ix, iy in (-1, -1), (-1, 1), (1, -1), (1, 1):
                if 0 <= y + iy + iy < COLUMNS and 0 <= x + ix + ix < ROWS:
                    if scene[y + iy][x + ix] == 3 or scene[y + iy][x + ix] == 4:
                        if scene[y + iy + iy][x + ix + ix] == 0:
                            moves_list.append(((x, y), (x + ix + ix, y + iy + iy)))  # запись хода в конец списка
        if scene[y][x] == 2:  # шашка с короной
            for ix, iy in (-1, -1), (-1, 1), (1, -1), (1, 1):
                isCorrect = 0  # определение правильности хода
                for i in range(1, COLUMNS):
                    if 0 <= y + iy * i < COLUMNS and 0 <= x + ix * i < ROWS:
                        if isCorrect == 1:
                            moves_list.append(((x, y), (x + ix * i, y + iy * i)))  # запись хода в конец списка
                        if scene[y + iy * i][x + ix * i] == 3 or scene[y + iy * i][x + ix * i] == 4:
                            isCorrect += 1
                        if scene[y + iy * i][x + ix * i] == 1 or scene[y + iy * i][x + ix * i] == 2 or isCorrect == 2:
                            if isCorrect > 0: moves_list.pop()  # удаление хода из списка
                            break
        return moves_list

    def check_left_player_moves(self, moves_list):  # проверка наличия остальных ходов
        for y in range(ROWS):  # сканируем всё поле
            for x in range(COLUMNS):
                if scene[y][x] == 1:  # шашка
                    for ix, iy in (-1, -1), (1, -1):
                        if 0 <= y + iy < COLUMNS and 0 <= x + ix < COLUMNS:
                            if scene[y + iy][x + ix] == 0:
                                moves_list.append(((x, y), (x + ix, y + iy)))  # запись хода в конец списка
                            if scene[y + iy][x + ix] == 3 or scene[y + iy][x + ix] == 4:
                                if 0 <= y + iy * 2 < COLUMNS and 0 <= x + ix * 2 < COLUMNS:
                                    if scene[y + iy * 2][x + ix * 2] == 0:
                                        moves_list.append(((x, y),
                                                           (x + ix * 2, y + iy * 2)))  # запись хода в конец списка
                if scene[y][x] == 2:  # шашка с короной
                    for ix, iy in (-1, -1), (-1, 1), (1, -1), (1, 1):
                        isCorrect = 0  # определение правильности хода
                        for i in range(1, COLUMNS):
                            if 0 <= y + iy * i < COLUMNS and 0 <= x + ix * i < ROWS:
                                if scene[y + iy * i][x + ix * i] == 0:
                                    moves_list.append(((x, y), (x + ix * i, y + iy * i)))  # запись хода в конец списка
                                if scene[y + iy * i][x + ix * i] == 3 or scene[y + iy * i][x + ix * i] == 4:
                                    isCorrect += 1
                                if scene[y + iy * i][x + ix * i] == 1 or scene[y + iy * i][
                                    x + ix * i] == 2 or isCorrect == 2:
                                    break
        return moves_list

# --------------------------------------- MAIN ---------------------------------------------
if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
