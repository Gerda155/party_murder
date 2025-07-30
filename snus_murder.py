import tkinter as tk
from tkinter import font, messagebox
import random
import threading
import time
import sys

if sys.platform.startswith('win'):
    import winsound
else:
    def beep(freq, dur):
        pass
    winsound = type('winsound', (), {'Beep': beep})

suspects = [
    "Полинка", "Катя", "Артём Чистый", "Иссус", "Саса Тимошенко", "Максим Беленький",
    "Ростик", "Маша", "Стасик", "Никита", "Николь", "Сасай-Масай", "Анаст", "Даник", 
    "Анжелика", "Роберт", "Леван", "Ли", "Бэй", "Тая", "Рената", "Хохол", "Костя", "Герда",
    "Виктор", "Ратибор", "Кирилл", "Мариус", "Немец"
]

motives = [
    "подстриг волосы", "не дал сигарету", "сжег испарик", "назвал нормисом", "не поверил Роберту", "не погадали",
    "не решил, кто будет сниматься в порно с батей Рабибора", "оскорбил мамку", "не поделили колонку на тусе",
    "выдернул шарик из пирсы", "не скинулся на пиво", "не позвал на бухаловку", "поступил в тех", "уронил в мошпите", "не поделили басиста выступающей нн группы"
]

locations = [
    "кухня", "балкон", "ванна", "алтарь", "туалет в фонтейне",
    "молодежка", "техникум на ванес", "у Герды дома", "курилка художки", "эллинги",
    "под мостом", "на пляже", "в хесе"
]

weapons = [
    "бутылка", "нож", "трусы ростика с сердечками", "жижа с выпечкой", "Книга по философии", "таро",
    "сгоревший испарик", "розочка", "пердёшь", "шипастый браслет", "дреды", "веган бургер"
]

alibis = {
    "Полинка" : "общалась с с.ai",
    "Катя" : "культурно отдыхала с московской",
    "Артём Чистый" : "был в автошкиле",
    "Иссус" : "гонял на тачке",
    "Саса Тимошенко" : "отдавалась творчеству",
    "Максим Беленький" : "летел в Берлин",
    "Ростик" : "спал",
    "Маша" : "снимала тик-токи",
    "Стасик" : "была в вет клинике",
    "Никита" : "чередовал сиги и ингалятор",
    "Николь" : "искала принцессу",
    "Сасай-Масай" : "был на рейве",
    "Анаст" : "рисовала гей-порно",
    "Даник" : "охотился на моль", 
    "Анжелика" : "стримела",
    "Роберт" : "учил людей жить",
    "Леван" : "он такого никогда не сделает",
    "Ли" : "она вообще не знает жертву",
    "Бэй" : "никогда не была на месте преступления",
    "Тая" : "была на фотосессии",
    "Рената" : "она была на свидании",
    "Хохол" : "*молчание*",
    "Костя" : "он там был, но он просто снимал",
    "Виктор" : "бегал полуголый под окнами людей",
    "Герда" : "былла в кровати вашей мамки"
}

class MurderMysteryApp:
    def __init__(self, root):
        self.root = root
        root.title("🦇 Убийство на вписке 🦇")
        root.geometry("700x600")
        root.configure(bg="#1A1A1A")

        self.title_font = font.Font(family="Consolas", size=32, weight="bold")
        self.text_font = font.Font(family="Consolas", size=15)
        self.button_font = font.Font(family="Arial", size=14, weight="bold")

        self.timer_seconds = 15
        self.timer_thread = None
        self.timer_running = False

        self.events = [
            "Вы услышали странный звонок в дверь...",
            "В соседней комнате кто-то тихо двигается...",
            "Ключевой свидетель внезапно пропал...",
            "На полу появились странные следы...",
            "Слышен скрип лестницы сверху..."
        ]

        self.start_frame = tk.Frame(root, bg="#1A1A1A")
        self.start_frame.pack(fill="both", expand=True)

        self.title_label = tk.Label(
            self.start_frame,
            text="🦇 Убийство на вписке 🦇",
            font=self.title_font,
            fg="#D12B2B",
            bg="#1A1A1A",
            pady=50
        )
        self.title_label.pack()

        self.start_button = tk.Button(
            self.start_frame,
            text="Начать расследование",
            font=self.button_font,
            bg="#D12B2B", fg="white",
            activebackground="#A32020", activeforeground="white",
            relief="raised", bd=5,
            command=self.start_game
        )
        self.start_button.pack(pady=25, ipadx=10, ipady=6)

        self.game_frame = tk.Frame(root, bg="#1A1A1A")

        self.result_label = tk.Label(
            self.game_frame,
            text="",
            font=self.text_font,
            fg="#E6E6E6",
            bg="#1A1A1A",
            justify="left",
            wraplength=660,
            anchor="nw"
        )
        self.result_label.pack(pady=15, fill="both", expand=True)

        self.next_button = tk.Button(
            self.game_frame,
            text="Показать детали",
            font=self.button_font,
            bg="#D12B2B", fg="white",
            activebackground="#A32020", activeforeground="white",
            relief="raised", bd=4,
            command=self.next_detail
        )
        self.next_button.pack(pady=8, ipadx=8, ipady=5)

        self.reset_button = tk.Button(
            self.game_frame,
            text="Начать заново",
            font=("Arial", 12),
            bg="#2F2F2F",
            fg="#E6E6E6",
            activebackground="#444444",
            activeforeground="#CCCCCC",
            relief="groove",
            command=self.reset,
            state="disabled"
        )
        self.reset_button.pack(pady=10, ipadx=6, ipady=4)

        self.choice_frame = tk.Frame(root, bg="#1A1A1A")

        self.choice_label = tk.Label(
            self.choice_frame,
            text="Кого посадим? Осталось времени:",
            font=self.text_font,
            fg="#E6E6E6",
            bg="#1A1A1A",
            pady=12
        )
        self.choice_label.pack()

        self.time_label = tk.Label(
            self.choice_frame,
            text="",
            font=self.text_font,
            fg="#FF5555",
            bg="#1A1A1A",
            pady=6
        )
        self.time_label.pack()

        self.suspect_var = tk.StringVar()
        self.suspect_var.set(None)

        self.radio_buttons = []

        self.submit_button = tk.Button(
            self.choice_frame,
            text="Подтвердить выбор",
            font=self.button_font,
            bg="#D12B2B", fg="white",
            activebackground="#A32020", activeforeground="white",
            relief="raised", bd=4,
            command=self.submit_choice
        )
        self.submit_button.pack(pady=14, ipadx=10, ipady=6)

        self.alibi_button = tk.Button(
            self.choice_frame,
            text="Допросить подозреваемого",
            font=("Arial", 12, "italic"),
            bg="#555555",
            fg="white",
            activebackground="#777777",
            activeforeground="white",
            relief="groove",
            command=self.ask_alibi
        )
        self.alibi_button.pack(pady=6, ipadx=6, ipady=4)

        self.random_event_thread = threading.Thread(target=self.random_events_loop, daemon=True)
        self.random_event_thread.start()

    def start_game(self):
        self.start_frame.pack_forget()
        self.choice_frame.pack_forget()
        self.game_frame.pack(fill="both", expand=True)
        self.reset()

    def next_detail(self):
        self.stage += 1
        details = [
            f"🩸 Жертва: {self.victim}"
        ]
        if self.stage >= 2:
            details.append(f"🧠 Мотив: {self.motive}")
        if self.stage >= 3:
            details.append(f"📍 Место преступления: {self.location}")
        if self.stage >= 4:
            details.append(f"🗡 Орудие убийства: {self.weapon}")
            self.next_button.config(text="Выбрать убийцу")
        self.result_label.config(text="\n\n".join(details))
        if self.stage == 5:
            self.next_button.config(state="disabled")
            self.reset_button.config(state="normal")
            self.show_choice_screen()

    def random_events_loop(self):
        while True:
            time.sleep(random.randint(20, 60))
            if hasattr(self, 'stage') and 1 <= self.stage <= 4:
                self.root.after(0, self.show_random_event)

    def show_random_event(self):
        event = random.choice(self.events)
        threading.Thread(target=winsound.Beep, args=(800, 300), daemon=True).start()
        messagebox.showinfo("Случайное событие", event)

    def reset(self):
        self.victim = random.choice(suspects)
        possible_killers = [s for s in suspects if s != self.victim]
        self.killer = random.choice(possible_killers)
        self.motive = random.choice(motives)
        self.location = random.choice(locations)
        self.weapon = random.choice(weapons)
        self.stage = 0
        self.result_label.config(text="Нажми 'Показать детали', чтобы начать расследование")
        self.next_button.config(state="normal", text="Показать детали")
        self.reset_button.config(state="disabled")
        self.suspect_var.set(None)
        self.choice_frame.pack_forget()
        self.game_frame.pack(fill="both", expand=True)

    def show_choice_screen(self):
        self.game_frame.pack_forget()
        others = [s for s in suspects if s != self.killer]
        choices = random.sample(others, 2) + [self.killer]
        random.shuffle(choices)

        for rb in self.radio_buttons:
            rb.destroy()
        self.radio_buttons.clear()

        for suspect in choices:
            rb = tk.Radiobutton(
                self.choice_frame,
                text=suspect,
                variable=self.suspect_var,
                value=suspect,
                font=self.text_font,
                fg="#E6E6E6",
                bg="#1A1A1A",
                selectcolor="#333333",
                activebackground="#1A1A1A",
                activeforeground="#FF5555",
                highlightthickness=0,
                pady=6
            )
            rb.pack(anchor="w", padx=50)
            self.radio_buttons.append(rb)

        self.choice_frame.pack(fill="both", expand=True)
        self.suspect_var.set(None)

        self.time_left = self.timer_seconds
        self.update_timer_label()
        self.timer_running = True
        self.timer_thread = threading.Thread(target=self.countdown_timer, daemon=True)
        self.timer_thread.start()

    def update_timer_label(self):
        self.time_label.config(text=f"{self.time_left} секунд")

    def countdown_timer(self):
        while self.timer_running and self.time_left > 0:
            time.sleep(1)
            self.time_left -= 1
            self.root.after(0, self.update_timer_label)
        if self.time_left == 0:
            self.root.after(0, self.time_out)

    def time_out(self):
        self.timer_running = False
        messagebox.showinfo("Время вышло", "Время на выбор вышло! Игра сама выбрала за тебя.")
        choices = [rb.cget("text") for rb in self.radio_buttons]
        bad_choices = [c for c in choices if c != self.killer]
        choice = random.choice(bad_choices) if bad_choices else choices[0]
        self.suspect_var.set(choice)
        self.submit_choice()

    def ask_alibi(self):
        suspects_in_choice = [rb.cget("text") for rb in self.radio_buttons]
        suspect_to_interrogate = random.choice(suspects_in_choice)
        alibi_text = alibis.get(suspect_to_interrogate, "Алиби отсутствует.")
        messagebox.showinfo("Допрос", f"Допросили {suspect_to_interrogate}:\n{alibi_text}")

    def submit_choice(self):
        self.timer_running = False
        choice = self.suspect_var.get()
        if not choice:
            messagebox.showwarning("Выбор не сделан", "Пожалуйста, выбери подозреваемого.")
            return
        if choice == self.killer:
            messagebox.showinfo("Верно!", f"Ты поймала настоящего убийцу — {self.killer}!")
        else:
            messagebox.showinfo("Промах...", f"Нет, настоящий убийца — {self.killer}. Ты посадила {choice}.")
        self.choice_frame.pack_forget()
        self.start_frame.pack(fill="both", expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = MurderMysteryApp(root)
    root.mainloop()
