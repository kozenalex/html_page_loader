import argparse
import os
from page_loader import download
from page_loader.logger import config_logger
DESCRIPTION = ''


parser = argparse.ArgumentParser(description=DESCRIPTION)
parser.add_argument('target_url', type=str, help='url of page to download')
parser.add_argument(
    '-o', '--output',
    type=str,
    default=os.getcwd(),
    help='output file path (default: "current working directory")'
)


def main():
    args = parser.parse_args()
    config_logger()
    file_path = download(args.target_url, args.output)
    print(file_path)


if __name__ == '__main__':
    main()
