#!env/bin/python3.9
import json, queue
from hashlib import sha256
from hash_gen import hash_gen as hg
from tx_gen import tx_gen, tx_con
from nacl.encoding import HexEncoder
from nacl.signing import SigningKey, VerifyKey
from node import node
from threading import Thread
import time


# FIXME: when using random keys, tx_con will not work


def main():
  keys = key_gen(False)
  init_tx(keys)
  gen_genesis_block()
  with open("transactions.json", "r") as f:
    utp_json = f.read()
  with open("genesis_block.json", "r") as f:
    gb = f.read()
  
  if (0):
    q1 = queue.Queue()
    q2 = queue.Queue()
    node(gb, utp_json, [q1, q2], 1)
  else:
    q_list = [queue.Queue() for i in range(8)]
    for i in range(2):
      worker = Thread(target=node, args=(gb, utp_json, q_list, i))
      worker.setDaemon(True)
      worker.start()
      worker.join()
  

def init_tx(keys):
  tx_gen(keys)
  tx_con(["6d401ad942eda74625767af121a7b74607f2636a1168aed49e7bcdc3aa525bc5"],
         [(20, keys[1].verify_key.encode(encoder=HexEncoder).decode('utf-8')),
          (80, keys[0].verify_key.encode(encoder=HexEncoder).decode('utf-8'))],
         keys[0])
  tx_con(["6d401ad942eda74625767af121a7b74607f2636a1168aed49e7bcdc3aa525bc5"],
         [(50, keys[2].verify_key.encode(encoder=HexEncoder).decode('utf-8')),
          (50, keys[1].verify_key.encode(encoder=HexEncoder).decode('utf-8'))],
         keys[0])


def gen_genesis_block():
  g_block = {
      "tx": sha256(b'BABYLON STAGE34').hexdigest(),
      "prev": sha256(b'Tadokoro Koji').hexdigest(),
      "nonce": 1145141919,
      "pow": sha256(b'A Midsummer Nights Dream').hexdigest()
  }
  g_block_json = json.dumps(g_block)
  with open("genesis_block.json", "w") as f:
    f.write(g_block_json)


def key_gen(new):
  # Pass-in True to use new keys, False to use test keys
  keys = []
  for x in range(8):
    if new:
      key = SigningKey.generate()
    else:
      # make a seed that is 31B long
      seed = b'\x20\x4a\xc7\x3f\x5e\xc9\x6e\x64\xb4\xc4\xb6\x10\xa4\x3c\x81\x26\x00\xa7\x1e\x8a\xb5\xc7\xa4\xb2\xb7\x0e\xe9\x9e\xbd\xf7\xf1'
      # change the tail of the seed
      key = SigningKey(seed + x.to_bytes(1, 'big'))
    keys.append(key)

  return keys


if __name__ == "__main__":
  main()
