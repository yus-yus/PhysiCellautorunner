import xml.etree.ElementTree as ET
from pathlib import Path

# physicell_settingsの設定を書き換えて保存する関数
def change_settings(PHYSICELL_SETTINGS_FILE_PATH: Path, change_part : str, change_elemement : int | str, save_path : Path) -> None:

    # XML
    tree = ET.parse(PHYSICELL_SETTINGS_FILE_PATH)
    root = tree.getroot()

    # 実行結果の保存先を変更
    root.find('./save/folder').text = str(save_path)

    # random_seedを変更する場合
    if change_part == r"./user_parameters/random_seed":
        root.find(r'./initial_conditions/cell_positions').attrib['enabled'] = 'false'

    # 設定を変更
    if root.find(change_part) is None:
        print(f"Warning: {change_part} not found in the XML.")
        return
    root.find(change_part).text = str(change_elemement)
    
    # 変更した設定をファイルに書き込む
    tree.write(PHYSICELL_SETTINGS_FILE_PATH)
    
