# -*- coding: utf-8 -*-

"""
@author: xuan
@contact: QQ: 595127207
@Created on: 2021/6/6 006 12:39
@Remark: 自定义过滤器
"""
import operator
from functools import reduce

import six
from django.db.models import Q
from django.db.models.constants import LOOKUP_SEP
from django_filters import utils
from django_filters.filters import CharFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import BaseFilterBackend


class DataLevelPermissionsFilter(BaseFilterBackend):
    """
    数据 级权限过滤器
    0. 获取用户的部门id，没有部门则返回空
    1. 判断过滤的数据是否有创建人所在部门 "creator" 字段,没有则返回全部
    2. 如果用户没有关联角色则返回本部门数据
    3. 根据角色的最大权限进行数据过滤(会有多个角色，进行去重取最大权限)
    3.1 判断用户是否为超级管理员角色/如果有1(所有数据) 则返回所有数据

    4. 只为仅本人数据权限时只返回过滤本人数据，并且部门为自己本部门(考虑到用户会变部门，只能看当前用户所在的部门数据)
    5. 自定数据权限 获取部门，根据部门过滤
    """

    def filter_queryset(self, request, queryset, view):
        """
        判断是否为超级管理员:
        如果不是超级管理员,则进入下一步权限判断
        """
        if request.user.is_superuser == 0:

            # 3. 根据所有角色 获取所有权限范围
            role_list = request.user.role.filter(status=1).values('admin', 'data_range')
            dataScope_list = []
            for ele in role_list:
                # 3.1 判断用户是否为超级管理员角色/如果有1(所有数据) 则返回所有数据
                if 3 == ele.get('data_range') or ele.get('admin') == True:
                    return queryset
                dataScope_list.append(ele.get('data_range'))
            dataScope_list = list(set(dataScope_list))

            # 4. 只为仅本人数据权限时只返回过滤本人数据，并且部门为自己本部门(考虑到用户会变部门，只能看当前用户所在的部门数据)
            if 0 in dataScope_list:
                return queryset.filter(creator=request.user)

            # 5. 自定数据权限 获取部门，根据部门过滤
            dept_list = []

            return queryset.none()
        else:
            return queryset


class CustomDjangoFilterBackend(DjangoFilterBackend):
    lookup_prefixes = {
        '^': 'istartswith',
        '=': 'iexact',
        '@': 'search',
        '$': 'iregex',
        '~': 'icontains'
    }

    def construct_search(self, field_name):
        lookup = self.lookup_prefixes.get(field_name[0])
        if lookup:
            field_name = field_name[1:]
        else:
            lookup = 'icontains'
        return LOOKUP_SEP.join([field_name, lookup])

    def find_filter_lookups(self, orm_lookups, search_term_key):
        for lookup in orm_lookups:
            if lookup.find(search_term_key) >= 0:
                return lookup
        return None

    def filter_queryset(self, request, queryset, view):
        filterset = self.get_filterset(request, queryset, view)
        if filterset is None:
            return queryset
        if filterset.__class__.__name__ == 'AutoFilterSet':
            queryset = filterset.queryset
            orm_lookups = []
            for search_field in filterset.filters:
                if isinstance(filterset.filters[search_field],CharFilter):
                    orm_lookups.append(self.construct_search(six.text_type(search_field)))
                else:
                    orm_lookups.append(search_field)
            conditions = []
            queries = []
            for search_term_key in filterset.data.keys():
                orm_lookup = self.find_filter_lookups(orm_lookups, search_term_key)
                if not orm_lookup:
                    continue
                query = Q(**{orm_lookup: filterset.data[search_term_key]})
                queries.append(query)
            if len(queries) > 0:
                conditions.append(reduce(operator.and_, queries))
                queryset = queryset.filter(reduce(operator.and_, conditions))
                return queryset
            else:
                return queryset

        if not filterset.is_valid() and self.raise_exception:
            raise utils.translate_validation(filterset.errors)
        return filterset.qs
