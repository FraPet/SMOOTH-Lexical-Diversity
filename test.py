import os
import config
import subprocess

def run_pipeline():
    lang = config.LANGUAGE
    data_path = config.TXT_PATH

    if lang == "it":
        test_file = "test_file-it.cha"
    elif lang == "en":
        test_file = "test_file-en.cha"
    else:
        raise ValueError(f"Unsupported language code: {lang}")

    file_path = os.path.join(data_path, test_file)
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Expected test file not found: {file_path}")

    print(f"[INFO] Running pipeline on {file_path} with language='{lang}'")
    subprocess.run(["python3", "main.py"], check=True)
    subprocess.run(["python3", "clitic_counter.py"], check=True)
    print(f"[INFO] Results saved in: {config.OUTPUT_PATH}")

if __name__ == "__main__":
    run_pipeline()
