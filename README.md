# Running
## Requirements

* OpenSSL
* `pip install -U -r requirements.txt`

## Renew cert
`python3 renew.py --domain <DOMAIN> --validation-path <PATH> --pfx-password <PFX_PASSWORD>`

`<PATH>` can be either a normal folder or SSH folder, in SSH case use the follwing path syntax: `<username>@<IP>:<PORT>:<path>`