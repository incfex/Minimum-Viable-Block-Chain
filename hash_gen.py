import json
from hashlib import sha256


def hash_gen(*args):
    end_str = ""
    for x in args:
        end_str += json.dumps(x)
    end_enc = end_str.encode('utf-8')
    end_sha = sha256(end_enc).hexdigest()
    return end_sha


def main():
    test = [{
        "value":
            100,
        "pubkey":
            "4e3ee84d21f827967b71ca31ae7e307303dc075d827643444a22919dd4847231"
    }, {
        "value":
            100,
        "pubkey":
            "73feccb9d1940877b658b37c223768ea67c09b8990f00d35633d09ae12d1526b"
    }, {}]
    print(hash_gen(test))


if __name__ == "__main__":
    main()
