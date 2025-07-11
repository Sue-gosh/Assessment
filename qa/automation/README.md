# End-to-End Tests (Playwright + pytest)

## Prerequisites
- Python 3.8+
- [Playwright for Python](https://playwright.dev/python/) (already installed)
- [pytest](https://docs.pytest.org/en/stable/) (already installed)

## Setup
1. Ensure the app is running:
   - Backend: `cd qa/packages/server && npm install && npm start` (runs on http://localhost:3000)
   - Frontend: `cd qa/packages/frontend && npm install && npm start` (runs on http://localhost:5173)
2. In a new terminal, run the tests from the project root:
   ```sh
   PYTHONPATH=qa/automation pytest qa/automation
   ```

## Test Files Overview

### ✅ Passing Tests (Happy Path)
- **`test_sort_functionality.py`** - Sort functionality tests (6 tests)
  - Sort by ID, Rating, Title, Author
  - Sort persistence across pages
  - Sort with search combination
  - Sort dropdown options verification

### ❌ High-Priority Failing Tests (5 Critical Bugs)

#### 1. **`test_sort_pagination_bug.py`** - CRITICAL: Sort State Management
**Why Highest Priority:** This breaks core user workflow and data consistency expectations.
- **Bug:** Sort order is not maintained when navigating between pages
- **Impact:** High - Users expect consistent sorting across pagination
- **Business Impact:** Poor user experience, potential data confusion

#### 2. **`test_search_functionality.py`** - HIGH: Invalid Regex Search
**Why High Priority:** This affects a core feature and can cause app errors.
- **Bug:** Invalid regex in search doesn't show proper validation error
- **Impact:** Medium-High - Can break search functionality and confuse users
- **Business Impact:** Search feature reliability

#### 3. **`test_mobile_ui_issues.py`** - HIGH: Mobile Layout Issues
**Why High Priority:** Mobile users cannot access core functionality.
- **Bug:** Sort button overlaps search bar in mobile view
- **Impact:** High - Blocks mobile users from sorting books
- **Business Impact:** Mobile user experience and accessibility

#### 4. **`test_bookshelf.py`** - MEDIUM-HIGH: Core Functionality
**Why Medium-High Priority:** Basic app functionality is broken.
- **Bug:** Bookshelf doesn't display books (likely backend connection issue)
- **Impact:** Critical - Core feature completely broken
- **Business Impact:** App unusable for main purpose

#### 5. **`test_ui_improvements.py`** - MEDIUM: User Experience
**Why Medium Priority:** Missing essential navigation and UX features.
- **Bug:** Missing back button, search placeholder, pagination improvements
- **Impact:** Medium - Poor user experience but app still functional
- **Business Impact:** User satisfaction and retention

## Running Specific Test Files

```sh
# Run all tests
PYTHONPATH=qa/automation pytest qa/automation

# Run only passing tests
PYTHONPATH=qa/automation pytest qa/automation/tests/test_sort_functionality.py

# Run high-priority bug tests
PYTHONPATH=qa/automation pytest qa/automation/tests/test_sort_pagination_bug.py
PYTHONPATH=qa/automation pytest qa/automation/tests/test_search_functionality.py
PYTHONPATH=qa/automation pytest qa/automation/tests/test_mobile_ui_issues.py

# Run tests with verbose output
PYTHONPATH=qa/automation pytest qa/automation -v

# Run tests and show print statements
PYTHONPATH=qa/automation pytest qa/automation -s
```

## Priority Bug Explanations

### 🚨 **CRITICAL - Sort Pagination Bug**
This is the highest priority because it breaks a fundamental user expectation. When users sort books and navigate pages, they expect the sort order to be maintained. This bug creates inconsistent data presentation and confuses users about the actual book order.

### 🔍 **HIGH - Search & Mobile Issues**
These affect core functionality that users rely on daily. Invalid search handling can cause app crashes, and mobile layout issues prevent mobile users from using the app effectively.

### ⚠️ **MEDIUM-HIGH - Core Display Issues**
The bookshelf not displaying books is critical but likely a backend/connection issue rather than a frontend bug. This needs immediate investigation.

### 📱 **MEDIUM - UX Improvements**
These are important for user satisfaction but don't break core functionality. They represent opportunities to improve the user experience.

## Notes
- Tests use Playwright's Chromium browser in headless mode by default.
- You can change the browser or run in headed mode by editing `conftest.py`.
- Mobile tests use viewport sizes for iPhone SE (375x667) and other common mobile sizes.
- The 5 failing tests are designed to document actual bugs, not element/code issues. 