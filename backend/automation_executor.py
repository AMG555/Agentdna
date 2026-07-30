"""Preview-only automation executor. Real OS actions require explicit adapters and confirmation."""
from .reasoning.policy import authorize
class AutomationExecutor:
    def preview(self,tool,argument):
        allowed,reason=authorize(tool,argument,confirmed=False)
        return {'tool':tool,'argument':argument,'allowed':allowed,'reason':reason,'requires_confirmation':True,'executed':False}
    def execute(self,tool,argument,confirmed=False):
        allowed,reason=authorize(tool,argument,confirmed)
        if not allowed: return {'executed':False,'reason':reason,'requires_confirmation':True}
        # Deliberately no native side effects until a platform adapter is installed.
        return {'executed':False,'reason':'native_adapter_not_installed','requires_confirmation':False,'preview':True}
executor=AutomationExecutor()
