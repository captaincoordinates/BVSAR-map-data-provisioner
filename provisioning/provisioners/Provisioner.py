from abc import ABC, abstractmethod
import pyproj

class Provisioner(ABC):

    srcCrs=pyproj.Proj("+init=EPSG:4326")
    mapUnitsPerInch=0.0254

    @abstractmethod
    def provision(self, minX, minY, maxX, maxY, outputDirectory, environmentConfig):
        pass
