import argparse
import os
import re
import sys
from subprocess import Popen

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))


def main():
    args = _get_args()

    _run_certbot(args.domain, args.certbot_folder, args.validation_path)
    _create_pfx(args.domain, args.certbot_folder)


def _get_args():
    parser = argparse.ArgumentParser(description='Cert Renewal')
    parser.add_argument('--domain', "-d", required=True, help="Domain name to renew")
    parser.add_argument('--validation-path', required=True,
                        help="Path where HTTP-01 validation file should be placed. Use '<username>@<IP>:<PORT>:<path>' for scp")
    parser.add_argument('--certbot-folder', required=False, help="Path to certbot out folder",
                        default="./letsencrypt")
    args = parser.parse_args()

    if not re.match(r"(\w@[^:]+:\d+:)*\w+", args.validation_path):
        raise RuntimeError(
            "--validation--path argument should either be a path or '<username>@<IP>:<PORT>:<path>' for SCP")

    return args


def _run_certbot(domain, certbot_folder, validation_path):
    config_dir = os.path.join(certbot_folder, "config")
    work_dir = os.path.join(certbot_folder, "work")
    logs_dir = os.path.join(certbot_folder, "logs")

    env = os.environ.copy()
    env["VALIDATION_PATH"] = validation_path

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
    ], env=env)
    p.communicate()
    if p.returncode != 0:
        raise RuntimeError("Error during certbot command")


def _create_pfx(domain, certbot_folder):
    domain_folder = os.path.join(certbot_folder, "live", domain)
    pfx_path = os.path.join(domain_folder, "certificate.pfx")
    privkey_path = os.path.join(domain_folder, "privkey.pem")
    fullchain_path = os.path.join(domain_folder, "fullchain.pem")

    p = Popen(["openssl", "pkcs12", "-export", "--out", pfx_path, "-inkey", privkey_path, "-in", fullchain_path])
    p.communicate()
    if p.returncode != 0:
        raise RuntimeError("Error during openssl command")


if __name__ == "__main__":
    sys.exit(main())
