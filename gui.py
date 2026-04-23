import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import random
import json
import os
import sys

# ── Try importing matplotlib ──────────────────────────────────────────────────
try:
    import matplotlib
    matplotlib.use("TkAgg")
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    HAS_MPL = True
except ImportError:
    HAS_MPL = False

# ── Import project modules ────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

import knapsack_01 as k01
import knapsack_unbounded as kub
from utils import (validate_items, validate_capacity, validate_ga_params,
                   generate_random_items, load_datasets, save_results_to_file,
                   format_solution)
from ga import GeneticAlgorithm


# ═════════════════════════════════════════════════════════════════════════════
#  THEME
# ═════════════════════════════════════════════════════════════════════════════
BG      = "#12131C"
PANEL   = "#1A1B2A"
PANEL2  = "#21223A"
BORDER  = "#2E3050"
TEXT    = "#DDE1F5"
MUTED   = "#6B6E8E"
ACCENT  = "#5B8DEF"
ACCENT2 = "#7C5BEF"
SUCCESS = "#3DDC97"
WARNING = "#F5C842"
ERROR   = "#EF5B5B"
FONT_H  = ("Consolas", 11, "bold")
FONT_B  = ("Consolas", 10)
FONT_S  = ("Consolas", 9)
FONT_XS = ("Consolas", 8)


# ═════════════════════════════════════════════════════════════════════════════
#  GA RUNNER  (delegates to GeneticAlgorithm from ga.py)
# ═════════════════════════════════════════════════════════════════════════════
def run_ga(items, capacity, mode, params, progress_cb=None, ga_instance=None):
    """
    Run the genetic algorithm for 0-1 or Unbounded knapsack.
    Uses GeneticAlgorithm class from ga.py.
    Returns (solution_dict, fitness_history_list).
    """
    n = len(items)

    if mode == "01":
        chromosome_factory = lambda: k01.create_chromosome(n)
        fitness_fn         = lambda c: k01.fitness_function(items, c, capacity)
        decode_fn          = lambda c: k01.decode_solution(c, items)
        crossover_fn       = k01.crossover
        mutation_fn        = k01.mutation
    else:
        chromosome_factory = lambda: kub.create_chromosome(n, capacity, items)
        fitness_fn         = lambda c: kub.fitness_function(c, items, capacity)
        decode_fn          = lambda c: kub.decode_solutions(c, items)
        crossover_fn       = kub.crossover
        mutation_fn        = kub.mutation

    ga = GeneticAlgorithm(
        population_size    = params["population_size"],
        generations        = params["generations"],
        mutation_rate      = params["mutation_rate"],
        crossover_rate     = params["crossover_rate"],
        chromosome_factory = chromosome_factory,
        fitness_fn         = fitness_fn,
        crossover_fn       = crossover_fn,
        mutation_fn        = mutation_fn,
    )

    # Store reference so the GUI can call ga.stop()
    if ga_instance is not None:
        ga_instance[0] = ga

    def _progress_callback(generation, best_fitness, best_chromosome):
        if progress_cb:
            progress_cb(generation + 1, params["generations"], best_fitness)

    best_chrom, _, fitness_history, _ = ga.evolve(progress_callback=_progress_callback)

    solution = decode_fn(best_chrom)
    return solution, fitness_history


# ═════════════════════════════════════════════════════════════════════════════
#  CUSTOM WIDGETS
# ═════════════════════════════════════════════════════════════════════════════
class DarkEntry(tk.Entry):
    def __init__(self, master, **kw):
        kw.setdefault("bg", PANEL2)
        kw.setdefault("fg", TEXT)
        kw.setdefault("insertbackground", ACCENT)
        kw.setdefault("relief", "flat")
        kw.setdefault("font", FONT_B)
        kw.setdefault("highlightthickness", 1)
        kw.setdefault("highlightbackground", BORDER)
        kw.setdefault("highlightcolor", ACCENT)
        super().__init__(master, **kw)


class DarkButton(tk.Button):
    def __init__(self, master, **kw):
        color = kw.pop("color", ACCENT)
        kw.setdefault("bg", color)
        kw.setdefault("fg", "#ffffff")
        kw.setdefault("activebackground", ACCENT2)
        kw.setdefault("activeforeground", "#ffffff")
        kw.setdefault("relief", "flat")
        kw.setdefault("font", FONT_H)
        kw.setdefault("cursor", "hand2")
        kw.setdefault("padx", 12)
        kw.setdefault("pady", 6)
        super().__init__(master, **kw)
        self._color = color
        self.bind("<Enter>", lambda e: self.config(bg=ACCENT2))
        self.bind("<Leave>", lambda e: self.config(bg=self._color))


class SectionLabel(tk.Label):
    def __init__(self, master, text, **kw):
        kw.setdefault("bg", BG)
        kw.setdefault("fg", ACCENT)
        kw.setdefault("font", ("Consolas", 9, "bold"))
        super().__init__(master, text=f"  {text.upper()}  ", **kw)


def hline(parent, color=BORDER):
    f = tk.Frame(parent, bg=color, height=1)
    f.pack(fill="x", pady=(4, 6))
    return f


# ═════════════════════════════════════════════════════════════════════════════
#  ITEMS TABLE  (editable treeview)
# ═════════════════════════════════════════════════════════════════════════════
class ItemsTable(tk.Frame):
    def __init__(self, master, **kw):
        kw.setdefault("bg", PANEL)
        super().__init__(master, **kw)
        self._build()

    def _build(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Dark.Treeview",
                        background=PANEL2, foreground=TEXT,
                        fieldbackground=PANEL2, rowheight=24,
                        font=FONT_B, borderwidth=0)
        style.configure("Dark.Treeview.Heading",
                        background=PANEL, foreground=ACCENT,
                        font=("Consolas", 9, "bold"), relief="flat")
        style.map("Dark.Treeview",
                  background=[("selected", ACCENT)],
                  foreground=[("selected", "#ffffff")])

        cols = ("#", "Name", "Weight", "Value")
        self.tree = ttk.Treeview(self, columns=cols, show="headings",
                                  style="Dark.Treeview", selectmode="browse",
                                  height=8)
        for col, w in zip(cols, [30, 160, 80, 80]):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=w, anchor="center")
        self.tree.column("Name", anchor="w")

        sb = tk.Scrollbar(self, orient="vertical", command=self.tree.yview,
                          bg=PANEL, troughcolor=PANEL2, width=10)
        self.tree.configure(yscrollcommand=sb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")
        self.tree.bind("<Double-1>", self._on_double_click)

    def set_items(self, items):
        self.tree.delete(*self.tree.get_children())
        for i, it in enumerate(items, 1):
            self.tree.insert("", "end",
                             values=(i, it["name"], it["weight"], it["value"]))

    def get_items(self):
        result = []
        for row in self.tree.get_children():
            _, name, w, v = self.tree.item(row, "values")
            try:
                result.append({"name": str(name),
                                "weight": float(w),
                                "value":  float(v)})
            except ValueError:
                pass
        return result

    def add_item(self, item):
        idx = len(self.tree.get_children()) + 1
        self.tree.insert("", "end",
                          values=(idx, item["name"], item["weight"], item["value"]))

    def delete_selected(self):
        sel = self.tree.selection()
        if sel:
            self.tree.delete(sel)
            self._renumber()

    def _renumber(self):
        for i, row in enumerate(self.tree.get_children(), 1):
            vals = list(self.tree.item(row, "values"))
            vals[0] = i
            self.tree.item(row, values=vals)

    def _on_double_click(self, event):
        region = self.tree.identify("region", event.x, event.y)
        if region != "cell":
            return
        col_id  = self.tree.identify_column(event.x)
        row_id  = self.tree.identify_row(event.y)
        col_idx = int(col_id.replace("#", "")) - 1
        if col_idx == 0:
            return

        x, y, w, h = self.tree.bbox(row_id, col_id)
        current     = self.tree.item(row_id, "values")[col_idx]

        var   = tk.StringVar(value=current)
        entry = tk.Entry(self, textvariable=var, bg=PANEL2, fg=TEXT,
                         insertbackground=ACCENT, relief="flat",
                         font=FONT_B, highlightthickness=1,
                         highlightbackground=ACCENT)
        entry.place(x=x, y=y, width=w, height=h)
        entry.focus_set()
        entry.select_range(0, "end")

        def commit(e=None):
            vals = list(self.tree.item(row_id, "values"))
            vals[col_idx] = var.get()
            self.tree.item(row_id, values=vals)
            entry.destroy()

        entry.bind("<Return>", commit)
        entry.bind("<FocusOut>", commit)
        entry.bind("<Escape>", lambda e: entry.destroy())


# ═════════════════════════════════════════════════════════════════════════════
#  FITNESS CHART  (matplotlib)
# ═════════════════════════════════════════════════════════════════════════════
class FitnessChart(tk.Frame):
    def __init__(self, master, **kw):
        kw.setdefault("bg", PANEL)
        super().__init__(master, **kw)
        self._build()

    def _build(self):
        if HAS_MPL:
            self.fig = Figure(figsize=(4, 2.2), dpi=90, facecolor=PANEL)
            self.ax  = self.fig.add_subplot(111, facecolor=PANEL2)
            self._style_ax()
            self.canvas = FigureCanvasTkAgg(self.fig, master=self)
            self.canvas.get_tk_widget().pack(fill="both", expand=True)
        else:
            tk.Label(self,
                     text="matplotlib not installed.\nRun: pip install matplotlib",
                     bg=PANEL2, fg=ERROR, font=FONT_S, justify="center"
                     ).pack(expand=True)

    def _style_ax(self):
        ax = self.ax
        ax.set_facecolor(PANEL2)
        for sp in ax.spines.values():
            sp.set_color(BORDER)
        ax.tick_params(colors=MUTED, labelsize=7)
        ax.xaxis.label.set_color(MUTED)
        ax.yaxis.label.set_color(MUTED)
        ax.set_xlabel("Generation", fontsize=8, color=MUTED)
        ax.set_ylabel("Best Fitness", fontsize=8, color=MUTED)
        ax.set_title("Fitness Over Generations", fontsize=9, color=TEXT, pad=6)

    def plot(self, history):
        if not HAS_MPL:
            return
        self.ax.clear()
        self._style_ax()
        gens = list(range(1, len(history) + 1))
        self.ax.plot(gens, history, color=ACCENT, linewidth=1.8, zorder=3)
        self.ax.fill_between(gens, history, alpha=0.15, color=ACCENT, zorder=2)
        best_val = max(history)
        best_gen = history.index(best_val) + 1
        self.ax.scatter([best_gen], [best_val], color=SUCCESS, s=40, zorder=4)
        self.ax.annotate(f"{best_val:.1f}",
                          xy=(best_gen, best_val),
                          xytext=(6, 6), textcoords="offset points",
                          color=SUCCESS, fontsize=7)
        self.fig.tight_layout(pad=0.6)
        self.canvas.draw()

    def clear(self):
        if not HAS_MPL:
            return
        self.ax.clear()
        self._style_ax()
        self.canvas.draw()


# ═════════════════════════════════════════════════════════════════════════════
#  MAIN APPLICATION
# ═════════════════════════════════════════════════════════════════════════════
class KnapsackApp(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Knapsack GA Solver  —  CS212 AI")
        self.geometry("1100x700")
        self.minsize(900, 600)
        self.configure(bg=BG)

        self.mode         = tk.StringVar(value="01")
        self._running     = False
        self._last_result = None
        self._datasets    = load_datasets()

        self._build_ui()
        self._load_default_items()

    # ── UI BUILD ──────────────────────────────────────────────────────────────
    def _build_ui(self):
        # Top bar
        topbar = tk.Frame(self, bg=PANEL, height=48)
        topbar.pack(fill="x")
        topbar.pack_propagate(False)
        tk.Label(topbar, text="⬡  KNAPSACK GA SOLVER",
                 font=("Consolas", 13, "bold"), fg=ACCENT, bg=PANEL
                 ).pack(side="left", padx=16, pady=10)
        tk.Label(topbar, text="CS212 Artificial Intelligence · Q19",
                 font=FONT_XS, fg=MUTED, bg=PANEL
                 ).pack(side="right", padx=16)

        content = tk.Frame(self, bg=BG)
        content.pack(fill="both", expand=True, padx=10, pady=8)

        left  = tk.Frame(content, bg=BG, width=440)
        right = tk.Frame(content, bg=BG)
        left.pack(side="left", fill="both", expand=False, padx=(0, 6))
        right.pack(side="left", fill="both", expand=True)
        left.pack_propagate(False)

        self._build_left(left)
        self._build_right(right)

        # Status bar
        self._status_var = tk.StringVar(value="Ready.")
        statusbar = tk.Frame(self, bg=PANEL, height=26)
        statusbar.pack(fill="x", side="bottom")
        statusbar.pack_propagate(False)
        tk.Label(statusbar, textvariable=self._status_var,
                 font=FONT_XS, fg=MUTED, bg=PANEL, anchor="w"
                 ).pack(side="left", padx=10, fill="y")

    def _build_left(self, parent):
        # ── Mode selector ────────────────────────────────────────────────────
        mode_card = tk.Frame(parent, bg=PANEL, pady=8, padx=10)
        mode_card.pack(fill="x", pady=(0, 6))
        SectionLabel(mode_card, "Problem Type").pack(anchor="w")
        hline(mode_card)
        btn_frame = tk.Frame(mode_card, bg=PANEL)
        btn_frame.pack(fill="x")

        self._btn_01 = tk.Button(btn_frame, text="0-1  Knapsack",
                                  font=FONT_H, relief="flat", cursor="hand2",
                                  bg=ACCENT, fg="#fff", padx=14, pady=6,
                                  command=lambda: self._set_mode("01"))
        self._btn_01.pack(side="left", expand=True, fill="x", padx=(0, 4))

        self._btn_ub = tk.Button(btn_frame, text="Unbounded",
                                  font=FONT_H, relief="flat", cursor="hand2",
                                  bg=PANEL2, fg=MUTED, padx=14, pady=6,
                                  command=lambda: self._set_mode("ub"))
        self._btn_ub.pack(side="left", expand=True, fill="x")

        # ── Dataset loader ───────────────────────────────────────────────────
        ds_card = tk.Frame(parent, bg=PANEL, pady=8, padx=10)
        ds_card.pack(fill="x", pady=(0, 6))
        SectionLabel(ds_card, "Load Dataset").pack(anchor="w")
        hline(ds_card)
        ds_row = tk.Frame(ds_card, bg=PANEL)
        ds_row.pack(fill="x")

        self._ds_var = tk.StringVar()
        ds_names = list(self._datasets.keys()) if self._datasets else ["No datasets found"]
        self._ds_combo = ttk.Combobox(ds_row, textvariable=self._ds_var,
                                       values=ds_names, state="readonly",
                                       font=FONT_B, width=22)
        style = ttk.Style()
        style.configure("TCombobox", fieldbackground=PANEL2,
                         background=PANEL2, foreground=TEXT,
                         selectbackground=ACCENT, selectforeground="#fff")
        self._ds_combo.pack(side="left", fill="x", expand=True, padx=(0, 6))
        if ds_names:
            self._ds_combo.current(0)
        DarkButton(ds_row, text="Load", command=self._load_dataset,
                   pady=4).pack(side="left")

        # ── Items table ──────────────────────────────────────────────────────
        items_card = tk.Frame(parent, bg=PANEL, pady=8, padx=10)
        items_card.pack(fill="both", expand=True, pady=(0, 6))
        SectionLabel(items_card, "Items  (double-click to edit)").pack(anchor="w")
        hline(items_card)

        self._items_table = ItemsTable(items_card)
        self._items_table.pack(fill="both", expand=True)

        btn_row = tk.Frame(items_card, bg=PANEL)
        btn_row.pack(fill="x", pady=(6, 0))
        DarkButton(btn_row, text="+ Add", color=SUCCESS,
                   command=self._add_item_dialog, pady=3
                   ).pack(side="left", padx=(0, 4))
        DarkButton(btn_row, text="✕ Delete", color=ERROR,
                   command=self._items_table.delete_selected, pady=3
                   ).pack(side="left", padx=(0, 4))
        DarkButton(btn_row, text="⟳ Random", color=ACCENT2,
                   command=self._random_items, pady=3
                   ).pack(side="left")

        # ── Capacity ─────────────────────────────────────────────────────────
        cap_card = tk.Frame(parent, bg=PANEL, pady=8, padx=10)
        cap_card.pack(fill="x", pady=(0, 6))
        SectionLabel(cap_card, "Capacity").pack(anchor="w")
        hline(cap_card)
        cap_row = tk.Frame(cap_card, bg=PANEL)
        cap_row.pack(fill="x")
        tk.Label(cap_row, text="Max Weight:", font=FONT_B,
                  fg=MUTED, bg=PANEL).pack(side="left")
        self._cap_entry = DarkEntry(cap_row, width=10)
        self._cap_entry.insert(0, "30")
        self._cap_entry.pack(side="left", padx=(8, 0))

    def _build_right(self, parent):
        # ── GA Parameters ────────────────────────────────────────────────────
        params_card = tk.Frame(parent, bg=PANEL, pady=8, padx=10)
        params_card.pack(fill="x", pady=(0, 6))
        SectionLabel(params_card, "GA Parameters").pack(anchor="w")
        hline(params_card)

        grid = tk.Frame(params_card, bg=PANEL)
        grid.pack(fill="x")
        labels   = ["Population Size", "Generations", "Mutation Rate", "Crossover Rate"]
        defaults = ["100", "200", "0.02", "0.8"]
        self._param_entries = {}

        for col, (lbl, default) in enumerate(zip(labels, defaults)):
            tk.Label(grid, text=lbl, font=FONT_XS, fg=MUTED, bg=PANEL
                     ).grid(row=0, column=col, padx=8, pady=(0, 2))
            e = DarkEntry(grid, width=10)
            e.insert(0, default)
            e.grid(row=1, column=col, padx=8, pady=(0, 4))
            self._param_entries[lbl] = e
            grid.columnconfigure(col, weight=1)

        # ── Run controls ─────────────────────────────────────────────────────
        ctrl_card = tk.Frame(parent, bg=PANEL, pady=8, padx=10)
        ctrl_card.pack(fill="x", pady=(0, 6))
        ctrl_row = tk.Frame(ctrl_card, bg=PANEL)
        ctrl_row.pack(fill="x")

        self._run_btn = DarkButton(ctrl_row, text="▶  RUN GA",
                                    color=SUCCESS, width=14,
                                    command=self._start_ga)
        self._run_btn.pack(side="left", padx=(0, 10))

        self._stop_btn = DarkButton(ctrl_row, text="■  STOP",
                                     color=ERROR, width=10,
                                     command=self._stop_ga, state="disabled")
        self._stop_btn.pack(side="left", padx=(0, 10))

        DarkButton(ctrl_row, text="💾  Export", color=ACCENT2, width=10,
                   command=self._export_results).pack(side="left")

        self._progress = ttk.Progressbar(ctrl_card, orient="horizontal",
                                          mode="determinate", maximum=100)
        ttk.Style().configure("TProgressbar", troughcolor=PANEL2,
                               background=ACCENT, borderwidth=0)
        self._progress.pack(fill="x", pady=(8, 0))

        # ── Fitness chart ────────────────────────────────────────────────────
        chart_card = tk.Frame(parent, bg=PANEL, pady=8, padx=10)
        chart_card.pack(fill="both", expand=True, pady=(0, 6))
        SectionLabel(chart_card, "Fitness Chart").pack(anchor="w")
        hline(chart_card)
        self._chart = FitnessChart(chart_card)
        self._chart.pack(fill="both", expand=True)

        # ── Results panel ────────────────────────────────────────────────────
        results_card = tk.Frame(parent, bg=PANEL, pady=8, padx=10)
        results_card.pack(fill="x", pady=(0, 4))
        SectionLabel(results_card, "Results").pack(anchor="w")
        hline(results_card)

        badges = tk.Frame(results_card, bg=PANEL)
        badges.pack(fill="x", pady=(0, 6))

        def badge(parent, label, var_name, color):
            f = tk.Frame(parent, bg=PANEL2, padx=10, pady=6)
            f.pack(side="left", expand=True, fill="x", padx=(0, 6))
            tk.Label(f, text=label, font=FONT_XS, fg=MUTED, bg=PANEL2).pack()
            v = tk.StringVar(value="—")
            setattr(self, var_name, v)
            tk.Label(f, textvariable=v, font=("Consolas", 14, "bold"),
                     fg=color, bg=PANEL2).pack()

        badge(badges, "Best Value",   "_val_var",  SUCCESS)
        badge(badges, "Total Weight", "_wt_var",   WARNING)
        badge(badges, "Items Picked", "_cnt_var",  ACCENT)

        self._result_text = tk.Text(results_card, height=5, bg=PANEL2,
                                     fg=TEXT, font=FONT_S, relief="flat",
                                     state="disabled", wrap="word",
                                     insertbackground=ACCENT)
        self._result_text.pack(fill="x")

    # ── ACTIONS ───────────────────────────────────────────────────────────────
    def _set_mode(self, mode):
        self.mode.set(mode)
        if mode == "01":
            self._btn_01.config(bg=ACCENT, fg="#fff")
            self._btn_ub.config(bg=PANEL2, fg=MUTED)
        else:
            self._btn_01.config(bg=PANEL2, fg=MUTED)
            self._btn_ub.config(bg=ACCENT, fg="#fff")

    def _load_default_items(self):
        if self._datasets:
            first_key = list(self._datasets.keys())[0]
            ds = self._datasets[first_key]
            self._items_table.set_items(ds["items"])
            self._cap_entry.delete(0, "end")
            self._cap_entry.insert(0, str(ds["capacity"]))

    def _load_dataset(self):
        name = self._ds_var.get()
        if not name or name not in self._datasets:
            return
        ds = self._datasets[name]
        self._items_table.set_items(ds["items"])
        self._cap_entry.delete(0, "end")
        self._cap_entry.insert(0, str(ds["capacity"]))
        self._status(f"Loaded: {name}")

    def _add_item_dialog(self):
        dlg = tk.Toplevel(self)
        dlg.title("Add Item")
        dlg.configure(bg=PANEL)
        dlg.resizable(False, False)
        dlg.grab_set()

        fields = {}
        for row, (label, default) in enumerate([("Name", ""),
                                                  ("Weight", "1"),
                                                  ("Value", "10")]):
            tk.Label(dlg, text=label, font=FONT_B, fg=TEXT, bg=PANEL
                     ).grid(row=row, column=0, padx=12, pady=6, sticky="w")
            e = DarkEntry(dlg, width=18)
            e.insert(0, default)
            e.grid(row=row, column=1, padx=12, pady=6)
            fields[label] = e

        def confirm():
            try:
                item = {
                    "name":   fields["Name"].get().strip(),
                    "weight": float(fields["Weight"].get()),
                    "value":  float(fields["Value"].get()),
                }
                if not item["name"]:
                    raise ValueError("Name cannot be empty.")
                self._items_table.add_item(item)
                dlg.destroy()
            except ValueError as ex:
                messagebox.showerror("Invalid Input", str(ex), parent=dlg)

        DarkButton(dlg, text="Add", command=confirm
                   ).grid(row=3, column=0, columnspan=2, pady=10)

    def _random_items(self):
        n = random.randint(5, 12)
        items = generate_random_items(n=n)
        self._items_table.set_items(items)
        self._status(f"Generated {n} random items.")

    def _start_ga(self):
        items = self._items_table.get_items()
        ok, msg = validate_items(items)
        if not ok:
            messagebox.showerror("Items Error", msg)
            return

        ok, capacity, msg = validate_capacity(self._cap_entry.get())
        if not ok:
            messagebox.showerror("Capacity Error", msg)
            return

        raw_params = {
            "population_size": self._param_entries["Population Size"].get(),
            "generations":     self._param_entries["Generations"].get(),
            "mutation_rate":   self._param_entries["Mutation Rate"].get(),
            "crossover_rate":  self._param_entries["Crossover Rate"].get(),
        }
        ok, params, msg = validate_ga_params(raw_params)
        if not ok:
            messagebox.showerror("GA Params Error", msg)
            return

        self._progress["value"] = 0
        self._clear_results()
        self._chart.clear()
        self._run_btn.config(state="disabled")
        self._stop_btn.config(state="normal")
        self._running = True
        self._ga_ref  = [None]   # holds the GeneticAlgorithm instance for stop()
        self._status("Running GA…")

        mode = self.mode.get()

        def worker():
            def progress_cb(gen, total, best_fit):
                pct = int(gen / total * 100)
                self.after(0, lambda: self._progress.config(value=pct))
                self.after(0, lambda: self._status(
                    f"Gen {gen}/{total}  |  Best fitness: {best_fit:.2f}"))

            try:
                solution, history = run_ga(
                    items, capacity, mode, params,
                    progress_cb=progress_cb,
                    ga_instance=self._ga_ref,
                )
                self.after(0, lambda: self._on_ga_done(solution, history))
            except Exception as ex:
                self.after(0, lambda: messagebox.showerror("GA Error", str(ex)))
                self.after(0, self._reset_controls)

        threading.Thread(target=worker, daemon=True).start()

    def _stop_ga(self):
        """Stop the GA cleanly via GeneticAlgorithm.stop() from ga.py."""
        if getattr(self, "_ga_ref", [None])[0] is not None:
            self._ga_ref[0].stop()
        self._running = False
        self.after(0, lambda: self._status("Stopped by user."))
        self.after(0, self._reset_controls)

    def _reset_controls(self):
        self._run_btn.config(state="normal")
        self._stop_btn.config(state="disabled")
        self._running = False

    def _on_ga_done(self, solution, history):
        self._running     = False
        self._last_result = solution
        self._reset_controls()
        self._progress["value"] = 100

        self._val_var.set(f"{solution['total_value']:.2f}")
        self._wt_var.set(f"{solution['total_weight']:.2f}")
        self._cnt_var.set(str(len(solution["selected_items"])))

        mode_label = ("0-1 Knapsack" if self.mode.get() == "01"
                      else "Unbounded Knapsack")
        formatted  = format_solution(solution, mode_label)

        self._result_text.config(state="normal")
        self._result_text.delete("1.0", "end")
        self._result_text.insert("end", formatted)
        self._result_text.config(state="disabled")

        self._chart.plot(history)
        self._status(f"Done!  Best value: {solution['total_value']:.2f}  |  "
                     f"Weight: {solution['total_weight']:.2f}")

    def _clear_results(self):
        for var in (self._val_var, self._wt_var, self._cnt_var):
            var.set("—")
        self._result_text.config(state="normal")
        self._result_text.delete("1.0", "end")
        self._result_text.config(state="disabled")

    def _export_results(self):
        if not self._last_result:
            messagebox.showinfo("Nothing to export", "Run the GA first.")
            return
        mode_label = ("0-1 Knapsack" if self.mode.get() == "01"
                      else "Unbounded Knapsack")
        text = format_solution(self._last_result, mode_label)
        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile="knapsack_results.txt",
        )
        if path:
            save_results_to_file(path, text)
            self._status(f"Results saved to: {path}")

    def _status(self, msg):
        self._status_var.set(f"  {msg}")


# ═════════════════════════════════════════════════════════════════════════════
#  SPLASH SCREEN
# ═════════════════════════════════════════════════════════════════════════════
def show_splash(root):
    splash = tk.Toplevel()
    splash.overrideredirect(True)
    w, h = 380, 200
    sw = splash.winfo_screenwidth()
    sh = splash.winfo_screenheight()
    splash.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")
    splash.configure(bg=PANEL)

    tk.Frame(splash, bg=ACCENT, height=3).pack(fill="x")
    tk.Label(splash, text="⬡", font=("Consolas", 32), fg=ACCENT, bg=PANEL
             ).pack(pady=(18, 4))
    tk.Label(splash, text="KNAPSACK GA SOLVER",
             font=("Consolas", 14, "bold"), fg=TEXT, bg=PANEL
             ).pack()
    tk.Label(splash, text="CS212 · Artificial Intelligence · Q19",
             font=FONT_XS, fg=MUTED, bg=PANEL
             ).pack(pady=(4, 16))

    bar = ttk.Progressbar(splash, orient="horizontal", mode="indeterminate",
                           length=280)
    bar.pack()
    bar.start(12)

    root.withdraw()
    root.after(1800, lambda: (splash.destroy(), root.deiconify()))


# ═════════════════════════════════════════════════════════════════════════════
#  ENTRY POINT
# ═════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    app = KnapsackApp()
    show_splash(app)
    app.mainloop()