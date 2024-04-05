import os, sys

# add ../../Sources to the PYTHONPATH
sys.path.append(os.path.join("..", "..", "Sources"))

from yocto_api import *


def load_cert_from_file(url):
    filename = url.replace("/", "_").replace(":", "_") + ".crt"
    if os.path.isfile(filename):
        with open(filename) as f:
            return f.read()
    return ""


def save_cert_to_file(url, trusted_cert):
    filename = url.replace("/", "_").replace(":", "_") + ".crt"
    with open(filename, "w") as f:
        f.write(trusted_cert)


def main():
    username = "admin"
    password = "1234"
    host = "localhost"
    url = "secure://" + username + ":" + password + "@" + host
    # load known TLS certificate into the API
    trusted_cert = load_cert_from_file(host)
    if trusted_cert != "":
        error = YAPI.AddTrustedCertificates(trusted_cert)
        if error != "":
            sys.exit(error)

    # test connection with VirtualHub
    errmsg = YRefParam()
    res = YAPI.TestHub(url, 1000, errmsg)
    if res == YAPI.SSL_UNK_CERT:
        # remote TLS certificate is unknown ask user what to do
        print("Remote SSL/TLS certificate is unknown")
        print("You can.")
        print("-(A)dd certificate to the API")
        print("-(I)Ignore this error and continue anyway")
        print("-(E)xit")
        print("Your choice: ")
        line = input(": ").lower()
        if line[0] == "a":
            # download remote certificate and save it locally
            trusted_cert = YAPI.DownloadHostCertificate(url, 5000)
            if trusted_cert.startswith("error"):
                sys.exit(trusted_cert)
            save_cert_to_file(host, trusted_cert)
            error = YAPI.AddTrustedCertificates(trusted_cert)
            if error != "":
                sys.exit(error)
        elif line[0] == 'i':
            YAPI.SetNetworkSecurityOptions(YAPI.NO_HOSTNAME_CHECK | YAPI.NO_TRUSTED_CA_CHECK |
                                           YAPI.NO_EXPIRATION_CHECK)
        else:
            sys.exit("Exiting.")
    elif res != YAPI.SUCCESS:
        sys.exit("YAPI.TestHub failed:" + errmsg.value)

    if YAPI.RegisterHub(url, errmsg) != YAPI.SUCCESS:
        sys.exit("YAPI.RegisterHub failed:" + errmsg.value)
    print("Device list")
    module = YModule.FirstModule()
    while module is not None:
        print(module.get_serialNumber() + ' (' + module.get_productName() + ')')
        module = module.nextModule()
    YAPI.FreeAPI()


if __name__ == '__main__':
    main()
