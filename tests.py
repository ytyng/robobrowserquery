#!/usr/bin/env python
import unittest

try:
    from .robobrowserquery import RoboBrowserQuery
except (ImportError, ValueError):
    from robobrowserquery import RoboBrowserQuery


class RoboBrowserQueryTest(unittest.TestCase):
    """
    Test for RoboBrowserQuery
    """

    def test_open(self):
        browser = RoboBrowserQuery()

        browser.open('https://www.mangazenkan.com/?state=robobrowserquery-test')

        d = browser.get_cookie_values_as_dicts()
        self.assertTrue(isinstance(d, list))

        d = browser.get_cookies_as_dicts()
        self.assertTrue(isinstance(d, list))

        f = browser.get_form()

        self.assertTrue(hasattr(f, 'fields'))
        self.assertTrue(hasattr(f, 'submit_fields'))
        f['name'].value = 'ONE PIECE'
        browser.submit_form(f)

        content = browser.get_decoded_content()

        self.assertIn("<html", content)

    def test_cookie(self):
        cookie_file_path = "/tmp/mangazenkan-cookie-test"
        browser = RoboBrowserQuery()

        browser.open('https://www.mangazenkan.com/mypage/'
                     '?state=robobrowserquery-test2')

        cookie_dict = {
            c['name']: c['value'] for c in
            browser.get_cookie_values_as_dicts()}
        session_id = cookie_dict['PHPSESSID']
        browser.save_cookies_to_file(cookie_file_path)

        browser = RoboBrowserQuery()
        browser.load_cookies_from_file(cookie_file_path)
        browser.open('https://www.mangazenkan.com/mypage/'
                     '?state=robobrowserquery-test2')
        cookie_dict_2 = {
            c['name']: c['value'] for c in
            browser.get_cookie_values_as_dicts()}

        self.assertEqual(session_id, cookie_dict_2['PHPSESSID'])


if __name__ == "__main__":
    unittest.main()
