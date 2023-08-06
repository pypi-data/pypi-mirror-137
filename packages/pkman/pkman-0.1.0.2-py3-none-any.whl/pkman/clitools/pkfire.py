import os
from .pkx import Cli
os.environ['ANSI_COLORS_DISABLED']="1"
import fire
def main():
    fire.Fire(Cli().pkfire)
if __name__ == '__main__':
    main()