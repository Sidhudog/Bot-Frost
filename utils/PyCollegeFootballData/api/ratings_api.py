# coding: utf-8

"""
    College Football Data API

    This is an API for accessing all sorts of college football data.  It currently has a wide array of data ranging from play by play to player statistics to game scores and more.  # noqa: E501

    OpenAPI spec version: 1.12.0
    Contact: admin@collegefootballdata.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from PyCollegeFootballData.api_client import ApiClient


class RatingsApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def get_conference_sp_ratings(self, **kwargs):  # noqa: E501
        """Get average S&P+ historical rating data by conference  # noqa: E501

        Conference average S&P+ ratings by year  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_conference_sp_ratings(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int year: Season filter
        :param str conference: Conference abbreviation filter
        :return: list[ConferenceSPRating]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_conference_sp_ratings_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.get_conference_sp_ratings_with_http_info(**kwargs)  # noqa: E501
            return data

    def get_conference_sp_ratings_with_http_info(self, **kwargs):  # noqa: E501
        """Get average S&P+ historical rating data by conference  # noqa: E501

        Conference average S&P+ ratings by year  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_conference_sp_ratings_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int year: Season filter
        :param str conference: Conference abbreviation filter
        :return: list[ConferenceSPRating]
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['year', 'conference']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_conference_sp_ratings" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'year' in params:
            query_params.append(('year', params['year']))  # noqa: E501
        if 'conference' in params:
            query_params.append(('conference', params['conference']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/ratings/sp/conferences', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[ConferenceSPRating]',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_sp_ratings(self, **kwargs):  # noqa: E501
        """Get S&P+ historical rating data (requires either a year or team specified)  # noqa: E501

        S&P+ rating data  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_sp_ratings(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int year: Season filter (required if team not specified)
        :param str team: Team filter (required if year not specified)
        :return: list[TeamSPRating]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_sp_ratings_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.get_sp_ratings_with_http_info(**kwargs)  # noqa: E501
            return data

    def get_sp_ratings_with_http_info(self, **kwargs):  # noqa: E501
        """Get S&P+ historical rating data (requires either a year or team specified)  # noqa: E501

        S&P+ rating data  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_sp_ratings_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int year: Season filter (required if team not specified)
        :param str team: Team filter (required if year not specified)
        :return: list[TeamSPRating]
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['year', 'team']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_sp_ratings" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'year' in params:
            query_params.append(('year', params['year']))  # noqa: E501
        if 'team' in params:
            query_params.append(('team', params['team']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/ratings/sp', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[TeamSPRating]',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)