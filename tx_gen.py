import json
from hashlib import sha256
from nacl.signing import SigningKey, VerifyKey
from nacl.encoding import HexEncoder
from hash_gen import hash_gen as hg

"""
Potential Improvements:
  use list of keys instead of names
"""

aiwass = SigningKey.generate()
abel = SigningKey.generate()
adam = SigningKey.generate()
cain = SigningKey.generate()
eve = SigningKey.generate()
isaac = SigningKey.generate()
judas = SigningKey.generate()
lilith = SigningKey.generate()

input = []
output = [
  {
    "value": 100,
    "pubkey": abel.verify_key.encode(encoder=HexEncoder).decode('utf-8')
  },
  {
    "value": 100,
    "pubkey": adam.verify_key.encode(encoder=HexEncoder).decode('utf-8')
  },
  {
    "value": 100,
    "pubkey": cain.verify_key.encode(encoder=HexEncoder).decode('utf-8')
  },
  {
    "value": 100,
    "pubkey": eve.verify_key.encode(encoder=HexEncoder).decode('utf-8')
  },
  {
    "value": 100,
    "pubkey": isaac.verify_key.encode(encoder=HexEncoder).decode('utf-8')
  },
  {
    "value": 100,
    "pubkey": judas.verify_key.encode(encoder=HexEncoder).decode('utf-8')
  },
  {
    "value": 100,
    "pubkey": lilith.verify_key.encode(encoder=HexEncoder).decode('utf-8')
  }
]
#sig_str = (json.dumps(input)+json.dumps(output)).encode('utf-8')
#sig = sha256(sig_str).hexdigest()
sig = hg(input, output)
number = hg(input, output, sig)

tx_0 = {
  "number": number,
  "input": input,
  "output": output,
  "sig": sig
}
tx_0_json = json.dumps(tx_0)
with open('transactions.json', "w") as f:
  f.write(tx_0_json)
