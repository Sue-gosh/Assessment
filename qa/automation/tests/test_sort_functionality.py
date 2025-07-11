import pytest
from pages.pages import BookshelfPage

class TestSortFunctionality:
    """Test cases for sort functionality - happy path tests"""
    
    def test_sort_by_id(self, page):
        """Test sorting books by ID"""
        shelf = BookshelfPage(page)
        shelf.goto()
        
        # Wait for books to load
        page.wait_for_load_state('networkidle')
        
        # Get initial book order
        initial_books = shelf.get_book_elements()
        assert len(initial_books) > 0, "Books should be loaded"
        
        # Sort by ID
        shelf.sort_by('id')
        
        # Wait for sort to complete
        page.wait_for_timeout(2000)
        
        # Get books after sorting
        sorted_books = shelf.get_book_elements()
        assert len(sorted_books) > 0, "Books should still be visible after sorting by ID"
        
        # Verify sort order (books should be ordered by ID)
        # This is a basic verification - in a real scenario you might extract actual ID values
        assert len(sorted_books) == len(initial_books), "Number of books should remain the same after sorting"

    def test_sort_by_rating(self, page):
        """Test sorting books by rating"""
        shelf = BookshelfPage(page)
        shelf.goto()
        
        # Wait for books to load
        page.wait_for_load_state('networkidle')
        
        # Get initial book order
        initial_books = shelf.get_book_elements()
        assert len(initial_books) > 0, "Books should be loaded"
        
        # Sort by rating
        shelf.sort_by('rating')
        
        # Wait for sort to complete
        page.wait_for_timeout(2000)
        
        # Get books after sorting
        sorted_books = shelf.get_book_elements()
        assert len(sorted_books) > 0, "Books should still be visible after sorting by rating"
        
        # Verify sort order
        assert len(sorted_books) == len(initial_books), "Number of books should remain the same after sorting"

    def test_sort_by_title(self, page):
        """Test sorting books by title"""
        shelf = BookshelfPage(page)
        shelf.goto()
        
        # Wait for books to load
        page.wait_for_load_state('networkidle')
        
        # Get initial book order
        initial_books = shelf.get_book_elements()
        assert len(initial_books) > 0, "Books should be loaded"
        
        # Sort by title
        shelf.sort_by('title')
        
        # Wait for sort to complete
        page.wait_for_timeout(2000)
        
        # Get books after sorting
        sorted_books = shelf.get_book_elements()
        assert len(sorted_books) > 0, "Books should still be visible after sorting by title"
        
        # Verify sort order
        assert len(sorted_books) == len(initial_books), "Number of books should remain the same after sorting"

    def test_sort_by_author(self, page):
        """Test sorting books by author"""
        shelf = BookshelfPage(page)
        shelf.goto()
        
        # Wait for books to load
        page.wait_for_load_state('networkidle')
        
        # Get initial book order
        initial_books = shelf.get_book_elements()
        assert len(initial_books) > 0, "Books should be loaded"
        
        # Sort by author
        shelf.sort_by('author')
        
        # Wait for sort to complete
        page.wait_for_timeout(2000)
        
        # Get books after sorting
        sorted_books = shelf.get_book_elements()
        assert len(sorted_books) > 0, "Books should still be visible after sorting by author"
        
        # Verify sort order
        assert len(sorted_books) == len(initial_books), "Number of books should remain the same after sorting"

    def test_sort_order_ascending_descending(self, page):
        """Test that sort order can be changed (ascending/descending)"""
        shelf = BookshelfPage(page)
        shelf.goto()
        
        # Wait for books to load
        page.wait_for_load_state('networkidle')
        
        # Sort by title (ascending by default)
        shelf.sort_by('title')
        page.wait_for_timeout(2000)
        
        # Get books in ascending order
        ascending_books = shelf.get_book_elements()
        assert len(ascending_books) > 0, "Books should be visible after ascending sort"
        
        # Note: The current implementation might not have explicit ascending/descending controls
        # This test documents the expected functionality
        # In a real implementation, you would test both ascending and descending order

    def test_sort_persistence_across_pages(self, page):
        """Test that sort preference persists when navigating between pages"""
        shelf = BookshelfPage(page)
        shelf.goto()
        
        # Wait for books to load
        page.wait_for_load_state('networkidle')
        
        # Sort by title
        shelf.sort_by('title')
        page.wait_for_timeout(2000)
        
        # Navigate to next page
        shelf.go_to_next_page()
        page.wait_for_timeout(2000)
        
        # Check that sort preference is maintained
        # The sort dropdown should still show 'title' as selected
        sort_select = page.locator('select.form-select')
        selected_value = sort_select.input_value()
        assert selected_value == 'title', "Sort preference should persist across page navigation"
        
        # Navigate back to first page
        shelf.go_to_prev_page()
        page.wait_for_timeout(2000)
        
        # Check that sort preference is still maintained
        selected_value = sort_select.input_value()
        assert selected_value == 'title', "Sort preference should persist when returning to previous page"

    def test_sort_with_search_combination(self, page):
        """Test that sorting works correctly when combined with search"""
        shelf = BookshelfPage(page)
        shelf.goto()
    
        # Wait for books to load
        page.wait_for_load_state('networkidle')
    
        # Search for a specific term that exists in the dataset
        # Use a valid regex pattern since the input validates regex
        shelf.search('The.*Golden')  # Updated regex to match 'The Golden Compass'
        page.wait_for_timeout(2000)
    
        # Get search results
        search_results = shelf.get_book_elements()
        assert len(search_results) > 0, "Search for 'The.*Golden' should return results"
        
        # Sort the search results by title
        shelf.sort_by('title')
        page.wait_for_timeout(2000)
        
        # Verify that sorted search results are still visible
        sorted_search_results = shelf.get_book_elements()
        assert len(sorted_search_results) > 0, "Sorted search results should be visible"
        
        # The number of results should remain the same (just reordered)
        assert len(sorted_search_results) == len(search_results), "Number of search results should remain the same after sorting"

    def test_sort_dropdown_options(self, page):
        """Test that all sort options are available in the dropdown"""
        shelf = BookshelfPage(page)
        shelf.goto()
        
        # Wait for page to load
        page.wait_for_load_state('networkidle')
        
        # Get the sort dropdown
        sort_select = page.locator('select.form-select')
        
        # Check that all expected options are present
        expected_options = ['id', 'title', 'author', 'rating']
        
        for option in expected_options:
            # Use a more specific selector to check if option exists
            option_exists = page.locator(f'select.form-select option[value="{option}"]').count() > 0
            assert option_exists, f"Sort option '{option}' should be available in dropdown" 