# README.md

# SMOOTH-Lexical-Diversity

This repository provides Python code for the analysis of **narrative transcripts**.  
It includes automated computation of **lexical diversity (LD) indices** and an optional script for **clitic detection**.  
The pipeline works with both **Italian** and **English** data, depending on the `LANGUAGE` specified in the configuration.

---

## Contents

- config.py – configuration file (input/output paths, language setting, spaCy model).  
- main.py – computes lexical diversity indices (TTR, MATTR, HD-D, MTLD, WIM).  
- lexdiv_functions.py – custom function for WIM calculation.  
- requirements.txt – list of Python dependencies.  
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

1. Place your .cha or .txt transcripts in the data/ folder.  
   - Each line should correspond to one utterance.  
   - Metadata lines (e.g., starting with @) are ignored.  
   - Only files ending with `-it.txt` / `-it.cha` or `-en.txt` / `-en.cha` will be processed, depending on the LANGUAGE setting.  

2. Edit config.py to set:  
   - TXT_PATH (input folder)  
   - OUTPUT_PATH (output folder)  
   - LANGUAGE = "it" for Italian or LANGUAGE = "en" for English # this variable set the language for the test script. The test script analyze only the subfolders corresponding to the language specified in this variable. 

3. Run test or main analysis:  
   - python test.py # analyze only specific-language folder
   - python main.py  # analyze all data content according to the corresponding spaCy model declared in `config.SPACY_MODELS`. Results are then stored in the directory
defined by `config.OUTPUT_PATH`.
   → Results will be saved in output/lexical_diversity_results.csv  

---

## Citation

If you use this code, please cite:  
xxxxx

For any technical question contact francesco.petriglia@unito.it

---

## License

These files are made available under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License (CC BY-NC-ND 4.0).  
For uses not covered by this license, please contact the corresponding author.

