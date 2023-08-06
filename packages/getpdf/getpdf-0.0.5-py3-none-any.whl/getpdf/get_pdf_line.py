from .main import getpdf
import sys

name_pdf = sys.argv[1]
n_results = int(sys.argv[2]) if len(sys.argv)>=3 else 10

def main():
    getpdf(param=name_pdf,n=n_results)