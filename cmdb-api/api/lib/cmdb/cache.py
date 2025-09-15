# -*- coding:utf-8 -*-

from __future__ import unicode_literals

from collections import defaultdict

import datetime
import os
import yaml
from flask import current_app
import json
from api.extensions import cache
from api.extensions import db
from api.lib.cmdb.custom_dashboard import CustomDashboardManager
from api.models.cmdb import Attribute, AutoDiscoveryExecHistory
from api.models.cmdb import AutoDiscoveryCI
from api.models.cmdb import AutoDiscoveryCIType
from api.models.cmdb import AutoDiscoveryCITypeRelation
from api.models.cmdb import AutoDiscoveryCounter
from api.models.cmdb import AutoDiscoveryRuleSyncHistory
from api.models.cmdb import CI
from api.models.cmdb import CIType
from api.models.cmdb import CITypeAttribute
from api.models.cmdb import PreferenceShowAttributes
from api.models.cmdb import PreferenceTreeView
from api.models.cmdb import RelationType


class AttributeCache(object):
    PREFIX_ID = 'Field::ID::{0}'
    PREFIX_NAME = 'Field::Name::{0}'
    PREFIX_ALIAS = 'Field::Alias::{0}'

    @classmethod
    def get(cls, key):
        if key is None:
            return
        attr = cache.get(cls.PREFIX_NAME.format(key))
        attr = attr or cache.get(cls.PREFIX_ID.format(key))
        attr = attr or cache.get(cls.PREFIX_ALIAS.format(key))

        if attr is None:
            attr = Attribute.get_by(name=key, first=True, to_dict=False)
            attr = attr or Attribute.get_by_id(key)
            attr = attr or Attribute.get_by(alias=key, first=True, to_dict=False)
            if attr is not None:
                cls.set(attr)

        return attr

    @classmethod
    def set(cls, attr):
        cache.set(cls.PREFIX_ID.format(attr.id), attr)
        cache.set(cls.PREFIX_NAME.format(attr.name), attr)
        cache.set(cls.PREFIX_ALIAS.format(attr.alias), attr)

    @classmethod
    def clean(cls, attr):
        cache.delete(cls.PREFIX_ID.format(attr.id))
        cache.delete(cls.PREFIX_NAME.format(attr.name))
        cache.delete(cls.PREFIX_ALIAS.format(attr.alias))


class CITypeCache(object):
    PREFIX_ID = "CIType::ID::{0}"
    PREFIX_NAME = "CIType::Name::{0}"
    PREFIX_ALIAS = "CIType::Alias::{0}"

    @classmethod
    def get(cls, key):
        if key is None:
            return
        ct = cache.get(cls.PREFIX_NAME.format(key))
        ct = ct or cache.get(cls.PREFIX_ID.format(key))
        ct = ct or cache.get(cls.PREFIX_ALIAS.format(key))
        if ct is None:
            ct = CIType.get_by(name=key, first=True, to_dict=False)
            ct = ct or CIType.get_by_id(key)
            ct = ct or CIType.get_by(alias=key, first=True, to_dict=False)
            if ct is not None:
                cls.set(ct)

        return ct

    @classmethod
    def set(cls, ct):
        cache.set(cls.PREFIX_NAME.format(ct.name), ct)
        cache.set(cls.PREFIX_ID.format(ct.id), ct)
        cache.set(cls.PREFIX_ALIAS.format(ct.alias), ct)

    @classmethod
    def clean(cls, key):
        ct = cls.get(key)
        if ct is not None:
            cache.delete(cls.PREFIX_NAME.format(ct.name))
            cache.delete(cls.PREFIX_ID.format(ct.id))
            cache.delete(cls.PREFIX_ALIAS.format(ct.alias))


class RelationTypeCache(object):
    PREFIX_ID = "RelationType::ID::{0}"
    PREFIX_NAME = "RelationType::Name::{0}"

    @classmethod
    def get(cls, key):
        if key is None:
            return
        ct = cache.get(cls.PREFIX_NAME.format(key))
        ct = ct or cache.get(cls.PREFIX_ID.format(key))
        if ct is None:
            ct = RelationType.get_by(name=key, first=True, to_dict=False) or RelationType.get_by_id(key)
            if ct is not None:
                cls.set(ct)

        return ct

    @classmethod
    def set(cls, ct):
        cache.set(cls.PREFIX_NAME.format(ct.name), ct)
        cache.set(cls.PREFIX_ID.format(ct.id), ct)

    @classmethod
    def clean(cls, key):
        ct = cls.get(key)
        if ct is not None:
            cache.delete(cls.PREFIX_NAME.format(ct.name))
            cache.delete(cls.PREFIX_ID.format(ct.id))


class CITypeAttributesCache(object):
    """
    key is type_id or type_name
    """

    PREFIX_ID = "CITypeAttributes::TypeID::{0}"
    PREFIX_NAME = "CITypeAttributes::TypeName::{0}"

    PREFIX_ID2 = "CITypeAttributes2::TypeID::{0}"
    PREFIX_NAME2 = "CITypeAttributes2::TypeName::{0}"

    @classmethod
    def get(cls, key):
        if key is None:
            return

        attrs = cache.get(cls.PREFIX_NAME.format(key))
        attrs = attrs or cache.get(cls.PREFIX_ID.format(key))
        if not attrs:
            attrs = CITypeAttribute.get_by(type_id=key, to_dict=False)

            if not attrs:
                ci_type = CIType.get_by(name=key, first=True, to_dict=False)
                if ci_type is not None:
                    attrs = CITypeAttribute.get_by(type_id=ci_type.id, to_dict=False)

            if attrs is not None:
                cls.set(key, attrs)

        return attrs

    @classmethod
    def get2(cls, key):
        """
        return [(type_attr, attr), ]
        :param key:
        :return:
        """
        if key is None:
            return

        attrs = cache.get(cls.PREFIX_NAME2.format(key))
        attrs = attrs or cache.get(cls.PREFIX_ID2.format(key))
        if not attrs:
            attrs = CITypeAttribute.get_by(type_id=key, to_dict=False)

            if not attrs:
                ci_type = CIType.get_by(name=key, first=True, to_dict=False)
                if ci_type is not None:
                    attrs = CITypeAttribute.get_by(type_id=ci_type.id, to_dict=False)

            if attrs is not None:
                attrs = [(i, AttributeCache.get(i.attr_id)) for i in attrs]
                cls.set2(key, attrs)

        return attrs

    @classmethod
    def set(cls, key, values):
        ci_type = CITypeCache.get(key)
        if ci_type is not None:
            cache.set(cls.PREFIX_ID.format(ci_type.id), values)
            cache.set(cls.PREFIX_NAME.format(ci_type.name), values)

    @classmethod
    def set2(cls, key, values):
        ci_type = CITypeCache.get(key)
        if ci_type is not None:
            cache.set(cls.PREFIX_ID2.format(ci_type.id), values)
            cache.set(cls.PREFIX_NAME2.format(ci_type.name), values)

    @classmethod
    def clean(cls, key):
        ci_type = CITypeCache.get(key)
        attrs = cls.get(key)
        if attrs is not None and ci_type:
            cache.delete(cls.PREFIX_ID.format(ci_type.id))
            cache.delete(cls.PREFIX_NAME.format(ci_type.name))

        attrs2 = cls.get2(key)
        if attrs2 is not None and ci_type:
            cache.delete(cls.PREFIX_ID2.format(ci_type.id))
            cache.delete(cls.PREFIX_NAME2.format(ci_type.name))


class CITypeAttributeCache(object):
    """
    key is type_id  & attr_id
    """

    PREFIX_ID = "CITypeAttribute::TypeID::{0}::AttrID::{1}"

    @classmethod
    def get(cls, type_id, attr_id):
        attr = cache.get(cls.PREFIX_ID.format(type_id, attr_id))
        attr = attr or cache.get(cls.PREFIX_ID.format(type_id, attr_id))
        attr = attr or CITypeAttribute.get_by(type_id=type_id, attr_id=attr_id, first=True, to_dict=False)

        if attr is not None:
            cls.set(type_id, attr_id, attr)

        return attr

    @classmethod
    def set(cls, type_id, attr_id, attr):
        cache.set(cls.PREFIX_ID.format(type_id, attr_id), attr)

    @classmethod
    def clean(cls, type_id, attr_id):
        cache.delete(cls.PREFIX_ID.format(type_id, attr_id))


class CMDBCounterCache(object):
    KEY = 'CMDB::Counter::dashboard'
    KEY2 = 'CMDB::Counter::adc'
    KEY3 = 'CMDB::Counter::sub'

    @classmethod
    def get(cls):
        result = cache.get(cls.KEY) or {}

        if not result:
            result = cls.reset()

        return result

    @classmethod
    def set(cls, result):
        cache.set(cls.KEY, json.loads(json.dumps(result)), timeout=0)

    @classmethod
    def reset(cls):
        customs = CustomDashboardManager.get()
        result = {}
        for custom in customs:
            if custom['category'] == 0:
                res = cls.sum_counter(custom)
            elif custom['category'] == 1:
                res = cls.attribute_counter(custom)
            else:
                res = cls.relation_counter(custom.get('type_id'),
                                           custom.get('level'),
                                           custom.get('options', {}).get('filter', ''),
                                           custom.get('options', {}).get('type_ids', ''))

            if res:
                result[custom['id']] = res

        cls.set(result)

        return json.loads(json.dumps(result))

    @classmethod
    def update(cls, custom, flush=True):
        result = cache.get(cls.KEY) or {}
        if not result:
            result = cls.reset()

        if custom['category'] == 0:
            res = cls.sum_counter(custom)
        elif custom['category'] == 1:
            res = cls.attribute_counter(custom)
        else:
            res = cls.relation_counter(custom.get('type_id'),
                                       custom.get('level'),
                                       custom.get('options', {}).get('filter', ''),
                                       custom.get('options', {}).get('type_ids', ''))

        if res and flush:
            result[custom['id']] = res
            cls.set(result)

        return json.loads(json.dumps(res))

    @classmethod
    def relation_counter(cls, type_id, level, other_filer, type_ids):
        from api.lib.cmdb.search.ci_relation.search import Search as RelSearch
        from api.lib.cmdb.search import SearchError
        from api.lib.cmdb.search.ci import search
        from api.lib.cmdb.attribute import AttributeManager

        query = "_type:{}".format(type_id)
        if other_filer:
            query = "{},{}".format(query, other_filer)
        s = search(query, count=1000000)
        try:
            type_names, _, _, _, _, _ = s.search()
        except SearchError as e:
            current_app.logger.error(e)
            return
        root_type = CITypeCache.get(type_id)
        show_attr_id = root_type and root_type.show_id
        show_attr = AttributeCache.get(show_attr_id)

        type_id_names = []
        for i in type_names:
            attr_value = i.get(show_attr and show_attr.name) or i.get(i.get('unique'))
            enum_map = AttributeManager.get_enum_map(show_attr_id or i.get('unique'))

            type_id_names.append((str(i.get('_id')), enum_map.get(attr_value, attr_value)))

        s = RelSearch([i[0] for i in type_id_names], level)
        try:
            stats = s.statistics(type_ids, need_filter=False)
        except SearchError as e:
            current_app.logger.error(e)
            return

        id2name = dict(type_id_names)
        type_ids = set()
        for i in (stats.get('detail') or []):
            for j in stats['detail'][i]:
                type_ids.add(j)
        for type_id in type_ids:
            _type = CITypeCache.get(type_id)
            id2name[type_id] = _type and _type.alias

        result = dict(summary={}, detail={})
        for i in stats:
            if i == "detail":
                for j in stats['detail']:
                    if id2name[j]:
                        result['detail'][id2name[j]] = stats['detail'][j]
                        result['detail'][id2name[j]] = dict()
                        for _j in stats['detail'][j]:
                            result['detail'][id2name[j]][id2name[_j]] = stats['detail'][j][_j]
            elif id2name.get(i):
                result['summary'][id2name[i]] = stats[i]

        return result

    @classmethod
    def attribute_counter(cls, custom):
        from api.lib.cmdb.search import SearchError
        from api.lib.cmdb.search.ci import search
        from api.lib.cmdb.utils import ValueTypeMap
        from api.lib.cmdb.attribute import AttributeManager

        custom.setdefault('options', {})
        type_id = custom.get('type_id')
        attr_id = custom.get('attr_id')
        type_ids = custom['options'].get('type_ids') or (type_id and [type_id])
        attr_ids = list(map(str, custom['options'].get('attr_ids') or (attr_id and [attr_id])))
        try:
            attr2value_type = [AttributeCache.get(i).value_type for i in attr_ids]
        except AttributeError:
            return

        other_filter = custom['options'].get('filter')
        other_filter = "{}".format(other_filter) if other_filter else ''

        if custom['options'].get('ret') == 'cis':
            enum_map = {}
            for _attr_id in attr_ids:
                _attr = AttributeCache.get(_attr_id)
                if _attr:
                    enum_map[_attr.alias] = AttributeManager.get_enum_map(_attr_id)

            query = "_type:({}),{}".format(";".join(map(str, type_ids)), other_filter)
            s = search(query, fl=attr_ids, ret_key='alias', count=100)
            try:
                cis, _, _, _, _, _ = s.search()
                cis = [{k: (enum_map.get(k) or {}).get(v, v) for k, v in ci.items()} for ci in cis]
            except SearchError as e:
                current_app.logger.error(e)
                return

            return cis

        origin_result = dict()
        result = dict()
        # level = 1
        query = "_type:({}),{}".format(";".join(map(str, type_ids)), other_filter)
        s = search(query, fl=attr_ids, facet=[attr_ids[0]], count=1)
        try:
            _, _, _, _, _, facet = s.search()
        except SearchError as e:
            current_app.logger.error(e)
            return

        enum_map1 = AttributeManager.get_enum_map(attr_ids[0])
        for i in (list(facet.values()) or [[]])[0]:
            k = ValueTypeMap.serialize2[attr2value_type[0]](str(i[0]))
            result[enum_map1.get(k, k)] = i[1]
            origin_result[k] = i[1]
        if len(attr_ids) == 1:
            return result

        # level = 2
        enum_map2 = AttributeManager.get_enum_map(attr_ids[1])
        for v in origin_result:
            query = "_type:({}),{},{}:{}".format(";".join(map(str, type_ids)), other_filter, attr_ids[0], v)
            s = search(query, fl=attr_ids, facet=[attr_ids[1]], count=1)
            try:
                _, _, _, _, _, facet = s.search()
            except SearchError as e:
                current_app.logger.error(e)
                return
            result[enum_map1.get(v, v)] = dict()
            origin_result[v] = dict()
            for i in (list(facet.values()) or [[]])[0]:
                k = ValueTypeMap.serialize2[attr2value_type[1]](str(i[0]))
                result[enum_map1.get(v, v)][enum_map2.get(k, k)] = i[1]
                origin_result[v][k] = i[1]

        if len(attr_ids) == 2:
            return result

        # level = 3
        enum_map3 = AttributeManager.get_enum_map(attr_ids[2])
        for v1 in origin_result:
            if not isinstance(result[enum_map1.get(v1, v1)], dict):
                continue
            for v2 in origin_result[v1]:
                query = "_type:({}),{},{}:{},{}:{}".format(";".join(map(str, type_ids)), other_filter,
                                                           attr_ids[0], v1, attr_ids[1], v2)
                s = search(query, fl=attr_ids, facet=[attr_ids[2]], count=1)
                try:
                    _, _, _, _, _, facet = s.search()
                except SearchError as e:
                    current_app.logger.error(e)
                    return
                result[enum_map1.get(v1, v1)][enum_map2.get(v2, v2)] = dict()
                for i in (list(facet.values()) or [[]])[0]:
                    k = ValueTypeMap.serialize2[attr2value_type[2]](str(i[0]))
                    result[enum_map1.get(v1, v1)][enum_map2.get(v2, v2)][enum_map3.get(k, k)] = i[1]

        return result

    @staticmethod
    def sum_counter(custom):
        from api.lib.cmdb.search import SearchError
        from api.lib.cmdb.search.ci import search

        custom.setdefault('options', {})
        type_id = custom.get('type_id')
        type_ids = custom['options'].get('type_ids') or (type_id and [type_id])
        other_filter = custom['options'].get('filter') or ''

        query = "_type:({}),{}".format(";".join(map(str, type_ids)), other_filter)
        s = search(query, count=1)
        try:
            _, _, _, _, numfound, _ = s.search()
        except SearchError as e:
            current_app.logger.error(e)
            return

        return numfound

    @classmethod
    def flush_adc_counter(cls):
        res = db.session.query(CI.type_id, CI.is_auto_discovery)
        result = dict()
        for i in res:
            result.setdefault(i.type_id, dict(total=0, auto_discovery=0))
            result[i.type_id]['total'] += 1
            if i.is_auto_discovery:
                result[i.type_id]['auto_discovery'] += 1

        cache.set(cls.KEY2, result, timeout=0)

        res = db.session.query(AutoDiscoveryCI.created_at,
                               AutoDiscoveryCI.updated_at,
                               AutoDiscoveryCI.adt_id,
                               AutoDiscoveryCI.type_id,
                               AutoDiscoveryCI.is_accept).filter(AutoDiscoveryCI.deleted.is_(False))

        today = datetime.datetime.today()
        this_month = datetime.datetime(today.year, today.month, 1)
        last_month = this_month - datetime.timedelta(days=1)
        last_month = datetime.datetime(last_month.year, last_month.month, 1)
        this_week = today - datetime.timedelta(days=datetime.date.weekday(today))
        this_week = datetime.datetime(this_week.year, this_week.month, this_week.day)
        last_week = this_week - datetime.timedelta(days=7)
        last_week = datetime.datetime(last_week.year, last_week.month, last_week.day)
        result = dict()
        for i in res:
            if i.type_id not in result:
                result[i.type_id] = dict(instance_count=0, accept_count=0,
                                         this_month_count=0, this_week_count=0, last_month_count=0, last_week_count=0)

                adts = AutoDiscoveryCIType.get_by(type_id=i.type_id, to_dict=False)
                result[i.type_id]['rule_count'] = len(adts) + AutoDiscoveryCITypeRelation.get_by(
                    ad_type_id=i.type_id, only_query=True).count()
                result[i.type_id]['exec_target_count'] = len(
                    set([j.oneagent_id for adt in adts for j in db.session.query(
                        AutoDiscoveryRuleSyncHistory.oneagent_id).filter(
                        AutoDiscoveryRuleSyncHistory.adt_id == adt.id)]))

            result[i.type_id]['instance_count'] += 1
            if i.is_accept:
                result[i.type_id]['accept_count'] += 1

            if last_month <= i.created_at < this_month:
                result[i.type_id]['last_month_count'] += 1
            elif i.created_at >= this_month:
                result[i.type_id]['this_month_count'] += 1

            if last_week <= i.created_at < this_week:
                result[i.type_id]['last_week_count'] += 1
            elif i.created_at >= this_week:
                result[i.type_id]['this_week_count'] += 1

        for type_id in result:
            existed = AutoDiscoveryCounter.get_by(type_id=type_id, first=True, to_dict=False)
            if existed is None:
                AutoDiscoveryCounter.create(type_id=type_id, **result[type_id])
            else:
                existed.update(**result[type_id])

        for i in AutoDiscoveryCounter.get_by(to_dict=False):
            if i.type_id not in result:
                i.delete()

    @classmethod
    def clear_ad_exec_history(cls):
        ci_types = CIType.get_by(to_dict=False)
        for ci_type in ci_types:
            for i in AutoDiscoveryExecHistory.get_by(type_id=ci_type.id, only_query=True).order_by(
                    AutoDiscoveryExecHistory.id.desc()).offset(50000):
                i.delete(commit=False)
            db.session.commit()

    @classmethod
    def get_adc_counter(cls):
        return cache.get(cls.KEY2) or cls.flush_adc_counter()

    @classmethod
    def flush_sub_counter(cls):
        result = dict(type_id2users=defaultdict(list))

        types = db.session.query(PreferenceShowAttributes.type_id,
                                 PreferenceShowAttributes.uid, 
                                 db.func.max(PreferenceShowAttributes.created_at).label('created_at')).filter(
            PreferenceShowAttributes.deleted.is_(False)).group_by(
            PreferenceShowAttributes.uid, PreferenceShowAttributes.type_id)
        for i in types:
            result['type_id2users'][i.type_id].append(i.uid)

        types = PreferenceTreeView.get_by(to_dict=False)
        for i in types:

            if i.uid not in result['type_id2users'][i.type_id]:
                result['type_id2users'][i.type_id].append(i.uid)

        cache.set(cls.KEY3, result, timeout=0)

        return result

    @classmethod
    def get_sub_counter(cls):
        return cache.get(cls.KEY3) or cls.flush_sub_counter()


class AutoDiscoveryMappingCache(object):
    PREFIX = 'CMDB::AutoDiscovery::Mapping::{}'

    @classmethod
    def get(cls, name):
        res = cache.get(cls.PREFIX.format(name)) or {}
        if not res:
            path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                "auto_discovery/mapping/{}.yaml".format(name))
            if os.path.exists(path):
                with open(path, 'r') as f:
                    mapping = yaml.safe_load(f)
                    res = mapping.get('mapping') or {}
                    res and cache.set(cls.PREFIX.format(name), res, timeout=0)

        return res
