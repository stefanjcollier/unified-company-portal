from unittest import TestCase
from datetime import date

from app.companies.consolidators.consolidate import consolidate_companies
from app.companies.models.unified_models import UnifiedCompany
from app.lib.dict import dict_without_blanks


class TestConsolidateCompanies(TestCase):

    def perform(self, companies):
        """ Return the non-None key values of the consolidated company """
        return dict_without_blanks(consolidate_companies(companies).dict())

    def test_with_one_company(self):
        """ It returns the given data """
        company = UnifiedCompany(number="1111", name="StefCo", jurisdiction_code='uk', address="St,City,Country,Postcode")
        expected_dict = {
            "number": "1111",
            "name": "StefCo",
            "jurisdiction_code": "uk",
            "address": "St,City,Country,Postcode",
        }
        self.assertDictEqual(self.perform([company]), expected_dict)

    def test_with_two_companies(self):
        """ It returns consolidated data filling in blanks """
        company1 = UnifiedCompany(number="1111", name="StefCo", jurisdiction_code='uk', address="St,City,Country,Postcode", date_established=date(year=2000, month=1, day=1))
        company2 = UnifiedCompany(number="1111", name="StefCo", jurisdiction_code='uk', address="St,City,Country,Postcode", date_dissolved=date(year=2001, month=12, day=25))
        expected_dict = {
            "number": "1111",
            "name": "StefCo",
            "jurisdiction_code": "uk",
            "address": "St,City,Country,Postcode",
            "date_established": date(year=2000, month=1, day=1),
            "date_dissolved": date(year=2001, month=12, day=25),
        }
        self.assertDictEqual(self.perform([company1, company2]), expected_dict)

    def test_with_two_companies_with_conflicting_data(self):
        """ When given differing data, it takes the last seen value """
        company1 = UnifiedCompany(number="1111", name="StefCo", jurisdiction_code='uk', address="St,City,Country,Postcode")
        company2 = UnifiedCompany(number="1111", name="StefCo", jurisdiction_code='de', address="St,City,Country,Postcode")
        expected_dict = {
            "number": "1111",
            "name": "StefCo",
            "jurisdiction_code": "de",
            "address": "St,City,Country,Postcode",
        }
        self.assertDictEqual(self.perform([company1, company2]), expected_dict)

    def test_with_one_company_with_people(self):
        """ It includes people """
        person = {"name": "Stefan"}
        company = UnifiedCompany(number="1111", name="StefCo", jurisdiction_code='uk', address="St,City,Country,Postcode", related_people=[person])
        expected_dict = {
            "number": "1111",
            "name": "StefCo",
            "jurisdiction_code": "uk",
            "address": "St,City,Country,Postcode",
            "related_people": [
                {"name": "Stefan"}
            ]
        }
        self.assertDictEqual(self.perform([company]), expected_dict)

    def test_with_two_companies_with_same_person(self):
        """ When the same person appears in multiple companies is creates one person with data from both """
        person1 = {"name": "Stefan", "date_from": date(year=2000, month=1, day=1)}
        company1 = UnifiedCompany(number="1111", name="StefCo", jurisdiction_code='uk', address="St,City,Country,Postcode", related_people=[person1])
        person2 = {"name": "Stefan", "role": "Director"}
        company2 = UnifiedCompany(number="1111", name="StefCo", jurisdiction_code='uk', address="St,City,Country,Postcode", related_people=[person2])
        expected_dict = {
            "number": "1111",
            "name": "StefCo",
            "jurisdiction_code": "uk",
            "address": "St,City,Country,Postcode",
            "related_people": [
                {"name": "Stefan", "role": "Director", "date_from": date(year=2000, month=1, day=1)}
            ]
        }
        self.assertDictEqual(self.perform([company1, company2]), expected_dict)

    def test_with_two_companies_with_differing_person(self):
        """ It doesn't merge different people """
        person = {"name": "Stefan"}
        company1 = UnifiedCompany(number="1111", name="StefCo", jurisdiction_code='uk', address="St,City,Country,Postcode", related_people=[person])
        other_person = {"name": "Dwight"}
        company2 = UnifiedCompany(number="1111", name="StefCo", jurisdiction_code='uk', address="St,City,Country,Postcode", related_people=[other_person])
        expected_dict = {
            "number": "1111",
            "name": "StefCo",
            "jurisdiction_code": "uk",
            "address": "St,City,Country,Postcode",
            "related_people": [
                {"name": "Stefan"},
                {"name": "Dwight"},
            ]
        }
        self.assertDictEqual(self.perform([company1, company2]), expected_dict)
