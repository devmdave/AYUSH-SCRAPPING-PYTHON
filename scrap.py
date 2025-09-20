from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import pandas as pd
import traceback

def scrape_two_combo_boxes(url, combo1_selector, combo2_selector, textbox_selector, output_csv="scraped_results.csv"):
    results = []

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)  # headless=True for background
            page = browser.new_page()
            page.goto(url, wait_until="networkidle")  # wait until network idle

            # Wait for first combo box to appear
            page.wait_for_selector(combo1_selector)
            combo1_options = page.locator(f"{combo1_selector} option").all()

            for option1 in combo1_options:
                value1 = option1.get_attribute("value")
                text1 = option1.inner_text().strip()

                if value1 is None or str(value1).strip() == "":
                    continue  # skip empty options

                try:
                    # Select combo1
                    page.select_option(combo1_selector, value=value1)

                    # Wait until combo2 updates
                    page.wait_for_selector(f"{combo2_selector} option", timeout=10000)

                    combo2_options = page.locator(f"{combo2_selector} option").all()

                    for option2 in combo2_options:
                        value2 = option2.get_attribute("value")
                        text2 = option2.inner_text().strip()

                        if value2 is None or str(value2).strip() == "":
                            continue

                        try:
                            # Select combo2
                            page.select_option(combo2_selector, value=value2)

                            # Wait until textbox is visible
                            page.wait_for_selector(textbox_selector, timeout=10000)

                            textbox_value = page.locator(textbox_selector).input_value()

                            print(f"[Combo1: {text1}] [Combo2: {text2}] => Textbox: {textbox_value}")
                            results.append((text1, text2, textbox_value))

                        except PlaywrightTimeoutError:
                            print(f"⚠ Timeout while processing Combo1: {text1}, Combo2: {text2}")
                        except Exception as e:
                            print(f"⚠ Error while processing Combo1: {text1}, Combo2: {text2}")
                            print(traceback.format_exc())

                except PlaywrightTimeoutError:
                    print(f"⚠ Timeout after selecting Combo1: {text1}")
                except Exception as e:
                    print(f"⚠ Error after selecting Combo1: {text1}")
                    print(traceback.format_exc())

            browser.close()

    except Exception as e:
        print("⚠ Fatal error occurred:")
        print(traceback.format_exc())

    # Save results even if error occurred
    if results:
        df = pd.DataFrame(results, columns=["ComboBox1", "ComboBox2", "TextboxValue"])
        df.to_excel("scraped_results.xlsx", index=False)
        df.to_csv(output_csv, index=False)
        print(f"\n✅ Data exported to scraped_results.xlsx and {output_csv}")

    return results


if __name__ == "__main__":
    url = "https://example.com"
    combo1_selector = "#comboBox1Id"
    combo2_selector = "#comboBox2Id"
    textbox_selector = "#textboxId"

    scrape_two_combo_boxes(url, combo1_selector, combo2_selector, textbox_selector)
