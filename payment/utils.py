from collections import OrderedDict
from hashlib import md5

from config import PAY_TRIO_SECRET_KEY, PAY_TRIO_SHOP_ID


def generate_sign(required_params):
    """pass in only required parameters for payment"""
    if not required_params:
        raise TypeError('pass in parameters to generate sign')
    required_params['shop_id'] = PAY_TRIO_SHOP_ID
    params = OrderedDict(sorted(required_params.items()))
    hash_string = ':'.join(str(v) for v in params.values())
    hash_string += PAY_TRIO_SECRET_KEY
    return md5(hash_string.encode('utf-8')).hexdigest()
