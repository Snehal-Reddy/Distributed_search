# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
import route_guide_pb2 as route__guide__pb2


class QueryNodeStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.AskQuery = channel.unary_stream(
                '/QueryNode/AskQuery',
                request_serializer=route__guide__pb2.Query.SerializeToString,
                response_deserializer=route__guide__pb2.Result.FromString,
                )
        self.AddDocuments = channel.unary_unary(
                '/QueryNode/AddDocuments',
                request_serializer=route__guide__pb2.Document.SerializeToString,
                response_deserializer=route__guide__pb2.Status.FromString,
                )
        self.DeleteDocument = channel.unary_unary(
                '/QueryNode/DeleteDocument',
                request_serializer=route__guide__pb2.DocumentId.SerializeToString,
                response_deserializer=route__guide__pb2.Status.FromString,
                )
        self.FetchDocuments = channel.unary_unary(
                '/QueryNode/FetchDocuments',
                request_serializer=route__guide__pb2.DocumentId.SerializeToString,
                response_deserializer=route__guide__pb2.Document.FromString,
                )


class QueryNodeServicer(object):
    """Missing associated documentation comment in .proto file."""

    def AskQuery(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def AddDocuments(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteDocument(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def FetchDocuments(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_QueryNodeServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'AskQuery': grpc.unary_stream_rpc_method_handler(
                    servicer.AskQuery,
                    request_deserializer=route__guide__pb2.Query.FromString,
                    response_serializer=route__guide__pb2.Result.SerializeToString,
            ),
            'AddDocuments': grpc.unary_unary_rpc_method_handler(
                    servicer.AddDocuments,
                    request_deserializer=route__guide__pb2.Document.FromString,
                    response_serializer=route__guide__pb2.Status.SerializeToString,
            ),
            'DeleteDocument': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteDocument,
                    request_deserializer=route__guide__pb2.DocumentId.FromString,
                    response_serializer=route__guide__pb2.Status.SerializeToString,
            ),
            'FetchDocuments': grpc.unary_unary_rpc_method_handler(
                    servicer.FetchDocuments,
                    request_deserializer=route__guide__pb2.DocumentId.FromString,
                    response_serializer=route__guide__pb2.Document.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'QueryNode', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class QueryNode(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def AskQuery(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/QueryNode/AskQuery',
            route__guide__pb2.Query.SerializeToString,
            route__guide__pb2.Result.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def AddDocuments(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/QueryNode/AddDocuments',
            route__guide__pb2.Document.SerializeToString,
            route__guide__pb2.Status.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DeleteDocument(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/QueryNode/DeleteDocument',
            route__guide__pb2.DocumentId.SerializeToString,
            route__guide__pb2.Status.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def FetchDocuments(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/QueryNode/FetchDocuments',
            route__guide__pb2.DocumentId.SerializeToString,
            route__guide__pb2.Document.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)


class DataNodeStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.AskQuery = channel.unary_stream(
                '/DataNode/AskQuery',
                request_serializer=route__guide__pb2.Query.SerializeToString,
                response_deserializer=route__guide__pb2.Result.FromString,
                )
        self.WriteRequest = channel.unary_unary(
                '/DataNode/WriteRequest',
                request_serializer=route__guide__pb2.Document.SerializeToString,
                response_deserializer=route__guide__pb2.Status.FromString,
                )
        self.WriteReply = channel.unary_unary(
                '/DataNode/WriteReply',
                request_serializer=route__guide__pb2.Status.SerializeToString,
                response_deserializer=route__guide__pb2.Status.FromString,
                )
        self.DeleteRequest = channel.unary_unary(
                '/DataNode/DeleteRequest',
                request_serializer=route__guide__pb2.DocumentId.SerializeToString,
                response_deserializer=route__guide__pb2.Status.FromString,
                )
        self.DeleteReply = channel.unary_unary(
                '/DataNode/DeleteReply',
                request_serializer=route__guide__pb2.Status.SerializeToString,
                response_deserializer=route__guide__pb2.Status.FromString,
                )
        self.FetchDocuments = channel.unary_unary(
                '/DataNode/FetchDocuments',
                request_serializer=route__guide__pb2.DocumentId.SerializeToString,
                response_deserializer=route__guide__pb2.Document.FromString,
                )
        self.getMID = channel.unary_unary(
                '/DataNode/getMID',
                request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
                response_deserializer=route__guide__pb2.DocumentId.FromString,
                )


class DataNodeServicer(object):
    """Missing associated documentation comment in .proto file."""

    def AskQuery(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def WriteRequest(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def WriteReply(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteRequest(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteReply(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def FetchDocuments(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def getMID(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_DataNodeServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'AskQuery': grpc.unary_stream_rpc_method_handler(
                    servicer.AskQuery,
                    request_deserializer=route__guide__pb2.Query.FromString,
                    response_serializer=route__guide__pb2.Result.SerializeToString,
            ),
            'WriteRequest': grpc.unary_unary_rpc_method_handler(
                    servicer.WriteRequest,
                    request_deserializer=route__guide__pb2.Document.FromString,
                    response_serializer=route__guide__pb2.Status.SerializeToString,
            ),
            'WriteReply': grpc.unary_unary_rpc_method_handler(
                    servicer.WriteReply,
                    request_deserializer=route__guide__pb2.Status.FromString,
                    response_serializer=route__guide__pb2.Status.SerializeToString,
            ),
            'DeleteRequest': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteRequest,
                    request_deserializer=route__guide__pb2.DocumentId.FromString,
                    response_serializer=route__guide__pb2.Status.SerializeToString,
            ),
            'DeleteReply': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteReply,
                    request_deserializer=route__guide__pb2.Status.FromString,
                    response_serializer=route__guide__pb2.Status.SerializeToString,
            ),
            'FetchDocuments': grpc.unary_unary_rpc_method_handler(
                    servicer.FetchDocuments,
                    request_deserializer=route__guide__pb2.DocumentId.FromString,
                    response_serializer=route__guide__pb2.Document.SerializeToString,
            ),
            'getMID': grpc.unary_unary_rpc_method_handler(
                    servicer.getMID,
                    request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                    response_serializer=route__guide__pb2.DocumentId.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'DataNode', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class DataNode(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def AskQuery(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/DataNode/AskQuery',
            route__guide__pb2.Query.SerializeToString,
            route__guide__pb2.Result.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def WriteRequest(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/DataNode/WriteRequest',
            route__guide__pb2.Document.SerializeToString,
            route__guide__pb2.Status.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def WriteReply(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/DataNode/WriteReply',
            route__guide__pb2.Status.SerializeToString,
            route__guide__pb2.Status.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DeleteRequest(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/DataNode/DeleteRequest',
            route__guide__pb2.DocumentId.SerializeToString,
            route__guide__pb2.Status.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DeleteReply(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/DataNode/DeleteReply',
            route__guide__pb2.Status.SerializeToString,
            route__guide__pb2.Status.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def FetchDocuments(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/DataNode/FetchDocuments',
            route__guide__pb2.DocumentId.SerializeToString,
            route__guide__pb2.Document.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def getMID(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/DataNode/getMID',
            google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            route__guide__pb2.DocumentId.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)


class HealthCheckStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Check = channel.unary_unary(
                '/HealthCheck/Check',
                request_serializer=route__guide__pb2.HealthCheckRequest.SerializeToString,
                response_deserializer=route__guide__pb2.HealthCheckResponse.FromString,
                )


class HealthCheckServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Check(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_HealthCheckServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Check': grpc.unary_unary_rpc_method_handler(
                    servicer.Check,
                    request_deserializer=route__guide__pb2.HealthCheckRequest.FromString,
                    response_serializer=route__guide__pb2.HealthCheckResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'HealthCheck', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class HealthCheck(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Check(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/HealthCheck/Check',
            route__guide__pb2.HealthCheckRequest.SerializeToString,
            route__guide__pb2.HealthCheckResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)


class LeaderNoticeStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.MasterChange = channel.unary_unary(
                '/LeaderNotice/MasterChange',
                request_serializer=route__guide__pb2.IsMaster.SerializeToString,
                response_deserializer=route__guide__pb2.Acknowledgement.FromString,
                )


class LeaderNoticeServicer(object):
    """Missing associated documentation comment in .proto file."""

    def MasterChange(self, request, context):
        """rpc by masterbackup to crawler to inform change in master
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_LeaderNoticeServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'MasterChange': grpc.unary_unary_rpc_method_handler(
                    servicer.MasterChange,
                    request_deserializer=route__guide__pb2.IsMaster.FromString,
                    response_serializer=route__guide__pb2.Acknowledgement.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'LeaderNotice', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class LeaderNotice(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def MasterChange(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/LeaderNotice/MasterChange',
            route__guide__pb2.IsMaster.SerializeToString,
            route__guide__pb2.Acknowledgement.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
