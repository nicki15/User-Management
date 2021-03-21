from unittest import TestCase
import os

from helpers import configuration
from DBManager.DBManager import create_database, add_newuser, get_user_by_email
from DBManager.DBManager import __hash_passwort__, __verify_password__



class DbManagerUnitTest(TestCase):

    def test_create_table(self):
        create_database()
        self.assertTrue(os.path.exists(configuration.DB_NAME))
        os.remove(configuration.DB_NAME)
        self.assertFalse(os.path.exists(configuration.DB_NAME))


    def test_add_new_user(self):
        create_database()
        name = 'Phil'
        email = 'Webseite@de'
        pw = '123456'
        result = add_newuser(name, email, pw)
        self.assertTrue(result[0])
        os.remove(configuration.DB_NAME)
        self.assertFalse(os.path.exists(configuration.DB_NAME))


    def test_add_user_already_exists(self):
        create_database()
        name = 'Phil'
        email = 'Webseite@de'
        pw = '123456'
        result = add_newuser(name, email, pw)
        self.assertTrue(result[0])
        secondResult = add_newuser(name, email, pw)
        self.assertFalse(secondResult[0])
        os.remove(configuration.DB_NAME)
        self.assertFalse(os.path.exists(configuration.DB_NAME))


    def test_get_existing_user_by_email(self):
        create_database()
        name = 'Phil'
        email = 'Webseite@de'
        pw = '123456'
        result = add_newuser(name, email, pw)
        self.assertTrue(result[0])
        res = get_user_by_email(email)
        self.assertTrue(type(res)==tuple)
        self.assertEqual(name, res[1])
        self.assertEqual(email, res[2])
        self.assertEqual(pw, res[3])
        os.remove(configuration.DB_NAME)
        self.assertFalse(os.path.exists(configuration.DB_NAME))


    def test_get_nonexisting_user_by_email(self):
        create_database()
        res = get_user_by_email(email='Basti@Web.de')
        self.assertIsNone(res)
        os.remove(configuration.DB_NAME)
        self.assertFalse(os.path.exists(configuration.DB_NAME))


    def test_verify_pwhash(self):
        pw = "nackt5"
        hs = __hash_passwort__(pw)
        self.assertTrue(hs,pw)


