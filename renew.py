import argparse
import os
import sys
from subprocess import Popen

CERTBOT_FOLDER = os.path.join("/", "etc", "letsencrypt", "live")


def main():
    args = _get_args()

    _run_certbot(args.domain)
    _create_pfx(args.domain)


def _get_args():
    parser = argparse.ArgumentParser(description='Cert Renewal')
    parser.add_argument('--domain', required=True, help="Domain name to renew")
    return parser.parse_args()


def _run_certbot(domain):
    p = Popen(["certbot", "certonly", "--preferred-challanges", "http", "-d", domain, "--manual"])
    p.communicate()


def _create_pfx(domain):
    domain_folder = os.path.join(CERTBOT_FOLDER, domain)
    pfx_path = os.path.join(domain_folder, "certificate.pfx")
    privkey_path = os.path.join(domain_folder, "privkey.pem")
    fullchain_path = os.path.join(domain_folder, "fullchain.pem")

    p = Popen(["openssl", "pkcs12", "-export", "--out", pfx_path, "-inkey", privkey_path, "-in", fullchain_path])
    p.communicate()


if __name__ == "__main__":
    sys.exit(main())
