import tkinter as tk
from tkinter import messagebox


class ClickerV20:
    def __init__(self, root, clicks=0, rebits=0, click_pwr=1, auto_lvl=0, codes_paid=False):
        self.root = root
        self.root.title("Кликер v20.0")
        self.root.geometry("600x800")

        self.clicks = clicks
        self.rebits = rebits
        self.click_pwr = click_pwr
        self.auto_lvl = auto_lvl
        self.codes_paid = codes_paid
        self.inf_mode = False

        self.setup_ui()
        self.run_autoclicker()

    def get_bg(self):
        if self.inf_mode: return "black"
        c = self.clicks
        if c >= 1000: return "#FFD700"
        if c >= 500:  return "#FF69B4"
        if c >= 250:  return "#DA70D6"
        if c >= 100:  return "#90ee90"
        if c >= 50:   return "#add8e6"
        if c >= 10:   return "#ffff00"
        return "#f0f0f0"

    def setup_ui(self):
        bg = self.get_bg()
        txt_col = "red" if self.inf_mode else "black"
        self.root.config(bg=bg)

        for widget in self.root.winfo_children():
            if not isinstance(widget, tk.Toplevel): widget.destroy()

        val = "INF" if self.inf_mode else int(self.clicks)
        self.label_bal = tk.Label(self.root, text=f"Баланс: {val}", font=("Arial", 26, "bold"), bg=bg, fg=txt_col)
        self.label_bal.pack(pady=40)

        self.label_stats = tk.Label(self.root, text=f"Сила: {self.click_pwr} | Ребиты: {self.rebits}",
                                    font=("Arial", 12, "bold"), bg=bg, fg=txt_col)
        self.label_stats.pack()

        btn_txt = "БЕЗДНА" if self.inf_mode else "КЛИКНИ"
        tk.Button(self.root, text=btn_txt, font=("Arial", 35, "bold"), bg="orange", command=self.do_click, width=12,
                  height=3).pack(expand=True)

        bot = tk.Frame(self.root, bg=bg)
        bot.pack(side="bottom", pady=40)
        tk.Button(bot, text="МАГАЗИН", font=("Arial", 14, "bold"), bg="lightblue", width=20, height=2,
                  command=self.open_shop).pack(pady=5)
        tk.Button(bot, text="В МЕНЮ", font=("Arial", 10), bg="lightgray", width=15, command=self.go_to_lobby).pack(
            pady=5)

    def do_click(self):
        if not self.inf_mode:
            self.clicks += self.click_pwr
        self.update_labels()

    def update_labels(self):
        bg = self.get_bg()
        txt_col = "red" if self.inf_mode else "black"
        self.root.config(bg=bg)
        val = "INF" if self.inf_mode else int(self.clicks)
        self.label_bal.config(text=f"Баланс: {val}", bg=bg, fg=txt_col)
        self.label_stats.config(text=f"Сила: {self.click_pwr} | Ребиты: {self.rebits}", bg=bg, fg=txt_col)

    def open_shop(self):
        shop = tk.Toplevel(self.root)
        shop.title("Магазин")
        shop.geometry("400x550")

        tk.Label(shop, text="--- УЛУЧШЕНИЯ ЗА КЛИКИ ---", font=("Arial", 10, "bold")).pack(pady=10)
        tk.Button(shop, text="СДЕЛАТЬ РЕСЕТ (+1 Ребит)\nЦена: 1000 кл.", bg="orange", command=self.do_rebit).pack(
            pady=5)

        p_price = 10 if self.click_pwr < 2 else (30 if self.click_pwr < 5 else self.click_pwr * 25)
        p_next = 2 if self.click_pwr < 2 else (5 if self.click_pwr < 5 else self.click_pwr + 5)
        tk.Button(shop, text=f"Сила +{p_next - self.click_pwr} (Цена: {p_price} кл.)",
                  command=lambda: self.buy_pwr(p_price, p_next)).pack(pady=5)

        tk.Label(shop, text="--- ЗА РЕБИТЫ ---", font=("Arial", 10, "bold")).pack(pady=10)
        a_price = 2 + (self.auto_lvl * 2)
        tk.Button(shop, text=f"Автоклик ур.{self.auto_lvl + 1} (Цена: {a_price} Реб.)", bg="#d1ffbd",
                  command=lambda: self.buy_auto(a_price)).pack(pady=5)

        if not self.codes_paid:
            tk.Button(shop, text="Открыть Коды (1 Ребит.)", bg="#ffcc00", command=self.unlock_codes).pack(pady=5)
        else:
            tk.Label(shop, text="ВВЕДИТЕ ЧИСЛО ИЛИ / :").pack()
            e = tk.Entry(shop, font=("Arial", 12));
            e.pack(pady=5)

            def apply():
                txt = e.get().strip()
                if txt == "/":
                    self.inf_mode = True
                    messagebox.showinfo("!", "INFINITY MODE!")
                elif txt.isdigit():  # Якщо введено число
                    bonus = int(txt)
                    self.clicks += bonus
                    messagebox.showinfo("!", f"Добавлено: +{bonus} кликов!")
                else:
                    messagebox.showwarning("!", "Вводи число или /")
                self.update_labels()
                e.delete(0, tk.END)

            tk.Button(shop, text="АКТИВИРОВАТЬ", bg="lightgreen", command=apply).pack(pady=5)

        tk.Button(shop, text="ЗАКРЫТЬ", bg="pink", command=shop.destroy, width=20).pack(pady=20)

    def buy_pwr(self, price, next_v):
        if self.clicks >= price:
            self.clicks -= price
            self.click_pwr = next_v
            self.update_labels()
        else:
            messagebox.showwarning("!", "Мало кликов!")

    def buy_auto(self, price):
        if self.rebits >= price:
            self.rebits -= price
            self.auto_lvl += 1
            self.update_labels()
        else:
            messagebox.showwarning("!", "Мало ребитов!")

    def unlock_codes(self):
        if self.rebits >= 1:
            self.rebits -= 1;
            self.codes_paid = True;
            self.update_labels()
            messagebox.showinfo("!", "Коды открыты!")
        else:
            messagebox.showwarning("!", "Нужен 1 ребит!")

    def do_rebit(self):
        if self.clicks >= 1000 or self.inf_mode:
            self.clicks = 0;
            self.rebits += 1;
            self.click_pwr = 1;
            self.update_labels()
            messagebox.showinfo("!", "Ребит сделан!")
        else:
            messagebox.showwarning("!", "Надо 1000 кликов!")

    def run_autoclicker(self):
        if self.auto_lvl > 0 and not self.inf_mode:
            self.clicks += self.auto_lvl
            self.update_labels()
        delay = max(100, 1000 - (self.auto_lvl * 100))
        self.root.after(delay, self.run_autoclicker)

    def go_to_lobby(self):
        self.root.destroy()
        show_lobby()


def show_lobby():
    root = tk.Tk()
    root.title("Лобби v20.0")
    root.geometry("400x300")
    tk.Label(root, text="КЛИКЕР v20.0", font=("Arial", 25)).pack(pady=50)
    tk.Button(root, text="ИГРАТЬ", font=("Arial", 15), bg="green", fg="white", width=15,
              command=lambda: [root.destroy(), start_game()]).pack()
    root.mainloop()


def start_game():
    game_root = tk.Tk()
    ClickerV20(game_root)
    game_root.mainloop()


if __name__ == "__main__":
    show_lobby()
