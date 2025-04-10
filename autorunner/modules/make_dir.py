from pathlib import Path

# フォルダを作成
def make_dir(parent_dir_path: Path, new_dir_name: str) -> Path:
    # Windows形式のパスを保持
    parent_dir_path = Path(parent_dir_path)
    new_dir_path: Path = parent_dir_path / new_dir_name

    # フォルダが存在するかどうか確認し、存在する場合は上書き
    if new_dir_path.exists():
        overwrite: str = input(f"The dir {new_dir_name} is already exists. Do you want to overwrite it? (y/n): ").strip().lower()
        if overwrite != 'y':
            new_dir_name = input("Please provide a new dir name: ").strip()
            return make_dir(parent_dir_path, new_dir_name)
    # フォルダが存在しない場合に作成
    new_dir_path.mkdir(parents=True, exist_ok=True)

    return new_dir_path
