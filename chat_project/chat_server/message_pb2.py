# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: message.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='message.proto',
  package='mju',
  syntax='proto2',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\rmessage.proto\x12\x03mju\"\xe6\x01\n\x04Type\x12#\n\x04type\x18\x01 \x02(\x0e\x32\x15.mju.Type.MessageType\"\xb8\x01\n\x0bMessageType\x12\x0b\n\x07\x43S_NAME\x10\x00\x12\x0c\n\x08\x43S_ROOMS\x10\x01\x12\x12\n\x0e\x43S_CREATE_ROOM\x10\x02\x12\x10\n\x0c\x43S_JOIN_ROOM\x10\x03\x12\x11\n\rCS_LEAVE_ROOM\x10\x04\x12\x0b\n\x07\x43S_CHAT\x10\x05\x12\x0f\n\x0b\x43S_SHUTDOWN\x10\x06\x12\x13\n\x0fSC_ROOMS_RESULT\x10\x07\x12\x0b\n\x07SC_CHAT\x10\x08\x12\x15\n\x11SC_SYSTEM_MESSAGE\x10\t\"\x16\n\x06\x43SName\x12\x0c\n\x04name\x18\x01 \x02(\t\"\t\n\x07\x43SRooms\"\x1d\n\x0c\x43SCreateRoom\x12\r\n\x05title\x18\x01 \x01(\t\"\x1c\n\nCSJoinRoom\x12\x0e\n\x06roomId\x18\x01 \x02(\x05\"\r\n\x0b\x43SLeaveRoom\"\x16\n\x06\x43SChat\x12\x0c\n\x04text\x18\x01 \x02(\t\"\x0c\n\nCSShutdown\"\x1d\n\x0cSCNameResult\x12\r\n\x05\x65rror\x18\x01 \x01(\t\"w\n\rSCRoomsResult\x12*\n\x05rooms\x18\x01 \x03(\x0b\x32\x1b.mju.SCRoomsResult.RoomInfo\x1a:\n\x08RoomInfo\x12\x0e\n\x06roomId\x18\x01 \x02(\x05\x12\r\n\x05title\x18\x02 \x01(\t\x12\x0f\n\x07members\x18\x03 \x03(\t\"#\n\x12SCCreateRoomResult\x12\r\n\x05\x65rror\x18\x01 \x01(\t\"!\n\x10SCJoinRoomResult\x12\r\n\x05\x65rror\x18\x01 \x01(\t\"\"\n\x11SCLeaveRoomResult\x12\r\n\x05\x65rror\x18\x01 \x01(\t\"&\n\x06SCChat\x12\x0e\n\x06member\x18\x01 \x02(\t\x12\x0c\n\x04text\x18\x02 \x02(\t\"\x1f\n\x0fSCSystemMessage\x12\x0c\n\x04text\x18\x01 \x02(\t'
)



_TYPE_MESSAGETYPE = _descriptor.EnumDescriptor(
  name='MessageType',
  full_name='mju.Type.MessageType',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='CS_NAME', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='CS_ROOMS', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='CS_CREATE_ROOM', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='CS_JOIN_ROOM', index=3, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='CS_LEAVE_ROOM', index=4, number=4,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='CS_CHAT', index=5, number=5,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='CS_SHUTDOWN', index=6, number=6,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='SC_ROOMS_RESULT', index=7, number=7,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='SC_CHAT', index=8, number=8,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='SC_SYSTEM_MESSAGE', index=9, number=9,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=69,
  serialized_end=253,
)
_sym_db.RegisterEnumDescriptor(_TYPE_MESSAGETYPE)


_TYPE = _descriptor.Descriptor(
  name='Type',
  full_name='mju.Type',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='type', full_name='mju.Type.type', index=0,
      number=1, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _TYPE_MESSAGETYPE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=23,
  serialized_end=253,
)


_CSNAME = _descriptor.Descriptor(
  name='CSName',
  full_name='mju.CSName',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='mju.CSName.name', index=0,
      number=1, type=9, cpp_type=9, label=2,
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
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=255,
  serialized_end=277,
)


_CSROOMS = _descriptor.Descriptor(
  name='CSRooms',
  full_name='mju.CSRooms',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=279,
  serialized_end=288,
)


_CSCREATEROOM = _descriptor.Descriptor(
  name='CSCreateRoom',
  full_name='mju.CSCreateRoom',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='title', full_name='mju.CSCreateRoom.title', index=0,
      number=1, type=9, cpp_type=9, label=1,
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
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=290,
  serialized_end=319,
)


_CSJOINROOM = _descriptor.Descriptor(
  name='CSJoinRoom',
  full_name='mju.CSJoinRoom',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='roomId', full_name='mju.CSJoinRoom.roomId', index=0,
      number=1, type=5, cpp_type=1, label=2,
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
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=321,
  serialized_end=349,
)


_CSLEAVEROOM = _descriptor.Descriptor(
  name='CSLeaveRoom',
  full_name='mju.CSLeaveRoom',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=351,
  serialized_end=364,
)


_CSCHAT = _descriptor.Descriptor(
  name='CSChat',
  full_name='mju.CSChat',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='text', full_name='mju.CSChat.text', index=0,
      number=1, type=9, cpp_type=9, label=2,
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
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=366,
  serialized_end=388,
)


_CSSHUTDOWN = _descriptor.Descriptor(
  name='CSShutdown',
  full_name='mju.CSShutdown',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=390,
  serialized_end=402,
)


_SCNAMERESULT = _descriptor.Descriptor(
  name='SCNameResult',
  full_name='mju.SCNameResult',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='error', full_name='mju.SCNameResult.error', index=0,
      number=1, type=9, cpp_type=9, label=1,
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
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=404,
  serialized_end=433,
)


_SCROOMSRESULT_ROOMINFO = _descriptor.Descriptor(
  name='RoomInfo',
  full_name='mju.SCRoomsResult.RoomInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='roomId', full_name='mju.SCRoomsResult.RoomInfo.roomId', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='title', full_name='mju.SCRoomsResult.RoomInfo.title', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='members', full_name='mju.SCRoomsResult.RoomInfo.members', index=2,
      number=3, type=9, cpp_type=9, label=3,
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
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=496,
  serialized_end=554,
)

_SCROOMSRESULT = _descriptor.Descriptor(
  name='SCRoomsResult',
  full_name='mju.SCRoomsResult',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='rooms', full_name='mju.SCRoomsResult.rooms', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_SCROOMSRESULT_ROOMINFO, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=435,
  serialized_end=554,
)


_SCCREATEROOMRESULT = _descriptor.Descriptor(
  name='SCCreateRoomResult',
  full_name='mju.SCCreateRoomResult',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='error', full_name='mju.SCCreateRoomResult.error', index=0,
      number=1, type=9, cpp_type=9, label=1,
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
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=556,
  serialized_end=591,
)


_SCJOINROOMRESULT = _descriptor.Descriptor(
  name='SCJoinRoomResult',
  full_name='mju.SCJoinRoomResult',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='error', full_name='mju.SCJoinRoomResult.error', index=0,
      number=1, type=9, cpp_type=9, label=1,
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
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=593,
  serialized_end=626,
)


_SCLEAVEROOMRESULT = _descriptor.Descriptor(
  name='SCLeaveRoomResult',
  full_name='mju.SCLeaveRoomResult',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='error', full_name='mju.SCLeaveRoomResult.error', index=0,
      number=1, type=9, cpp_type=9, label=1,
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
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=628,
  serialized_end=662,
)


_SCCHAT = _descriptor.Descriptor(
  name='SCChat',
  full_name='mju.SCChat',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='member', full_name='mju.SCChat.member', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='text', full_name='mju.SCChat.text', index=1,
      number=2, type=9, cpp_type=9, label=2,
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
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=664,
  serialized_end=702,
)


_SCSYSTEMMESSAGE = _descriptor.Descriptor(
  name='SCSystemMessage',
  full_name='mju.SCSystemMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='text', full_name='mju.SCSystemMessage.text', index=0,
      number=1, type=9, cpp_type=9, label=2,
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
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=704,
  serialized_end=735,
)

_TYPE.fields_by_name['type'].enum_type = _TYPE_MESSAGETYPE
_TYPE_MESSAGETYPE.containing_type = _TYPE
_SCROOMSRESULT_ROOMINFO.containing_type = _SCROOMSRESULT
_SCROOMSRESULT.fields_by_name['rooms'].message_type = _SCROOMSRESULT_ROOMINFO
DESCRIPTOR.message_types_by_name['Type'] = _TYPE
DESCRIPTOR.message_types_by_name['CSName'] = _CSNAME
DESCRIPTOR.message_types_by_name['CSRooms'] = _CSROOMS
DESCRIPTOR.message_types_by_name['CSCreateRoom'] = _CSCREATEROOM
DESCRIPTOR.message_types_by_name['CSJoinRoom'] = _CSJOINROOM
DESCRIPTOR.message_types_by_name['CSLeaveRoom'] = _CSLEAVEROOM
DESCRIPTOR.message_types_by_name['CSChat'] = _CSCHAT
DESCRIPTOR.message_types_by_name['CSShutdown'] = _CSSHUTDOWN
DESCRIPTOR.message_types_by_name['SCNameResult'] = _SCNAMERESULT
DESCRIPTOR.message_types_by_name['SCRoomsResult'] = _SCROOMSRESULT
DESCRIPTOR.message_types_by_name['SCCreateRoomResult'] = _SCCREATEROOMRESULT
DESCRIPTOR.message_types_by_name['SCJoinRoomResult'] = _SCJOINROOMRESULT
DESCRIPTOR.message_types_by_name['SCLeaveRoomResult'] = _SCLEAVEROOMRESULT
DESCRIPTOR.message_types_by_name['SCChat'] = _SCCHAT
DESCRIPTOR.message_types_by_name['SCSystemMessage'] = _SCSYSTEMMESSAGE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Type = _reflection.GeneratedProtocolMessageType('Type', (_message.Message,), {
  'DESCRIPTOR' : _TYPE,
  '__module__' : 'message_pb2'
  # @@protoc_insertion_point(class_scope:mju.Type)
  })
_sym_db.RegisterMessage(Type)

CSName = _reflection.GeneratedProtocolMessageType('CSName', (_message.Message,), {
  'DESCRIPTOR' : _CSNAME,
  '__module__' : 'message_pb2'
  # @@protoc_insertion_point(class_scope:mju.CSName)
  })
_sym_db.RegisterMessage(CSName)

CSRooms = _reflection.GeneratedProtocolMessageType('CSRooms', (_message.Message,), {
  'DESCRIPTOR' : _CSROOMS,
  '__module__' : 'message_pb2'
  # @@protoc_insertion_point(class_scope:mju.CSRooms)
  })
_sym_db.RegisterMessage(CSRooms)

CSCreateRoom = _reflection.GeneratedProtocolMessageType('CSCreateRoom', (_message.Message,), {
  'DESCRIPTOR' : _CSCREATEROOM,
  '__module__' : 'message_pb2'
  # @@protoc_insertion_point(class_scope:mju.CSCreateRoom)
  })
_sym_db.RegisterMessage(CSCreateRoom)

CSJoinRoom = _reflection.GeneratedProtocolMessageType('CSJoinRoom', (_message.Message,), {
  'DESCRIPTOR' : _CSJOINROOM,
  '__module__' : 'message_pb2'
  # @@protoc_insertion_point(class_scope:mju.CSJoinRoom)
  })
_sym_db.RegisterMessage(CSJoinRoom)

CSLeaveRoom = _reflection.GeneratedProtocolMessageType('CSLeaveRoom', (_message.Message,), {
  'DESCRIPTOR' : _CSLEAVEROOM,
  '__module__' : 'message_pb2'
  # @@protoc_insertion_point(class_scope:mju.CSLeaveRoom)
  })
_sym_db.RegisterMessage(CSLeaveRoom)

CSChat = _reflection.GeneratedProtocolMessageType('CSChat', (_message.Message,), {
  'DESCRIPTOR' : _CSCHAT,
  '__module__' : 'message_pb2'
  # @@protoc_insertion_point(class_scope:mju.CSChat)
  })
_sym_db.RegisterMessage(CSChat)

CSShutdown = _reflection.GeneratedProtocolMessageType('CSShutdown', (_message.Message,), {
  'DESCRIPTOR' : _CSSHUTDOWN,
  '__module__' : 'message_pb2'
  # @@protoc_insertion_point(class_scope:mju.CSShutdown)
  })
_sym_db.RegisterMessage(CSShutdown)

SCNameResult = _reflection.GeneratedProtocolMessageType('SCNameResult', (_message.Message,), {
  'DESCRIPTOR' : _SCNAMERESULT,
  '__module__' : 'message_pb2'
  # @@protoc_insertion_point(class_scope:mju.SCNameResult)
  })
_sym_db.RegisterMessage(SCNameResult)

SCRoomsResult = _reflection.GeneratedProtocolMessageType('SCRoomsResult', (_message.Message,), {

  'RoomInfo' : _reflection.GeneratedProtocolMessageType('RoomInfo', (_message.Message,), {
    'DESCRIPTOR' : _SCROOMSRESULT_ROOMINFO,
    '__module__' : 'message_pb2'
    # @@protoc_insertion_point(class_scope:mju.SCRoomsResult.RoomInfo)
    })
  ,
  'DESCRIPTOR' : _SCROOMSRESULT,
  '__module__' : 'message_pb2'
  # @@protoc_insertion_point(class_scope:mju.SCRoomsResult)
  })
_sym_db.RegisterMessage(SCRoomsResult)
_sym_db.RegisterMessage(SCRoomsResult.RoomInfo)

SCCreateRoomResult = _reflection.GeneratedProtocolMessageType('SCCreateRoomResult', (_message.Message,), {
  'DESCRIPTOR' : _SCCREATEROOMRESULT,
  '__module__' : 'message_pb2'
  # @@protoc_insertion_point(class_scope:mju.SCCreateRoomResult)
  })
_sym_db.RegisterMessage(SCCreateRoomResult)

SCJoinRoomResult = _reflection.GeneratedProtocolMessageType('SCJoinRoomResult', (_message.Message,), {
  'DESCRIPTOR' : _SCJOINROOMRESULT,
  '__module__' : 'message_pb2'
  # @@protoc_insertion_point(class_scope:mju.SCJoinRoomResult)
  })
_sym_db.RegisterMessage(SCJoinRoomResult)

SCLeaveRoomResult = _reflection.GeneratedProtocolMessageType('SCLeaveRoomResult', (_message.Message,), {
  'DESCRIPTOR' : _SCLEAVEROOMRESULT,
  '__module__' : 'message_pb2'
  # @@protoc_insertion_point(class_scope:mju.SCLeaveRoomResult)
  })
_sym_db.RegisterMessage(SCLeaveRoomResult)

SCChat = _reflection.GeneratedProtocolMessageType('SCChat', (_message.Message,), {
  'DESCRIPTOR' : _SCCHAT,
  '__module__' : 'message_pb2'
  # @@protoc_insertion_point(class_scope:mju.SCChat)
  })
_sym_db.RegisterMessage(SCChat)

SCSystemMessage = _reflection.GeneratedProtocolMessageType('SCSystemMessage', (_message.Message,), {
  'DESCRIPTOR' : _SCSYSTEMMESSAGE,
  '__module__' : 'message_pb2'
  # @@protoc_insertion_point(class_scope:mju.SCSystemMessage)
  })
_sym_db.RegisterMessage(SCSystemMessage)


# @@protoc_insertion_point(module_scope)
