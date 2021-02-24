import json
from hashlib import sha256
from hash_gen import hash_gen as hg

#FIXME:
#  This needs pubkey, but i am giving it all keys

def tx_vfy(tx_dict, vtp_list):
  """
  tx_dict is transaction input in dictionary format

  vtp_list is verified transaction pool in dictionary format
  """

  # Check the number hash is correct
  num_o = tx_dict["number"]
  num_n = hg(tx_dict["input"] + tx_dict["output"] + tx_dict["sig"])
  if num_o != num_n:
    print("hash num incorrect!")
    return 0

  # Check each number in the input exist as a transaction already on the blockchain
  for tx in tx_dict["input"]:
    b_input = next(b for b in bc if b["tx"] == tx["number"], 0)
    if (not b_input):
      return 0

    # Check each output in the input actually exists in the named transaction
    vtp_tx = next(t for t in vtp_list if t["number"] == tx["number"], 0)
    if (not vtp_tx):
      print("transaction does not exist!")
      return 0
    # Check ...value and pubkey
    t_output = next(
        o for o in vtp_tx["output"]
        if o["pubkey"] == vtp_tx["output"]["pubkey"] and
        o["value"] == vtp_tx["output"]["value"], 0)
    if (not t_output):
      print("transaction value and pubkey does not match!")
      return 0
    # Check sig with pubkey
    sig_o = vtp_tx["sig"].encode('utf-8')
    usig_n = hg(vtp_tx["input"], vtp_tx["output"]).encode('utf-8')
    verify_key = VerifyKey(t_output["pubkey"].encode('utf-8'), encoder=HexEncoder)
    try:
      usig_o = verify_key.verify(sig_o, encoder=HexEncoder)
    except:
      print("sig verify failed!")
      return 0

  return 1
    


def main():
  return


if __name__ == "__main__":
  main()