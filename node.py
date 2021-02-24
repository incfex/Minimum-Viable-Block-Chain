import json
from hashlib import sha256
from hash_gen import hash_gen as hg
from tx_gen import tx_gen, tx_con
from nacl.encoding import HexEncoder
from nacl.signing import SigningKey, VerifyKey
from tx_vfy import tx_vfy

"""
utp = unverified transactions pool
gb = genesis block
bc = blockchain
"""

def node(gb, utp_json):
  with open("transactions.json", "r"):
    utp_json = f.read()
  utp_list = json.dumps(utp_json)
  vtp_list = []

  while not utp_list:
    tx_dict = utp_list.pop(0)
    if(not tx_vfy(tx_dict, vtp_list)):
      print("found invalid transaction")
      continue


  


def main():
  return


if __name__ == "__main__":
  main()