# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: replication.proto
# Protobuf Python Version: 5.29.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    29,
    0,
    '',
    'replication.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x11replication.proto\x12\x0breplication\"/\n\x0cWriteRequest\x12\x0c\n\x04\x64\x61ta\x18\x01 \x01(\t\x12\x11\n\ttimestamp\x18\x02 \x01(\t\",\n\x08WriteAck\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x0f\n\x07node_id\x18\x02 \x01(\t\"x\n\rMetricsReport\x12\x0f\n\x07node_id\x18\x01 \x01(\t\x12\x11\n\tqueue_len\x18\x02 \x01(\x05\x12\x10\n\x08\x63pu_util\x18\x03 \x01(\x02\x12\x1c\n\x14pending_replications\x18\x04 \x01(\x05\x12\x13\n\x0bsteal_delay\x18\x05 \x01(\x03\"$\n\x0cStealRequest\x12\x14\n\x0crequester_id\x18\x01 \x01(\t\"@\n\rStealResponse\x12/\n\x0cstolen_tasks\x18\x01 \x03(\x0b\x32\x19.replication.WriteRequest2\xd7\x01\n\x0bReplication\x12=\n\tSendWrite\x12\x19.replication.WriteRequest\x1a\x15.replication.WriteAck\x12\x42\n\rReportMetrics\x12\x1a.replication.MetricsReport\x1a\x15.replication.WriteAck\x12\x45\n\x0cRequestSteal\x12\x19.replication.StealRequest\x1a\x1a.replication.StealResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'replication_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_WRITEREQUEST']._serialized_start=34
  _globals['_WRITEREQUEST']._serialized_end=81
  _globals['_WRITEACK']._serialized_start=83
  _globals['_WRITEACK']._serialized_end=127
  _globals['_METRICSREPORT']._serialized_start=129
  _globals['_METRICSREPORT']._serialized_end=249
  _globals['_STEALREQUEST']._serialized_start=251
  _globals['_STEALREQUEST']._serialized_end=287
  _globals['_STEALRESPONSE']._serialized_start=289
  _globals['_STEALRESPONSE']._serialized_end=353
  _globals['_REPLICATION']._serialized_start=356
  _globals['_REPLICATION']._serialized_end=571
# @@protoc_insertion_point(module_scope)
