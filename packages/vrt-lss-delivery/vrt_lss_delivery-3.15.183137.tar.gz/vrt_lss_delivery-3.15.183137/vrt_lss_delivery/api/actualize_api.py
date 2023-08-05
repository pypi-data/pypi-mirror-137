# coding: utf-8

"""
    Veeroute.Delivery

    Veeroute Delivery API  # noqa: E501

    The version of the OpenAPI document: 3.15.183137
    Contact: support@veeroute.com
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from vrt_lss_delivery.api_client import ApiClient
from vrt_lss_delivery.exceptions import (  # noqa: F401
    ApiTypeError,
    ApiValueError
)


class ActualizeApi(object):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def actualize(self, actualize_task, **kwargs):  # noqa: E501
        """Trips actualization.  # noqa: E501

        Trips actualization.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.actualize(actualize_task, async_req=True)
        >>> result = thread.get()

        :param actualize_task: New request for actualization. (required)
        :type actualize_task: ActualizeTask
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :type _preload_content: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: PlanResult
        """
        kwargs['_return_http_data_only'] = True
        return self.actualize_with_http_info(actualize_task, **kwargs)  # noqa: E501

    def actualize_with_http_info(self, actualize_task, **kwargs):  # noqa: E501
        """Trips actualization.  # noqa: E501

        Trips actualization.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.actualize_with_http_info(actualize_task, async_req=True)
        >>> result = thread.get()

        :param actualize_task: New request for actualization. (required)
        :type actualize_task: ActualizeTask
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _return_http_data_only: response data without head status code
                                       and headers
        :type _return_http_data_only: bool, optional
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :type _preload_content: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: tuple(PlanResult, status_code(int), headers(HTTPHeaderDict))
        """

        local_var_params = locals()

        all_params = [
            'actualize_task'
        ]
        all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth'
            ]
        )

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method actualize" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'actualize_task' is set
        if self.api_client.client_side_validation and ('actualize_task' not in local_var_params or  # noqa: E501
                                                        local_var_params['actualize_task'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `actualize_task` when calling `actualize`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'actualize_task' in local_var_params:
            body_params = local_var_params['actualize_task']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['ApiKeyAuth']  # noqa: E501
        
        response_types_map = {
            200: "PlanResult",
            400: "InlineResponse400",
            401: "InlineResponse401",
            415: "InlineResponse415",
            429: "InlineResponse429",
            500: "InlineResponse500",
            501: "InlineResponse501",
            502: "InlineResponse502",
            503: "InlineResponse503",
            504: "InlineResponse504",
        }

        return self.api_client.call_api(
            '/delivery/actualize', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_types_map=response_types_map,
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats,
            _request_auth=local_var_params.get('_request_auth'))
