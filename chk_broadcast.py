import json
from hash_gen import hash_gen as hg
from nacl.encoding import HexEncoder
from nacl.signing import SigningKey, VerifyKey
from tx_vfy import tx_vfy


def chk_broadcast(bqs, tails_list, blk_list, utp_list):
  """
  bqs: broadcast queue for itself

  tails_list: current tail tuple list [(tx, count)]
    tx: transaction number of block
    count: how long is the chain

  blk_list: list of blocks

  utp_list: unverified transaction pool in dictionary format
  """
  try:
    bb_json = bqs.get(False)
  except:
    return (tails_list)
  print("got new broadcast")

  # Process new block
  bb_dict = json.loads(bb_json)

  # Verify pow
  pow_n = hg(bb_dict["tx"], bb_dict["prev"], bb_dict["nonce"])
  if pow_n != bb_dict["pow"]:
    print("new block pow failed!")
    return (tails_list)
  # Verify prev
  b_prev = next(b for b in blk_list if b["tx"] == bb_dict["prev"], 0)
  if not b_prev:
    print("previous block not found!")
    return (tails_list)
  # Verify transaction
  tx = next(t for t in utp_list if bb_dict["tx"] == t["number"], 0)
  if not tx:
    print("transaction in the block not found!")
    return (tails_list)
  txv_result = tx_vfy(tx, utp_list, blk_list, 0, 1)
  if not txv_result:
    print("transaction verification failed!")
    return (tails_list)

  # Append the block to blockchain
  # Check if the prev is one of the tails
  # If not found, add to the tail, set counter to 1
  if next(t[0] for t in tails_list if t[0] == bb_dict["prev"], 0):
    tails_list.append((bb_dict["tx"], 1))
  # If found in tail, counter increase by 1
  tail = [(bb_dict["prev"],t[1]+1) for t in tails_list if t[0] == bb_dict["prev"]]

  # Sort the tail list based on the counter before return
  tail.sort(key = lambda x:x[1])
  
  print(tail)

  return (tail)
  


def main():
  return


if __name__ == "__main__":
  main()