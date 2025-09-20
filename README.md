# Automated Two-Combo Box Scraper

This Python project uses **Playwright** to automatically scrape data from a web page with **two dependent combo boxes** and an input textbox. The scraper:

1. Loops through all options of the **first combo box**.
2. For each first combo selection, loops through all options of the **second combo box**.
3. Waits for the **textbox to update** and retrieves its value.
4. Logs errors or timeouts during scraping for easier debugging.
5. Exports the results automatically to **Excel (`.xlsx`)** and **CSV (`.csv`)**.

---

## Features

- Fully automatic scraping of all combo box combinations.
- Handles **dependent combo boxes** (second depends on first).
- Waits dynamically for elements instead of using fixed sleep.
- Logs errors and timeouts for easy debugging.
- Partial results are saved if the script encounters errors.
- Export to Excel and CSV for easy sharing and analysis.

---

## Requirements

- Python 3.8+
- Playwright
- Pandas
- Openpyxl (for Excel export)

---

### Install Dependencies

```bash
# Install Python packages
pip install playwright pandas openpyxl

# Install Playwright browsers
playwright install
