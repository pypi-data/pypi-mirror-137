# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: systemathics/apis/services/static_data/v1/static_sector.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='systemathics/apis/services/static_data/v1/static_sector.proto',
  package='systemathics.apis.services.static_data.v1',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n=systemathics/apis/services/static_data/v1/static_sector.proto\x12)systemathics.apis.services.static_data.v1\"Q\n\x13StaticSectorRequest\x12\x10\n\x08provider\x18\x01 \x01(\t\x12\x0e\n\x04\x63ode\x18\x02 \x01(\tH\x00\x12\x0f\n\x05level\x18\x03 \x01(\x05H\x00\x42\x07\n\x05value\"z\n\x14StaticSectorResponse\x12>\n\x04\x64\x61ta\x18\x01 \x03(\x0b\x32\x30.systemathics.apis.services.static_data.v1.Level\x12\x13\n\x0b\x64\x65scription\x18\x02 \x01(\t\x12\r\n\x05\x63ount\x18\x03 \x01(\x05\"U\n\x05Level\x12\x0c\n\x04Name\x18\x01 \x01(\t\x12\r\n\x05Index\x18\x02 \x01(\x05\x12\x0c\n\x04\x43ode\x18\x03 \x01(\t\x12\x12\n\ndefinition\x18\x04 \x01(\t\x12\r\n\x05label\x18\x05 \x01(\t2\xa7\x01\n\x13StaticSectorService\x12\x8f\x01\n\x0cStaticSector\x12>.systemathics.apis.services.static_data.v1.StaticSectorRequest\x1a?.systemathics.apis.services.static_data.v1.StaticSectorResponseb\x06proto3'
)




_STATICSECTORREQUEST = _descriptor.Descriptor(
  name='StaticSectorRequest',
  full_name='systemathics.apis.services.static_data.v1.StaticSectorRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='provider', full_name='systemathics.apis.services.static_data.v1.StaticSectorRequest.provider', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='code', full_name='systemathics.apis.services.static_data.v1.StaticSectorRequest.code', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='level', full_name='systemathics.apis.services.static_data.v1.StaticSectorRequest.level', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
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
    _descriptor.OneofDescriptor(
      name='value', full_name='systemathics.apis.services.static_data.v1.StaticSectorRequest.value',
      index=0, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
  ],
  serialized_start=108,
  serialized_end=189,
)


_STATICSECTORRESPONSE = _descriptor.Descriptor(
  name='StaticSectorResponse',
  full_name='systemathics.apis.services.static_data.v1.StaticSectorResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='data', full_name='systemathics.apis.services.static_data.v1.StaticSectorResponse.data', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='description', full_name='systemathics.apis.services.static_data.v1.StaticSectorResponse.description', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='count', full_name='systemathics.apis.services.static_data.v1.StaticSectorResponse.count', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
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
  serialized_start=191,
  serialized_end=313,
)


_LEVEL = _descriptor.Descriptor(
  name='Level',
  full_name='systemathics.apis.services.static_data.v1.Level',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='Name', full_name='systemathics.apis.services.static_data.v1.Level.Name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='Index', full_name='systemathics.apis.services.static_data.v1.Level.Index', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='Code', full_name='systemathics.apis.services.static_data.v1.Level.Code', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='definition', full_name='systemathics.apis.services.static_data.v1.Level.definition', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='label', full_name='systemathics.apis.services.static_data.v1.Level.label', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
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
  serialized_start=315,
  serialized_end=400,
)

_STATICSECTORREQUEST.oneofs_by_name['value'].fields.append(
  _STATICSECTORREQUEST.fields_by_name['code'])
_STATICSECTORREQUEST.fields_by_name['code'].containing_oneof = _STATICSECTORREQUEST.oneofs_by_name['value']
_STATICSECTORREQUEST.oneofs_by_name['value'].fields.append(
  _STATICSECTORREQUEST.fields_by_name['level'])
_STATICSECTORREQUEST.fields_by_name['level'].containing_oneof = _STATICSECTORREQUEST.oneofs_by_name['value']
_STATICSECTORRESPONSE.fields_by_name['data'].message_type = _LEVEL
DESCRIPTOR.message_types_by_name['StaticSectorRequest'] = _STATICSECTORREQUEST
DESCRIPTOR.message_types_by_name['StaticSectorResponse'] = _STATICSECTORRESPONSE
DESCRIPTOR.message_types_by_name['Level'] = _LEVEL
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

StaticSectorRequest = _reflection.GeneratedProtocolMessageType('StaticSectorRequest', (_message.Message,), {
  'DESCRIPTOR' : _STATICSECTORREQUEST,
  '__module__' : 'systemathics.apis.services.static_data.v1.static_sector_pb2'
  # @@protoc_insertion_point(class_scope:systemathics.apis.services.static_data.v1.StaticSectorRequest)
  })
_sym_db.RegisterMessage(StaticSectorRequest)

StaticSectorResponse = _reflection.GeneratedProtocolMessageType('StaticSectorResponse', (_message.Message,), {
  'DESCRIPTOR' : _STATICSECTORRESPONSE,
  '__module__' : 'systemathics.apis.services.static_data.v1.static_sector_pb2'
  # @@protoc_insertion_point(class_scope:systemathics.apis.services.static_data.v1.StaticSectorResponse)
  })
_sym_db.RegisterMessage(StaticSectorResponse)

Level = _reflection.GeneratedProtocolMessageType('Level', (_message.Message,), {
  'DESCRIPTOR' : _LEVEL,
  '__module__' : 'systemathics.apis.services.static_data.v1.static_sector_pb2'
  # @@protoc_insertion_point(class_scope:systemathics.apis.services.static_data.v1.Level)
  })
_sym_db.RegisterMessage(Level)



_STATICSECTORSERVICE = _descriptor.ServiceDescriptor(
  name='StaticSectorService',
  full_name='systemathics.apis.services.static_data.v1.StaticSectorService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=403,
  serialized_end=570,
  methods=[
  _descriptor.MethodDescriptor(
    name='StaticSector',
    full_name='systemathics.apis.services.static_data.v1.StaticSectorService.StaticSector',
    index=0,
    containing_service=None,
    input_type=_STATICSECTORREQUEST,
    output_type=_STATICSECTORRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_STATICSECTORSERVICE)

DESCRIPTOR.services_by_name['StaticSectorService'] = _STATICSECTORSERVICE

# @@protoc_insertion_point(module_scope)
