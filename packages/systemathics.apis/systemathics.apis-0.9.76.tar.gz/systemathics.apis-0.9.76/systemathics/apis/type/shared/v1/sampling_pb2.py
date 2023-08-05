# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: systemathics/apis/type/shared/v1/sampling.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='systemathics/apis/type/shared/v1/sampling.proto',
  package='systemathics.apis.type.shared.v1',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n/systemathics/apis/type/shared/v1/sampling.proto\x12 systemathics.apis.type.shared.v1*\xa6\x01\n\x08Sampling\x12\x17\n\x13SAMPLING_ONE_MINUTE\x10\x00\x12\x18\n\x14SAMPLING_FIVE_MINUTE\x10\x01\x12\x17\n\x13SAMPLING_TEN_MINUTE\x10\x02\x12\x1b\n\x17SAMPLING_FIFTEEN_MINUTE\x10\x03\x12\x1a\n\x16SAMPLING_THIRTY_MINUTE\x10\x04\x12\x15\n\x11SAMPLING_ONE_HOUR\x10\x05\x62\x06proto3'
)

_SAMPLING = _descriptor.EnumDescriptor(
  name='Sampling',
  full_name='systemathics.apis.type.shared.v1.Sampling',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='SAMPLING_ONE_MINUTE', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='SAMPLING_FIVE_MINUTE', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='SAMPLING_TEN_MINUTE', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='SAMPLING_FIFTEEN_MINUTE', index=3, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='SAMPLING_THIRTY_MINUTE', index=4, number=4,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='SAMPLING_ONE_HOUR', index=5, number=5,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=86,
  serialized_end=252,
)
_sym_db.RegisterEnumDescriptor(_SAMPLING)

Sampling = enum_type_wrapper.EnumTypeWrapper(_SAMPLING)
SAMPLING_ONE_MINUTE = 0
SAMPLING_FIVE_MINUTE = 1
SAMPLING_TEN_MINUTE = 2
SAMPLING_FIFTEEN_MINUTE = 3
SAMPLING_THIRTY_MINUTE = 4
SAMPLING_ONE_HOUR = 5


DESCRIPTOR.enum_types_by_name['Sampling'] = _SAMPLING
_sym_db.RegisterFileDescriptor(DESCRIPTOR)


# @@protoc_insertion_point(module_scope)
