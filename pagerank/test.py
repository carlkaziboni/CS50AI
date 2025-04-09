import unittest
import pagerank

class PageRankTest(unittest.TestCase):
    
    def test_transition_model(self):
        return self.assertEqual({"1.html": 0.0375, "2.html": 0.8875, "3.html": 0.0375, "4.html": 0.0375},
                                pagerank.transition_model(pagerank.crawl("pagerank/corpus0"), "1.html", 0.85))
    
if __name__ == "__main__":
    unittest.main()