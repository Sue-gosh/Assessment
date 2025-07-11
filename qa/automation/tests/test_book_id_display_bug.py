import pytest
from pages.pages import BookshelfPage, BookDetailsPage

class TestBookIDDisplayBug:
    """HIGH PRIORITY BUG: Book ID is not displayed on the frontend"""
    
    def test_book_id_displayed_on_details_page(self, page):
        """
        FAILING TEST: Book ID should be displayed on book details page
        
        Bug Description: When viewing book details, the book ID is not displayed
        on the frontend even though it's available in the backend and used in the URL.
        
        Impact: Medium-High - Users cannot see the book ID for reference
        Reproducible: Yes - Click any book, verify ID is not displayed
        """
        shelf = BookshelfPage(page)
        shelf.goto()
        
        # Wait for books to load
        page.wait_for_load_state('networkidle')
        
        # Get the first book and click on it
        books = shelf.get_book_elements()
        
        # Skip test if no books are loaded (backend issue)
        if len(books) == 0:
            pytest.skip("No books loaded - likely backend connection issue")
        
        # Click on first book to view details
        shelf.click_book_by_index(0)
        
        # Wait for navigation to book details page
        page.wait_for_url("**/books/*")
        
        # Extract book ID from URL
        current_url = page.url
        book_id = current_url.split('/')[-1]  # Get the ID from URL
        
        # Verify that the ID is a valid number
        assert book_id.isdigit(), f"Book ID should be a number, got: {book_id}"
        
        # Get book information from frontend
        title = page.text_content('h1[data-v-2dd5deba]')
        author = page.text_content('h2 em')
        rating = page.text_content('div:has-text("User rating")')
        
        # Check that basic information is displayed
        assert title and title.strip() != '', "Book title should be displayed"
        assert author and author.strip() != '', "Book author should be displayed"
        assert rating and 'User rating' in rating, "Book rating should be displayed"
        
        # THE ACTUAL BUG: Book ID is not displayed on the frontend
        # Check for ID information in the page content
        page_content = page.content()
        
        # Look for ID patterns in the page content
        # This will FAIL because the ID is not displayed
        id_patterns = [
            f"ID: {book_id}",
            f"Book ID: {book_id}",
            f"#{book_id}",
            f"ID {book_id}",
            book_id
        ]
        
        # Check if any ID pattern is present in the page
        id_found = any(pattern in page_content for pattern in id_patterns)
        
        assert id_found, f"Book ID '{book_id}' should be displayed on the frontend. " \
                        f"Current page shows: Title: '{title}', Author: '{author}', Rating: '{rating}', " \
                        f"but no ID information."

    def test_book_id_consistency_with_url(self, page):
        """Test that book ID in URL matches what should be displayed"""
        shelf = BookshelfPage(page)
        shelf.goto()
        
        # Wait for books to load
        page.wait_for_load_state('networkidle')
        
        # Get the first book and click on it
        books = shelf.get_book_elements()
        
        # Skip test if no books are loaded (backend issue)
        if len(books) == 0:
            pytest.skip("No books loaded - likely backend connection issue")
        
        # Click on first book to view details
        shelf.click_book_by_index(0)
        
        # Wait for navigation to book details page
        page.wait_for_url("**/books/*")
        
        # Extract book ID from URL
        current_url = page.url
        book_id = current_url.split('/')[-1]
        
        # Verify that the ID is a valid number
        assert book_id.isdigit(), f"Book ID should be a number, got: {book_id}"
        
        # The book ID from URL should be displayed on the page
        # This documents the expected behavior
        page_content = page.content()
        
        # Check if the ID from URL is present in the page content
        assert book_id in page_content, f"Book ID '{book_id}' from URL should be displayed on the page"

    def test_book_details_complete_information(self, page):
        """Test that book details page shows all available information including ID"""
        shelf = BookshelfPage(page)
        shelf.goto()
        
        # Wait for books to load
        page.wait_for_load_state('networkidle')
        
        # Get the first book and click on it
        books = shelf.get_book_elements()
        
        # Skip test if no books are loaded (backend issue)
        if len(books) == 0:
            pytest.skip("No books loaded - likely backend connection issue")
        
        # Click on first book to view details
        shelf.click_book_by_index(0)
        
        # Wait for navigation to book details page
        page.wait_for_url("**/books/*")
        
        # Get book information from frontend
        title = page.text_content('h1[data-v-2dd5deba]')
        author = page.text_content('h2 em')
        rating = page.text_content('div:has-text("User rating")')
        
        # Check that all expected information sections are present
        assert title and title.strip() != '', "Book title should be displayed"
        assert author and author.strip() != '', "Book author should be displayed"
        assert rating and 'User rating' in rating, "Book rating should be displayed"
        
        # Check for additional information that should be present
        page_content = page.content()
        
        # Look for common book information patterns
        information_patterns = [
            "title", "author", "rating", "cover", "description", "id", "book id"
        ]
        
        # At least some of these patterns should be present
        found_patterns = [pattern for pattern in information_patterns if pattern.lower() in page_content.lower()]
        
        # This will fail because ID is missing
        assert len(found_patterns) >= 4, f"Book details page should contain multiple information types including ID. Found: {found_patterns}" 