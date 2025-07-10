import pytest
from pages.pages import BookshelfPage, BookDetailsPage

# --- Positive Test 1: Bookshelf loads and displays books
def test_bookshelf_displays_books(page):
    shelf = BookshelfPage(page)
    shelf.goto()
    books = shelf.get_book_elements()
    assert books and len(books) > 0, "Bookshelf should display a list of books"

# --- Positive Test 2: Can view details of a book
def test_view_book_details(page):
    shelf = BookshelfPage(page)
    shelf.goto()
    shelf.click_book_by_index(0)
    details = BookDetailsPage(page)
    title = details.get_title()
    author = details.get_author()
    rating = details.get_rating()
    assert title and title.strip() != '', "Book title should be visible"
    assert author and author.strip() != '', "Book author should be visible"
    assert rating and 'User rating' in rating, "Book rating should be visible"

# --- Negative Test 1: Invalid regex in search shows validation error
def test_invalid_regex_search_shows_error(page):
    shelf = BookshelfPage(page)
    shelf.goto()
    shelf.search('[')  # Invalid regex
    assert shelf.is_invalid_feedback_visible(), "Invalid regex feedback not shown"

# --- Negative Test 2: Book with missing author or rating is handled gracefully
# (Assume 'Ender' book is missing author or rating in the dataset)
def test_book_with_missing_author_or_rating(page):
    shelf = BookshelfPage(page)
    shelf.goto()
    shelf.search('Ender')
    shelf.click_book_by_index(0)
    details = BookDetailsPage(page)
    author = details.get_author()
    rating = details.get_rating()
    # Accept either a placeholder or empty, but should not break the UI
    assert author is not None, "Book author should be handled gracefully (not None)"
    assert rating is not None, "Book rating should be handled gracefully (not None)" 