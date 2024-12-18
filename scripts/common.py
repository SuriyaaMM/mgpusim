import os
import shutil
import subprocess
import pandas as pd

# Determine the directory where this script is located
script_directory = os.path.dirname(os.path.abspath(__file__))

# global configuration variables
samples_directory = os.path.join(script_directory, "../samples/")
output_metric_file = "metrics"
benchmark_applications = ["pagerank", "matrixmultiplication", "nbody", "spmv"]
benchmark_applications_config = ["-node 1024", "", "", ""]
counter = 0