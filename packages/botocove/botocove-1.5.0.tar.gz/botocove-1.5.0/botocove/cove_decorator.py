import functools
import logging
from dataclasses import asdict
from typing import Any, Callable, Dict, List, Optional

from boto3.session import Session

from botocove.cove_host_account import CoveHostAccount
from botocove.cove_runner import CoveRunner
from botocove.cove_types import CoveOutput, CoveSessionInformation, R

logger = logging.getLogger(__name__)


def dataclass_converter(d: CoveSessionInformation) -> Dict[str, Any]:
    """Unpack dataclass into dict and remove None values"""
    return {k: v for k, v in asdict(d).items() if v is not None}


def cove(
    _func: Optional[Callable[..., R]] = None,
    *,
    target_ids: Optional[List[str]] = None,
    ignore_ids: Optional[List[str]] = None,
    rolename: Optional[str] = None,
    role_session_name: Optional[str] = None,
    policy: Optional[str] = None,
    policy_arns: Optional[List[str]] = None,
    assuming_session: Optional[Session] = None,
    raise_exception: bool = False,
    org_master: bool = True,
    thread_workers: int = 20
) -> Callable:
    def decorator(func: Callable[..., R]) -> Callable[..., CoveOutput]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> CoveOutput:

            host_account = CoveHostAccount(
                target_ids=target_ids,
                ignore_ids=ignore_ids,
                rolename=rolename,
                role_session_name=role_session_name,
                policy=policy,
                policy_arns=policy_arns,
                org_master=org_master,
                assuming_session=assuming_session,
            )

            runner = CoveRunner(
                host_account=host_account,
                func=func,
                raise_exception=raise_exception,
                func_args=args,
                func_kwargs=kwargs,
                thread_workers=thread_workers,
            )

            output = runner.run_cove_function()

            # Rewrite dataclasses into untyped dicts to retain current functionality
            return CoveOutput(
                Results=[dataclass_converter(r) for r in output["Results"]],
                Exceptions=[
                    dataclass_converter(e)
                    for e in output["Exceptions"]
                    if e.AssumeRoleSuccess
                ],
                FailedAssumeRole=[
                    dataclass_converter(f)
                    for f in output["Exceptions"]
                    if not f.AssumeRoleSuccess
                ],
            )

        return wrapper

    # Handle both bare decorator and with argument
    if _func is None:
        return decorator
    else:
        return decorator(_func)
