from abc import ABC, abstractmethod
from decimal import Decimal
from enum import Enum
from typing import Union, Any, List, Dict, Callable
from dataclasses import dataclass

from zpy.logger import zL


def show_info(fn: str, params: Union[List[Any], Dict[Any, Any]], ret_type: Enum, v_model):
    print("\n|-------------------------------------------------|\n")
    print(f"   Function Called: {fn} ")
    print("            Params: {}".format(params))
    print("       Return Type: {}".format(ret_type.name))
    print(f"        Ref  Model: {v_model}")
    print("\n|-------------------------------------------------|\n")


@dataclass
class ZDBConfig:
    user: str
    password: str
    database: str
    host: str
    port: int = 3306
    autocommit: bool = False
    raise_on_warnings = True
    service: str = None  # Use for Oracle


parser_types = [
    None,
    lambda x: float(x),
    lambda x: str(x),
    lambda x: int(x),
    lambda x: Decimal(str(x).strip(' "')),
    lambda x: bool(x),
]


class DBTypes(Enum):
    cursor = 1
    float = 2
    string = 3
    integer = 4
    decimal = 5
    bool = 6


def get_map_type(r_type: DBTypes) -> Callable:
    return parser_types[r_type.value - 1]


def build_params(dict_params: dict, list_params: List[Any]) -> List[Any]:
    if dict_params is not None:
        return list(dict_params.values())
    if list_params is not None:
        return list_params
    return []


def process_exception(throw: bool, e: Exception):
    if throw is True:
        raise e
    zL.e("Failed when try to call function or stored procedure.", exc_info=e)


class ZDatabase(ABC):
    @classmethod
    @abstractmethod
    def setup(cls, config: dict, verbose: bool = False):
        """
        Setup connection arguments using dictionary
        """
        ...

    @classmethod
    @abstractmethod
    def setup_of(cls, config: ZDBConfig, verbose: bool = False):
        """
        Setup connection data
        """
        ...

    @classmethod
    @abstractmethod
    def from_of(cls, user: str, password: str, host: str, db_name: str, verbose: bool = False):
        """
        Setup connection data
        """
        ...

    def new_connect(self) -> Any:
        ...

    def __validate_config(self) -> Union[dict, str]:
        ...

    def call(self, name: str, ret_type: DBTypes, params: dict = None, list_params: List[Any] = None, model: Any = None,
             connection=None, jsonfy: bool = False, throw=False) -> Any:
        """Stored procedure caller

        Args:
            name (str): Stored procedure name
            ret_type (DBTypes): Type of data returned from stored procedure
            params (dict, optional): params for the procedure. Defaults to None.
            list_params (List[Any], optional): positional list params to the procedure. Defaults to None.
            model (Any, optional): model for build returned data. Defaults to None.
            connection ([type], optional): connection database. Defaults to None.
            jsonfy (bool, optional): return data in dict format if model is null. Defaults to False.
            throw (bool,optional)

        Returns:
            Any: processed data
        """
        ...

    def exec(self, fn_name: str, ret_type: DBTypes, params: dict = None, list_params: List[Any] = None,
             model: Any = None,
             connection=None, jsonfy: bool = False, throw=False) -> Any:
        """Function executor

        Args:
            fn_name (str): Stored procedure name
            ret_type (DBTypes): Type of data returned from stored procedure
            params (dict, optional): params for the procedure. Defaults to None.
            list_params (List[Any], optional): positional list params to the procedure. Defaults to None.
            model (Any, optional): model for build returned data. Defaults to None.
            connection ([type], optional): connection database. Defaults to None.
            jsonfy (bool, optional): return data in dcit format if model is null. Defaults to False.
            throw (bool,optional)
        Returns:
            Any: processed data
        """
        ...

    @abstractmethod
    def init_local_client(self, path: str):
        """
        Initialize local client
        """
        ...

    @abstractmethod
    def connect(self):
        ...

    @abstractmethod
    def close(self) -> None:
        ...

    @abstractmethod
    def is_connected(self) -> bool:
        ...

    @abstractmethod
    def get_connection(self) -> Any:
        ...


class ZDBPool(ABC):

    @abstractmethod
    def setup_db(self, db: ZDatabase) -> None:
        ...

    @abstractmethod
    def get_db(self):
        ...

    @abstractmethod
    def setup_extras(self, config: dict) -> None:
        ...

    @abstractmethod
    def get_pool_connection(self) -> Any:
        ...

    @abstractmethod
    def release_connection(self, connection) -> bool:
        ...

    @abstractmethod
    def close_pool(self):
        pass

    @abstractmethod
    def initialize_pool(
            self,
            max_connections: int = 5,
            min_connections: int = 1,
    ) -> bool:
        ...
