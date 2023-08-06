"""Entry point"""

from karaone import cli, __app_name__
from karaone.cli import __app_name__
 
def main():

    cli.app(prog_name = __app_name__)

if __name__ == "__main__":
    main()