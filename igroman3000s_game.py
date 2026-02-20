import tkinter as tk
from tkinter import messagebox, simpledialog, colorchooser


class ClickerV20_Final:
    def __init__(self, root, clicks=0, rebirths=0, color="#f0f0f0", mode="normal", click_pwr=1, auto_lvl=0,
                 codes_paid=False):
        self.root = root
        self.root.title("Кликер v20.2 - FINAL")
        self.root.geometry("600x850")

        self.clicks, self.rebirths = clicks, rebirths
        self.click_pwr, self.auto_lvl = click_pwr, auto_lvl
        self.bg_color, self.mode = color, mode
        self.codes_paid = codes_paid

        self.setup_ui()
        if self.auto_lvl > 0: self.run_autoclicker()

    def setup_ui(self):
        txt_col, bg_label, btn_text = "black", self.bg_color, "КЛИКНИ"

        if self.mode == "inf_mode":
            self.root.config(bg="black");
            txt_col, bg_label, btn_text = "red", "black", "БЕЗДНА"
        elif self.mode == "rkn_blue":
            self.root.config(bg="blue");
            txt_col, bg_label, btn_text = "white", "blue", "ВРУБИТЬ ВПН"
        elif self.mode == "semki":
            self.root.config(bg="white")
            self.bg_canvas = tk.Canvas(self.root, width=600, height=850, bg="white", highlightthickness=0)
            self.bg_canvas.place(x=0, y=0)
            for i in range(0, 850, 40):
                self.bg_canvas.create_text(300, i, text="СЕМКИ ЕСТЬ " * 8, fill="#e0e0e0", font=("Arial", 10, "bold"))
            txt_col, bg_label, btn_text = "black", "white", "СЕМКИ ЕСТЬ?"
        elif self.bg_color == "#FFD1DC":
            btn_text = "МУР КЛИК"

        self.root.config(bg=bg_label)
        val = "300+INF" if self.mode == "rkn_blue" else ("INF" if self.clicks == float('inf') else str(self.clicks))
        pref = "Семки: " if self.mode == "semki" else "Баланс: "

        tk.Label(self.root, text=f"{pref}{val}", font=("Arial", 22, "bold"), fg=txt_col, bg=bg_label,
                 wraplength=580).pack(pady=40)
        tk.Label(self.root, text=f"Сила: {self.click_pwr} | Rebirth: {self.rebirths}", font=("Arial", 10), bg=bg_label,
                 fg=txt_col).pack()

        btn_bg = "red" if self.mode == "inf_mode" else ("white" if self.mode == "rkn_blue" else "yellow")
        tk.Button(self.root, text=btn_text, font=("Arial", 25, "bold"), bg=btn_bg, command=self.do_click, width=15,
                  height=2).pack(pady=30)
        tk.Button(self.root, text="СДЕЛАТЬ РЕСЕТ (+1 Reb)\nЦена: 1000 кликов", bg="orange",
                  command=self.do_rebirth).pack(pady=10)

        bot = tk.Frame(self.root, bg=bg_label)
        bot.pack(side="bottom", pady=20)
        tk.Button(bot, text="МАГАЗИН", width=15, command=self.open_shop_menu).pack(side="left", padx=20)
        tk.Button(bot, text="В МЕНЮ", width=15, command=self.go_to_lobby).pack(side="right", padx=20)

    def do_click(self):
        if self.clicks != float('inf') and self.mode != "rkn_blue": self.clicks += self.click_pwr
        self.update_stats_only()

    def update_stats_only(self):
        val = "300+INF" if self.mode == "rkn_blue" else ("INF" if self.clicks == float('inf') else str(self.clicks))
        pref = "Семки: " if self.mode == "semki" else "Баланс: "
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Label) and (
                    "Баланс" in str(widget.cget("text")) or "Семки" in str(widget.cget("text"))):
                widget.config(text=f"{pref}{val}")

    def do_rebirth(self):
        if self.clicks >= 1000 or self.clicks == float('inf'):
            self.refresh_app(c=0, r=self.rebirths + 1, p=1, a=0, paid=False)
        else:
            messagebox.showwarning("!", "Нужно 1000 кликов!")

    def open_shop_menu(self):
        shop = tk.Toplevel(self.root);
        shop.title("Магазин & Коды")
        shop.geometry("400x450")
        p_pr = 1 + (self.click_pwr // 5);
        a_pr = 2 + (self.auto_lvl * 2)
        tk.Button(shop, text=f"Сила Клика - {p_pr} Reb", command=self.buy_pwr, width=25).pack(pady=5)
        tk.Button(shop, text=f"Авто-кликер - {a_pr} Reb", command=self.buy_auto, width=25).pack(pady=5)

        if not self.codes_paid:
            tk.Button(shop, text="Открыть Коды - 1 Reb", bg="orange", command=self.pay_for_codes, width=25).pack(pady=5)
        else:
            tk.Label(shop, text="ВВЕДИТЕ КОД (или /команду):").pack(pady=5)
            e = tk.Entry(shop, justify="center");
            e.pack(pady=5)

            def use_code():
                c = e.get().strip()
                if c == "/777":
                    self.clicks += 777; self.update_stats_only(); messagebox.showinfo("Admin", "+777 кликов!")
                elif c == "/inf":
                    shop.destroy(); self.ask_inf()
                elif c == "дуска падуска":
                    self.refresh_app(self.clicks + 10 ** 50, self.rebirths, "#FFD1DC", "normal", self.click_pwr,
                                     self.auto_lvl, True)
                elif c == "чтоб РКН здох":
                    self.refresh_app(float('inf'), self.rebirths, "blue", "rkn_blue", self.click_pwr, self.auto_lvl,
                                     True)
                elif c == "генерал котл":
                    self.refresh_app(self.clicks, self.rebirths, "white", "semki", self.click_pwr, self.auto_lvl, True)
                elif c == "RESET":
                    self.refresh_app()
                e.delete(0, tk.END)

            tk.Button(shop, text="АКТИВИРОВАТЬ", bg="lightgreen", command=use_code, width=25).pack(pady=5)

        tk.Button(shop, text="НЕ ОТКРЫВАТЬ", bg="black", fg="white", command=self.root.quit, width=25).pack(pady=20)

    def buy_pwr(self):
        p_pr = 1 + (self.click_pwr // 5)
        if self.rebirths >= p_pr: self.rebirths -= p_pr; self.click_pwr += 5; self.refresh_app(self.clicks,
                                                                                               self.rebirths,
                                                                                               self.bg_color, self.mode,
                                                                                               self.click_pwr,
                                                                                               self.auto_lvl,
                                                                                               self.codes_paid)

    def buy_auto(self):
        a_pr = 2 + (self.auto_lvl * 2)
        if self.rebirths >= a_pr: self.rebirths -= a_pr; self.auto_lvl += 1; self.refresh_app(self.clicks,
                                                                                              self.rebirths,
                                                                                              self.bg_color, self.mode,
                                                                                              self.click_pwr,
                                                                                              self.auto_lvl,
                                                                                              self.codes_paid)

    def pay_for_codes(self):
        if self.rebirths >= 1: self.rebirths -= 1; self.codes_paid = True; self.refresh_app(self.clicks, self.rebirths,
                                                                                            self.bg_color, self.mode,
                                                                                            self.click_pwr,
                                                                                            self.auto_lvl, True)

    def run_autoclicker(self):
        if self.auto_lvl > 0:
            if self.clicks != float('inf'): self.clicks += self.click_pwr
            self.update_stats_only()
            self.root.after(max(100, 1000 - (self.auto_lvl * 50)), self.run_autoclicker)

    def ask_inf(self):
        if messagebox.askyesno("?", "Хотите врубить infinity мод за бесп?"):
            self.refresh_app(float('inf'), self.rebirths, "black", "inf_mode", self.click_pwr, self.auto_lvl, True)

    def open_admin(self):  # Для лобі або консолі
        if simpledialog.askstring("Admin", "Пароль:") == "665640":
            v = simpledialog.askinteger("Admin", "Дать Reb:");
            self.rebirths += v;
            self.update_stats_only()

    def refresh_app(self, c=0, r=0, col="#f0f0f0", m="normal", p=1, a=0, paid=False):
        self.root.destroy();
        start_app(c, r, col, m, p, a, paid)

    def go_to_lobby(self):
        self.root.destroy();
        show_lobby(self.clicks, self.rebirths, self.bg_color, self.mode, self.click_pwr, self.auto_lvl, self.codes_paid)


def start_app(c=0, r=0, col="#f0f0f0", m="normal", p=1, a=0, paid=False):
    win = tk.Tk();
    ClickerV20_Final(win, c, r, col, m, p, a, paid);
    win.mainloop()


def show_lobby(c=0, r=0, col="#f0f0f0", m="normal", p=1, a=0, paid=False):
    lb = tk.Tk();
    lb.title("Лобби");
    lb.geometry("400x300");
    lb.config(bg="white")
    tk.Label(lb, text="CLICKER v20.0", font=("Impact", 30), bg="white").pack(pady=40)
    tk.Button(lb, text="ИГРАТЬ", font=("Arial", 16, "bold"), bg="green", fg="white", width=15,
              command=lambda: [lb.destroy(), start_app(c, r, col, m, p, a, paid)]).pack(pady=10)
    tk.Button(lb, text="ВЫХОД", font=("Arial", 12), bg="red", fg="white", width=15, command=lb.quit).pack(pady=10)
    lb.mainloop()


if __name__ == "__main__":
    show_lobby()
