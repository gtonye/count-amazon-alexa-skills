# *--Encoding: utf-8 --*
"""Configuration file."""

AMAZON_BASE_URL = 'https://www.amazon.com'
SKILL_STORE_URL = '{}{}'.format(
    AMAZON_BASE_URL,
    '/s/ref=lp_14284820011_hi_1?rh=n%3A13727921011&ie=UTF8&qid=1519567704'
)

# when opening or closing a tab require the waiting time below to not trigger
# errors such as https://stackoverflow.com/questions/27775759
# /send-keys-control-click-in-selenium-with-python-bindings
BROWSER_ACTION_WAIT_TIME = 3
