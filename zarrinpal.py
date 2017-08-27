from suds import client


class ZarrinPalAPI(object):

    SERVICE_ADDRESS = 'https://www.zarinpal.com/pg/services/WebGate/wsdl'
    __pa__ = 'https://www.zarinpal.com/pg/StartPay/'
    __merchant_id__ = ''
    __call_address__ = ''
    __cli__ = None
    __auth__ = None

    def get_payment_address(self):
        return self.__pa__ + self.__auth__

    def __init__(self, merchant_id, callback_address):
        if not isinstance(merchant_id, str):
            raise TypeError('merchant_id is str not %s' % type(merchant_id))
        if not isinstance(callback_address, str) and not isinstance(callback_address, unicode):
            raise TypeError('callback_address is unicode or str not %s' % type(callback_address))
        self.__merchant_id__ = merchant_id
        self.__call_address__ = callback_address
        self.__cli__ = client.Client(self.SERVICE_ADDRESS)

    def request(self, amount, description, mail=None, mobile=None):
        """
        request a token from ZarrinPal
        :param amount: amount to transfer
        :param description: description of transaction
        :param mail: user email address
        :param mobile: user mobile number
        :return: str to redirect to
        """
        if not isinstance(amount, int):
            raise TypeError('amount is int not %s' % type(amount))
        if not isinstance(description, str) and not isinstance(description, unicode):
            raise TypeError('description is str or unicode not %s' % type(description))
        result = self.__cli__.service.PaymentRequest(self.__merchant_id__, amount,
                                                     description,
                                                     mail,
                                                     mobile,
                                                     self.__call_address__
                                                     )

        if result.Status == 100:
            self.__auth__ = result.Authority
            return result.Authority
        self.__auth__ = None
        return None

    def verify(self, authority_code, amount):
        """
        Verify payment request
        :param authority_code: auth code returned by request method!
        :param amount: amount of transfer
        :return: True, RefID if operation was success, else False and error message
        """
        result = self.__cli__.service.PaymentVerification(self.__merchant_id__,
                                                          authority_code,
                                                          amount)
        if result.Status == 100:
            return True, str(result.RefID)
        elif result.Status == 101:
            return False, 'request submitted'
        else:
            return False, 'request canceled by user or unknown error happened'

