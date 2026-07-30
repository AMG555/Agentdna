"""Bounded, policy-gated ReAct planner. It plans; it never gets arbitrary shell access."""
from .policy import authorize
class ReactLoop:
    def __init__(self,max_steps=3): self.max_steps=max_steps
    def plan(self, goal, context, confirmed=False):
        # Deterministic plan shell; LLMs may fill language, never tool permissions.
        tool='show_suggestion'; argument=f'{goal} | context: {context}'
        allowed,reason=authorize(tool,argument,confirmed)
        return {'goal':goal,'steps':[{'tool':tool,'argument':argument,'authorized':allowed,'reason':reason}], 'max_steps':self.max_steps}
react=ReactLoop()
