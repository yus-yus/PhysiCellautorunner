import sys
from pathlib import Path
import json
import itertools
import os

# 必要なモジュールをインポート
from modules.make_dir import make_dir
from modules.change_settings import change_settings
from modules.run import run


# 範囲の文字列をリストに変換する関数
def parse_range(range_str):
    if '..' in range_str:
        try:
            start, end = map(int, range_str.split('..'))
            return list(range(start, end + 1))
        except ValueError:
            print(f"Invalid range format: {range_str}")
            return []
    else:
        return [v.strip() for v in range_str.split(",") if v.strip()]

# 設定を変更しながらシミュレーションを実行する
def auto_run(json_path, phys_cell_path, exe_path, save_parent_dir_path, phys_cell_settings_path):
    # JSONから設定を読み込む
    with open(json_path, 'r', encoding="utf-8") as f:
        param_dict = json.load(f)

    # パラメータ名とその値リストを展開
    keys = list(param_dict.keys())
    
    # 値をリストに変換
    for key, value in param_dict.items():
        param_dict[key] = parse_range(value)
    
    # すべての組み合わせを生成
    value_product = list(itertools.product(*(param_dict[key] for key in keys)))

    for idx, combo in enumerate(value_product, 1):
        name = "output" + str(idx)
        save_path = make_dir(save_parent_dir_path, name)
        
        for key, value in zip(keys, combo):
            change_settings(phys_cell_settings_path, key, value, save_path)
    
        run(phys_cell_path, exe_path)

if __name__ == "__main__":
    # GUIで渡されたパラメータ
    json_path = sys.argv[1]  # 編集済みJSONファイルのパス
    phys_cell_path = sys.argv[2]  # PhysiCellのインストールディレクトリ
    exe_path = sys.argv[3]  # 実行可能ファイル
    save_parent_dir_path = sys.argv[4]  # 結果保存先ディレクトリ
    phys_cell_settings_path = sys.argv[5]  # PhysiCell設定ファイルのパス

    auto_run(json_path, phys_cell_path, exe_path, save_parent_dir_path, phys_cell_settings_path)
