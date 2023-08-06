import sys
from .brd import IOS_learned_interface,DNAC_Sites
if __name__ == "__main__":
    print(IOS_learned_interface(sys.argv[1]))
    print(DNAC_Sites(sys.argv[1]))