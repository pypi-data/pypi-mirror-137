import os
import sys

import copy
import shutil
import unittest

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

import gro_exp


class UserModelCase(unittest.TestCase):
    #################
    # Remove Output #
    #################
    @classmethod
    def setUpClass(self):
        if os.path.isdir("tests"):
            os.chdir("tests")

        folder = "output"
        if not os.path.exists('output'):
            os.makedirs('output')
        if not os.path.exists("output/temp"):
            os.makedirs("output/temp")
        open(folder+"/temp.txt", 'a').close()

        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)

    # Test functions to read msd and
    def test_gromacs_analyse(self):

        gro_exp.utils.density("data/density.xvg", is_print=True, is_plot=True)
        gro_exp.utils.msd("data/msd.xvg", is_print=True, is_plot=True)

    # Test function to read DDB Data Bank
    def test_read_exp(self):
        data = gro_exp.utils.read_exp(
            "data/benzene_exp_density.xls", "DEN", temp=298.15, press=100000, tol_temp = 0.15, tol_p = 1000, p_nan=True, is_print=True, is_plot=True, area=[800,1000])


if __name__ == '__main__':
    unittest.main(verbosity=2)
