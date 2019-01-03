# *--Encoding: utf-8 --*
"""Scrap the Amazon Skill Store page.

This Scripts contains methods that help to scrap the Amazon Skill
store page to count the number of skills.
"""
import argparse
import sys

from re import match
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.options import Options

from config import (SKILL_STORE_URL, BROWSER_ACTION_WAIT_TIME)

ALEXA_SKILL_SEARCH_XPATH = '//h4[text()="Alexa Skills"'
LINK_XPATH = '//a[contains(@class, "a-link-normal s-ref-text-link")]'
SKILL_CAT_XPATH = '//ul[.{}]]{}'.format(
    ALEXA_SKILL_SEARCH_XPATH,
    LINK_XPATH
)
RESULTS_XPATH = '//span[@id="s-result-count"]'
RESULT_PATTERN = '.*[of|of over]? ([0-9][0-9,.]+) results.*'

CONTROL_KEY = Keys.COMMAND if sys.platform == 'darwin' else Keys.CONTROL


class ReportType(object):
    """Defines the different types of report for the skill counting."""
    FULL = 'full'
    MINIMAL = 'minimal'


class BrowserType(object):
    """Defines the type of browser to use for the scrapping."""
    HEADLESS = 'headless'
    IN_WINDOW = 'in_window'


def get_skill_cats_count(
    skill_store_url=SKILL_STORE_URL,
    browser_type=BrowserType.HEADLESS
):
    """Scrap of the skill store page and count the skill on the store.

    :param skill_store_url: the homepage for the skill store on Amazon.
    :param browser_type: the type of browser to use for the scrapping.
    :return: A list with tuples, [(skill name, count)...].
    """
    if browser_type == BrowserType.HEADLESS:
        options = Options()
        options.set_headless()

    skills = list()

    driver = webdriver.Firefox(options=options)
    driver.get(skill_store_url)

    driver_skill_cat_els = driver.find_elements(By.XPATH, SKILL_CAT_XPATH)
    for skill_cat_el in driver_skill_cat_els:
        skill_cat_name = skill_cat_el.text

        number_of_skill = get_number_of_skill_in_category(driver, skill_cat_el)
        skills.append((skill_cat_name, number_of_skill))

        driver.close()
        while len(driver.window_handles) > 1:
            sleep(BROWSER_ACTION_WAIT_TIME)
        driver.switch_to.window(driver.window_handles[-1])

    driver.quit()
    return skills


def get_number_of_skill_in_category(driver, skill_cat_el):
    """Search for the number of skill in the category.

    :param driver: a selenium driver element.
    :param skill_cat_el: a skill category element (link of a category on the
    left column in the skill store home page).
    :return: the category count.
    """
    skill_cat_cnt = 0

    # click on the skill category
    skill_cat_el.send_keys(CONTROL_KEY + Keys.RETURN)
    while len(driver.window_handles) < 2:
        sleep(BROWSER_ACTION_WAIT_TIME)
    driver.switch_to.window(driver.window_handles[-1])

    try:
        element_present = EC.presence_of_element_located(
            (By.ID, 's-result-count')
        )
        WebDriverWait(driver, 10).until(element_present)
    except TimeoutException:
        return 0

    driver_result_els = driver.find_elements(By.XPATH, RESULTS_XPATH)
    if len(driver_result_els) > 0:
        result = driver_result_els[0]
        match_results = match(RESULT_PATTERN, result.text)
        if not match_results:
            match_results = match('([0-9][0-9,.]*) result.*', result.text)
        if match_results:
            skill_cat_cnt_str = match_results.groups()[0]
            skill_cat_cnt = int(skill_cat_cnt_str.replace(',', ''))

    return skill_cat_cnt


def run(setup_args):
    """Performs the counting of the Alexa skill in the store

    :param setup_args: all the arguments from the command line such as:
    - report_type: the report type with a breakdown between categories.
    - browser_type: the type of the browser to use.
    """
    skill_categories_count = get_skill_cats_count(
        browser_type=setup_args.browser_type
    )

    if setup_args.report_type == ReportType.FULL:
        for skill_cat_count in skill_categories_count:
            print(skill_cat_count[0], ':\t', skill_cat_count[1])

    total_skill_cnt = 0
    for a_tuple in skill_categories_count:
        total_skill_cnt += a_tuple[1]

    print('Number of skills in the store:\t', total_skill_cnt)
    pass


def setup():
    """Parse arguments for the script and return configuration in object.

    :return: the arguments from the command line
    """
    cmd_args_parser = argparse.ArgumentParser()
    cmd_args_parser.add_argument(
        '--browser-type',
        help='The type of browser: [headless, in_window]',
        default=BrowserType.HEADLESS
    )
    cmd_args_parser.add_argument(
        '--report-type',
        help='Report breakdown by categories or the total: [full, minimal]',
        default=ReportType.MINIMAL
    )

    return cmd_args_parser.parse_args()


if __name__ == '__main__':
    run(setup_args=setup())
