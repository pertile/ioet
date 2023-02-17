import unittest

from wage.wage import calculate_wage


class TestCalculateWage(unittest.TestCase):
    def test_datafile(self):
        """
        Test that it can sum a list of integers
        """
        with open("datatest.txt", "r") as file:
            line1 = file.readline()
            result = calculate_wage(line1)
                
            self.assertEqual(result, 215)

            line2 = file.readline()
            result = calculate_wage(line2)

            self.assertEqual(result, 85)

            line3 = file.readline()
            result = calculate_wage(line3)

            self.assertAlmostEqual(result, 179.416666, places=5)

            line4 = file.readline()
            result = calculate_wage(line4)

            self.assertEqual(result, 639)

            line5 = file.readline()
            result = calculate_wage(line5)

            self.assertEqual(result, 518.5)
    

if __name__ == '__main__':
    unittest.main()
