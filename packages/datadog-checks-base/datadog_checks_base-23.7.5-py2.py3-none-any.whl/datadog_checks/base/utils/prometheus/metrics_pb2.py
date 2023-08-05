# flake8: noqa
# pylint: skip-file
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: metrics.proto

import sys

from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pb2
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import enum_type_wrapper

_b = sys.version_info[0] < 3 and (lambda x: x) or (lambda x: x.encode('latin1'))
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor.FileDescriptor(
    name='metrics.proto',
    package='io.prometheus.client',
    syntax='proto2',
    serialized_pb=_b(
        '\n\rmetrics.proto\x12\x14io.prometheus.client\"(\n\tLabelPair\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t\"\x16\n\x05Gauge\x12\r\n\x05value\x18\x01 \x01(\x01\"\x18\n\x07\x43ounter\x12\r\n\x05value\x18\x01 \x01(\x01\"+\n\x08Quantile\x12\x10\n\x08quantile\x18\x01 \x01(\x01\x12\r\n\x05value\x18\x02 \x01(\x01\"e\n\x07Summary\x12\x14\n\x0csample_count\x18\x01 \x01(\x04\x12\x12\n\nsample_sum\x18\x02 \x01(\x01\x12\x30\n\x08quantile\x18\x03 \x03(\x0b\x32\x1e.io.prometheus.client.Quantile\"\x18\n\x07Untyped\x12\r\n\x05value\x18\x01 \x01(\x01\"c\n\tHistogram\x12\x14\n\x0csample_count\x18\x01 \x01(\x04\x12\x12\n\nsample_sum\x18\x02 \x01(\x01\x12,\n\x06\x62ucket\x18\x03 \x03(\x0b\x32\x1c.io.prometheus.client.Bucket\"7\n\x06\x42ucket\x12\x18\n\x10\x63umulative_count\x18\x01 \x01(\x04\x12\x13\n\x0bupper_bound\x18\x02 \x01(\x01\"\xbe\x02\n\x06Metric\x12.\n\x05label\x18\x01 \x03(\x0b\x32\x1f.io.prometheus.client.LabelPair\x12*\n\x05gauge\x18\x02 \x01(\x0b\x32\x1b.io.prometheus.client.Gauge\x12.\n\x07\x63ounter\x18\x03 \x01(\x0b\x32\x1d.io.prometheus.client.Counter\x12.\n\x07summary\x18\x04 \x01(\x0b\x32\x1d.io.prometheus.client.Summary\x12.\n\x07untyped\x18\x05 \x01(\x0b\x32\x1d.io.prometheus.client.Untyped\x12\x32\n\thistogram\x18\x07 \x01(\x0b\x32\x1f.io.prometheus.client.Histogram\x12\x14\n\x0ctimestamp_ms\x18\x06 \x01(\x03\"\x88\x01\n\x0cMetricFamily\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0c\n\x04help\x18\x02 \x01(\t\x12.\n\x04type\x18\x03 \x01(\x0e\x32 .io.prometheus.client.MetricType\x12,\n\x06metric\x18\x04 \x03(\x0b\x32\x1c.io.prometheus.client.Metric*M\n\nMetricType\x12\x0b\n\x07\x43OUNTER\x10\x00\x12\t\n\x05GAUGE\x10\x01\x12\x0b\n\x07SUMMARY\x10\x02\x12\x0b\n\x07UNTYPED\x10\x03\x12\r\n\tHISTOGRAM\x10\x04\x42\x16\n\x14io.prometheus.client'
    ),
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

_METRICTYPE = _descriptor.EnumDescriptor(
    name='MetricType',
    full_name='io.prometheus.client.MetricType',
    filename=None,
    file=DESCRIPTOR,
    values=[
        _descriptor.EnumValueDescriptor(name='COUNTER', index=0, number=0, options=None, type=None),
        _descriptor.EnumValueDescriptor(name='GAUGE', index=1, number=1, options=None, type=None),
        _descriptor.EnumValueDescriptor(name='SUMMARY', index=2, number=2, options=None, type=None),
        _descriptor.EnumValueDescriptor(name='UNTYPED', index=3, number=3, options=None, type=None),
        _descriptor.EnumValueDescriptor(name='HISTOGRAM', index=4, number=4, options=None, type=None),
    ],
    containing_type=None,
    options=None,
    serialized_start=923,
    serialized_end=1000,
)
_sym_db.RegisterEnumDescriptor(_METRICTYPE)

MetricType = enum_type_wrapper.EnumTypeWrapper(_METRICTYPE)
COUNTER = 0
GAUGE = 1
SUMMARY = 2
UNTYPED = 3
HISTOGRAM = 4


_LABELPAIR = _descriptor.Descriptor(
    name='LabelPair',
    full_name='io.prometheus.client.LabelPair',
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name='name',
            full_name='io.prometheus.client.LabelPair.name',
            index=0,
            number=1,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode('utf-8'),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
        ),
        _descriptor.FieldDescriptor(
            name='value',
            full_name='io.prometheus.client.LabelPair.value',
            index=1,
            number=2,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode('utf-8'),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    options=None,
    is_extendable=False,
    syntax='proto2',
    extension_ranges=[],
    oneofs=[],
    serialized_start=39,
    serialized_end=79,
)


_GAUGE = _descriptor.Descriptor(
    name='Gauge',
    full_name='io.prometheus.client.Gauge',
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name='value',
            full_name='io.prometheus.client.Gauge.value',
            index=0,
            number=1,
            type=1,
            cpp_type=5,
            label=1,
            has_default_value=False,
            default_value=float(0),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
        )
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    options=None,
    is_extendable=False,
    syntax='proto2',
    extension_ranges=[],
    oneofs=[],
    serialized_start=81,
    serialized_end=103,
)


_COUNTER = _descriptor.Descriptor(
    name='Counter',
    full_name='io.prometheus.client.Counter',
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name='value',
            full_name='io.prometheus.client.Counter.value',
            index=0,
            number=1,
            type=1,
            cpp_type=5,
            label=1,
            has_default_value=False,
            default_value=float(0),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
        )
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    options=None,
    is_extendable=False,
    syntax='proto2',
    extension_ranges=[],
    oneofs=[],
    serialized_start=105,
    serialized_end=129,
)


_QUANTILE = _descriptor.Descriptor(
    name='Quantile',
    full_name='io.prometheus.client.Quantile',
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name='quantile',
            full_name='io.prometheus.client.Quantile.quantile',
            index=0,
            number=1,
            type=1,
            cpp_type=5,
            label=1,
            has_default_value=False,
            default_value=float(0),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
        ),
        _descriptor.FieldDescriptor(
            name='value',
            full_name='io.prometheus.client.Quantile.value',
            index=1,
            number=2,
            type=1,
            cpp_type=5,
            label=1,
            has_default_value=False,
            default_value=float(0),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    options=None,
    is_extendable=False,
    syntax='proto2',
    extension_ranges=[],
    oneofs=[],
    serialized_start=131,
    serialized_end=174,
)


_SUMMARY = _descriptor.Descriptor(
    name='Summary',
    full_name='io.prometheus.client.Summary',
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name='sample_count',
            full_name='io.prometheus.client.Summary.sample_count',
            index=0,
            number=1,
            type=4,
            cpp_type=4,
            label=1,
            has_default_value=False,
            default_value=0,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
        ),
        _descriptor.FieldDescriptor(
            name='sample_sum',
            full_name='io.prometheus.client.Summary.sample_sum',
            index=1,
            number=2,
            type=1,
            cpp_type=5,
            label=1,
            has_default_value=False,
            default_value=float(0),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
        ),
        _descriptor.FieldDescriptor(
            name='quantile',
            full_name='io.prometheus.client.Summary.quantile',
            index=2,
            number=3,
            type=11,
            cpp_type=10,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    options=None,
    is_extendable=False,
    syntax='proto2',
    extension_ranges=[],
    oneofs=[],
    serialized_start=176,
    serialized_end=277,
)


_UNTYPED = _descriptor.Descriptor(
    name='Untyped',
    full_name='io.prometheus.client.Untyped',
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name='value',
            full_name='io.prometheus.client.Untyped.value',
            index=0,
            number=1,
            type=1,
            cpp_type=5,
            label=1,
            has_default_value=False,
            default_value=float(0),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
        )
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    options=None,
    is_extendable=False,
    syntax='proto2',
    extension_ranges=[],
    oneofs=[],
    serialized_start=279,
    serialized_end=303,
)


_HISTOGRAM = _descriptor.Descriptor(
    name='Histogram',
    full_name='io.prometheus.client.Histogram',
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name='sample_count',
            full_name='io.prometheus.client.Histogram.sample_count',
            index=0,
            number=1,
            type=4,
            cpp_type=4,
            label=1,
            has_default_value=False,
            default_value=0,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
        ),
        _descriptor.FieldDescriptor(
            name='sample_sum',
            full_name='io.prometheus.client.Histogram.sample_sum',
            index=1,
            number=2,
            type=1,
            cpp_type=5,
            label=1,
            has_default_value=False,
            default_value=float(0),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
        ),
        _descriptor.FieldDescriptor(
            name='bucket',
            full_name='io.prometheus.client.Histogram.bucket',
            index=2,
            number=3,
            type=11,
            cpp_type=10,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    options=None,
    is_extendable=False,
    syntax='proto2',
    extension_ranges=[],
    oneofs=[],
    serialized_start=305,
    serialized_end=404,
)


_BUCKET = _descriptor.Descriptor(
    name='Bucket',
    full_name='io.prometheus.client.Bucket',
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name='cumulative_count',
            full_name='io.prometheus.client.Bucket.cumulative_count',
            index=0,
            number=1,
            type=4,
            cpp_type=4,
            label=1,
            has_default_value=False,
            default_value=0,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
        ),
        _descriptor.FieldDescriptor(
            name='upper_bound',
            full_name='io.prometheus.client.Bucket.upper_bound',
            index=1,
            number=2,
            type=1,
            cpp_type=5,
            label=1,
            has_default_value=False,
            default_value=float(0),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    options=None,
    is_extendable=False,
    syntax='proto2',
    extension_ranges=[],
    oneofs=[],
    serialized_start=406,
    serialized_end=461,
)


_METRIC = _descriptor.Descriptor(
    name='Metric',
    full_name='io.prometheus.client.Metric',
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name='label',
            full_name='io.prometheus.client.Metric.label',
            index=0,
            number=1,
            type=11,
            cpp_type=10,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
        ),
        _descriptor.FieldDescriptor(
            name='gauge',
            full_name='io.prometheus.client.Metric.gauge',
            index=1,
            number=2,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
        ),
        _descriptor.FieldDescriptor(
            name='counter',
            full_name='io.prometheus.client.Metric.counter',
            index=2,
            number=3,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
        ),
        _descriptor.FieldDescriptor(
            name='summary',
            full_name='io.prometheus.client.Metric.summary',
            index=3,
            number=4,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
        ),
        _descriptor.FieldDescriptor(
            name='untyped',
            full_name='io.prometheus.client.Metric.untyped',
            index=4,
            number=5,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
        ),
        _descriptor.FieldDescriptor(
            name='histogram',
            full_name='io.prometheus.client.Metric.histogram',
            index=5,
            number=7,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
        ),
        _descriptor.FieldDescriptor(
            name='timestamp_ms',
            full_name='io.prometheus.client.Metric.timestamp_ms',
            index=6,
            number=6,
            type=3,
            cpp_type=2,
            label=1,
            has_default_value=False,
            default_value=0,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    options=None,
    is_extendable=False,
    syntax='proto2',
    extension_ranges=[],
    oneofs=[],
    serialized_start=464,
    serialized_end=782,
)


_METRICFAMILY = _descriptor.Descriptor(
    name='MetricFamily',
    full_name='io.prometheus.client.MetricFamily',
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name='name',
            full_name='io.prometheus.client.MetricFamily.name',
            index=0,
            number=1,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode('utf-8'),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
        ),
        _descriptor.FieldDescriptor(
            name='help',
            full_name='io.prometheus.client.MetricFamily.help',
            index=1,
            number=2,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode('utf-8'),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
        ),
        _descriptor.FieldDescriptor(
            name='type',
            full_name='io.prometheus.client.MetricFamily.type',
            index=2,
            number=3,
            type=14,
            cpp_type=8,
            label=1,
            has_default_value=False,
            default_value=0,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
        ),
        _descriptor.FieldDescriptor(
            name='metric',
            full_name='io.prometheus.client.MetricFamily.metric',
            index=3,
            number=4,
            type=11,
            cpp_type=10,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    options=None,
    is_extendable=False,
    syntax='proto2',
    extension_ranges=[],
    oneofs=[],
    serialized_start=785,
    serialized_end=921,
)

_SUMMARY.fields_by_name['quantile'].message_type = _QUANTILE
_HISTOGRAM.fields_by_name['bucket'].message_type = _BUCKET
_METRIC.fields_by_name['label'].message_type = _LABELPAIR
_METRIC.fields_by_name['gauge'].message_type = _GAUGE
_METRIC.fields_by_name['counter'].message_type = _COUNTER
_METRIC.fields_by_name['summary'].message_type = _SUMMARY
_METRIC.fields_by_name['untyped'].message_type = _UNTYPED
_METRIC.fields_by_name['histogram'].message_type = _HISTOGRAM
_METRICFAMILY.fields_by_name['type'].enum_type = _METRICTYPE
_METRICFAMILY.fields_by_name['metric'].message_type = _METRIC
DESCRIPTOR.message_types_by_name['LabelPair'] = _LABELPAIR
DESCRIPTOR.message_types_by_name['Gauge'] = _GAUGE
DESCRIPTOR.message_types_by_name['Counter'] = _COUNTER
DESCRIPTOR.message_types_by_name['Quantile'] = _QUANTILE
DESCRIPTOR.message_types_by_name['Summary'] = _SUMMARY
DESCRIPTOR.message_types_by_name['Untyped'] = _UNTYPED
DESCRIPTOR.message_types_by_name['Histogram'] = _HISTOGRAM
DESCRIPTOR.message_types_by_name['Bucket'] = _BUCKET
DESCRIPTOR.message_types_by_name['Metric'] = _METRIC
DESCRIPTOR.message_types_by_name['MetricFamily'] = _METRICFAMILY
DESCRIPTOR.enum_types_by_name['MetricType'] = _METRICTYPE

LabelPair = _reflection.GeneratedProtocolMessageType(
    'LabelPair',
    (_message.Message,),
    dict(
        DESCRIPTOR=_LABELPAIR,
        __module__='metrics_pb2'
        # @@protoc_insertion_point(class_scope:io.prometheus.client.LabelPair)
    ),
)
_sym_db.RegisterMessage(LabelPair)

Gauge = _reflection.GeneratedProtocolMessageType(
    'Gauge',
    (_message.Message,),
    dict(
        DESCRIPTOR=_GAUGE,
        __module__='metrics_pb2'
        # @@protoc_insertion_point(class_scope:io.prometheus.client.Gauge)
    ),
)
_sym_db.RegisterMessage(Gauge)

Counter = _reflection.GeneratedProtocolMessageType(
    'Counter',
    (_message.Message,),
    dict(
        DESCRIPTOR=_COUNTER,
        __module__='metrics_pb2'
        # @@protoc_insertion_point(class_scope:io.prometheus.client.Counter)
    ),
)
_sym_db.RegisterMessage(Counter)

Quantile = _reflection.GeneratedProtocolMessageType(
    'Quantile',
    (_message.Message,),
    dict(
        DESCRIPTOR=_QUANTILE,
        __module__='metrics_pb2'
        # @@protoc_insertion_point(class_scope:io.prometheus.client.Quantile)
    ),
)
_sym_db.RegisterMessage(Quantile)

Summary = _reflection.GeneratedProtocolMessageType(
    'Summary',
    (_message.Message,),
    dict(
        DESCRIPTOR=_SUMMARY,
        __module__='metrics_pb2'
        # @@protoc_insertion_point(class_scope:io.prometheus.client.Summary)
    ),
)
_sym_db.RegisterMessage(Summary)

Untyped = _reflection.GeneratedProtocolMessageType(
    'Untyped',
    (_message.Message,),
    dict(
        DESCRIPTOR=_UNTYPED,
        __module__='metrics_pb2'
        # @@protoc_insertion_point(class_scope:io.prometheus.client.Untyped)
    ),
)
_sym_db.RegisterMessage(Untyped)

Histogram = _reflection.GeneratedProtocolMessageType(
    'Histogram',
    (_message.Message,),
    dict(
        DESCRIPTOR=_HISTOGRAM,
        __module__='metrics_pb2'
        # @@protoc_insertion_point(class_scope:io.prometheus.client.Histogram)
    ),
)
_sym_db.RegisterMessage(Histogram)

Bucket = _reflection.GeneratedProtocolMessageType(
    'Bucket',
    (_message.Message,),
    dict(
        DESCRIPTOR=_BUCKET,
        __module__='metrics_pb2'
        # @@protoc_insertion_point(class_scope:io.prometheus.client.Bucket)
    ),
)
_sym_db.RegisterMessage(Bucket)

Metric = _reflection.GeneratedProtocolMessageType(
    'Metric',
    (_message.Message,),
    dict(
        DESCRIPTOR=_METRIC,
        __module__='metrics_pb2'
        # @@protoc_insertion_point(class_scope:io.prometheus.client.Metric)
    ),
)
_sym_db.RegisterMessage(Metric)

MetricFamily = _reflection.GeneratedProtocolMessageType(
    'MetricFamily',
    (_message.Message,),
    dict(
        DESCRIPTOR=_METRICFAMILY,
        __module__='metrics_pb2'
        # @@protoc_insertion_point(class_scope:io.prometheus.client.MetricFamily)
    ),
)
_sym_db.RegisterMessage(MetricFamily)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('\n\024io.prometheus.client'))
# @@protoc_insertion_point(module_scope)
