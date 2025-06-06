from .base import SafeEnum


class AlertType(SafeEnum):
    ALERT = "alert"
    CORRECTION = "correction"


class DatasetType(SafeEnum):
    FILTERABLE = "filterable"
    CANTABULAR_FLEXIBLE_TABLE = "cantabular_flexible_table"
    CANTABULAR_MULTIVARIATE_TABLE = "cantabular_multivariable_table"
    STATIC = "static"


class DistributionFormat(SafeEnum):
    CSV = "csv"
    SDMX = "sdmx"
    XLS = "xls"
    XLSX = "xlsx"
    CSDB = "csdb"



class MediaType(SafeEnum):
    CSV = "text/csv"
    SDMX = "application/vnd.sdmx.structurespecficdata+xml"
    XLS = "application/vnd.ms-excel"
    XLSX = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    CSDB = "text/plain"



class QualityDesignation(SafeEnum):
    ACCREDITED_OFFICIAL = "accredited-official"
    OFFICIAL = "official"
    OFFICIAL_IN_DEVELOPMENT = "official-in-development"



VALIDATION_SCHEMA = {
    "dataset": {
        "id": {"type": "string", "required": True},
        "type": {"type": "enum", "enum": DatasetType, "required": True},
        "title": {"type": "string", "required": True},
        "description": {"type": "string", "required": True},
        "topic": {"type": "string", "required": True},
        "last_updated": {"type": "datetime", "required": True, "auto": True},
        "license": {"type": "string", "required": True, "default": "Open Government License v3.0"},
        "next_release": {"type": "string", "required": False},
        "keyword": {"type": "string", "required": False},
        "qmi": {
            "href": {"type": "string", "required": True}
        },
        "contact": {
            "name": {"type": "string", "required": True},
            "email": {"type": "string", "required": True},
            "telephone": {"type": "string", "required": False},
        },
        "publisher": {
            "name": {"type": "string", "required": True},
            "href": {"type": "string", "required": True}
        }
    },

    "edition": {
        "dataset_id": {"type": "string", "required": True, "source": "path"},
        "edition": {"type": "string", "required": True, "source": "path"},
        "edition_title": {"type": "string", "required": True},
        "release_date": {"type": "datetime", "required": True},
        "version": {"type": "int", "required": True, "auto": True},
        "last_updated": {"type": "datetime", "required": False},
        "quality_designation": {"type": "enum", "enum": QualityDesignation, "required": False},

        "usage_note": {
            "title": {"type": "string", "required": True},
            "note": {"type": "string", "required": True}
        },

        "alert": {
            "title": {"type": "enum", "enum": AlertType, "required": True},
            "date": {"type": "datetime", "required": True},
            "description": {"type": "string", "required": True}
        },
        "distribution": {
            "title": {"type": "string", "required": True},
            "format": {"type": "enum", "enum": DistributionFormat, "required": True},
            "download_url": {"type": "string", "required": True, "auto": True},
            "byte_size": {"type": "int", "required": True},
            "media_type": {"type": "enum", "enum": MediaType, "required": True}
        }
    }
}




