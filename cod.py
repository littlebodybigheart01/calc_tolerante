import tkinter as tk
import os
import sys

roman_to_arabic = {
    "I": 1, "II": 2, "III": 3, "IV": 4, "V": 5, "VI": 6,
    "VII": 7, "VIII": 8, "IX": 9, "X": 10, "XI": 11, "XII": 12
}

arabic_to_roman = {v: k for k, v in roman_to_arabic.items()}
clase_precizie = [i for i in range(1, 13)]
tolerante_16_25 = [0.6, 1, 1.6, 2.5, 4, 6, 10, 16, 25, 40, 60, 100]
tolerante_25_40 = [0.8, 1.2, 2, 3, 5, 8, 12, 20, 30, 50, 80, 120]
tolerante_40_63 = [1, 1.6, 2.5, 4, 6, 10, 16, 25, 40, 60, 100, 160]

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class ToleranteApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Aplicație Toleranțe - Tema 4 PI")
        self.geometry("400x320")
        try:
            ico_path = resource_path("icon.ico")
            self.iconbitmap(ico_path)
        except:
            pass
        self.choice_var = tk.IntVar(value=1)
        frame_opt = tk.Frame(self)
        frame_opt.pack(pady=10)
        tk.Radiobutton(frame_opt, text="1. Clasa de precizie (număr roman)", variable=self.choice_var, value=1, command=self._update_fields).pack(side=tk.LEFT, padx=5)
        tk.Radiobutton(frame_opt, text="2. Toleranța (µm)", variable=self.choice_var, value=2, command=self._update_fields).pack(side=tk.LEFT, padx=5)
        frame_inputs = tk.Frame(self)
        frame_inputs.pack(pady=10)
        self.label_dim = tk.Label(frame_inputs, text="Dimensiunea nominală [mm]:")
        self.label_dim.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_dim = tk.Entry(frame_inputs)
        self.entry_dim.grid(row=0, column=1, padx=5, pady=5)
        self.label_secondary = tk.Label(frame_inputs, text="Clasa de precizie (I-XII):")
        self.label_secondary.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.entry_secondary = tk.Entry(frame_inputs)
        self.entry_secondary.grid(row=1, column=1, padx=5, pady=5)
        self.btn_calc = tk.Button(self, text="Calculează", command=self._calculeaza)
        self.btn_calc.pack(pady=10)
        self.result_label = tk.Label(self, text="", fg="blue", wraplength=350, justify=tk.LEFT)
        self.result_label.pack(pady=10)
        self._update_fields()

    def _update_fields(self):
        choice = self.choice_var.get()
        self.entry_secondary.delete(0, tk.END)
        if choice == 1:
            self.label_secondary.config(text="Clasa de precizie (I-XII):")
        else:
            self.label_secondary.config(text="Toleranța (µm):")
        self.result_label.config(text="")

    def _calculeaza(self):
        choice = self.choice_var.get()
        try:
            dim_nominala = float(self.entry_dim.get())
        except:
            self.result_label.config(text="Eroare: Dimensiunea nominală invalidă!")
            return
        if dim_nominala < 20 or dim_nominala > 50:
            self.result_label.config(text="Dimensiunea nominală trebuie să fie între 20 și 50 mm.")
            return
        if dim_nominala <= 25:
            tolerante_curente = tolerante_16_25
        elif dim_nominala <= 40:
            tolerante_curente = tolerante_25_40
        else:
            tolerante_curente = tolerante_40_63
        if choice == 1:
            clasa_roman_input = self.entry_secondary.get().strip().upper()
            if clasa_roman_input not in roman_to_arabic:
                self.result_label.config(text="Eroare: Introduceți o clasa de precizie romană validă (I-XII).")
                return
            clasa_precizie_input = roman_to_arabic[clasa_roman_input]
            indice = clasa_precizie_input - 1
            tol = tolerante_curente[indice]
            self.result_label.config(text=f"Toleranța la paralelism, perpendicularitate și înclinare\nClasa de precizie: {clasa_roman_input} (adică {clasa_precizie_input})\nToleranța: {tol} µm")
        else:
            try:
                tol_input = float(self.entry_secondary.get())
            except:
                self.result_label.config(text="Eroare: Toleranța trebuie să fie un număr real.")
                return
            if tol_input not in tolerante_curente:
                self.result_label.config(text="Toleranța introdusă nu există în tabelul curent pentru dimensiunea nominală aleasă.")
                return
            indice = tolerante_curente.index(tol_input)
            clasa_arabic = clase_precizie[indice]
            clasa_romana = arabic_to_roman[clasa_arabic]
            self.result_label.config(text=f"Toleranța la paralelism, perpendicularitate și înclinare\nClasa de precizie: {clasa_romana} (adică {clasa_arabic})")

def main():
    app = ToleranteApp()
    app.mainloop()

if __name__ == "__main__":
    main()
