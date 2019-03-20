import unittest
import random
import split as sp


class test_split(unittest.TestCase):

    def setUp(self):
        self.data = sp.read_doc('sample_csv.csv')
        self.data_2 = sp.read_doc('sample_workbook.xlsx')
        self.headings_list = ['Name', 'Age', 'Occupation']
        self.choice = random.randint(0, 3)

    def test_read_doc(self):
        self.assertTrue(self.data.equals(self.data_2))

    def test_get_headings(self):
        self.assertEqual(self.headings_list, sp.get_headings(self.data))

    def test_choose_headings(self):
        choice = sp.choose_headings(self.headings_list)
        # print(choice)
        self.assertIn(self.headings_list[choice], self.headings_list)

    def test_get_number(self):
        self.assertEqual(sp.get_number_of_records(self.data),
                         sp.get_number_of_records(self.data_2))

    def test_choose_number_of_records(self):
        self.assertIs(type(sp.choose_number_of_records()), int)


if __name__ == "__main__":
    unittest.main()
