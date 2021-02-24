import json
from hashlib import sha256
from nacl.signing import SigningKey, VerifyKey
from nacl.encoding import HexEncoder
from hash_gen import hash_gen as hg


def tx_gen(keys):
  # Generate first transaction
  input = []
  # Give every key-pair 100 to spend
  output = [{
      "value": 100,
      "pubkey": x.verify_key.encode(encoder=HexEncoder).decode('utf-8')
  } for x in keys]
  # Calculate hashes
  sig = hg(input, output)
  sig = sig.encode('utf-8')
  sig = keys[0].sign(sig, encoder=HexEncoder).decode('utf-8')
  number = hg(input, output, sig)
  # Populate dictionary for tx0
  tx0 = {"number": number, "input": input, "output": output, "sig": sig}
  # Make tx0 the first transaction in the list
  tx0_json = json.dumps([tx0])
  # WRITE the json string to file
  with open('transactions.json', "w") as f:
    f.write(tx0_json)


def tx_con(txn, rx, s_key):
  '''
  txn is the transaction number of input, have format of list

  rx is the output, have format of tuple (value, receiver public key)
    value is double,
    public key is encoded by HexEncoder

  s_key is the sender's private key
  '''
  # Read tx from files
  with open('transactions.json', "r") as f:
    txs = f.read()
  txs_list = json.loads(txs)
  input = []
  for t in txn:
    tx_dict = next(i for i in txs_list if i["number"] == t)
    input_dict = {
        "number":
            t,
        "output":
            next(i for i in tx_dict["output"]
                 if i["pubkey"] == s_key.verify_key.encode(
                     encoder=HexEncoder).decode('utf-8'))
    }
    input.append(input_dict)

  # Craft output
  output=[]
  for t in rx:
    rx_dict = {
      "value": t[0],
      "pubkey": t[1]
    }
    output.append(rx_dict)

  sig = hg(input, output)
  sig = sig.encode('utf-8')
  sig = s_key.sign(sig, encoder=HexEncoder).decode('utf-8')
  number = hg(input,output,sig)
  tx = {
    "number": number,
    "input": input,
    "output": output,
    "sig": sig
  }
  txs_list.append(tx)
  txs_json = json.dumps(txs_list)
  with open('transactions.json', "w") as f:
    f.write(txs_json)


def main():
  return


if __name__ == "__main__":
  main()
