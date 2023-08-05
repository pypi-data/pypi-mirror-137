import unittest
import pytest

import time
import Avalara.SDK
from Avalara.SDK.api.shipping_verification_api import ShippingVerificationApi  # noqa: E501

@pytest.mark.usefixtures("params")
class TestShippingVerificationApi(unittest.TestCase):
    """ShippingVerificationApi unit test stubs"""
    def setUp(self):
        configuration = Avalara.SDK.Configuration(
            username = self.params['username'], 
            password = self.params['password'],
            environment='sandbox'
        )
        with Avalara.SDK.ApiClient(configuration) as api_client:
            self.api = ShippingVerificationApi(api_client)

    def tearDown(self):
        pass

    def test_deregister_shipment(self):
        try:
            # self.api.deregister_shipment("Default","dededed")
            self.api.verify_shipment("DEFAULT", "063e1af4-11d3-4489-b8ba-ae1149758df4")
            print('Success')
        except Avalara.SDK.ApiException as e:
            print("Exception when calling ShippingVerification->verify_shipment: %s\n" % e)
            assert False

        print("Completed")
        pass

if __name__ == '__main__':
    unittest.main()