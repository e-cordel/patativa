from abc import ABC, abstractmethod
from typing import Dict, List

from models import Cordel


class RepositoryInterface(ABC):
    
    
    def get_cordeis(self) -> List[Cordel]:
        raise NotImplementedError()

    @property
    def base_url(self):
        raise AttributeError()

    def __process(self):
        raise NotImplementedError()
