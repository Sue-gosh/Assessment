import pytest
from pages.pages import BookshelfPage

class TestSearchFunctionality:
    """Test cases for search functionality issues"""
    
    def test_invalid_regex_search_shows_error(self, page):
        """Test that invalid regex in search shows validation error"""
        shelf = BookshelfPage(page)
        shelf.goto()
        
        # Search with invalid regex
        shelf.search('[')  # Invalid regex
        
        # Should show invalid feedback
        assert shelf.is_invalid_feedback_visible(), "Invalid regex feedback should be shown"

    def test_valid_regex_search_works(self, page):
        """Test that valid regex search returns results"""
        shelf = BookshelfPage(page)
        shelf.goto()
        
        # Wait for books to load
        page.wait_for_load_state('networkidle')
        
        # Search with valid regex pattern for "The"
        shelf.search('The')
        page.wait_for_timeout(2000)
        
        # Get search results
        search_results = shelf.get_book_elements()
        assert len(search_results) > 0, "Search for 'The' should return results"

    def test_regex_search_with_special_characters(self, page):
        """Test that regex search works with special characters"""
        shelf = BookshelfPage(page)
        shelf.goto()
        
        # Wait for books to load
        page.wait_for_load_state('networkidle')
        
        # Search with regex pattern that includes special characters
        shelf.search('The.*Golden')  # Valid regex pattern for "The Golden Compass"
        page.wait_for_timeout(2000)
        
        # Get search results
        search_results = shelf.get_book_elements()
        assert len(search_results) > 0, "Regex search 'The.*Golden' should return results"

    def test_search_clears_invalid_feedback_on_valid_input(self, page):
        """Test that invalid feedback clears when valid regex is entered"""
        shelf = BookshelfPage(page)
        shelf.goto()
        
        # First enter invalid regex
        shelf.search('[')  # Invalid regex
        assert shelf.is_invalid_feedback_visible(), "Invalid regex should show feedback"
        
        # Then enter valid regex
        shelf.search('The')  # Valid regex
        assert not shelf.is_invalid_feedback_visible(), "Valid regex should clear invalid feedback" 