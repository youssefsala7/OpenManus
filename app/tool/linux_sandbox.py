from typing import Optional
from app.tool.base import BaseTool, ToolResult
from app.config import config

class LinuxSandboxTool(BaseTool):
    """A tool to start an e2b DesktopSandbox and return the VNC URL, using config.cloud_sandbox for credentials."""

    name: str = "linux_sandbox"
    description: str = (
        "Starts an e2b DesktopSandbox and returns the VNC URL. "
        "API key and domain are read from config.cloud_sandbox."
    )
    parameters: dict = {"type": "object", "properties": {}, "required": []}

    async def execute(self, **kwargs) -> ToolResult:
        """
        Start an e2b DesktopSandbox and return the VNC URL, using config.cloud_sandbox.
        """
        try:
            from e2b_desktop import Sandbox as DesktopSandbox
        except ImportError:
            return ToolResult(error="e2b_desktop is not installed. Please install it via pip.")
        sandbox_config = getattr(config, "cloud_sandbox", None)
        if not sandbox_config or not sandbox_config.get("api_key") or not sandbox_config.get("domain"):
            return ToolResult(error="cloud_sandbox config missing or incomplete. Please set api_key and domain in config.cloud_sandbox.")
        try:
            desktop = DesktopSandbox(api_key=sandbox_config["api_key"], domain=sandbox_config["domain"])
            desktop.stream.start()
            url = desktop.stream.get_url()
            return ToolResult(output={
                "status": "started",
                "vnc_url": url,
                "domain": sandbox_config["domain"],
            })
        except Exception as e:
            return ToolResult(error=f"Failed to start e2b DesktopSandbox: {e}")
