import unittest

from db import db, Thingy

class TestThingy(unittest.TestCase):

    def setUp(self):
        db.reset()

    def test_no_results(self):
        things = db.get_things('no.such.thingy')
        self.assertEqual(len(things), 0, 'There should be none')

    def test_thingy_was_saved(self):
        thingy = Thingy(db, 101, 'test_thingy')

        with thingy:
            thingy.name = 'test_thingy_was_saved'

        things = db.get_things('test_thingy_was_saved')
        self.assertEqual(len(things), 1, 'There should be one thing')
        self.assertEqual(thingy.id, things[0].id, 'It should be the one we created above')
        self.assertEqual(thingy.name, things[0].name, 'It should have been saved')

