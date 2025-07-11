import pytest
from pages.pages import BookshelfPage

class TestSortPaginationBug:
    """HIGHEST PRIORITY BUG: Sort functionality doesn't maintain state across pagination"""
    
    def test_sort_order_maintained_across_pagination(self, page):
        """
        FAILING TEST: Sort order should be maintained across pagination
        
        Bug Description: When users sort books and navigate to the next page,
        the sort order starts fresh (from A) instead of continuing where it left off
        from the previous page. This breaks the user's expectation of consistent
        sorting across the entire dataset.
        
        Impact: High - This breaks the user's expectation of consistent sorting across pages
        Reproducible: Yes - Sort by title, go to next page, verify sort continues from previous page
        """
        shelf = BookshelfPage(page)
        shelf.goto()
        
        # Wait for books to load
        page.wait_for_load_state('networkidle')
        
        # Sort by title
        shelf.sort_by('title')
        
        # Verify sort option is selected
        sort_select = page.locator('select.form-select')
        selected_value = sort_select.input_value()
        assert selected_value == 'title', "Sort dropdown should show 'title' as selected"
        
        # Get sorted book titles from first page
        first_page_books = shelf.get_book_elements()
        
        # Skip test if no books are loaded (backend issue)
        if len(first_page_books) == 0:
            pytest.skip("No books loaded - likely backend connection issue")
        
        # Extract book titles by clicking on each book and getting the title from details page
        first_page_titles = []
        
        for i in range(min(3, len(first_page_books))):  # Test first 3 books
            # Click on the book to go to details page
            shelf.click_book_by_index(i)
            
            # Wait for navigation to book details page
            page.wait_for_url("**/books/*")
            
            # Get the title from the h1 element
            title = page.text_content('h1[data-v-2dd5deba]')
            if title and title.strip():
                first_page_titles.append(title.strip())
            
            # Go back to bookshelf
            page.go_back()
            page.wait_for_load_state('networkidle')
            
            # Re-sort to maintain the sort state
            shelf.sort_by('title')
        
        # Verify first page has books
        assert len(first_page_titles) > 0, "First page should have book titles"
        
        # Get the last title from first page (to verify continuation)
        last_title_first_page = first_page_titles[-1] if first_page_titles else ""
        
        # Check if next page button is available
        next_button = page.locator('button:has(svg.bi-chevron-right)')
        
        if next_button.is_visible() and not next_button.is_disabled():
            # Navigate to next page
            shelf.go_to_next_page()
            page.wait_for_timeout(2000)  # Wait for page load
            
            # Get book titles from second page (same method)
            second_page_books = shelf.get_book_elements()
            second_page_titles = []
            
            for i in range(min(3, len(second_page_books))):  # Test first 3 books
                # Click on the book to go to details page
                shelf.click_book_by_index(i)
                
                # Wait for navigation to book details page
                page.wait_for_url("**/books/*")
                
                # Get the title from the h1 element
                title = page.text_content('h1[data-v-2dd5deba]')
                if title and title.strip():
                    second_page_titles.append(title.strip())
                
                # Go back to bookshelf
                page.go_back()
                page.wait_for_load_state('networkidle')
                
                # Re-sort to maintain the sort state
                shelf.sort_by('title')
            
            # Verify second page has books
            assert len(second_page_titles) > 0, "Second page should have book titles"
            
            # Get the first title from second page
            first_title_second_page = second_page_titles[0] if second_page_titles else ""
            
            # THE ACTUAL BUG: Sort should continue from where first page left off
            # Expected: Second page should continue the alphabetical sort from first page
            # Actual: Second page starts fresh from 'A' (alphabetical beginning)
            
            # Check if second page starts with 'A' or similar (indicating fresh sort)
            if first_title_second_page:
                # This will FAIL because the sort starts fresh on each page
                # The second page should continue from where the first page ended
                # Instead, it starts from the beginning of the alphabet
                
                # Verify that second page doesn't start fresh from 'A'
                # (This test documents the bug - it should fail)
                assert not first_title_second_page.lower().startswith('a'), \
                    f"Second page should not start fresh from 'A'. " \
                    f"First page ended with: '{last_title_first_page}', " \
                    f"Second page starts with: '{first_title_second_page}'. " \
                    f"Sort should continue from previous page, not restart."
                
                # Alternative check: Verify sort continuity
                # The first title of second page should come after the last title of first page
                if last_title_first_page and first_title_second_page:
                    assert first_title_second_page.lower() > last_title_first_page.lower(), \
                        f"Sort should continue across pages. " \
                        f"First page ended with: '{last_title_first_page}', " \
                        f"Second page should start after this, not restart from beginning."
            
            # Verify sort dropdown still shows correct option
            selected_value = sort_select.input_value()
            assert selected_value == 'title', \
                "Sort dropdown should maintain selected option across pages"
        else:
            # If no next page, document that pagination is not available
            pytest.skip("Next page not available - pagination may not be implemented or only one page exists") 