import os
import config
import subprocess

def run_pipeline():
    """
    Run lexical diversity (main.py) and clitic counter (clitic_counter.py)
    on the test file corresponding to the configured language.
    """

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

    # Run lexical diversity analysis
    print("[INFO] Running main.py ...")
    subprocess.run(["python", "main.py"], check=True)

    # Run clitic counter
    print("[INFO] Running clitic_counter.py ...")
    subprocess.run(["python", "clitic_counter.py"], check=True)

    # Show where results are saved
    print(f"[INFO] Results saved in: {config.OUTPUT_PATH}")

if __name__ == "__main__":
    run_pipeline()
