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

  """
  gb: genesis block

  utp_json: unverified transactions pool in json format
  """
  bc = [json.loads(gb)]
  utp_list = json.loads(utp_json)
  vtp_list = []

  # Special treatment for first transaction
  tx_dict = utp_list.pop(0)
  if(not tx_vfy(tx_dict, vtp_list, bc, 1)):
    print("found invalid transaction")
  print("tx passed")
  vtp_list.append(tx_dict)
  
  # Normal transactions
  while utp_list:
    tx_dict = utp_list.pop(0)
    if(not tx_vfy(tx_dict, vtp_list, bc)):
      print("found invalid transaction")
      continue
    print("tx passed")
    vtp_list.append(tx_dict)


  


def main():
  return


if __name__ == "__main__":
  main()