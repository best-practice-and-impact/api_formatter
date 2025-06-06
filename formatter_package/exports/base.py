from validators.custom_serializer import custom_serialize


class BaseExporter:
    def __init__(self, record):
        self.record = record.to_dict()

    def serializer(self):
        return custom_serialize(self.record)
