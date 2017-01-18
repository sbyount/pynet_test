from ciscoconfparse import CiscoConfParse

def main():

    config_file = "cisco_ipsec.txt"

    cisco_cfg = CiscoConfParse(config_file)

    pfs_group = cisco_cfg.find_objects_wo_child(parentspec=r"crypto map CRYPTO",
        childspec=r"set transform-set AES-SHA")

    print "\nCrypto Maps not using AES:"
    for i in pfs_group:
        print "  {0}".format(i.text)
    print

if __name__ == '__main__':
    main()
