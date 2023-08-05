# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: systemathics/apis/services/intraday/v1/intraday_vwap.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from systemathics.apis.type.shared.v1 import identifier_pb2 as systemathics_dot_apis_dot_type_dot_shared_dot_v1_dot_identifier__pb2
from systemathics.apis.type.shared.v1 import constraints_pb2 as systemathics_dot_apis_dot_type_dot_shared_dot_v1_dot_constraints__pb2
from systemathics.apis.type.shared.v1 import sampling_pb2 as systemathics_dot_apis_dot_type_dot_shared_dot_v1_dot_sampling__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='systemathics/apis/services/intraday/v1/intraday_vwap.proto',
  package='systemathics.apis.services.intraday.v1',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n:systemathics/apis/services/intraday/v1/intraday_vwap.proto\x12&systemathics.apis.services.intraday.v1\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\x31systemathics/apis/type/shared/v1/identifier.proto\x1a\x32systemathics/apis/type/shared/v1/constraints.proto\x1a/systemathics/apis/type/shared/v1/sampling.proto\"\xee\x01\n\x14IntradayVwapsRequest\x12@\n\nidentifier\x18\x01 \x01(\x0b\x32,.systemathics.apis.type.shared.v1.Identifier\x12<\n\x08sampling\x18\x02 \x01(\x0e\x32*.systemathics.apis.type.shared.v1.Sampling\x12\x42\n\x0b\x63onstraints\x18\x03 \x01(\x0b\x32-.systemathics.apis.type.shared.v1.Constraints\x12\x12\n\nadjustment\x18\x04 \x01(\x08\"[\n\x15IntradayVwapsResponse\x12\x42\n\x04\x64\x61ta\x18\x01 \x03(\x0b\x32\x34.systemathics.apis.services.intraday.v1.IntradayVwap\"l\n\x0cIntradayVwap\x12.\n\ntime_stamp\x18\x01 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\r\n\x05price\x18\x02 \x01(\x01\x12\x0e\n\x06volume\x18\x03 \x01(\x03\x12\r\n\x05score\x18\x04 \x01(\x01\x32\xa5\x01\n\x14IntradayVwapsService\x12\x8c\x01\n\rIntradayVwaps\x12<.systemathics.apis.services.intraday.v1.IntradayVwapsRequest\x1a=.systemathics.apis.services.intraday.v1.IntradayVwapsResponseb\x06proto3'
  ,
  dependencies=[google_dot_protobuf_dot_timestamp__pb2.DESCRIPTOR,systemathics_dot_apis_dot_type_dot_shared_dot_v1_dot_identifier__pb2.DESCRIPTOR,systemathics_dot_apis_dot_type_dot_shared_dot_v1_dot_constraints__pb2.DESCRIPTOR,systemathics_dot_apis_dot_type_dot_shared_dot_v1_dot_sampling__pb2.DESCRIPTOR,])




_INTRADAYVWAPSREQUEST = _descriptor.Descriptor(
  name='IntradayVwapsRequest',
  full_name='systemathics.apis.services.intraday.v1.IntradayVwapsRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='identifier', full_name='systemathics.apis.services.intraday.v1.IntradayVwapsRequest.identifier', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='sampling', full_name='systemathics.apis.services.intraday.v1.IntradayVwapsRequest.sampling', index=1,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='constraints', full_name='systemathics.apis.services.intraday.v1.IntradayVwapsRequest.constraints', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='adjustment', full_name='systemathics.apis.services.intraday.v1.IntradayVwapsRequest.adjustment', index=3,
      number=4, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
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
  serialized_start=288,
  serialized_end=526,
)


_INTRADAYVWAPSRESPONSE = _descriptor.Descriptor(
  name='IntradayVwapsResponse',
  full_name='systemathics.apis.services.intraday.v1.IntradayVwapsResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='data', full_name='systemathics.apis.services.intraday.v1.IntradayVwapsResponse.data', index=0,
      number=1, type=11, cpp_type=10, label=3,
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
  serialized_start=528,
  serialized_end=619,
)


_INTRADAYVWAP = _descriptor.Descriptor(
  name='IntradayVwap',
  full_name='systemathics.apis.services.intraday.v1.IntradayVwap',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='time_stamp', full_name='systemathics.apis.services.intraday.v1.IntradayVwap.time_stamp', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='price', full_name='systemathics.apis.services.intraday.v1.IntradayVwap.price', index=1,
      number=2, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='volume', full_name='systemathics.apis.services.intraday.v1.IntradayVwap.volume', index=2,
      number=3, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='score', full_name='systemathics.apis.services.intraday.v1.IntradayVwap.score', index=3,
      number=4, type=1, cpp_type=5, label=1,
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
  serialized_start=621,
  serialized_end=729,
)

_INTRADAYVWAPSREQUEST.fields_by_name['identifier'].message_type = systemathics_dot_apis_dot_type_dot_shared_dot_v1_dot_identifier__pb2._IDENTIFIER
_INTRADAYVWAPSREQUEST.fields_by_name['sampling'].enum_type = systemathics_dot_apis_dot_type_dot_shared_dot_v1_dot_sampling__pb2._SAMPLING
_INTRADAYVWAPSREQUEST.fields_by_name['constraints'].message_type = systemathics_dot_apis_dot_type_dot_shared_dot_v1_dot_constraints__pb2._CONSTRAINTS
_INTRADAYVWAPSRESPONSE.fields_by_name['data'].message_type = _INTRADAYVWAP
_INTRADAYVWAP.fields_by_name['time_stamp'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
DESCRIPTOR.message_types_by_name['IntradayVwapsRequest'] = _INTRADAYVWAPSREQUEST
DESCRIPTOR.message_types_by_name['IntradayVwapsResponse'] = _INTRADAYVWAPSRESPONSE
DESCRIPTOR.message_types_by_name['IntradayVwap'] = _INTRADAYVWAP
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

IntradayVwapsRequest = _reflection.GeneratedProtocolMessageType('IntradayVwapsRequest', (_message.Message,), {
  'DESCRIPTOR' : _INTRADAYVWAPSREQUEST,
  '__module__' : 'systemathics.apis.services.intraday.v1.intraday_vwap_pb2'
  # @@protoc_insertion_point(class_scope:systemathics.apis.services.intraday.v1.IntradayVwapsRequest)
  })
_sym_db.RegisterMessage(IntradayVwapsRequest)

IntradayVwapsResponse = _reflection.GeneratedProtocolMessageType('IntradayVwapsResponse', (_message.Message,), {
  'DESCRIPTOR' : _INTRADAYVWAPSRESPONSE,
  '__module__' : 'systemathics.apis.services.intraday.v1.intraday_vwap_pb2'
  # @@protoc_insertion_point(class_scope:systemathics.apis.services.intraday.v1.IntradayVwapsResponse)
  })
_sym_db.RegisterMessage(IntradayVwapsResponse)

IntradayVwap = _reflection.GeneratedProtocolMessageType('IntradayVwap', (_message.Message,), {
  'DESCRIPTOR' : _INTRADAYVWAP,
  '__module__' : 'systemathics.apis.services.intraday.v1.intraday_vwap_pb2'
  # @@protoc_insertion_point(class_scope:systemathics.apis.services.intraday.v1.IntradayVwap)
  })
_sym_db.RegisterMessage(IntradayVwap)



_INTRADAYVWAPSSERVICE = _descriptor.ServiceDescriptor(
  name='IntradayVwapsService',
  full_name='systemathics.apis.services.intraday.v1.IntradayVwapsService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=732,
  serialized_end=897,
  methods=[
  _descriptor.MethodDescriptor(
    name='IntradayVwaps',
    full_name='systemathics.apis.services.intraday.v1.IntradayVwapsService.IntradayVwaps',
    index=0,
    containing_service=None,
    input_type=_INTRADAYVWAPSREQUEST,
    output_type=_INTRADAYVWAPSRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_INTRADAYVWAPSSERVICE)

DESCRIPTOR.services_by_name['IntradayVwapsService'] = _INTRADAYVWAPSSERVICE

# @@protoc_insertion_point(module_scope)
