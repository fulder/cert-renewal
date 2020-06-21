import argparse
import os
import sys
from subprocess import Popen

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))


def main():
    args = _get_args()

    _run_certbot(args.domain, args.certbot_folder)
    _create_pfx(args.domain, args.certbot_folder)


def _get_args():
    parser = argparse.ArgumentParser(description='Cert Renewal')
    parser.add_argument('--domain', "-d", required=True, help="Domain name to renew")
    parser.add_argument('--certbot-folder', required=False, help="Path to certbot out folder",
                        default="/etc/letsencrypt")
    return parser.parse_args()


def _run_certbot(domain, certbot_folder):
    config_dir = os.path.join(certbot_folder, "config")
    work_dir = os.path.join(certbot_folder, "work")
    logs_dir = os.path.join(certbot_folder, "logs")

    p = Popen([
        "certbot", "certonly",
        "--preferred-challenges", "http",
        "-d", domain,
        "--manual",
        "--config-dir", config_dir,
        "--work-dir", work_dir,
        "--logs-dir", logs_dir,
        "--staging",
        "--manual-auth-hook", os.path.join(CURRENT_DIR, "pre_hook.py"),
        "--manual-cleanup-hook", os.path.join(CURRENT_DIR, "post_hook.py"),
    ])
    p.communicate()


def _create_pfx(domain, certbot_folder):
    domain_folder = os.path.join(certbot_folder, "live", domain)
    pfx_path = os.path.join(domain_folder, "certificate.pfx")
    privkey_path = os.path.join(domain_folder, "privkey.pem")
    fullchain_path = os.path.join(domain_folder, "fullchain.pem")

    p = Popen(["openssl", "pkcs12", "-export", "--out", pfx_path, "-inkey", privkey_path, "-in", fullchain_path])
    p.communicate()


if __name__ == "__main__":
    sys.exit(main())
