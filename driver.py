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
  

  # Worker with proc=2 is malicious
  workers = []
  if (0):
    q1 = queue.Queue()
    q2 = queue.Queue()
    node(gb, utp_json, [q1, q2], 1)
  else:
    q_list = [queue.Queue() for i in range(8)]
    for i in range(8):
      workers.append(Thread(target=node, args=(gb, utp_json, q_list, i)))
      workers[i].setDaemon(True)
      workers[i].start()
      # Uncomment the following to test broadcast
      # workers[i].join()
    for w in workers:
      # Comment the following to test broadcast
      w.join()
    

  

def init_tx(keys):
  tx_gen(keys)
  #Valid
  tx_con(["6d401ad942eda74625767af121a7b74607f2636a1168aed49e7bcdc3aa525bc5"],
         [(20, keys[2].verify_key.encode(encoder=HexEncoder).decode('utf-8')),
          (80, keys[0].verify_key.encode(encoder=HexEncoder).decode('utf-8'))],
         keys[7])
  #Valid, chain from first previous tx
  tx_con(["6487c35153003bcf6cdf8fea0b4c3ee794470761c42af0be3ef7405d95614b8e"],
         [(10, keys[2].verify_key.encode(encoder=HexEncoder).decode('utf-8')),
          (10, keys[1].verify_key.encode(encoder=HexEncoder).decode('utf-8'))],
         keys[2])
  #Double Spend
  tx_con(["6d401ad942eda74625767af121a7b74607f2636a1168aed49e7bcdc3aa525bc5"],
         [(50, keys[1].verify_key.encode(encoder=HexEncoder).decode('utf-8')),
          (50, keys[2].verify_key.encode(encoder=HexEncoder).decode('utf-8'))],
         keys[7])
  #Money not match
  tx_con(["6d401ad942eda74625767af121a7b74607f2636a1168aed49e7bcdc3aa525bc5"],
         [(10, keys[3].verify_key.encode(encoder=HexEncoder).decode('utf-8')),
          (10, keys[4].verify_key.encode(encoder=HexEncoder).decode('utf-8'))],
         keys[1])
  #Valid
  tx_con(["323222b356b4aaa54e41aeb1777621875cc0e82ee575dc53430041f1ebed130f"],
         [(5, keys[4].verify_key.encode(encoder=HexEncoder).decode('utf-8')),
          (5, keys[3].verify_key.encode(encoder=HexEncoder).decode('utf-8'))],
         keys[2])
  #Valid
  tx_con(["a9f661d44c8be7fee955f6a50eb549fbafac3b5f9481dfaee035d6f4b70641bd"],
         [(2, keys[5].verify_key.encode(encoder=HexEncoder).decode('utf-8')),
          (3, keys[6].verify_key.encode(encoder=HexEncoder).decode('utf-8'))],
         keys[3])
  #Valid: Combining 100 + 5 from 2 different tx of key4 and send to key7
  tx_con(["a9f661d44c8be7fee955f6a50eb549fbafac3b5f9481dfaee035d6f4b70641bd",
         "6d401ad942eda74625767af121a7b74607f2636a1168aed49e7bcdc3aa525bc5"],
         [(105, keys[7].verify_key.encode(encoder=HexEncoder).decode('utf-8'))],
         keys[4])
  #Valid: Spending the combined tx
  tx_con(["4dd0695621881eb3eae248a3d8a2a1a42f1ab7995369174419bf3794bd27e41c"],
         [(25, keys[5].verify_key.encode(encoder=HexEncoder).decode('utf-8')),
          (80, keys[6].verify_key.encode(encoder=HexEncoder).decode('utf-8'))],
         keys[7])
  #Valid:
  tx_con(["6d401ad942eda74625767af121a7b74607f2636a1168aed49e7bcdc3aa525bc5"],
         [(45, keys[6].verify_key.encode(encoder=HexEncoder).decode('utf-8')),
          (55, keys[2].verify_key.encode(encoder=HexEncoder).decode('utf-8'))],
         keys[3])
  #Valid:
  tx_con(["6d401ad942eda74625767af121a7b74607f2636a1168aed49e7bcdc3aa525bc5"],
         [(25, keys[3].verify_key.encode(encoder=HexEncoder).decode('utf-8')),
          (75, keys[6].verify_key.encode(encoder=HexEncoder).decode('utf-8'))],
         keys[0])
  #Valid:
  tx_con(["6d401ad942eda74625767af121a7b74607f2636a1168aed49e7bcdc3aa525bc5"],
         [(5, keys[7].verify_key.encode(encoder=HexEncoder).decode('utf-8')),
          (95, keys[3].verify_key.encode(encoder=HexEncoder).decode('utf-8'))],
         keys[6])
  #Valid:
  tx_con(["2b9af69a919a5385b9fd62f584ebe9b13c17ffe61a0ebfe117a6ea0c53b0050b",
          "ec9641281ad6c83bbd8d0c2ee7fb08cfcbe1ba445fff9def1c7b2f109b80fbf2"],
         [(60, keys[2].verify_key.encode(encoder=HexEncoder).decode('utf-8')),
          (60, keys[6].verify_key.encode(encoder=HexEncoder).decode('utf-8'))],
         keys[3])
  #Valid:
  tx_con(["6d401ad942eda74625767af121a7b74607f2636a1168aed49e7bcdc3aa525bc5"],
         [(67, keys[7].verify_key.encode(encoder=HexEncoder).decode('utf-8')),
          (33, keys[1].verify_key.encode(encoder=HexEncoder).decode('utf-8'))],
         keys[2])
  #double spend and mismatch:
  tx_con(["6d401ad942eda74625767af121a7b74607f2636a1168aed49e7bcdc3aa525bc5"],
         [(10, keys[2].verify_key.encode(encoder=HexEncoder).decode('utf-8')),
          (10, keys[3].verify_key.encode(encoder=HexEncoder).decode('utf-8'))],
         keys[7])
  #double spend:
  tx_con(["6d401ad942eda74625767af121a7b74607f2636a1168aed49e7bcdc3aa525bc5"],
         [(90, keys[7].verify_key.encode(encoder=HexEncoder).decode('utf-8')),
          (10, keys[2].verify_key.encode(encoder=HexEncoder).decode('utf-8'))],
         keys[6])


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
