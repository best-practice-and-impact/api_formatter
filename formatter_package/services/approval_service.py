from models.file_record import UploadStatus
from datetime import datetime
from models.user import Role
from helpers.request.client import Client

class ApprovalService:
    def approve(self, record, approver):
        if approver.role != Role.APPROVER:
            raise PermissionError("Only approvers can approve records.")

        if record.status != UploadStatus.PENDING:
            raise ValueError("Only pending records can be approved.")

        record.status = UploadStatus.APPROVED
        record.approved_by = approver

        return record


    def send_to_external_api(self, metadata):
        # TODO: Implement actual API call here
        print("Sending approved metadata to external API...")
        #Client.post("https://api.example.com/approve", json=metadata)
