import unittest
import pandas as pd
from search_movies import Searchmovies
from unittest.mock import patch
import os

class TestSearchMovies(unittest.TestCase):

    def setUp(self):
        movie_file_path = os.path.join(os.path.dirname(__file__), 'movies.txt')
        self.search_movies = Searchmovies(movie_file_path)

    def test_read_movies(self):
        """Test if the movie data is read correctly into a DataFrame."""
        movie_df = self.search_movies.movies_df

        self.assertGreater(len(movie_df), 0, "The DataFrame should not be empty.")
        self.assertEqual(len(movie_df.columns), 2, "The DataFrame should have two columns (Title, Description).")

        self.assertIn("Harry Potter and the Prisoner of Azkaban", movie_df['Title'].values)

    def test_normalize_string(self):
        """Test the normalize_string function."""
        result = self.search_movies.normalize_string("Harry Potter")
        self.assertEqual(result, "harry potter")  

        result = self.search_movies.normalize_string("The Matrix")
        self.assertEqual(result, "matrix the") 

    def test_levenshtein_distance(self):
        """Test the Levenshtein distance calculation."""
        distance = self.search_movies.levenshtein_distance("kitten", "sitting")
        self.assertEqual(distance, 3) 

        distance = self.search_movies.levenshtein_distance("flaw", "lawn")
        self.assertEqual(distance, 2)

    def test_get_word_combinations(self):
        """Test word combination generation."""
        words = "Harry Potter and the Prisoner of Azkaban".split()
        result = self.search_movies.get_word_combinations(words, 2)
        self.assertEqual(result, ['Harry Potter', 'Potter and', 'and the', 'the Prisoner', 'Prisoner of', 'of Azkaban'])

    def test_is_within_distance(self):
        """Test if a title is within a given Levenshtein distance from the search term."""
        row = pd.Series({'Title': "Harry Potter and the Prisoner of Azkaban", 'Description': "Harry faces new dangers in his third year."})
        search_term = "harry potter"
        max_distance = 2
        
        distance = self.search_movies.is_within_distance(row, search_term, max_distance)
        self.assertIsNotNone(distance) 

        search_term = "matrix"
        distance = self.search_movies.is_within_distance(row, search_term, max_distance)
        self.assertIsNone(distance) 


    @patch('builtins.input', side_effect=["Poter Hary", ":q!"])
    @patch('builtins.print')
    def test_search_title_fuzzy(self, mock_print, mock_input):
        """Test the search function and check if needed terms are inside"""

        self.search_movies.search_title("Poter Hary")
        print_calls = [call[0][0] for call in mock_print.call_args_list]
        

        self.assertTrue(any("hary poter" in call for call in print_calls))
        self.assertTrue(any("Used Distance is 2" in call for call in print_calls))
        self.assertTrue(any("Title: Harry Potter and the Prisoner of Azkaban" in call for call in print_calls))
        self.assertTrue(any("Levenshtein Distance: 2" in call for call in print_calls))


if __name__ == "__main__":
    unittest.main()