from ciscoconfparse import CiscoConfParse

def main():

    config_file = "cisco_ipsec.txt"

    cisco_cfg = CiscoConfParse(config_file)

    pfs_group = cisco_cfg.find_objects_w_child(parentspec=r"crypto map CRYPTO",
        childspec=r"set pfs group2")

    print "\nCrypto Maps using PFS group2:"
    for i in pfs_group:
        print "  {0}".format(i.text)
    print

if __name__ == '__main__':
    main()
