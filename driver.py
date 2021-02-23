import json
from hashlib import sha256

def main():


def gen_genesis_block():
  g_block = {
    "tx" = sha256(b'BABYLON STAGE34').hexdigest()
    "prev" = sha256(b'Tadokoro Koji').hexdigest()
    "nonce" = 1145141919
    "pow" = sha256(b'A Midsummer Nights Dream').hexdigest()
  }
  g_block_json = json.dumps(g_block)