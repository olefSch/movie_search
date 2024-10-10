# 🎬 Movie Search Engine

This repository contains a simple yet powerful **Movie Search Engine** that allows you to search for movies using **fuzzy matching** based on the **Levenshtein distance** algorithm. The script reads a movie dataset, normalizes search terms, and returns relevant movies even if the query is slightly misspelled.

## Features

- **Fuzzy Matching**: Search movie titles even with spelling mistakes using Levenshtein distance.
- **Lemmatization**: (Optional) Use SpaCy's lemmatizer to further normalize text.
- **Dynamic Distance Calculation**: Automatically adjusts the allowed Levenshtein distance based on the length of the search term.
- **Smooth Handling of Large Datasets**: Efficiently processes movie data from tab-separated files using Pandas.

## 🛠️ Installation

### Prerequisites:
- Python 3.x
- A tab-separated (TSV) file with movie titles and descriptions.
- The following Python libraries:
  - `pandas`
  - `spacy`

### Setup:

1. Clone this repository:
   ```bash
   git clone https://github.com/your-repo-url/movie-search-engine
   cd movie-search-engine
   ```
2. Dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. You need a txt with like this:
    ```text
    Title<TAB>Description
    ```
4. Run the script:
   ```bash
   python searchmovies.py movies.txt
   ```

## 🧠 How It Works

1. **Lemmatization** (Optional): The input text can be lemmatized using SpaCy to ensure that words are in their base form, making the search more flexible.

2. **Normalization**: The search term is normalized by:
   - Converting the search string to lowercase.
   - Sorting the words to ignore word order.

3. **Levenshtein Distance**: The algorithm measures the minimum number of single-character edits (insertions, deletions, or substitutions) required to change one string into another. This allows for fuzzy matching of movie titles.

4. **Dynamic Distance Calculation**: The maximum allowed Levenshtein distance is dynamically calculated based on the length of the search term:
   ```python
   dynamic_distance = (search_term_length - 1) // 4
   ```
5. Search Process:
  - The script first attempts to find exact matches for the search term.
  - If no exact matches are found, it searches for fuzzy matches (titles within a certain Levenshtein distance).
  - The results are sorted by Levenshtein distance and displayed.
