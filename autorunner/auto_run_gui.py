import tkinter as tk
from tkinter import filedialog, messagebox
from settings import save_settings, load_settings
import subprocess


def browse_xml_file():
    filename = filedialog.askopenfilename(filetypes=[("XML Files", "*.xml")])
    xml_path_entry.delete(0, tk.END)
    xml_path_entry.insert(0, filename)

def browse_json_dir():  # 出力ディレクトリ選択用の関数
    foldername = filedialog.askdirectory()  # ユーザーがディレクトリを選択
    json_output_dir_entry.delete(0, tk.END)  # エントリーをクリア
    json_output_dir_entry.insert(0, foldername)  # 選択したディレクトリを設定

def browse_json_file():  # 編集済み設定ファイル選択用の関数
    filename = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])  # JSONファイルのみ選択
    json_path_entry.delete(0, tk.END)
    json_path_entry.insert(0, filename)

def browse_results_dir():  # シミュレーション結果の保存先用のディレクトリ選択
    foldername = filedialog.askdirectory()
    results_dir_entry.delete(0, tk.END)
    results_dir_entry.insert(0, foldername)

def generate_json():
    xml_file = xml_path_entry.get()  # 元となるXMLファイルのパス
    json_output_dir = json_output_dir_entry.get()  # JSONファイルを保存するディレクトリ

    if not xml_file or not json_output_dir:
        messagebox.showerror("エラー", "XMLファイルと出力先のディレクトリを指定してください。")
        return
    
    # JSONファイル名を固定
    json_file = f"{json_output_dir}/generated_config.json"
    
    # generate_json.py を呼び出す
    command = [
        "python", "generate_json.py", xml_file, json_file
    ]
    
    try:
        subprocess.run(command, check=True)
        messagebox.showinfo("成功", f"JSONファイルが {json_file} に生成されました。")
    except subprocess.CalledProcessError:
        messagebox.showerror("エラー", "JSONファイルの生成に失敗しました。")

def run_simulation():
    json_file = json_path_entry.get()
    results_dir = results_dir_entry.get()
    phys_cell_dir = phys_cell_path_entry.get()  # PhysiCellのインストールパス
    exe_file = exe_path_entry.get()  # 実行ファイル
    phys_cell_settings_file = settings_file_entry.get()  # PhysiCell設定ファイルのパス

    if not json_file or not results_dir or not phys_cell_dir or not exe_file or not phys_cell_settings_file:
        messagebox.showerror("エラー", "必要なパスがすべて指定されていません。")
        return

    # auto_run.py を呼び出す
    command = [
        "python", "auto_run.py",
        json_file, phys_cell_dir, exe_file, results_dir, phys_cell_settings_file
    ]
    
    try:
        subprocess.run(command, check=True)
        messagebox.showinfo("成功", f"シミュレーションが {results_dir} に実行されました。")
    except subprocess.CalledProcessError:
        messagebox.showerror("エラー", "シミュレーションの実行に失敗しました。")


def main():
    global xml_path_entry, json_output_dir_entry, json_path_entry, results_dir_entry
    global phys_cell_path_entry, exe_path_entry, settings_file_entry

    # 初期設定を読み込む
    settings = load_settings()

    # GUIの設定
    root = tk.Tk()
    root.title("PhysiCell 自動実行ツール")

    # PHYSICELL_PATH の設定
    tk.Label(root, text="PhysiCell のインストールディレクトリ").grid(row=0, column=0)
    phys_cell_path_entry = tk.Entry(root, width=40)
    phys_cell_path_entry.grid(row=0, column=1)
    phys_cell_path_entry.insert(0, settings["PHYSICELL_PATH"])  # 前回の設定を反映
    tk.Button(root, text="ディレクトリ選択", command=lambda: browse_path(phys_cell_path_entry)).grid(row=0, column=2)

    # PHYSICELL_SETTINGS_FILE_PATH の設定
    tk.Label(root, text="PhysiCell 設定ファイル").grid(row=1, column=0)
    settings_file_entry = tk.Entry(root, width=40)
    settings_file_entry.grid(row=1, column=1)
    settings_file_entry.insert(0, settings["PHYSICELL_SETTINGS_FILE_PATH"])  # 前回の設定を反映
    tk.Button(root, text="ファイル選択", command=lambda: browse_file(settings_file_entry)).grid(row=1, column=2)

    # EXE_PATH の設定
    tk.Label(root, text="実行ファイル").grid(row=2, column=0)
    exe_path_entry = tk.Entry(root, width=40)
    exe_path_entry.grid(row=2, column=1)
    exe_path_entry.insert(0, settings["EXE_PATH"])  # 前回の設定を反映
    tk.Button(root, text="ファイル選択", command=lambda: browse_file(exe_path_entry)).grid(row=2, column=2)

    # XMLファイルの選択
    tk.Label(root, text="元となるXMLファイル").grid(row=4, column=0)
    xml_path_entry = tk.Entry(root, width=40)
    xml_path_entry.grid(row=4, column=1)
    tk.Button(root, text="ファイル選択", command=browse_xml_file).grid(row=4, column=2)

    # JSONファイル保存先ディレクトリの選択
    tk.Label(root, text="設定ファイルの保存先ディレクトリ").grid(row=5, column=0)
    json_output_dir_entry = tk.Entry(root, width=40)
    json_output_dir_entry.grid(row=5, column=1)
    tk.Button(root, text="ディレクトリ選択", command=browse_json_dir).grid(row=5, column=2)

    # JSON生成ボタン
    tk.Button(root, text="設定ファイル生成", command=generate_json).grid(row=6, column=1)

    # 編集済みJSONファイルの選択
    tk.Label(root, text="編集済み設定ファイル").grid(row=7, column=0)
    json_path_entry = tk.Entry(root, width=40)
    json_path_entry.grid(row=7, column=1)
    tk.Button(root, text="ファイル選択", command=browse_json_file).grid(row=7, column=2)

    # 結果ディレクトリの選択
    tk.Label(root, text="シミュレーション結果保存先").grid(row=8, column=0)
    results_dir_entry = tk.Entry(root, width=40)
    results_dir_entry.grid(row=8, column=1)
    tk.Button(root, text="ディレクトリ選択", command=browse_results_dir).grid(row=8, column=2)

    # 実行ボタン
    tk.Button(root, text="シミュレーション実行", command=run_simulation).grid(row=9, column=1)

    # 設定保存ボタン
    def save_config():
        phys_cell_path = phys_cell_path_entry.get()
        settings_file_path = settings_file_entry.get()
        exe_path = exe_path_entry.get()
        
        # 必要な設定が入力されているか確認
        if not phys_cell_path or not settings_file_path or not exe_path:
            messagebox.showerror("エラー", "すべての設定を入力してください。")
            return
        
        # 設定を保存
        save_settings(phys_cell_path, settings_file_path, exe_path)
        messagebox.showinfo("成功", "設定が保存されました。")

    tk.Button(root, text="設定保存", command=save_config).grid(row=3, column=1)

    # ファイル選択ダイアログの関数
    def browse_path(entry):
        foldername = filedialog.askdirectory()
        entry.delete(0, tk.END)
        entry.insert(0, foldername)

    def browse_file(entry):
        filename = filedialog.askopenfilename()
        entry.delete(0, tk.END)
        entry.insert(0, filename)

    root.mainloop()


if __name__ == "__main__":
    main()