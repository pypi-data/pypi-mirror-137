import unittest
from ds_util.bloomfilter import create_bf, jaccard_similarity

class AnonimizationTest(unittest.TestCase):

    def test_bf_creation(self):
        with self.assertRaises(AssertionError):
            create_bf('abc',20,3,bf_representation='none')

    def test_jaccard_sim(self):
        a='ANA'
        b='ANE'

        bfa_b = create_bf(a,20,3,bf_representation='binary')
        bfb_b = create_bf(b,20,3,bf_representation='binary')

        bfa_pos1 = create_bf(a,20,3,bf_representation='pos1')
        bfb_pos1 = create_bf(b,20,3,bf_representation='pos1')

        sim_b = jaccard_similarity(bfa_b,bfb_b,bf_representation='binary')
        sim_pos =  jaccard_similarity(bfa_pos1,bfb_pos1,bf_representation='pos1')

        self.assertAlmostEqual(sim_b,sim_pos)
        self.assertEqual(sim_b,sim_pos)

        self.assertGreater(jaccard_similarity(bfa_b,bfb_b,bf_representation='binary'),.4)
        

if __name__ == '__main__':
    unittest.main()