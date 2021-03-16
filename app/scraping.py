from telnetlib import EC

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait


def get_book(title, j):
    driver = webdriver.Chrome('chromedriver')
    driver.get('https://www.gutenberg.org/')
    search_field = driver.find_element_by_id('menu-book-search')
    search_field.send_keys(title.lower())
    search_field.send_keys(Keys.RETURN)
    results = WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'booklink')))
    titles = [result.find_element_by_class_name("title").text for result in results]

    for i, book in enumerate(titles):
        print(f"{i + 1}. " + book)

    choice = int(input("What book were you thinking of?(1-25): "))

    chosen_book = results[choice+1]
    chosen_book.click()
    text = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.LINK_TEXT, 'Plain Text UTF-8')))
    text.click()
    book_text = driver.page_source
    with open(f"documents/book{j+1}.py", "w") as text_file:
        text_file.write(book_text)
    with open(f"documents/book{j+1}.py", "r") as text_file:
        book_lines = text_file.readlines()
    print(f"Book{j+1} saved!")
    return book_lines