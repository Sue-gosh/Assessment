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

## Notes
- Tests use Playwright's Chromium browser in headless mode by default.
- You can change the browser or run in headed mode by editing `conftest.py`. 