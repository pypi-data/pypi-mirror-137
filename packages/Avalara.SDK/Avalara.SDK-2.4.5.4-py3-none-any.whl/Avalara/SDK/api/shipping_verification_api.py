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

    Avalara Shipping Verification only
    API for evaluating transactions against direct-to-consumer Beverage Alcohol shipping regulations.  This API is currently in beta.  

@author     Sachin Baijal <sachin.baijal@avalara.com>
@author     Jonathan Wenger <jonathan.wenger@avalara.com>
@copyright  2022 Avalara, Inc.
@license    https://www.apache.org/licenses/LICENSE-2.0
@version    2.4.5.4
@link       https://github.com/avadev/AvaTax-REST-V3-Python-SDK
"""

import re  # noqa: F401
import sys  # noqa: F401

from Avalara.SDK.api_client import ApiClient, Endpoint as _Endpoint
from Avalara.SDK.model_utils import (  # noqa: F401
    check_allowed_values,
    check_validations,
    date,
    datetime,
    file_type,
    none_type,
    validate_and_convert_types
)
from Avalara.SDK.model.error_details import ErrorDetails
from Avalara.SDK.model.shipping_verify_result import ShippingVerifyResult
from Avalara.SDK.exceptions import ApiTypeError, ApiValueError, ApiException

class ShippingVerificationApi(object):

    def __init__(self, api_client):
        self.__set_configuration(api_client)
    
    def __verify_api_client(self,api_client):
        if api_client is None:
            raise ApiValueError("APIClient not defined")
    
    def __set_configuration(self, api_client):
        self.__verify_api_client(api_client)
        api_client.set_sdk_version("2.4.5.4")
        self.api_client = api_client
		
        self.deregister_shipment_endpoint = _Endpoint(
            settings={
                'response_type': None,
                'auth': [
                    'BasicAuth',
                    'Bearer'
                ],
                'endpoint_path': '/api/v2/companies/{companyCode}/transactions/{transactionCode}/shipment/registration',
                'operation_id': 'deregister_shipment',
                'http_method': 'DELETE',
                'servers': None,
            },
            params_map={
                'all': [
                    'company_code',
                    'transaction_code',
                    'document_type',
                ],
                'required': [
                    'company_code',
                    'transaction_code',
                ],
                'nullable': [
                ],
                'enum': [
                    'document_type',
                ],
                'validation': [
                ]
            },
            root_map={
                'validations': {
                },
                'allowed_values': {
                    ('document_type',): {

                        "SALESINVOICE": "SalesInvoice",
                        "RETURNINVOICE": "ReturnInvoice"
                    },
                },
                'openapi_types': {
                    'company_code':
                        (str,),
                    'transaction_code':
                        (str,),
                    'document_type':
                        (str,),
                },
                'attribute_map': {
                    'company_code': 'companyCode',
                    'transaction_code': 'transactionCode',
                    'document_type': 'documentType',
                },
                'location_map': {
                    'company_code': 'path',
                    'transaction_code': 'path',
                    'document_type': 'query',
                },
                'collection_format_map': {
                }
            },
            headers_map={
                'accept': [
                    'application/json'
                ],
                'content_type': [],
            },
            api_client=api_client
        )
        self.register_shipment_endpoint = _Endpoint(
            settings={
                'response_type': None,
                'auth': [
                    'BasicAuth',
                    'Bearer'
                ],
                'endpoint_path': '/api/v2/companies/{companyCode}/transactions/{transactionCode}/shipment/registration',
                'operation_id': 'register_shipment',
                'http_method': 'PUT',
                'servers': None,
            },
            params_map={
                'all': [
                    'company_code',
                    'transaction_code',
                    'document_type',
                ],
                'required': [
                    'company_code',
                    'transaction_code',
                ],
                'nullable': [
                ],
                'enum': [
                    'document_type',
                ],
                'validation': [
                ]
            },
            root_map={
                'validations': {
                },
                'allowed_values': {
                    ('document_type',): {

                        "SALESINVOICE": "SalesInvoice",
                        "RETURNINVOICE": "ReturnInvoice"
                    },
                },
                'openapi_types': {
                    'company_code':
                        (str,),
                    'transaction_code':
                        (str,),
                    'document_type':
                        (str,),
                },
                'attribute_map': {
                    'company_code': 'companyCode',
                    'transaction_code': 'transactionCode',
                    'document_type': 'documentType',
                },
                'location_map': {
                    'company_code': 'path',
                    'transaction_code': 'path',
                    'document_type': 'query',
                },
                'collection_format_map': {
                }
            },
            headers_map={
                'accept': [
                    'application/json'
                ],
                'content_type': [],
            },
            api_client=api_client
        )
        self.register_shipment_if_compliant_endpoint = _Endpoint(
            settings={
                'response_type': (ShippingVerifyResult,),
                'auth': [
                    'BasicAuth',
                    'Bearer'
                ],
                'endpoint_path': '/api/v2/companies/{companyCode}/transactions/{transactionCode}/shipment/registerIfCompliant',
                'operation_id': 'register_shipment_if_compliant',
                'http_method': 'PUT',
                'servers': None,
            },
            params_map={
                'all': [
                    'company_code',
                    'transaction_code',
                    'document_type',
                ],
                'required': [
                    'company_code',
                    'transaction_code',
                ],
                'nullable': [
                ],
                'enum': [
                    'document_type',
                ],
                'validation': [
                ]
            },
            root_map={
                'validations': {
                },
                'allowed_values': {
                    ('document_type',): {

                        "SALESINVOICE": "SalesInvoice",
                        "RETURNINVOICE": "ReturnInvoice"
                    },
                },
                'openapi_types': {
                    'company_code':
                        (str,),
                    'transaction_code':
                        (str,),
                    'document_type':
                        (str,),
                },
                'attribute_map': {
                    'company_code': 'companyCode',
                    'transaction_code': 'transactionCode',
                    'document_type': 'documentType',
                },
                'location_map': {
                    'company_code': 'path',
                    'transaction_code': 'path',
                    'document_type': 'query',
                },
                'collection_format_map': {
                }
            },
            headers_map={
                'accept': [
                    'application/json'
                ],
                'content_type': [],
            },
            api_client=api_client
        )
        self.verify_shipment_endpoint = _Endpoint(
            settings={
                'response_type': (ShippingVerifyResult,),
                'auth': [
                    'BasicAuth',
                    'Bearer'
                ],
                'endpoint_path': '/api/v2/companies/{companyCode}/transactions/{transactionCode}/shipment/verify',
                'operation_id': 'verify_shipment',
                'http_method': 'GET',
                'servers': None,
            },
            params_map={
                'all': [
                    'company_code',
                    'transaction_code',
                    'document_type',
                ],
                'required': [
                    'company_code',
                    'transaction_code',
                ],
                'nullable': [
                ],
                'enum': [
                    'document_type',
                ],
                'validation': [
                ]
            },
            root_map={
                'validations': {
                },
                'allowed_values': {
                    ('document_type',): {

                        "SALESINVOICE": "SalesInvoice",
                        "RETURNINVOICE": "ReturnInvoice"
                    },
                },
                'openapi_types': {
                    'company_code':
                        (str,),
                    'transaction_code':
                        (str,),
                    'document_type':
                        (str,),
                },
                'attribute_map': {
                    'company_code': 'companyCode',
                    'transaction_code': 'transactionCode',
                    'document_type': 'documentType',
                },
                'location_map': {
                    'company_code': 'path',
                    'transaction_code': 'path',
                    'document_type': 'query',
                },
                'collection_format_map': {
                }
            },
            headers_map={
                'accept': [
                    'application/json'
                ],
                'content_type': [],
            },
            api_client=api_client
        )

    def deregister_shipment(
        self,
        company_code,
        transaction_code,
        **kwargs
    ):
        """Removes the transaction from consideration when evaluating regulations that span multiple transactions.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.deregister_shipment(company_code, transaction_code, async_req=True)
        >>> result = thread.get()

        Args:
            company_code (str): The company code of the company that recorded the transaction
            transaction_code (str): The transaction code to retrieve

        Keyword Args:
            document_type (str): (Optional): The document type of the transaction to operate on. If omitted, defaults to \"SalesInvoice\". [optional]
            _return_http_data_only (bool): response data without head status
                code and headers. Default is True.
            _preload_content (bool): if False, the urllib3.HTTPResponse object
                will be returned without reading/decoding response data.
                Default is True.
            _request_timeout (int/float/tuple): timeout setting for this request. If
                one number provided, it will be total request timeout. It can also
                be a pair (tuple) of (connection, read) timeouts.
                Default is None.
            _check_input_type (bool): specifies if type checking
                should be done one the data sent to the server.
                Default is True.
            _check_return_type (bool): specifies if type checking
                should be done one the data received from the server.
                Default is True.
            _host_index (int/None): specifies the index of the server
                that we want to use.
                Default is read from the configuration.
            async_req (bool): execute request asynchronously

        Returns:
            None
                If the method is called asynchronously, returns the request
                thread.
        """
        self.__verify_api_client(self.api_client)
        kwargs['async_req'] = kwargs.get(
            'async_req', False
        )
        kwargs['_return_http_data_only'] = kwargs.get(
            '_return_http_data_only', True
        )
        kwargs['_preload_content'] = kwargs.get(
            '_preload_content', True
        )
        kwargs['_request_timeout'] = kwargs.get(
            '_request_timeout', None
        )
        kwargs['_check_input_type'] = kwargs.get(
            '_check_input_type', True
        )
        kwargs['_check_return_type'] = kwargs.get(
            '_check_return_type', True
        )
        kwargs['_host_index'] = kwargs.get('_host_index')
        kwargs['company_code'] = \
            company_code
        kwargs['transaction_code'] = \
            transaction_code
        return self.deregister_shipment_endpoint.call_with_http_info(**kwargs)

    def register_shipment(
        self,
        company_code,
        transaction_code,
        **kwargs
    ):
        """Registers the transaction so that it may be included when evaluating regulations that span multiple transactions.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.register_shipment(company_code, transaction_code, async_req=True)
        >>> result = thread.get()

        Args:
            company_code (str): The company code of the company that recorded the transaction
            transaction_code (str): The transaction code to retrieve

        Keyword Args:
            document_type (str): (Optional): The document type of the transaction to operate on. If omitted, defaults to \"SalesInvoice\". [optional]
            _return_http_data_only (bool): response data without head status
                code and headers. Default is True.
            _preload_content (bool): if False, the urllib3.HTTPResponse object
                will be returned without reading/decoding response data.
                Default is True.
            _request_timeout (int/float/tuple): timeout setting for this request. If
                one number provided, it will be total request timeout. It can also
                be a pair (tuple) of (connection, read) timeouts.
                Default is None.
            _check_input_type (bool): specifies if type checking
                should be done one the data sent to the server.
                Default is True.
            _check_return_type (bool): specifies if type checking
                should be done one the data received from the server.
                Default is True.
            _host_index (int/None): specifies the index of the server
                that we want to use.
                Default is read from the configuration.
            async_req (bool): execute request asynchronously

        Returns:
            None
                If the method is called asynchronously, returns the request
                thread.
        """
        self.__verify_api_client(self.api_client)
        kwargs['async_req'] = kwargs.get(
            'async_req', False
        )
        kwargs['_return_http_data_only'] = kwargs.get(
            '_return_http_data_only', True
        )
        kwargs['_preload_content'] = kwargs.get(
            '_preload_content', True
        )
        kwargs['_request_timeout'] = kwargs.get(
            '_request_timeout', None
        )
        kwargs['_check_input_type'] = kwargs.get(
            '_check_input_type', True
        )
        kwargs['_check_return_type'] = kwargs.get(
            '_check_return_type', True
        )
        kwargs['_host_index'] = kwargs.get('_host_index')
        kwargs['company_code'] = \
            company_code
        kwargs['transaction_code'] = \
            transaction_code
        return self.register_shipment_endpoint.call_with_http_info(**kwargs)

    def register_shipment_if_compliant(
        self,
        company_code,
        transaction_code,
        **kwargs
    ):
        """Evaluates a transaction against a set of direct-to-consumer shipping regulations and, if compliant, registers the transaction so that it may be included when evaluating regulations that span multiple transactions.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.register_shipment_if_compliant(company_code, transaction_code, async_req=True)
        >>> result = thread.get()

        Args:
            company_code (str): The company code of the company that recorded the transaction
            transaction_code (str): The transaction code to retrieve

        Keyword Args:
            document_type (str): (Optional): The document type of the transaction to operate on. If omitted, defaults to \"SalesInvoice\". [optional]
            _return_http_data_only (bool): response data without head status
                code and headers. Default is True.
            _preload_content (bool): if False, the urllib3.HTTPResponse object
                will be returned without reading/decoding response data.
                Default is True.
            _request_timeout (int/float/tuple): timeout setting for this request. If
                one number provided, it will be total request timeout. It can also
                be a pair (tuple) of (connection, read) timeouts.
                Default is None.
            _check_input_type (bool): specifies if type checking
                should be done one the data sent to the server.
                Default is True.
            _check_return_type (bool): specifies if type checking
                should be done one the data received from the server.
                Default is True.
            _host_index (int/None): specifies the index of the server
                that we want to use.
                Default is read from the configuration.
            async_req (bool): execute request asynchronously

        Returns:
            ShippingVerifyResult
                If the method is called asynchronously, returns the request
                thread.
        """
        self.__verify_api_client(self.api_client)
        kwargs['async_req'] = kwargs.get(
            'async_req', False
        )
        kwargs['_return_http_data_only'] = kwargs.get(
            '_return_http_data_only', True
        )
        kwargs['_preload_content'] = kwargs.get(
            '_preload_content', True
        )
        kwargs['_request_timeout'] = kwargs.get(
            '_request_timeout', None
        )
        kwargs['_check_input_type'] = kwargs.get(
            '_check_input_type', True
        )
        kwargs['_check_return_type'] = kwargs.get(
            '_check_return_type', True
        )
        kwargs['_host_index'] = kwargs.get('_host_index')
        kwargs['company_code'] = \
            company_code
        kwargs['transaction_code'] = \
            transaction_code
        return self.register_shipment_if_compliant_endpoint.call_with_http_info(**kwargs)

    def verify_shipment(
        self,
        company_code,
        transaction_code,
        **kwargs
    ):
        """Evaluates a transaction against a set of direct-to-consumer shipping regulations.  # noqa: E501

        The transaction and its lines must meet the following criteria in order to be evaluated: * The transaction must be recorded. Using a type of *SalesInvoice* is recommended. * A parameter with the name *AlcoholRouteType* must be specified and the value must be one of the following: '*DTC*', '*Retailer DTC*' * A parameter with the name *RecipientName* must be specified and the value must be the name of the recipient. * Each alcohol line must include a *ContainerSize* parameter that describes the volume of a single container. Use the *unit* field to specify one of the following units: '*Litre*', '*Millilitre*', '*gallon (US fluid)*', '*quart (US fluid)*', '*ounce (fluid US customary)*' * Each alcohol line must include a *PackSize* parameter that describes the number of containers in a pack. Specify *Count* in the *unit* field.  Optionally, the transaction and its lines may use the following parameters: * The *ShipDate* parameter may be used if the date of shipment is different than the date of the transaction. The value should be ISO-8601 compliant (e.g. 2020-07-21). * The *RecipientDOB* parameter may be used to evaluate age restrictions. The value should be ISO-8601 compliant (e.g. 2020-07-21). * The *PurchaserDOB* parameter may be used to evaluate age restrictions. The value should be ISO-8601 compliant (e.g. 2020-07-21). * The *SalesLocation* parameter may be used to describe whether the sale was made *OnSite* or *OffSite*. *OffSite* is the default value. * The *AlcoholContent* parameter may be used to describe the alcohol percentage by volume of the item. Specify *Percentage* in the *unit* field.  **Security Policies** This API depends on all of the following active subscriptions: *AvaAlcohol, AutoAddress, AvaTaxPro*  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.verify_shipment(company_code, transaction_code, async_req=True)
        >>> result = thread.get()

        Args:
            company_code (str): The company code of the company that recorded the transaction
            transaction_code (str): The transaction code to retrieve

        Keyword Args:
            document_type (str): (Optional): The document type of the transaction to operate on. If omitted, defaults to \"SalesInvoice\". [optional]
            _return_http_data_only (bool): response data without head status
                code and headers. Default is True.
            _preload_content (bool): if False, the urllib3.HTTPResponse object
                will be returned without reading/decoding response data.
                Default is True.
            _request_timeout (int/float/tuple): timeout setting for this request. If
                one number provided, it will be total request timeout. It can also
                be a pair (tuple) of (connection, read) timeouts.
                Default is None.
            _check_input_type (bool): specifies if type checking
                should be done one the data sent to the server.
                Default is True.
            _check_return_type (bool): specifies if type checking
                should be done one the data received from the server.
                Default is True.
            _host_index (int/None): specifies the index of the server
                that we want to use.
                Default is read from the configuration.
            async_req (bool): execute request asynchronously

        Returns:
            ShippingVerifyResult
                If the method is called asynchronously, returns the request
                thread.
        """
        self.__verify_api_client(self.api_client)
        kwargs['async_req'] = kwargs.get(
            'async_req', False
        )
        kwargs['_return_http_data_only'] = kwargs.get(
            '_return_http_data_only', True
        )
        kwargs['_preload_content'] = kwargs.get(
            '_preload_content', True
        )
        kwargs['_request_timeout'] = kwargs.get(
            '_request_timeout', None
        )
        kwargs['_check_input_type'] = kwargs.get(
            '_check_input_type', True
        )
        kwargs['_check_return_type'] = kwargs.get(
            '_check_return_type', True
        )
        kwargs['_host_index'] = kwargs.get('_host_index')
        kwargs['company_code'] = \
            company_code
        kwargs['transaction_code'] = \
            transaction_code
        return self.verify_shipment_endpoint.call_with_http_info(**kwargs)

