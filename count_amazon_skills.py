"""Scrap the Amazon Skill Store page.

This Scripts contains methods that help to scrap the Amazon Skill
store page to count the number of skills.
"""
from re import match
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


AMAZON_BASE_URL = 'https://www.amazon.com'
SKILL_STORE_URL = '{}{}'.format(
    AMAZON_BASE_URL,
    '/s/ref=lp_14284820011_hi_1?rh=n%3A13727921011&ie=UTF8&qid=1519567704'
)
ALEXA_SKILL_SEARCH_XPATH = '//h4[text()="Alexa Skills"'
LINK_XPATH = '//a[contains(@class, "a-link-normal s-ref-text-link")]'
SKILL_CAT_XPATH = '//ul[.{}]]{}'.format(
    ALEXA_SKILL_SEARCH_XPATH,
    LINK_XPATH
)
RESULTS_XPATH = '//span[@id="s-result-count"]'
RESULT_PATTERN = '.*[of|of over]? ([0-9][0-9,.]+) results.*'


def scrap(skill_store_url=SKILL_STORE_URL):
    """Scrap of the skill store page."""
    skills = list()

    driver = webdriver.Firefox()
    driver.get(skill_store_url)

    driver_skill_cat_els = driver.find_elements(By.XPATH, SKILL_CAT_XPATH)
    for skill_cat_el in driver_skill_cat_els:
        skill_cat_name = skill_cat_el.text
        skill_cat_cnt = '0'

        # click on the skill category
        skill_cat_el.send_keys(Keys.COMMAND + Keys.RETURN)
        while len(driver.window_handles) < 2:
            sleep(1)
        driver.switch_to_window(driver.window_handles[-1])

        try:
            element_present = EC.presence_of_element_located(
                (By.ID, 's-result-count')
            )
            WebDriverWait(driver, 10).until(element_present)
        except TimeoutException:
            break

        driver_result_els = driver.find_elements(By.XPATH, RESULTS_XPATH)
        if driver_result_els > 0:
            result = driver_result_els[0]
            match_results = match(RESULT_PATTERN, result.text)
            if not match_results:
                match_results = match('([0-9][0-9,.]*) result.*', result.text)
            if match_results:
                skill_cat_cnt = match_results.groups()[0]

        skills.append(
            (skill_cat_name, int(skill_cat_cnt.replace(',', '')))
        )

        driver.close()
        while len(driver.window_handles) > 1:
            sleep(1)
        driver.switch_to_window(driver.window_handles[-1])

    driver.quit()
    return skills


if __name__ == '__main__':
    SKILLS_LIST = scrap()
    SKILLS_LIST_TOTAL_CNT = reduce(lambda x, y: x + y[1], SKILLS_LIST, 0)
    print SKILLS_LIST_TOTAL_CNT
