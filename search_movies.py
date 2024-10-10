"""
Copyright: Ole Schildt, ole.schildt.22@heilbronn.dhbw.de
"""
import pandas as pd
import sys
import spacy
from spacy.util import is_package

class Searchmovies():
    """
    Class representing a search engine for movies
    """

    def __init__(self, filename):
        """
        Args:
            filename (str): Path to the movie file
        """
        self.lemma_flag = False #Do not use True !!! It will take time ;)

        model_name = "en_core_web_sm"
        if not is_package(model_name):
            print(f"Model '{model_name}' not found. Downloading and installing the model...")
            spacy.cli.download(model_name)
        self.nlp = spacy.load("en_core_web_sm")

        self.read_movies(filename)

    def read_movies(self, filename):
        """
        Reads movie file separated by tab and splits     
        it into titles and descriptions into class variables

        Args:
            filename (str): Path to the movie file
        Returns:
            None
        """
        try:
            self.movies_df = pd.read_csv(filename, sep='\t', header=None, names=['Title', 'Description'])
        except Exception as e:
            print(f"Error while reading :p : {e}")
            sys.exit()
    
    def lemmatize(self, text):
        """
        Lemmatizes the input text using spaCy.

        Args:
            text (str): Input string to be lemmatized.
        
        Returns:
            str: A string where each word is replaced by its lemmatized form.
        """
        if self.lemma_flag:
            doc = self.nlp(text)  
            lemmatized_text = ' '.join([token.lemma_ for token in doc])
            return lemmatized_text
        return text

    def normalize_string(self, s):
        """
        Normalizing and sorting string.
        
        Args:
            s (str): Input string.
        
        Returns:
            str: Sorted string
        """
        lemmatized_string = self.lemmatize(s)
        return ' '.join(sorted(lemmatized_string.lower().split()))

    def levenshtein_distance(self, str1, str2):
        """
        Calculates the Levenshtein distance between two strings.
        
        Args:
            str1 (str): The first string.
            str2 (str): The second string.
        
        Returns:
            int: The Levenshtein distance between str1 and str2.
        """
        # initialize matrix
        matrix = [[0 for j in range(len(str2)+1)] for i in range(len(str1)+1)]

        # initialize base case 
        for i in range(len(str1)+1):
            matrix[i][len(str2)] = len(str1) - i
        for j in range(len(str2)+1):
            matrix[len(str1)][j] = len(str2) -j

        # looping backwards throigh the matrix and leaving the base case out
        for i in range(len(str1)-1, -1, -1):
            for j in range(len(str2)-1, -1, -1):
                if str1[i] == str2[j]:
                    matrix[i][j] = matrix[i + 1][j + 1] 
                else:
                    # one plus lowest case for delete insert and replace
                    matrix[i][j] = (1 + min(matrix[i + 1][j], matrix[i][j + 1], matrix[i + 1][j +1]))
        
        return matrix[0][0]
        


    def get_word_combinations(self, words, n):
        """
        Return all consecutive n-word combinations from a list of words.
        
        Args:
            words (list): List of words from the title.
            n (int): Number of words in the search term.
        
        Returns:
            list: A list of n-word combinations from the title.
        """
        return [' '.join(words[i:i+n]) for i in range(len(words) - n + 1)]

    def is_within_distance(self, row, search_term, max_distance):
        """
        Checks if any combination of words in the title is within the specified Levenshtein distance 
        from the search term.

        Args:
            row (pd.Series): A row from the DataFrame (with movie title and description).
            search_term (str): The normalized search term.
            max_distance (int): The maximum allowed Levenshtein distance.
        
        Returns:
            int or None: The Levenshtein distance if within the allowed distance, otherwise None.
        """
        search_term_words = search_term.split()
        search_term_word_count = len(search_term_words)

        title_words = row['Title'].split()

        word_combinations = self.get_word_combinations(title_words, search_term_word_count)

        for combination in word_combinations:
            normalized_combination = self.normalize_string(combination)
            distance = self.levenshtein_distance(search_term, normalized_combination)
            if distance <= max_distance:
                return distance

        return None
    
    def calculate_dynamic_distance(self, search_term_length):
        """
        Calculates the dynamic Levenshtein distance based on the length of the search term.
        
        Args:
            search_term_length (int): The length of the search term.
        
        Returns:
            int: The dynamically calculated maximum allowed Levenshtein distance.
        """
        dynamic_distance = (search_term_length - 1) // 4
        print(f'Used Distance is {dynamic_distance}')
        return dynamic_distance

    def search_title(self, search_term):
        """
        Normalizes the search term (so the order of words doesn't matter) and finds all matches 
        within a certain Levenshtein distance.
        
        Args:
            search_term (str): String to search for.
        
        Returns:
            None
        """
        
        normalized_search_term = self.normalize_string(search_term)
        print(normalized_search_term)

        max_distance = self.calculate_dynamic_distance(len(normalized_search_term))
        
        identical = self.movies_df[self.movies_df['Title'].str.lower().str.contains(search_term.lower())]
        
        if identical.empty:
            matches = []
            for _, row in self.movies_df.iterrows():
                distance = self.is_within_distance(row, normalized_search_term, max_distance)
                if distance is not None:
                    matches.append((row['Title'], row['Description'], distance))
            
            if matches:
                sorted_matches = sorted(matches, key=lambda x: (x[2], x[0].lower())) 
                for title, description, distance in sorted_matches:
                    print(f"Title: {title}\nDescription: {description}\nLevenshtein Distance: {distance}\n")
            else:
                print(f"No movies found for '{search_term}'.")
        else:
            identical.apply(lambda row: print(f"Title: {row['Title']}\nDescription: {row['Description']}\n"), axis=1)


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("pls add your filename")
        sys.exit()

    filename = sys.argv[1]
    
    movie_search = Searchmovies(filename)
    
    try:
        while True:
            
            search_term = input("Your search term (vim commands to exit): ")

            if search_term == ":q!":
                sys.exit()

            movie_search.search_title(search_term)
            
    except KeyboardInterrupt:
        print("\nExit")
        sys.exit()