#!/usr/bin/python
# coding=utf-8

from __future__ import unicode_literals

from unittest2 import TestCase

from ..ares import call_ares
from ..helpers import normalize_company_id_length


class CallARESTestCase(TestCase):
    def test_invalid_values(self):
        invalid_values = [False, True, 42, -42, "foo"]

        for invalid_value in invalid_values:
            self.assertFalse(call_ares(invalid_value))

    def test_numerically_valid(self):
        # IČ 25596641 je numericky platné, není však zaregistrované
        # Viz http://phpfashion.com/jak-overit-platne-ic-a-rodne-cislo
        self.assertFalse(call_ares(company_id=25596641), dict)

    def test_valid_values(self):
        self.assertIsInstance(call_ares(company_id=27074358), dict)

        actual = call_ares(company_id=68407700)['address']['street']
        # ČVUT v Praze
        expected = "Zikova 1903/4"
        self.assertEqual(actual, expected)

        other_valid_company_ids = ('62739913', '25063677', '1603094', '01603094')

        try:
            for one_id in other_valid_company_ids:
                ares_data = call_ares(company_id=one_id)
                self.assertEqual(normalize_company_id_length(one_id), ares_data['legal']['company_id'])
        except KeyError as error:
            self.fail(error)
