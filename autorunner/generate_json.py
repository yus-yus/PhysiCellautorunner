import xml.etree.ElementTree as ET
import json
import sys

# 引数からファイルパスを取得
xml_file_path = sys.argv[1]  # XMLファイルのパス
json_file_path = sys.argv[2]  # 出力するJSONファイルのパス

# 出力を格納する辞書
data_dict = {}

# XMLファイルを解析
tree = ET.parse(xml_file_path)
root = tree.getroot()

# 再帰的に全ての要素とその値を辞書に格納する関数
def extract_elements(element, parent_path=""):
    tag_name = element.tag
    current_path = f"{parent_path}/{tag_name}" if parent_path else tag_name
    value = element.text.strip() if element.text else ""
    
    if value:
        current_path = current_path.lstrip("/PhysiCell_settings")
        data_dict[current_path] = value
    
    for child in element:
        extract_elements(child, current_path)

# ルート要素から開始
extract_elements(root)

# JSONとして保存
with open(json_file_path, 'w', encoding='utf-8') as f:
    json.dump(data_dict, f, ensure_ascii=False, indent=4)

print(f"JSONファイルが保存されました: {json_file_path}")
