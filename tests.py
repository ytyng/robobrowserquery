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

        browser.open(
            'https://www.mangazenkan.com/?state=robobrowserquery-test')

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

    def test_cookie_serialize(self):
        browser = RoboBrowserQuery()

        browser.open('https://www.mangazenkan.com/mypage/'
                     '?state=robobrowserquery-test3')

        cookie_dict = {
            c['name']: c['value'] for c in
            browser.get_cookie_values_as_dicts()}
        session_id = cookie_dict['PHPSESSID']
        cookie_text = browser.get_serialized_cookies()
        self.assertTrue(cookie_text)
        browser = RoboBrowserQuery()
        browser.set_serialized_cookies(cookie_text)
        browser.open('https://www.mangazenkan.com/mypage/'
                     '?state=robobrowserquery-test3')
        cookie_dict_2 = {
            c['name']: c['value'] for c in
            browser.get_cookie_values_as_dicts()}

        self.assertEqual(session_id, cookie_dict_2['PHPSESSID'])

    def test_meta_refresh(self):
        browser = RoboBrowserQuery()
        browser.open('http://example.com/')
        browser.meta_refresh()
        self.assertEqual(browser.url, 'http://example.com/')
        browser.load_html("""
        <html><head>
        <meta content="0; URL=http://example.com/?refreshed" http-equiv="Refresh"/>
        </head>
        </html>
        """)
        browser.meta_refresh()
        self.assertEqual(browser.url, 'http://example.com/?refreshed')

        browser.load_html("""
        <html><head>
        <meta content="0; URL=http://example.com/?refreshed2" http-equiv="refresh"/>
        </head>
        </html>
        """)
        browser.meta_refresh()
        self.assertEqual(browser.url, 'http://example.com/?refreshed2')

    def test_parse_url(self):
        browser = RoboBrowserQuery()
        browser.open('http://example.com/')

        q = browser.get_parsed_query()
        self.assertFalse(q)

        browser.open('http://example.com/?a=b&c=d&e[]=f&e[]=g')
        parsed_query = browser.get_parsed_query()

        self.assertEqual(parsed_query['a'], 'b')
        self.assertEqual(parsed_query['c'], 'd')
        self.assertIn("f", parsed_query['e[]'])
        self.assertIn("g", parsed_query['e[]'])

    def test_reparse(self):
        browser = RoboBrowserQuery()
        browser.open('http://example.com/')
        self.assertTrue(browser.state.parsed.find('title').text)
        for decode in [True, False]:
            for encoding in [None, 'utf=8']:
                browser.reparse(decode=decode, encoding=encoding)
                self.assertTrue(browser.state.parsed.find('title').text)

    def test_text_match(self):
        browser = RoboBrowserQuery()
        browser.open('http://example.com/')
        a_list = list(browser.find_elements_by_text_match('a', 'information'))
        self.assertEqual(len(a_list), 1)
        self.assertTrue(a_list[0].attr('href'))


if __name__ == "__main__":
    unittest.main()
