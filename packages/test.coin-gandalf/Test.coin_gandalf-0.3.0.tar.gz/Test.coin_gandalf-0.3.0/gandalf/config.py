from base58 import b58decode
from nacl.signing import VerifyKey

HASH_LEN = 32
PUBLIC_KEY_LEN = 32

MAX_TRANSACTIONS_PER_BLOCK = 10
MAX_DATA_SIZE = 512

ROOT_HASH = b58decode("8G2HqteEwBfoyhjjkK619a5P35otJBroRP7phuo7rrcV")
ROOT_HASH_SIGNATURE = b58decode(
    "2imbRXkUKutQJRS6ESwXDBawBZixinjSJ9owv5Zgyui5ThaKizqDH83gjfcBzCa7X7sBvJ5TztRUzBBRsNZWNYs7"
)

TOWER_PUBLIC_KEY = VerifyKey(b58decode("DSXsRPfX1u7NGprHpMoREwmexK2L3y6vjPxFxbwKSnUr"))

TOWER_PUBLIC_KEY.verify(ROOT_HASH, ROOT_HASH_SIGNATURE)
