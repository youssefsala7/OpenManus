from typing import List

from pydantic import Field
from app.config import config
from app.agent.toolcall import ToolCallAgent
from app.prompt.validator import NEXT_STEP_PROMPT, SYSTEM_PROMPT
from app.tool import Terminate, StrReplaceEditor, Validator, ToolCollection, LatexGenerator
from app.config import config

class PPTAgent(ToolCallAgent):
    """An agent that implements the validate paradigm."""

    name: str = "PPTAgent"
    description: str = "An AI-driven generation agent that produces answer with validation process."

    system_prompt: str = SYSTEM_PROMPT
    next_step_prompt: str = NEXT_STEP_PROMPT

    available_tools: ToolCollection = ToolCollection(
    LatexGenerator(), Validator(),  Terminate()
    )
    special_tool_names: List[str] = Field(default_factory=lambda: [Terminate().name])

    max_steps: int = 30

    working_dir: str = "."
