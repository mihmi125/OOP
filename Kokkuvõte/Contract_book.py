"""Movie."""


class Movie:
    """Movie object, do not change."""

    def __init__(self, name: str, year: int, genres: list):
        """Movie constructor."""
        self.name = name
        self.year = year
        self.genres = genres


def create_movie(name_with_year: str, genre1: str, genre2: str):
    """
    Create a new movie from name and 2 genres.

    Name is in format "name some thing (2019)".
    Year is inside parenthesis and always 4 digits.
    Everything before parenthesis is a name.
    Return None, if:
    - year is below 1900 and above 2020 ("blah (1200)", "blah (3000)")
    - name is empty ("(1933)")
    Otherwise create a new movie and return it.

    Year has to be int.
    Remove trailing space from name.
    "film (1999)" => should give "film" 1999
    """
    pass


def get_ordered_movies(movies: list) -> list:
    """
    Return sorted movies by year (desc, newer first) and count of genres (asc).

    If both year and count of genres are the same, keep the original order.
    """
    pass


def add_genres(movies: list, genres: list) -> None:
    """
    Modify the movies in the list by adding genres.

    A genre is added if it does not already exist.
    """
    pass


def remove_movies_by_genre(movies: list, genre: str) -> list:
    """
    Return a new list where all the movies with the given genre are removed.

    The order of movies should remain the same.
    The original movies list should remain unchanged.
    """
    pass