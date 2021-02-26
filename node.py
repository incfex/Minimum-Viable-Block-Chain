import json, copy
from hash_gen import hash_gen as hg
from nacl.encoding import HexEncoder
from nacl.signing import SigningKey, VerifyKey
from tx_vfy import tx_vfy
from chk_broadcast import chk_broadcast

"""
utp = unverified transactions pool
gb = genesis block
blk_list = blocks list
"""

def node(gb, utp_json, bq_list, proc):

  """
  gb: genesis block

  utp_json: unverified transactions pool in json format

  bq_list: list of broadcast queues except itself

  proc: process number
  """
  virgin = 1
  blk_list = [json.loads(gb)]
  utp_list = json.loads(utp_json)
  vtp_list = []
  tails_list = []
  # bqs: broadcast queue for itself
  bqs = bq_list[proc]
  # Pick out itself from the queue list
  bq_list = bq_list[:proc]+bq_list[(proc+1):]

  while len(utp_list) > 0:
  #for asdf in range(2):

    # Special treatment for first transaction
    if virgin:
      tx_dict = utp_list.pop(0)
      if(not tx_vfy(tx_dict, vtp_list, blk_list, 1)):
        print("found invalid transaction")
      #print("tx passed")
      vtp_list.append(tx_dict)
      virgin = 0
    # Normal transactions
    else: 
      tx_dict = utp_list.pop(0)
      if(not tx_vfy(tx_dict, vtp_list, blk_list)):
        print("found invalid transaction")
        continue
      #print("tx passed")
      vtp_list.append(tx_dict)
    # Construct block
    tx = tx_dict["number"]
    if len(tails_list) <= 0:
      prev = blk_list[-1]["pow"]
    else:
      prev = tails_list[-1][0]
    pow_tar = "7ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
    pow_cur = pow_tar
    nonce = 0
    while pow_cur >= pow_tar:
      nonce += 1
      pow_cur = hg(tx,prev,nonce)
    block = {
      "tx": tx,
      "prev": prev,
      "nonce": nonce,
      "pow": pow_cur
    }
    block_json = json.dumps(block)
    blk_list.append(block)
    if not next((t[0] for t in tails_list if t[0] == block["prev"]), 0):
      temp_t = (block["pow"],1)
      tails_list.append(temp_t)
    else: 
      # If found in tail, counter increase by 1
      tails_list = [tuple([block["pow"],(t[1]+1)]) for t in tails_list if t[0] == block["prev"]]

    # Broadcast block
    for q in bq_list:
      q.put(block_json)

    # Check for broadcast
    tails_list, blk_list = chk_broadcast(bqs, tails_list, blk_list, utp_list, vtp_list)
    print("\nblk_list")
    print(blk_list)
    print("\nvtp")
    print(vtp_list)
    # revoke invalid transactions
    vtp_list, utp_list = revoke_tx(tails_list, vtp_list, utp_list, blk_list)
    print(vtp_list)

  blk_json = json.dumps(blk_list)
  file_string = "./blocks/block" + str(proc)
  #print(blk_json)
  with open(file_string, "w") as f:
    f.write(blk_json)
    

def revoke_tx(tails_list, vtp_list, utp_list, blk_list):
  # get the longest tail in the chain
  tails_list.sort(key = lambda x:x[1])
  print("\ntails_list")
  print(tails_list)
  long_t = tails_list[-1][0]
  long_c = []
  # The following hash is the prev of genesis block
  while long_t != "1b02e8005aea3c0b96d566584c26e9141729693189a3ab59d9458ae5f841a1d4":
    result = next((b for b in blk_list if b["pow"] == long_t), 0)
    if result:
      long_c.append(result["tx"])
      long_t = result["prev"]
    else:
      print("revoke failed! Previous block not found")
      break
  print("\nlong_c")
  print(long_c)
  print()
  #return(vtp_list, utp_list)
  # Move the tx from vtp to utp if not found in the longest blockchain
  for tx in vtp_list:
    if not next((c for c in long_c if c == tx["number"]), 0):
      vtp_list.remove(tx)
      utp_list.insert(0, tx)
      print("\ntx")
      print(tx)
      print("transaction revoked!")

  return(vtp_list, utp_list)




def main():
  return


if __name__ == "__main__":
  main()