import json
from hash_gen import hash_gen as hg
from nacl.encoding import HexEncoder
from nacl.signing import SigningKey, VerifyKey
from tx_vfy import tx_vfy

"""
utp = unverified transactions pool
gb = genesis block
bc = blockchain
"""

def node(gb, utp_json, bq_list, bqs):

  """
  gb: genesis block

  utp_json: unverified transactions pool in json format

  bq_list: list of broadcast queues except itself

  bqs: broadcast queue for itself
  """
  virgin = 1
  bc = [json.loads(gb)]
  utp_list = json.loads(utp_json)
  vtp_list = []

  # Special treatment for first transaction
  if virgin:
    tx_dict = utp_list.pop(0)
    if(not tx_vfy(tx_dict, vtp_list, bc, 1)):
      print("found invalid transaction")
    print("tx passed")
    vtp_list.append(tx_dict)
    virgin = 0
  # Normal transactions
  else: 
    while utp_list:
      tx_dict = utp_list.pop(0)
      if(not tx_vfy(tx_dict, vtp_list, bc)):
        print("found invalid transaction")
        continue
      print("tx passed")
      vtp_list.append(tx_dict)

  # Construct block
  tx = tx_dict["number"]
  prev = bc[-1]["pow"]
  pow_tar = "7ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
  pow_cur = pow_tar
  nonce = 0
  while pow_cur >= pow_tar:
    nonce += 1
    pow_cur = hg(tx,prev,nonce)
    print(pow_cur)
  block = {
    "tx" = tx,
    "prev" = prev,
    "nonce" = nonce,
    "pow" = pow_cur
  }
  block_json = json.dumps(block)

  # Broadcast block
  for q in bq_list:
    q.put(block_json)




def main():
  return


if __name__ == "__main__":
  main()