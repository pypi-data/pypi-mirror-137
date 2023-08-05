# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: systemathics/apis/services/tick_analytics/v1/tick_bars.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from google.protobuf import duration_pb2 as google_dot_protobuf_dot_duration__pb2
from systemathics.apis.type.shared.v1 import constraints_pb2 as systemathics_dot_apis_dot_type_dot_shared_dot_v1_dot_constraints__pb2
from systemathics.apis.type.shared.v1 import identifier_pb2 as systemathics_dot_apis_dot_type_dot_shared_dot_v1_dot_identifier__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='systemathics/apis/services/tick_analytics/v1/tick_bars.proto',
  package='systemathics.apis.services.tick_analytics.v1',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n<systemathics/apis/services/tick_analytics/v1/tick_bars.proto\x12,systemathics.apis.services.tick_analytics.v1\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\x1egoogle/protobuf/duration.proto\x1a\x32systemathics/apis/type/shared/v1/constraints.proto\x1a\x31systemathics/apis/type/shared/v1/identifier.proto\"\x95\x03\n\x0fTickBarsRequest\x12@\n\nidentifier\x18\x01 \x01(\x0b\x32,.systemathics.apis.type.shared.v1.Identifier\x12\x42\n\x0b\x63onstraints\x18\x02 \x01(\x0b\x32-.systemathics.apis.type.shared.v1.Constraints\x12\x45\n\x05\x66ield\x18\x03 \x01(\x0e\x32\x36.systemathics.apis.services.tick_analytics.v1.BarPrice\x12+\n\x08sampling\x18\x04 \x01(\x0b\x32\x19.google.protobuf.Duration\x12)\n\x06period\x18\x05 \x01(\x0b\x32\x19.google.protobuf.Duration\x12)\n\x06offset\x18\x06 \x01(\x0b\x32\x19.google.protobuf.Duration\x12\x12\n\nadjustment\x18\x07 \x01(\x08\x12\x0e\n\x06\x61\x63\x63\x65pt\x18\x08 \x03(\t\x12\x0e\n\x06reject\x18\t \x03(\t\"\xa7\x01\n\x10TickBarsResponse\x12.\n\ntime_stamp\x18\x01 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x0c\n\x04open\x18\x02 \x01(\x01\x12\x0c\n\x04high\x18\x03 \x01(\x01\x12\x0b\n\x03low\x18\x04 \x01(\x01\x12\r\n\x05\x63lose\x18\x05 \x01(\x01\x12\x0e\n\x06volume\x18\x06 \x01(\x03\x12\r\n\x05\x63ount\x18\x07 \x01(\x05\x12\x0c\n\x04vwap\x18\x08 \x01(\x01*`\n\x08\x42\x61rPrice\x12\x19\n\x15\x42\x41R_PRICE_UNSPECIFIED\x10\x00\x12\x13\n\x0f\x42\x41R_PRICE_TRADE\x10\x01\x12\x11\n\rBAR_PRICE_BID\x10\x02\x12\x11\n\rBAR_PRICE_ASK\x10\x03\x32\x9f\x01\n\x0fTickBarsService\x12\x8b\x01\n\x08TickBars\x12=.systemathics.apis.services.tick_analytics.v1.TickBarsRequest\x1a>.systemathics.apis.services.tick_analytics.v1.TickBarsResponse0\x01\x62\x06proto3'
  ,
  dependencies=[google_dot_protobuf_dot_timestamp__pb2.DESCRIPTOR,google_dot_protobuf_dot_duration__pb2.DESCRIPTOR,systemathics_dot_apis_dot_type_dot_shared_dot_v1_dot_constraints__pb2.DESCRIPTOR,systemathics_dot_apis_dot_type_dot_shared_dot_v1_dot_identifier__pb2.DESCRIPTOR,])

_BARPRICE = _descriptor.EnumDescriptor(
  name='BarPrice',
  full_name='systemathics.apis.services.tick_analytics.v1.BarPrice',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='BAR_PRICE_UNSPECIFIED', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='BAR_PRICE_TRADE', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='BAR_PRICE_BID', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='BAR_PRICE_ASK', index=3, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=856,
  serialized_end=952,
)
_sym_db.RegisterEnumDescriptor(_BARPRICE)

BarPrice = enum_type_wrapper.EnumTypeWrapper(_BARPRICE)
BAR_PRICE_UNSPECIFIED = 0
BAR_PRICE_TRADE = 1
BAR_PRICE_BID = 2
BAR_PRICE_ASK = 3



_TICKBARSREQUEST = _descriptor.Descriptor(
  name='TickBarsRequest',
  full_name='systemathics.apis.services.tick_analytics.v1.TickBarsRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='identifier', full_name='systemathics.apis.services.tick_analytics.v1.TickBarsRequest.identifier', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='constraints', full_name='systemathics.apis.services.tick_analytics.v1.TickBarsRequest.constraints', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='field', full_name='systemathics.apis.services.tick_analytics.v1.TickBarsRequest.field', index=2,
      number=3, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='sampling', full_name='systemathics.apis.services.tick_analytics.v1.TickBarsRequest.sampling', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='period', full_name='systemathics.apis.services.tick_analytics.v1.TickBarsRequest.period', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='offset', full_name='systemathics.apis.services.tick_analytics.v1.TickBarsRequest.offset', index=5,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='adjustment', full_name='systemathics.apis.services.tick_analytics.v1.TickBarsRequest.adjustment', index=6,
      number=7, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='accept', full_name='systemathics.apis.services.tick_analytics.v1.TickBarsRequest.accept', index=7,
      number=8, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='reject', full_name='systemathics.apis.services.tick_analytics.v1.TickBarsRequest.reject', index=8,
      number=9, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=279,
  serialized_end=684,
)


_TICKBARSRESPONSE = _descriptor.Descriptor(
  name='TickBarsResponse',
  full_name='systemathics.apis.services.tick_analytics.v1.TickBarsResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='time_stamp', full_name='systemathics.apis.services.tick_analytics.v1.TickBarsResponse.time_stamp', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='open', full_name='systemathics.apis.services.tick_analytics.v1.TickBarsResponse.open', index=1,
      number=2, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='high', full_name='systemathics.apis.services.tick_analytics.v1.TickBarsResponse.high', index=2,
      number=3, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='low', full_name='systemathics.apis.services.tick_analytics.v1.TickBarsResponse.low', index=3,
      number=4, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='close', full_name='systemathics.apis.services.tick_analytics.v1.TickBarsResponse.close', index=4,
      number=5, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='volume', full_name='systemathics.apis.services.tick_analytics.v1.TickBarsResponse.volume', index=5,
      number=6, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='count', full_name='systemathics.apis.services.tick_analytics.v1.TickBarsResponse.count', index=6,
      number=7, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='vwap', full_name='systemathics.apis.services.tick_analytics.v1.TickBarsResponse.vwap', index=7,
      number=8, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=687,
  serialized_end=854,
)

_TICKBARSREQUEST.fields_by_name['identifier'].message_type = systemathics_dot_apis_dot_type_dot_shared_dot_v1_dot_identifier__pb2._IDENTIFIER
_TICKBARSREQUEST.fields_by_name['constraints'].message_type = systemathics_dot_apis_dot_type_dot_shared_dot_v1_dot_constraints__pb2._CONSTRAINTS
_TICKBARSREQUEST.fields_by_name['field'].enum_type = _BARPRICE
_TICKBARSREQUEST.fields_by_name['sampling'].message_type = google_dot_protobuf_dot_duration__pb2._DURATION
_TICKBARSREQUEST.fields_by_name['period'].message_type = google_dot_protobuf_dot_duration__pb2._DURATION
_TICKBARSREQUEST.fields_by_name['offset'].message_type = google_dot_protobuf_dot_duration__pb2._DURATION
_TICKBARSRESPONSE.fields_by_name['time_stamp'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
DESCRIPTOR.message_types_by_name['TickBarsRequest'] = _TICKBARSREQUEST
DESCRIPTOR.message_types_by_name['TickBarsResponse'] = _TICKBARSRESPONSE
DESCRIPTOR.enum_types_by_name['BarPrice'] = _BARPRICE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

TickBarsRequest = _reflection.GeneratedProtocolMessageType('TickBarsRequest', (_message.Message,), {
  'DESCRIPTOR' : _TICKBARSREQUEST,
  '__module__' : 'systemathics.apis.services.tick_analytics.v1.tick_bars_pb2'
  # @@protoc_insertion_point(class_scope:systemathics.apis.services.tick_analytics.v1.TickBarsRequest)
  })
_sym_db.RegisterMessage(TickBarsRequest)

TickBarsResponse = _reflection.GeneratedProtocolMessageType('TickBarsResponse', (_message.Message,), {
  'DESCRIPTOR' : _TICKBARSRESPONSE,
  '__module__' : 'systemathics.apis.services.tick_analytics.v1.tick_bars_pb2'
  # @@protoc_insertion_point(class_scope:systemathics.apis.services.tick_analytics.v1.TickBarsResponse)
  })
_sym_db.RegisterMessage(TickBarsResponse)



_TICKBARSSERVICE = _descriptor.ServiceDescriptor(
  name='TickBarsService',
  full_name='systemathics.apis.services.tick_analytics.v1.TickBarsService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=955,
  serialized_end=1114,
  methods=[
  _descriptor.MethodDescriptor(
    name='TickBars',
    full_name='systemathics.apis.services.tick_analytics.v1.TickBarsService.TickBars',
    index=0,
    containing_service=None,
    input_type=_TICKBARSREQUEST,
    output_type=_TICKBARSRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_TICKBARSSERVICE)

DESCRIPTOR.services_by_name['TickBarsService'] = _TICKBARSSERVICE

# @@protoc_insertion_point(module_scope)
