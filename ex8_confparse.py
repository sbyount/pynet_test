from ciscoconfparse import CiscoConfParse

def main():

    config_file = "cisco_ipsec.txt"

    cisco_cfg = CiscoConfParse(config_file)

    crypto_map = cisco_cfg.find_objects(r"^crypto map CRYPTO")

    for i in crypto_map:
        print
        print i.text

        for child in i.children:
            print child.text
        print

if __name__ == '__main__':
    main()
