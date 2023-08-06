import unittest
from config import config
import logging


class AAA_simpcfg(unittest.TestCase):

    def test_AAA_init(self):
        _ = config('AAA_AAA')

    def test_AAB_initRepeat(self):
        A,B = config('AAA_AAB'),config('AAA_AAB')
        self.assertEqual(A,B,msg='Calling same config did not return same value')

    def test_AAC(self):
        cfg = config('AAA_AAC')

        # Place value in, make sure works
        cfg['test'] = 3
        self.assertTrue(('test' in cfg), msg='Contains did not return True')
        self.assertEqual(cfg['test'],3, msg='Did not retrieve value correctly')

        # Update value
        cfg['test'] = 4
        self.assertEqual(cfg['test'],4, msg='Value did not update')

    def test_AAD(self):
        cfg = config('AAA_AAD')

        # See if we validation works
        #logging.disable()
        cfg[3] = 3
        x = cfg.get(3, dtype=int, options=(3,3), min=2, mineq=3, max=4, maxeq=3,\
                    isIter=False, isHashable=True, callable=False)
        self.assertEqual(x,3)
        logging.disable(logging.NOTSET)


        self.assertFalse(cfg.validate(3, min=3, raise_err=False),\
            'Validation failed for min')
        self.assertFalse(cfg.validate(3, mineq=4, raise_err=False),\
            'Validation failed for mineq')
        self.assertFalse(cfg.validate(3, max=3, raise_err=False),\
            'Validation failed for max')
        self.assertFalse(cfg.validate(3, maxeq=2, raise_err=False),\
            'Validation failed for maxeq')
        self.assertFalse(cfg.validate(3, isIter=True, raise_err=False),\
            'Validation failed for isIter')
        self.assertFalse(cfg.validate({}, isHashable=True, raise_err=False),\
            'Validation failed for isHashable')
        self.assertFalse(cfg.validate(3, callable=True, raise_err=False),\
            'Validation failed for callable')
        self.assertFalse(cfg.validate(3, options=(2,4), raise_err=False),\
            'Validation failed for options')
        self.assertFalse(cfg.validate(3, dtype=float, raise_err=False),\
            'Validation failed for dtype')
        self.assertFalse(cfg.validate(3, dtype=(float,str), raise_err=False),\
            'Validation failed for dtype')
        self.assertTrue(cfg.validate(3, min=5, always_allow=(3,4), \
            raise_err=False),'Validation failed for dtype')









if __name__ == '__main__':
    unittest.main()
