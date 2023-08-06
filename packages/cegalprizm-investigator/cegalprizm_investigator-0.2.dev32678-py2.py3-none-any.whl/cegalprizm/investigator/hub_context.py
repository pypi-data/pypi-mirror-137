# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.

"""This file contains the definition of the InvPyHubContext class

This class is used internally to interact with a Hub connection
"""

from typing import Dict, Iterable

from google.protobuf.any_pb2 import Any

from cegalprizm.hub import PetrelContext, ConnectorFilter, ConnectionParameters, Hub, HubClient

# pylint: disable=relative-beyond-top-level
# pylint: disable=logging-fstring-interpolation

from . import logger

_VERIFY_PAYLOADS: str = "investigator.ListInvestigations"

class InvPyHubContext():

    def __init__(self, hub_petrel_context: PetrelContext = None, hub_connection_parameters: ConnectionParameters = None):
        logger.debug("Creating InvPyHubContext")
        self._hub_client = None
        self._original_connection_parameters = None
        self._connection_parameters = None
        self._connector_filter = None
        self._wellknown_connector_identifier = None

        if hub_petrel_context is not None:
            self._original_connection_parameters = hub_petrel_context.connection_parameters
            self._connector_filter = hub_petrel_context.connector_filter
        elif hub_connection_parameters is not None:
            self._original_connection_parameters = hub_connection_parameters
            self._connector_filter = ConnectorFilter()
        else:
            self._original_connection_parameters = ConnectionParameters()
            self._connector_filter = ConnectorFilter()

        self._check_hub_status()

    def _check_hub_status(self)->bool:
        try:
            logger.debug("Checking Hub status")
            connection_parameters = self._connection_parameters if self._connection_parameters else self._original_connection_parameters
            hub = Hub(connection_parameters=connection_parameters)
            server_status = hub.query_server()
            if server_status.license == "Basic":
                logger.debug("Connected to CegalHub server in basic mode - Only unlicensed API is available")
                self._connection_parameters = self._original_connection_parameters
            else:
                logger.debug("Full API available if Keystone licensing permits it")
                self._connection_parameters = ConnectionParameters(host=self._original_connection_parameters.host,
                                                                    port=self._original_connection_parameters.port,
                                                                    use_tls=self._original_connection_parameters.use_tls,
                                                                    use_auth=True)
            self._set_target_connector()
            return True
        except Exception as e:
            logger.debug(e)
            logger.debug("Do not use Keystone licensing")
            self._connection_parameters = self._original_connection_parameters
            return False

    def _set_target_connector(self)->bool:
        try:
            if self._find_target_connector("cegal.hub.petrel", False):
                return True

            if self._find_target_connector("cegal.investigator", False):
                return True

            if self._find_target_connector("cegal.investigator", True):
                return True

            logger.warning("No target connector found")
            return False
        except:
            logger.warning("No target connector found")
            return False

    def _find_target_connector(self, wellknown_identifier: str, check_public: bool)->bool:
        connection_parameters = self._connection_parameters if self._connection_parameters else self._original_connection_parameters
        hub = Hub(connection_parameters=connection_parameters)
        if len(self._connector_filter.target_connector_id) > 0:
            for conn in hub.query_connectors():
                if conn.connector_id == self._connector_filter.target_connector_id:
                    if _VERIFY_PAYLOADS in conn.supported_payloads.keys():
                        logger.info(f"Connector {conn.wellknown_identifier}: {conn.connector_id}")
                        self._wellknown_connector_identifier = conn.wellknown_identifier
                        return True
            logger.warning(f"Connector {self._connector_filter.target_connector_id} cannot be used with cegalprizm.investigator")
            return False

        for conn in hub.query_connectors():
            if conn.wellknown_identifier == wellknown_identifier:
                if check_public:
                    if conn.supports_public_requests:
                        if _VERIFY_PAYLOADS in conn.supported_payloads.keys():
                            logger.info(f"Public {wellknown_identifier}: {conn.connector_id}")
                            self._connector_filter.target_connector_id = conn.connector_id
                            self._wellknown_connector_identifier = wellknown_identifier
                            return True
                else:
                    if not conn.supports_public_requests:
                        if _VERIFY_PAYLOADS in conn.supported_payloads.keys():
                            logger.info(f"Private {wellknown_identifier}: {conn.connector_id}")
                            self._connector_filter.target_connector_id = conn.connector_id
                            self._wellknown_connector_identifier = wellknown_identifier
                            return True
        return False

    def _client(self) -> HubClient:
        if self._hub_client is None:
            logger.debug("Creating new HubClient")
            self._check_hub_status()
            self._hub_client = HubClient(connection_parameters=self._connection_parameters)
        return self._hub_client

    def force_new(self):
        self._hub_client = None

    def set_connector_labels(self, labels: Dict[str, str]):
        self._connector_filter.labels = labels
        self._hub_client = None

    def do_unary_request(self, wellknown_payload_identifier: str, payload: Any, wellknown_connector_identifier: str = None):
        if wellknown_connector_identifier is None:
            wellknown_connector_identifier = self._wellknown_connector_identifier

        logger.debug(f"do_unary_request: {wellknown_payload_identifier}")
        result = self._client().do_unary_request(wellknown_connector_identifier=wellknown_connector_identifier,
                                                 wellknown_payload_identifier=wellknown_payload_identifier,
                                                 payload=payload,
                                                 connector_filter=self._connector_filter)
        if result[0]:
            logger.debug("Success")
        else:
            logger.debug(f"Failed: {result[1]}")
        return result

    def do_client_streaming(self, wellknown_payload_identifier: str, iter_payloads: Iterable[Any]):
        logger.debug(f"do_client_streaming: {wellknown_payload_identifier}")
        result = self._client().do_client_streaming(wellknown_connector_identifier=self._wellknown_connector_identifier,
                                                    wellknown_payload_identifier=wellknown_payload_identifier,
                                                    iterable_payloads=iter_payloads,
                                                    connector_filter=self._connector_filter)
        if result[0]:
            logger.debug("Success")
        else:
            logger.debug(f"Failed: {result[1]}")
        return result

    def do_server_streaming(self, wellknown_payload_identifier: str, payload: Any):
        logger.debug(f"do_server_streaming: {wellknown_payload_identifier}")
        return self._client().do_server_streaming(wellknown_connector_identifier=self._wellknown_connector_identifier,
                                                  wellknown_payload_identifier=wellknown_payload_identifier,
                                                  payload=payload,
                                                  connector_filter=self._connector_filter)
                                                      