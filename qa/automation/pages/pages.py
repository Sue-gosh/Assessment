from playwright.sync_api import Page

class BookshelfPage:
    URL = "http://localhost:5173/"

    def __init__(self, page: Page):
        self.page = page

    def goto(self):
        self.page.goto(self.URL)

    def get_book_elements(self):
        # Books are clickable links with Vue data attributes
        return self.page.query_selector_all('a[data-v-78b5a187]')

    def get_book_titles(self):
        # Extract titles from the book links (if available)
        books = self.get_book_elements()
        titles = []
        for book in books:
            # Try to get title from various attributes or text content
            title = book.get_attribute('title') or book.get_attribute('alt') or book.text_content()
            if title and title.strip():
                titles.append(title.strip())
        return titles

    def click_book_by_index(self, index: int):
        books = self.get_book_elements()
        if books and len(books) > index:
            books[index].click()

    def search(self, query: str):
        self.page.fill('input[is="regexp-input"]', query)
        self.page.keyboard.press('Enter')

    def is_invalid_feedback_visible(self):
        return self.page.is_visible('.invalid-feedback')

    def sort_by(self, value: str):
        self.page.select_option('select.form-select', value)

    def go_to_next_page(self):
        self.page.click('button:has(svg.bi-chevron-right)')

    def go_to_prev_page(self):
        self.page.click('button:has(svg.bi-chevron-left)')

class BookDetailsPage:
    def __init__(self, page: Page):
        self.page = page

    def get_title(self):
        # Title is in h1 element with Vue data attribute
        return self.page.text_content('h1[data-v-2dd5deba]')

    def get_author(self):
        return self.page.text_content('h2 em')

    def get_rating(self):
        return self.page.text_content('div:has-text("User rating")') 