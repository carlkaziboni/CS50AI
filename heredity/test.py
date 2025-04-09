import unittest
import heredity

class GeneProbTest(unittest.TestCase):
    def test_example(self):
        people = {
        'Harry': {'name': 'Harry', 'mother': 'Lily', 'father': 'James', 'trait': None},
        'James': {'name': 'James', 'mother': None, 'father': None, 'trait': True},
        'Lily': {'name': 'Lily', 'mother': None, 'father': None, 'trait': False}
        }
        prob = heredity.get_gene_prob(people, "Harry", {"Lily"}, {"Harry"}, {"James"})
        self.assertEqual(prob, 0.9802)

if __name__ == "__main__":
    unittest.main()
