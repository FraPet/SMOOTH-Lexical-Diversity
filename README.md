# SMOOTH-Lexical-Diversity

This repository provides the Python code used to analyze **narrative transcripts** for research on language development in children with cochlear implants.  It includes automated computation of **lexical diversity (LD) indices** and a dedicated script for **clitic detection** as used in this paper (Multilevel Narrative Assessment in Children with Early Cochlear Implants Compared to Typically Hearing Peers. Francesco Petriglia, Andrea Marini, Agata Marchetti Guerrini, Diego Di Lisi, Patrizia Consolino, Francesca Marina Bosco).  
The pipeline works with both **Italian** and **English** data, depending on the spaCy model selected in the configuration.

---

## Contents

- config.py – configuration file (input/output paths, language setting).  <-- start from here
- main.py – computes lexical diversity indices (TTR, MATTR, HD-D, MTLD, WIM).  
- clitic_counter.py – identifies and counts clitic pronouns using spaCy.  
- lexdiv_functions.py – custom function for WIM calculation.  
- requirements.txt – list of Python dependencies.  
- test_pipeline.py – runs both analyses on the appropriate **test file** (`test_file-it.cha` or `test_file-en.cha`).  
- data/ – folder where input transcripts (.cha or .txt, one utterance per line) should be placed.  
- output/ – folder where results will be saved.  

---

## Installation

It is recommended to use a virtual environment (venv) to keep dependencies isolated.  

1. Clone the repository:  
   git clone https://github.com/<your-username>/SMOOTH-Lexical-Diversity.git  
   cd SMOOTH-Lexical-Diversity  

2. Create and activate a virtual environment:  
   python -m venv venv  
   source venv/bin/activate        # on Linux/Mac  
   .\venv\Scripts\Activate.ps1     # on Windows PowerShell  
   venv\Scripts\activate.bat       # on Windows CMD  

3. Install dependencies:  
   pip install -r requirements.txt  

4. Download the spaCy models:  
python -m spacy download it_core_news_lg  
python -m spacy download en_core_web_lg  

---

## Usage

1. Place your `.cha` or `.txt` transcripts in the `data/` folder.  
   Each line should correspond to one utterance. Metadata lines (e.g., starting with `@`) are ignored.  

2. Edit `config.py` to set:  
   - TXT_PATH (input folder)  
   - OUTPUT_PATH (output folder)  
   - LANGUAGE = "it" for Italian or LANGUAGE = "en" for English  

3. Run the LD analysis:  
   python main.py  
   → Results will be saved in `output/lexical_diversity_results.csv`  

4. Run the clitic analysis (optional):  
   python clitic_counter.py  
   → Results will be saved in `output/clitic_results.csv`  

5. Run the test pipeline (to apply both analyses on the mock test file):  
   python test_pipeline.py  
   → This will select `test_file-it.cha` or `test_file-en.cha` depending on the `LANGUAGE` in `config.py`.  
   → Results will be saved in the `output/` folder.  

---

## Citation

If you use this code, please cite:  
xxxxx

For any technical question contact [francesco.petriglia@unito.it](mailto:francesco.petriglia@unito.it)

---

## License

This project is released under the MIT License.
