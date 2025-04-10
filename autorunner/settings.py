import json
import os

# 設定ファイルのパス（このコードが実行されているディレクトリに保存されます）
settings_file = "settings.json"

# 設定を保存する関数
def save_settings(phys_cell_path, settings_file_path, exe_path):
    settings = {
        "PHYSICELL_PATH": phys_cell_path,
        "PHYSICELL_SETTINGS_FILE_PATH": settings_file_path,
        "EXE_PATH": exe_path
    }
    
    # 設定をJSON形式で保存
    with open(settings_file, "w", encoding="utf-8") as f:
        json.dump(settings, f, ensure_ascii=False, indent=4)

# 設定を読み込む関数
def load_settings():
    # 設定ファイルが存在する場合、読み込み
    if os.path.exists(settings_file):
        with open(settings_file, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        # 設定ファイルがない場合はデフォルト設定を返す
        return {
            "PHYSICELL_PATH": "",
            "PHYSICELL_SETTINGS_FILE_PATH": "",
            "EXE_PATH": ""
        }
    