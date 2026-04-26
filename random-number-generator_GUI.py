import random
import tkinter as tk
from tkinter import font as tkfont




def get_hint(secret, guess):

    diff = abs(secret - guess)
    if diff == 0:
        return None
    elif diff <= 5:
        direction = "higher" if secret > guess else "lower"
        return f" So close! Go a little {direction}."
    elif diff <= 15:
        direction = "higher" if secret > guess else "lower"
        return f"  Try going {direction}."
    elif diff <= 30:
        direction = "higher" if secret > guess else "lower"
        return f"  GO a bit {direction}."
    else:
        if secret > guess:
            return " Too low it is higher than that."
        else:
            return " Too high it is lower than that."


# ─── Main App ───────────────────────

class NumberGuessingApp:
    MAX_GUESSES = 7

    # colour palette
    BG        = "#0d0d1a"
    CARD      = "#13132b"
    ACCENT    = "#7c3aed"        
    ACCENT2   = "#06b6d4"        
    SUCCESS   = "#22c55e"
    DANGER    = "#ef4444"
    TEXT      = "#e2e8f0"
    MUTED     = "#64748b"
    ENTRY_BG  = "#1e1e3f"

    def __init__(self, root):
        self.root = root
        self.root.title("Number Guessing Game ")
        self.root.configure(bg=self.BG)
        self.root.resizable(False, False)

        # centre window
        w, h = 480, 680
        sw = root.winfo_screenwidth()
        sh = root.winfo_screenheight()
        root.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")

        self._build_fonts()
        self._build_ui()
        self._new_game()

    # ── fonts ─────────────────────────────────────────────────────
    def _build_fonts(self):
        self.f_title   = tkfont.Font(family="Courier New", size=20, weight="bold")
        self.f_sub     = tkfont.Font(family="Courier New", size=10)
        self.f_label   = tkfont.Font(family="Courier New", size=11)
        self.f_entry   = tkfont.Font(family="Courier New", size=22, weight="bold")
        self.f_btn     = tkfont.Font(family="Courier New", size=12, weight="bold")
        self.f_hint    = tkfont.Font(family="Courier New", size=11, slant="italic")
        self.f_counter = tkfont.Font(family="Courier New", size=28, weight="bold")
        self.f_small   = tkfont.Font(family="Courier New", size=9)

    # ── UI layout ────────────────────────────────
    def _build_ui(self):
        pad = dict(padx=28)

        # ── title bar ──
        title_frame = tk.Frame(self.root, bg=self.ACCENT, height=6)
        title_frame.pack(fill="x")

        tk.Label(self.root, text="NUMBER GUESSING GAME",
                 font=self.f_title, bg=self.BG, fg=self.ACCENT2,
                 pady=18).pack(**pad)

        tk.Label(self.root,
                 text="Crack the secret number between 1 – 100",
                 font=self.f_sub, bg=self.BG, fg=self.MUTED).pack()

        # ── divider ──
        tk.Frame(self.root, bg=self.ACCENT, height=1).pack(fill="x", pady=14, **pad)

        # ── attempts counter ──
        counter_frame = tk.Frame(self.root, bg=self.CARD,
                                 highlightbackground=self.ACCENT,
                                 highlightthickness=1)
        counter_frame.pack(pady=4, **pad, fill="x")

        tk.Label(counter_frame, text="ATTEMPTS LEFT",
                 font=self.f_small, bg=self.CARD, fg=self.MUTED).pack(pady=(10,0))

        self.lbl_counter = tk.Label(counter_frame, text="7",
                                    font=self.f_counter, bg=self.CARD,
                                    fg=self.ACCENT2)
        self.lbl_counter.pack()

        self.lbl_progress = tk.Label(counter_frame, text=f"Guess 1 of {self.MAX_GUESSES}",
                                     font=self.f_small, bg=self.CARD,
                                     fg=self.MUTED)
        self.lbl_progress.pack(pady=(0,10))

        # ── entry ──
        tk.Label(self.root, text="YOUR GUESS",
                 font=self.f_small, bg=self.BG, fg=self.MUTED).pack(pady=(18,4), **pad, anchor="w")

        entry_frame = tk.Frame(self.root, bg=self.ENTRY_BG,
                               highlightbackground=self.ACCENT,
                               highlightthickness=2)
        entry_frame.pack(**pad, fill="x")

        self.entry_var = tk.StringVar()
        self.entry = tk.Entry(entry_frame, textvariable=self.entry_var,
                              font=self.f_entry, bg=self.ENTRY_BG,
                              fg=self.TEXT, insertbackground=self.ACCENT2,
                              relief="flat", justify="center",
                              bd=10)
        self.entry.pack(fill="x")
        self.entry.bind("<Return>", lambda e: self._submit())
        self.entry.focus()

        # ── guess button ──
        self.btn_guess = tk.Button(self.root, text="GUESS  →",
                                   font=self.f_btn,
                                   bg=self.ACCENT, fg="white",
                                   activebackground="#6d28d9",
                                   activeforeground="white",
                                   relief="flat", cursor="hand2",
                                   pady=12,
                                   command=self._submit)
        self.btn_guess.pack(pady=14, **pad, fill="x")

        # ── hint box ──
        self.lbl_hint = tk.Label(self.root, text="",
                                 font=self.f_hint, bg=self.BG,
                                 fg=self.ACCENT2, wraplength=400,
                                 justify="center")
        self.lbl_hint.pack(pady=4)

        # ── history list ──
        tk.Label(self.root, text="GUESS HISTORY",
                 font=self.f_small, bg=self.BG, fg=self.MUTED).pack(pady=(14,4), **pad, anchor="w")

        hist_frame = tk.Frame(self.root, bg=self.CARD,
                              highlightbackground=self.MUTED,
                              highlightthickness=1)
        hist_frame.pack(**pad, fill="x")

        self.history_text = tk.Text(hist_frame, height=6,
                                    font=self.f_small,
                                    bg=self.CARD, fg=self.TEXT,
                                    relief="flat", state="disabled",
                                    bd=8, spacing1=3,
                                    insertbackground=self.ACCENT2)
        self.history_text.pack(fill="x")

        # ── play again button (hidden until game ends) ──
        self.btn_again = tk.Button(self.root, text="▶  PLAY AGAIN",
                                   font=self.f_btn,
                                   bg=self.SUCCESS, fg="white",
                                   activebackground="#16a34a",
                                   activeforeground="white",
                                   relief="flat", cursor="hand2",
                                   pady=10,
                                   command=self._new_game)

        # ── bottom accent line ──
        tk.Frame(self.root, bg=self.ACCENT2, height=3).pack(fill="x", side="bottom")

    # ── game state ─────────────────────────────────────────────────────────────
    def _new_game(self):
        self.secret   = random.randint(1, 100)
        self.attempts = 0
        self.game_over = False

        self.lbl_counter.config(text=str(self.MAX_GUESSES), fg=self.ACCENT2)
        self.lbl_progress.config(text=f"Guess 1 of {self.MAX_GUESSES}")
        self.lbl_hint.config(text="Enter a number and press GUESS or hit Enter", fg=self.MUTED)
        self.entry_var.set("")
        self.entry.config(state="normal")
        self.btn_guess.config(state="normal", bg=self.ACCENT)
        self.btn_again.pack_forget()

        self._clear_history()
        self.entry.focus()

    def _submit(self):
        if self.game_over:
            return

        raw = self.entry_var.get().strip()

        # validate
        try:
            guess = int(raw)
        except ValueError:
            self._flash_hint("  Enter a whole number!", self.DANGER)
            self.entry_var.set("")
            return

        if guess < 1 or guess > 100:
            self._flash_hint("⚠️  Number must be between 1 and 100!", self.DANGER)
            self.entry_var.set("")
            return

        self.attempts += 1
        remaining = self.MAX_GUESSES - self.attempts

        # correct!
        if guess == self.secret:
            self._add_history(self.attempts, guess, "✅ CORRECT!")
            self._end_game(won=True)
            return

        hint = get_hint(self.secret, guess)
        self._add_history(self.attempts, guess, hint)
        self.entry_var.set("")

        # update counter
        self.lbl_counter.config(text=str(remaining))
        self.lbl_progress.config(text=f"Guess {self.attempts + 1} of {self.MAX_GUESSES}")
        self._flash_hint(hint, self.ACCENT2)

        # colour counter red when low
        if remaining <= 3:
            self.lbl_counter.config(fg=self.DANGER)
        elif remaining <= 5:
            self.lbl_counter.config(fg="#f97316")  # orange

        if remaining == 0:
            self._end_game(won=False)

    def _end_game(self, won):
        self.game_over = True
        self.entry.config(state="disabled")
        self.btn_guess.config(state="disabled", bg=self.MUTED)

        if won:
            msg = f" CORRECT!  The number was {self.secret}\n   Guessed in {self.attempts} attempt(s)!"
            self.lbl_hint.config(text=msg, fg=self.SUCCESS,
                                 font=tkfont.Font(family="Courier New", size=12, weight="bold"))
            self.lbl_counter.config(fg=self.SUCCESS)
        else:
            msg = f" GAME OVER!  The number was {self.secret}"
            self.lbl_hint.config(text=msg, fg=self.DANGER,
                                 font=tkfont.Font(family="Courier New", size=12, weight="bold"))
            self.lbl_counter.config(text="0", fg=self.DANGER)

        self.btn_again.pack(pady=10, padx=28, fill="x")

    # ── helpers ────────────────────────────────────────────────────────────────
    def _flash_hint(self, text, color):
        self.lbl_hint.config(text=text, fg=color,
                             font=self.f_hint)

    def _add_history(self, attempt_num, guess, result):
        self.history_text.config(state="normal")
        line = f"  #{attempt_num:02}  →  {guess:>3}   {result}\n"
        self.history_text.insert("end", line)
        self.history_text.see("end")
        self.history_text.config(state="disabled")

    def _clear_history(self):
        self.history_text.config(state="normal")
        self.history_text.delete("1.0", "end")
        self.history_text.config(state="disabled")


# ─── Entry point ───────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    app = NumberGuessingApp(root)
    root.mainloop()
