"""
AvaTax Software Development Kit for Python.

   Copyright 2022 Avalara, Inc.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

    Avalara Shipping Verification for Beverage Alcohol
    API for evaluating transactions against direct-to-consumer Beverage Alcohol shipping regulations.  This API is currently in beta.  

@author     Sachin Baijal <sachin.baijal@avalara.com>
@author     Jonathan Wenger <jonathan.wenger@avalara.com>
@copyright  2022 Avalara, Inc.
@license    https://www.apache.org/licenses/LICENSE-2.0
@link       https://github.com/avadev/AvaTax-REST-V3-Python-SDK
"""

import sys
import unittest

import Avalara.SDK
from Avalara.SDK.model.age_verify_failure_code import AgeVerifyFailureCode


class TestAgeVerifyFailureCode(unittest.TestCase):
    """AgeVerifyFailureCode unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testAgeVerifyFailureCode(self):
        """Test AgeVerifyFailureCode"""
        # FIXME: construct object with mandatory attributes with example values
        # model = AgeVerifyFailureCode()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
