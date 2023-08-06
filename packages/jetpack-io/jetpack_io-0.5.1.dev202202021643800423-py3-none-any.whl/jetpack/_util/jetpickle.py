from typing import Any, Protocol, cast

import jsonpickle
import tblib


def encode(val: Any) -> bytes:
    if isinstance(val, BaseException):
        val = _pickle_prep_exception(val)
    return bytes(jsonpickle.encode(val), "utf-8")


def decode(val: bytes) -> Any:
    decoded = jsonpickle.decode(val)
    if isinstance(decoded, BaseException):
        decoded = _unpickle_prep_exception(decoded)
    return decoded


class ExceptionWithJetpackFields(Protocol):
    jetpack_traceback: Any
    jetpack_cause: Any
    __cause__: Any
    __traceback__: Any


# pickle_prep_exception prepares the python exception object for json_pickling. It does
# this by converting the native C-object at exception.__traceback__ to be a
# python dict. It does this recursively by following the exception chain via
# exception.__cause__. The "prepared exception" objects are stored at
# `.jetpack_traceback` and `.jetpack_cause` fields.
def _pickle_prep_exception(err: BaseException) -> BaseException:
    error = cast(ExceptionWithJetpackFields, err)
    error.jetpack_traceback = tblib.Traceback(err.__traceback__).to_dict()

    error.jetpack_cause = None
    if err.__cause__ is not None:
        error.jetpack_cause = _pickle_prep_exception(err.__cause__)

    return err


# unpickle_prep_exception undoes the changes in pickle_prep_exception, and sets the
# jetpack-specific fields on the exceptin object to None
def _unpickle_prep_exception(err: BaseException) -> BaseException:
    error = cast(ExceptionWithJetpackFields, err)
    err.__traceback__ = tblib.Traceback.from_dict(
        error.jetpack_traceback
    ).as_traceback()

    if error.jetpack_cause is not None:
        err.__cause__ = _unpickle_prep_exception(error.jetpack_cause)
        error.jetpack_cause = None

    error.jetpack_traceback = None
    return err
