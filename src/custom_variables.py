from enum import Enum

class DatasetType(Enum):
    FILTERABLE = "filterable",
    CANTABULAR_FLEXIBLE_TABLE = "cantabular_flexible_table",
    CANTABULAR_MULTIVARIATE_TABLE = "cantabular_multivariate_table",
    STATIC = "static"
    
    @classmethod
    def _missing_(cls, value):
        return ""
    
class AlterType(Enum):
    ALERT = "alert",
    CORRECTION = "correction"
    
    @classmethod
    def _missing_(cls, value):
        return ""
    
class QualityDesignation(Enum):
    ACCREDITED_OFFICAL = "accredited-offical",
    OFFICIAL = "official",
    OFFICIAL_IN_DEVELOPMENT = "offical-in-development"
    
    @classmethod
    def _missing_(cls, value):
        return ""
    
class DistributionFormat(Enum):
    CSV = "csv",
    SDMX = "sdmx",
    XLS = "xls",
    XLSX = "xlsx",
    CSDB = "csdb"
    
    @classmethod
    def _missing_(cls, value):
        return ""
    
class MediaType(Enum):
    CSV = "text/csv",
    SDMX = "application/vnd.sdmx.structurespecficdata+xml",
    XLS = "application/vnd.ms-excel",
    XLSX = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    CSDB = "text/plain"
    
    @classmethod
    def _missing_(cls, value):
        return ""