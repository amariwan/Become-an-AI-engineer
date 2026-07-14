# Human-in-the-Loop Pattern
# Quelle: chapters/09_ai_agenten.tex (Zeile 1062)
class HITLManager:
    def __init__(self):
        self.pending_approvals = {}

    def request_approval(self, action: str, context: dict) -> str:
        approval_id = str(uuid.uuid4())
        self.pending_approvals[approval_id] = {
            "action": action,
            "context": context,
            "status": "pending",
        }
        # Benachrichtigung an Slack / Teams / E-Mail
        notify_human({
            "type": "agent_approval",
            "approval_id": approval_id,
            "action": action,
            "context": context,
        })
        return approval_id

    def approve(self, approval_id: str) -> bool:
        if approval_id in self.pending_approvals:
            self.pending_approvals[approval_id]["status"] = "approved"
            return True
        return False

    def reject(self, approval_id: str) -> bool:
        if approval_id in self.pending_approvals:
            self.pending_approvals[approval_id]["status"] = "rejected"
            return True
        return False

    def wait_for_approval(self, approval_id: str,
                          timeout: int = 300) -> bool:
        start = time.time()
        while time.time() - start < timeout:
            status = self.pending_approvals[approval_id]["status"]
            if status == "approved":
                return True
            if status == "rejected":
                return False
            time.sleep(1)
        return False  # Timeout

