# -*- encoding: utf-8 -*-
from rest_framework import serializers

from django.core.exceptions import ValidationError
from rest_framework.validators import UniqueValidator
from rest_framework.utils.serializer_helpers import *
from rest_framework.relations import PKOnlyObject
from rest_framework.fields import SkipField

from django.db import models


class NormalizedListSerializer(serializers.ListSerializer):
    def __init__(self, *args, **kwargs):
        super(NormalizedListSerializer, self).__init__(*args, **kwargs)
        self.instancelist_dict = {}
        self.instance_repr_dict = {}

    def make_normalized_item_list(self, normalized_item):
        ret = []
        for item in self.instancelist_dict[normalized_item]:
            normalized_item_dict = OrderedDict()
            fields = self.instance_repr_dict[normalized_item]
            for field in fields:
                try:
                    attribute = field.get_attribute(item)
                except SkipField:
                    continue
                check_for_none = attribute.pk if isinstance(attribute, PKOnlyObject) else attribute
                if check_for_none is None:
                    normalized_item_dict[field.field_name] = None
                else:
                    normalized_item_dict[field.field_name] = field.to_representation(attribute)
            ret.append(normalized_item_dict)
        return ret

    def to_representation(self, data):
        """
        List of object instances -> List of dicts of primitive datatypes.
        """
        # Dealing with nested relationships, data can be a Manager,
        # so, first get a queryset from the Manager if needed

        iterable = data.all() if isinstance(data, models.Manager) else data
            

        if self.parent is None:
            post = [
                self.child.to_representation(item) for item in iterable
            ]
            normalized_dict = OrderedDict()
            normalized_dict[self.child.Meta.model_name] = ReturnList(post, serializer=self)
            result = [normalized_dict]
            for normalized_item in self.child.Meta.normalized_fields:
                if normalized_item in self.instancelist_dict:
                    normalized_dict[normalized_item] = \
                            ReturnList(self.make_normalized_item_list(normalized_item), serializer=self)
            return result

        if self.field_name in self.child.Meta.normalized_fields:
            result = [ item.id for item in iterable ]
            parent = self.root
            if not self.field_name in parent.instancelist_dict:
                parent.instancelist_dict[self.field_name] = []
                parent.instance_repr_dict[self.field_name] = self.child._readable_fields
            parent.instancelist_dict[self.field_name] = \
                    list(set(parent.instancelist_dict[self.field_name]) | set(iterable))
        else:
            result = [
                self.child.to_representation(item) for item in iterable
            ]

        return result

    @property
    def data(self):
        ret = super(NormalizedListSerializer, self).data
        # TODO : fixme
        return ReturnDict(ret[0], serializer=self)


class NormalizedSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        super(NormalizedSerializer, self).__init__(*args, **kwargs)
        self.instancelist_dict = {}
        self.instance_repr_dict = {}
        self.list_serializer_class = NormalizedListSerializer
        self.test = []

    def make_normalized_item(self, instance, fields):
        ret = OrderedDict()
        for field in fields:
            try:
                attribute = field.get_attribute(instance)
            except SkipField:
                continue
            check_for_none = attribute.pk if isinstance(attribute, PKOnlyObject) else attribute
            if check_for_none is None:
                ret[field.field_name] = None
            else:
                ret[field.field_name] = field.to_representation(attribute)
        return ret

    def to_representation(self, instance):
        """
        Object instance -> Dict of primitive datatypes.
        """
        ret = OrderedDict()
        fields = self._readable_fields
        

        if self.parent is None:
            normalized_dict = OrderedDict()
            normalized_dict[self.Meta.model_name] = \
                    ReturnList([self.make_normalized_item(instance, fields)], serializer=self)
            for normalized_item in self.Meta.normalized_fields:
                if normalized_item in self.instancelist_dict:
                    normalized_item_list = []
                    for item in self.instancelist_dict[normalized_item]:
                        item_fields = self.instance_repr_dict[normalized_item]
                        normalized_item_list.append(self.make_normalized_item(item, item_fields))
                    normalized_dict[normalized_item] = \
                            ReturnList(normalized_item_list, serializer=self)
            return normalized_dict

        if self.field_name in self.Meta.normalized_fields:
            parent = self.root
            if not self.field_name in parent.instancelist_dict:
                parent.instancelist_dict[self.field_name] = []
                parent.instance_repr_dict[self.field_name] = self._readable_fields
            if not instance in  parent.instancelist_dict[self.field_name]:
                 parent.instancelist_dict[self.field_name].append(instance)
            return instance.id

        return self.make_normalized_item(instance, fields)

    @property
    def data(self):
        ret = super(NormalizedSerializer, self).data
        return ReturnDict(ret, serializer=self)

    def __getitem__(self, key):
        field = self.fields[key]
        value = self.data.get(key)
        error = self.errors.get(key) if hasattr(self, '_errors') else None
        if isinstance(field, NormalizedSerializer):
            if isinstance(value, ReturnList):
                values = { field.field_name : NestedBoundField(field, value, error) }
                return NestedBoundField(field, values, error)
            return NestedBoundField(field, value, error)
            """
            if isinstance(value, ReturnList):
                values = [
                        NestedBoundField(field, item, error) for item in value
                    ]
                values = ReturnList(values, serializer=self)
                values = { field.field_name : values }
                return NestedBoundField(field, values, error)
            return NestedBoundField(field, value, error)
            """
        return BoundField(field, value, error)

