"""
    This file is here in order to
    check if the main file works properly.
"""

from bot_template import MainBot

url = 'https://lesitedantonin.000webhostapp.com'

test_bot = MainBot(url)

test_bot.get_response_from(url)
test_bot.get_hypertexts_links(url)
test_bot.get_title_from_page()
test_bot.get_element_by_HTML_markup("footer")