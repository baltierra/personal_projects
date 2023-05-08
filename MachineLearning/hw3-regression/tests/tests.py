import sys
import unittest
import logging as log
import numpy as np


class TestLogReg(unittest.TestCase):
    def __init__(self, test, log_reg_ctor):
        super(TestLogReg, self).__init__(test)
        self.log_reg_ctor = log_reg_ctor

    def setUp(self):
        self.X_train = np.array([[1,2,1], [1,1,5], [1,2,5], [1,3,5], [1,1,6], [1,2,6], [1,5,1], [1,6,1], [1,7,1], [1,6,2], [1,7,2], [1,5,5]], dtype=float)
        self.y_train =  np.array([1 if ii < 6 else 0 for ii in range(self.X_train.shape[0])], dtype=float)

    def testPosUnregUpdate(self): 
        """
        test update based on positive example 
        """
        eta = 0.1
        train_x = np.array([self.X_train[2,:].copy()])
        train_y  = np.array([self.y_train[2]])
        lr = self.log_reg_ctor(train_x.shape[1], eta)
        lr.w = np.ones_like(lr.w)
        for i in range(len(train_x)):
            lr.sgd_update(train_x[i],train_y[i], lam=0)
        self.assertAlmostEqual(lr.w[0], 1.0000335350130467)
        self.assertAlmostEqual(lr.w[1], 1.0000670700260932)
        self.assertAlmostEqual(lr.w[2], 1.0001676750652333)

    def testNegUnregUpdate(self): 
        """
        test update based on negative example 
        """
        eta = 0.2
        train_x = np.array([self.X_train[9,:].copy()])
        train_y  = np.array([self.y_train[9]])
        lr = self.log_reg_ctor(train_x.shape[1], eta)
        lr.w = np.ones_like(lr.w)
        for i in range(len(train_x)):
            lr.sgd_update(train_x[i],train_y[i], lam=0)
        self.assertAlmostEqual(lr.w[0],  0.80002467891519724)
        self.assertAlmostEqual(lr.w[1], -0.19985192650881656)
        self.assertAlmostEqual(lr.w[2],  0.60004935783039448)        

    def testPosRegUpdate(self): 
        """
        test regularized update based on positive example 
        """
        eta = 0.1
        train_x = np.array([self.X_train[2,:].copy()])
        train_y  = np.array([self.y_train[2]])
        lr = self.log_reg_ctor(train_x.shape[1], eta)
        lr.w = np.ones_like(lr.w)
        for i in range(len(train_x)):
            lr.sgd_update(train_x[i],train_y[i], lam=0.1)
        self.assertAlmostEqual(lr.w[0], 1.0000335350130467)
        self.assertAlmostEqual(lr.w[1], 0.98006707002609317)
        self.assertAlmostEqual(lr.w[2], 0.98016767506523328)

    def testNegRegUpdate(self): 
        """
        test update based on negative example 
        """
        eta = 0.2
        train_x = np.array([self.X_train[9,:].copy()])
        train_y  = np.array([self.y_train[9]])
        lr = self.log_reg_ctor(train_x.shape[1], eta)
        lr.w = np.ones_like(lr.w)
        for i in range(len(train_x)):
            lr.sgd_update(train_x[i],train_y[i], lam=0.1)
        self.assertAlmostEqual(lr.w[0],  0.80002467891519724)
        self.assertAlmostEqual(lr.w[1], -0.23985192650881657)
        self.assertAlmostEqual(lr.w[2],  0.56004935783039445)

def run_test_suite(name, ctor):
    if name == "prob 2A":
        prob2A = unittest.TestSuite()
        for test in ["testPosUnregUpdate","testNegUnregUpdate"]:
            prob2A.addTest(TestLogReg(test, ctor))
        assert unittest.TextTestRunner(verbosity=2).run(prob2A).wasSuccessful(), "one or more tests for prob 2A failed"
    elif name == "prob 2E":
        prob2A = unittest.TestSuite()
        for test in ["testNegRegUpdate", "testPosRegUpdate"]:
            prob2A.addTest(TestLogReg(test, ctor))
        assert unittest.TextTestRunner(verbosity=2).run(prob2A).wasSuccessful(), "one or more tests for prob 2E failed"
    else:   
        raise Exception('unrecognized test suite name: {}'.format(name))
