# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chirpstack-api/geo/geo.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from chirpstack_api.gw import gw_pb2 as chirpstack__api_dot_gw_dot_gw__pb2
from chirpstack_api.common import common_pb2 as chirpstack__api_dot_common_dot_common__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='chirpstack-api/geo/geo.proto',
  package='geo',
  syntax='proto3',
  serialized_options=b'\n\025io.chirpstack.api.geoB\026GeolocationServerProtoP\001Z+github.com/brocaar/chirpstack-api/go/v3/geo',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x1c\x63hirpstack-api/geo/geo.proto\x12\x03geo\x1a\x1a\x63hirpstack-api/gw/gw.proto\x1a\"chirpstack-api/common/common.proto\"3\n\rResolveResult\x12\"\n\x08location\x18\x01 \x01(\x0b\x32\x10.common.Location\"0\n\x0b\x46rameRXInfo\x12!\n\x07rx_info\x18\x01 \x03(\x0b\x32\x10.gw.UplinkRXInfo\"\x86\x01\n\x12ResolveTDOARequest\x12\x17\n\x07\x64\x65v_eui\x18\x01 \x01(\x0cR\x06\x64\x65vEUI\x12\x34\n\rframe_rx_info\x18\x02 \x01(\x0b\x32\x10.geo.FrameRXInfoR\x0b\x66rameRXInfo\x12!\n\x19\x64\x65vice_reference_altitude\x18\x03 \x01(\x01\"\x97\x01\n\x1cResolveMultiFrameTDOARequest\x12\x17\n\x07\x64\x65v_eui\x18\x01 \x01(\x0cR\x06\x64\x65vEUI\x12;\n\x11\x66rame_rx_info_set\x18\x02 \x03(\x0b\x32\x10.geo.FrameRXInfoR\x0e\x66rameRXInfoSet\x12!\n\x19\x64\x65vice_reference_altitude\x18\x03 \x01(\x01\"9\n\x13ResolveTDOAResponse\x12\"\n\x06result\x18\x01 \x01(\x0b\x32\x12.geo.ResolveResult\"C\n\x1dResolveMultiFrameTDOAResponse\x12\"\n\x06result\x18\x01 \x01(\x0b\x32\x12.geo.ResolveResult2\xc0\x01\n\x18GeolocationServerService\x12\x42\n\x0bResolveTDOA\x12\x17.geo.ResolveTDOARequest\x1a\x18.geo.ResolveTDOAResponse\"\x00\x12`\n\x15ResolveMultiFrameTDOA\x12!.geo.ResolveMultiFrameTDOARequest\x1a\".geo.ResolveMultiFrameTDOAResponse\"\x00\x42^\n\x15io.chirpstack.api.geoB\x16GeolocationServerProtoP\x01Z+github.com/brocaar/chirpstack-api/go/v3/geob\x06proto3'
  ,
  dependencies=[chirpstack__api_dot_gw_dot_gw__pb2.DESCRIPTOR,chirpstack__api_dot_common_dot_common__pb2.DESCRIPTOR,])




_RESOLVERESULT = _descriptor.Descriptor(
  name='ResolveResult',
  full_name='geo.ResolveResult',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='location', full_name='geo.ResolveResult.location', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
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
  serialized_start=101,
  serialized_end=152,
)


_FRAMERXINFO = _descriptor.Descriptor(
  name='FrameRXInfo',
  full_name='geo.FrameRXInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='rx_info', full_name='geo.FrameRXInfo.rx_info', index=0,
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
  serialized_start=154,
  serialized_end=202,
)


_RESOLVETDOAREQUEST = _descriptor.Descriptor(
  name='ResolveTDOARequest',
  full_name='geo.ResolveTDOARequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='dev_eui', full_name='geo.ResolveTDOARequest.dev_eui', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='devEUI', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='frame_rx_info', full_name='geo.ResolveTDOARequest.frame_rx_info', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='frameRXInfo', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='device_reference_altitude', full_name='geo.ResolveTDOARequest.device_reference_altitude', index=2,
      number=3, type=1, cpp_type=5, label=1,
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
  serialized_start=205,
  serialized_end=339,
)


_RESOLVEMULTIFRAMETDOAREQUEST = _descriptor.Descriptor(
  name='ResolveMultiFrameTDOARequest',
  full_name='geo.ResolveMultiFrameTDOARequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='dev_eui', full_name='geo.ResolveMultiFrameTDOARequest.dev_eui', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='devEUI', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='frame_rx_info_set', full_name='geo.ResolveMultiFrameTDOARequest.frame_rx_info_set', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='frameRXInfoSet', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='device_reference_altitude', full_name='geo.ResolveMultiFrameTDOARequest.device_reference_altitude', index=2,
      number=3, type=1, cpp_type=5, label=1,
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
  serialized_start=342,
  serialized_end=493,
)


_RESOLVETDOARESPONSE = _descriptor.Descriptor(
  name='ResolveTDOAResponse',
  full_name='geo.ResolveTDOAResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='result', full_name='geo.ResolveTDOAResponse.result', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
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
  serialized_start=495,
  serialized_end=552,
)


_RESOLVEMULTIFRAMETDOARESPONSE = _descriptor.Descriptor(
  name='ResolveMultiFrameTDOAResponse',
  full_name='geo.ResolveMultiFrameTDOAResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='result', full_name='geo.ResolveMultiFrameTDOAResponse.result', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
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
  serialized_start=554,
  serialized_end=621,
)

_RESOLVERESULT.fields_by_name['location'].message_type = chirpstack__api_dot_common_dot_common__pb2._LOCATION
_FRAMERXINFO.fields_by_name['rx_info'].message_type = chirpstack__api_dot_gw_dot_gw__pb2._UPLINKRXINFO
_RESOLVETDOAREQUEST.fields_by_name['frame_rx_info'].message_type = _FRAMERXINFO
_RESOLVEMULTIFRAMETDOAREQUEST.fields_by_name['frame_rx_info_set'].message_type = _FRAMERXINFO
_RESOLVETDOARESPONSE.fields_by_name['result'].message_type = _RESOLVERESULT
_RESOLVEMULTIFRAMETDOARESPONSE.fields_by_name['result'].message_type = _RESOLVERESULT
DESCRIPTOR.message_types_by_name['ResolveResult'] = _RESOLVERESULT
DESCRIPTOR.message_types_by_name['FrameRXInfo'] = _FRAMERXINFO
DESCRIPTOR.message_types_by_name['ResolveTDOARequest'] = _RESOLVETDOAREQUEST
DESCRIPTOR.message_types_by_name['ResolveMultiFrameTDOARequest'] = _RESOLVEMULTIFRAMETDOAREQUEST
DESCRIPTOR.message_types_by_name['ResolveTDOAResponse'] = _RESOLVETDOARESPONSE
DESCRIPTOR.message_types_by_name['ResolveMultiFrameTDOAResponse'] = _RESOLVEMULTIFRAMETDOARESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ResolveResult = _reflection.GeneratedProtocolMessageType('ResolveResult', (_message.Message,), {
  'DESCRIPTOR' : _RESOLVERESULT,
  '__module__' : 'chirpstack_api.geo.geo_pb2'
  # @@protoc_insertion_point(class_scope:geo.ResolveResult)
  })
_sym_db.RegisterMessage(ResolveResult)

FrameRXInfo = _reflection.GeneratedProtocolMessageType('FrameRXInfo', (_message.Message,), {
  'DESCRIPTOR' : _FRAMERXINFO,
  '__module__' : 'chirpstack_api.geo.geo_pb2'
  # @@protoc_insertion_point(class_scope:geo.FrameRXInfo)
  })
_sym_db.RegisterMessage(FrameRXInfo)

ResolveTDOARequest = _reflection.GeneratedProtocolMessageType('ResolveTDOARequest', (_message.Message,), {
  'DESCRIPTOR' : _RESOLVETDOAREQUEST,
  '__module__' : 'chirpstack_api.geo.geo_pb2'
  # @@protoc_insertion_point(class_scope:geo.ResolveTDOARequest)
  })
_sym_db.RegisterMessage(ResolveTDOARequest)

ResolveMultiFrameTDOARequest = _reflection.GeneratedProtocolMessageType('ResolveMultiFrameTDOARequest', (_message.Message,), {
  'DESCRIPTOR' : _RESOLVEMULTIFRAMETDOAREQUEST,
  '__module__' : 'chirpstack_api.geo.geo_pb2'
  # @@protoc_insertion_point(class_scope:geo.ResolveMultiFrameTDOARequest)
  })
_sym_db.RegisterMessage(ResolveMultiFrameTDOARequest)

ResolveTDOAResponse = _reflection.GeneratedProtocolMessageType('ResolveTDOAResponse', (_message.Message,), {
  'DESCRIPTOR' : _RESOLVETDOARESPONSE,
  '__module__' : 'chirpstack_api.geo.geo_pb2'
  # @@protoc_insertion_point(class_scope:geo.ResolveTDOAResponse)
  })
_sym_db.RegisterMessage(ResolveTDOAResponse)

ResolveMultiFrameTDOAResponse = _reflection.GeneratedProtocolMessageType('ResolveMultiFrameTDOAResponse', (_message.Message,), {
  'DESCRIPTOR' : _RESOLVEMULTIFRAMETDOARESPONSE,
  '__module__' : 'chirpstack_api.geo.geo_pb2'
  # @@protoc_insertion_point(class_scope:geo.ResolveMultiFrameTDOAResponse)
  })
_sym_db.RegisterMessage(ResolveMultiFrameTDOAResponse)


DESCRIPTOR._options = None

_GEOLOCATIONSERVERSERVICE = _descriptor.ServiceDescriptor(
  name='GeolocationServerService',
  full_name='geo.GeolocationServerService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=624,
  serialized_end=816,
  methods=[
  _descriptor.MethodDescriptor(
    name='ResolveTDOA',
    full_name='geo.GeolocationServerService.ResolveTDOA',
    index=0,
    containing_service=None,
    input_type=_RESOLVETDOAREQUEST,
    output_type=_RESOLVETDOARESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='ResolveMultiFrameTDOA',
    full_name='geo.GeolocationServerService.ResolveMultiFrameTDOA',
    index=1,
    containing_service=None,
    input_type=_RESOLVEMULTIFRAMETDOAREQUEST,
    output_type=_RESOLVEMULTIFRAMETDOARESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_GEOLOCATIONSERVERSERVICE)

DESCRIPTOR.services_by_name['GeolocationServerService'] = _GEOLOCATIONSERVERSERVICE

# @@protoc_insertion_point(module_scope)
