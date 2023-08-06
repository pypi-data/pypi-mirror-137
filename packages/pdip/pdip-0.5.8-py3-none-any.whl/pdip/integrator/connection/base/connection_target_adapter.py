from abc import abstractmethod
from typing import List

from ...integration.domain.base import IntegrationBase


class ConnectionTargetAdapter:
    def clear_data(
            self,
            integration: IntegrationBase
    ) -> int:
        pass

    @abstractmethod
    def prepare_insert_row(
            self,
            data,
            columns
    ):
        pass

    @abstractmethod
    def prepare_data(
            self,
            integration: IntegrationBase,
            source_data: any
    ) -> List[any]:
        pass

    @abstractmethod
    def prepare_target_query(
            self,
            integration: IntegrationBase
    ) -> str:
        pass

    @abstractmethod
    def write_target_data(
            self,
            integration: IntegrationBase,
            prepared_data: List[any]
    ) -> int:
        pass

    @abstractmethod
    def do_target_operation(
            self,
            integration: IntegrationBase
    ) -> int:
        pass
