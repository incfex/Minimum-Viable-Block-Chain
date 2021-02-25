import json
from hashlib import sha256
from hash_gen import hash_gen as hg
from nacl.signing import SigningKey, VerifyKey
from nacl.encoding import HexEncoder

#TODO:
# Check for double spend

def tx_vfy(tx_dict, vtp_list, bc, ignore=0, is_utp=0):
  """
  tx_dict: transaction input in dictionary format

  vtp_list: verified transaction pool in dictionary format

  bc: blockchain in dictionary format

  ignore: ignore the input/output value check, default to 0; turn on for first tx
  
  is_utp: is calling from broadcasted block check, in this case, do not perform 
  already in blockchain check, default to 0.
  """

  # Check the number hash is correct
  num_o = tx_dict["number"]
  num_n = hg(tx_dict["input"], tx_dict["output"], tx_dict["sig"])
  if num_o != num_n:
    print("hash num incorrect!")
    return 0

  # Check transaction is not already on the blockchain
  if not is_utp:
    if not next((b for b in bc if b["tx"] == tx_dict["number"]), 1):
      print("transaction is already on the blockchain!")
      return 0
  
  input_value = 0
  # Check each number in the input exist as a transaction already on the blockchain
  for tx in tx_dict["input"]:
    b_input = next((b for b in bc if b["tx"] == tx["number"]), 0)
    if not b_input:
      print("input transaction is not found in the blockchain")
      return 0

    # Check each output in the input actually exists in the named transaction
    vtp_tx = next((t for t in vtp_list if t["number"] == tx["number"]), 0)
    if (not vtp_tx):
      print("transaction does not exist!")
      return 0
    # Check ...value and pubkey
    t_output = next((
        o for o in vtp_tx["output"]
        if o["pubkey"] == tx["output"]["pubkey"] and
        o["value"] == tx["output"]["value"]), 0)
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
    # Add up input value
    input_value += tx["output"]["value"]

  # Add up output value
  output_value = 0
  for v in tx_dict["output"]:
    output_value += v["value"]
  # Check if io value match
  if ignore:
    return 1
  if input_value != output_value:
    print("input output value does not match!")
    return 0

  return 1
    


def main():
  return


if __name__ == "__main__":
  main()