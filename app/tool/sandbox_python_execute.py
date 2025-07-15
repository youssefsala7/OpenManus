from dotenv import load_dotenv
load_dotenv()
from typing import Dict
from app.tool.base import BaseTool
import asyncio
import multiprocessing
import sys
from io import StringIO
from app.config import config

class SandboxPythonExecute(BaseTool):
    """A tool for executing Python code either locally (with timeout) or in a sandboxed environment using e2b_code_interpreter."""

    name: str = "python_execute"
    description: str = (
        "Executes Python code string. Note: Only print outputs are visible, function return values are not captured. Use print statements to see results. "
        "Set mode='sandbox' to run in a secure sandbox (e2b), otherwise runs locally."
    )
    parameters: dict = {
        "type": "object",
        "properties": {
            "code": {
                "type": "string",
                "description": "The Python code to execute.",
            },
            "mode": {
                "type": "string",
                "enum": ["local", "sandbox"],
                "description": "Execution mode: 'local' (default) or 'sandbox' (e2b sandbox)",
            },
            "timeout": {
                "type": "integer",
                "description": "Execution timeout in seconds (default: 5 for local, 10 for sandbox)",
            },
        },
        "required": ["code"],
    }

    def _run_code(self, code: str, result_dict: dict, safe_globals: dict) -> None:
        original_stdout = sys.stdout
        try:
            output_buffer = StringIO()
            sys.stdout = output_buffer
            exec(code, safe_globals, safe_globals)
            result_dict["observation"] = output_buffer.getvalue()
            result_dict["success"] = True
        except Exception as e:
            result_dict["observation"] = str(e)
            result_dict["success"] = False
        finally:
            sys.stdout = original_stdout

    async def execute(
        self,
        code: str,
        timeout: int = None,
        mode: str = "local",
    ) -> Dict:
        """
        Executes the provided Python code in the selected environment.
        Args:
            code (str): The Python code to execute.
            timeout (int): Execution timeout in seconds.
            mode (str): 'local' or 'sandbox'.
        Returns:
            Dict: Contains 'observation' with execution output or error message and 'success' status.
        """
        if mode == "sandbox":
            # Use e2b_code_interpreter Sandbox
            try:
                from e2b_code_interpreter import Sandbox
            except ImportError:
                return {"observation": "e2b_code_interpreter not installed.", "success": False}
            # Get sandbox config from app.config.config
            sandbox_config = getattr(config, "cloud_sandbox", {})
            # You can pass config to Sandbox() if needed, e.g. Sandbox(api_key=sandbox_config.get("api_key"))
            sbx = Sandbox(**sandbox_config) if sandbox_config else Sandbox()
            try:
                # Default timeout for sandbox is 10s if not set
                effective_timeout = timeout if timeout is not None else 10
                async def run():
                    execution = sbx.run_code(code)
                    logs = execution.logs if hasattr(execution, 'logs') else str(execution)
                    success = execution.error is None if hasattr(execution, 'error') else True
                    observation = logs
                    if not success:
                        observation = f"Error: {getattr(execution, 'error', 'Unknown error')}\n{logs}"
                    return {"observation": observation, "success": success}
                result = await asyncio.wait_for(run(), timeout=effective_timeout)
                return result
            except asyncio.TimeoutError:
                return {"observation": f"Execution timeout after {effective_timeout} seconds", "success": False}
            except Exception as e:
                return {"observation": str(e), "success": False}
            finally:
                sbx.kill()
        else:
            # Local execution (default)
            effective_timeout = timeout if timeout is not None else 5
            with multiprocessing.Manager() as manager:
                result = manager.dict({"observation": "", "success": False})
                if isinstance(__builtins__, dict):
                    safe_globals = {"__builtins__": __builtins__}
                else:
                    safe_globals = {"__builtins__": __builtins__.__dict__.copy()}
                proc = multiprocessing.Process(
                    target=self._run_code, args=(code, result, safe_globals)
                )
                proc.start()
                proc.join(effective_timeout)
                if proc.is_alive():
                    proc.terminate()
                    proc.join(1)
                    return {
                        "observation": f"Execution timeout after {effective_timeout} seconds",
                        "success": False,
                    }
                return dict(result)
