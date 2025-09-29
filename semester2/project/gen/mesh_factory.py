from abc import ABC, abstractmethod
from gen.mesh import Mesh


# Abstract Factory class for Meshes
class MeshFactory(ABC):
    def __init__(self):
        pass

    @abstractmethod
    # def get_mesh(self, *args, **kwargs) -> Mesh:
    def get_mesh(self, *args) -> Mesh:
        pass
