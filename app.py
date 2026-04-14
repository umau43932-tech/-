from __future__ import annotations

from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox

from file_organizer import organize_directory


class OrganizerApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("ファイル整理アプリ")
        self.root.geometry("620x420")

        self.selected_path = tk.StringVar()

        top_frame = tk.Frame(root)
        top_frame.pack(fill="x", padx=12, pady=12)

        tk.Label(top_frame, text="整理するフォルダ:").pack(side="left")
        tk.Entry(top_frame, textvariable=self.selected_path, width=52).pack(side="left", padx=8)
        tk.Button(top_frame, text="参照", command=self.choose_directory).pack(side="left")

        action_frame = tk.Frame(root)
        action_frame.pack(fill="x", padx=12)

        tk.Button(action_frame, text="整理を実行", command=self.run_organize, bg="#2d7ef7", fg="white").pack(side="left")
        tk.Button(action_frame, text="ドライラン", command=self.run_dry).pack(side="left", padx=8)

        self.log = tk.Text(root, height=18)
        self.log.pack(fill="both", expand=True, padx=12, pady=12)

        self.write_log("使い方: フォルダを選択して『整理を実行』を押してください。")

    def choose_directory(self) -> None:
        folder = filedialog.askdirectory(title="整理するフォルダを選択")
        if folder:
            self.selected_path.set(folder)
            self.write_log(f"選択: {folder}")

    def run_dry(self) -> None:
        self._organize(move_files=False)

    def run_organize(self) -> None:
        self._organize(move_files=True)

    def _organize(self, move_files: bool) -> None:
        path = self.selected_path.get().strip()
        if not path:
            messagebox.showwarning("入力エラー", "フォルダを選択してください。")
            return

        directory = Path(path)
        try:
            results = organize_directory(directory, move_files=move_files)
        except ValueError as e:
            messagebox.showerror("エラー", str(e))
            return
        except Exception as e:  # noqa: BLE001
            messagebox.showerror("予期せぬエラー", str(e))
            return

        mode = "実行" if move_files else "ドライラン"
        self.write_log(f"\n[{mode}] {directory}")
        if not results:
            self.write_log("対象ファイルが見つかりませんでした。")
        for r in results:
            self.write_log(f"- {r.source.name} -> {r.destination.relative_to(directory)}")

        if move_files:
            messagebox.showinfo("完了", f"{len(results)} 件のファイルを整理しました。")

    def write_log(self, text: str) -> None:
        self.log.insert(tk.END, text + "\n")
        self.log.see(tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = OrganizerApp(root)
    root.mainloop()
