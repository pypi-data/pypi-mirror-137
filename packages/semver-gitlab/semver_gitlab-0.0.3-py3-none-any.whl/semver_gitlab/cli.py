import argparse
import logging
import os
import sys

from semver_gitlab import semver_dfx

logger = logging.getLogger("dfx-semver")


def main():
    parser = argparse.ArgumentParser(prog='semver',
                                     description='calculates the next semantic version')
    parser.add_argument('-b', '--branch',
                        type=str,
                        help='The branch version to be calculated. develop, release and master are valid values',
                        default=os.environ.get("BRANCH_NAME", None),
                        choices=['develop', 'release', 'main'])
    parser.add_argument('-p', '--project',
                        type=str,
                        help='GitLab project id')
    parser.add_argument('--url',
                        type=str,
                        metavar='URL',
                        help='GitLab Repository URL for on-prem installations',
                        default=os.environ.get("GITLAB_PROJECT_URL", None))
    parser.add_argument('-t', '--token',
                        type=str,
                        metavar="Access Token",
                        help="GitLab Access Token")
    parser.add_argument('--pre',
                        action='store_true',
                        help='add a pre-release tag')

    args = parser.parse_args()

    try:
        semver_dfx.init(args)
    except:
        logger.exception("semver failed")
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()
