import subprocess
from pathlib import Path

# Windows の exe ファイルのパス (WSL に合わせてパス変換)
EXE_PATH = Path(r"/mnt/c/Users/yusyus/MAS/PhysiCell/project.exe")
PHYSICELL_PATH = Path(r"/mnt/c/Users/yusyus/MAS/PhysiCell")

# subprocess 実行とエラー出力の詳細な確認
def run(PHYSICELL_PATH: Path, EXE_PATH: Path, OUTPUT_PATH: Path = None) -> None:
    subprocess.run(
        str(EXE_PATH), 
        shell=True, 
        cwd=str(PHYSICELL_PATH),  # 作業ディレクトリを指定
    )
        

