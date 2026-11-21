


import sys
import unittest.case
from multiprocessing import Value
from unittest.case import _AssertRaisesContext


def in_assert_raises_stack() -> bool:
    print("====IN ASSERT RAISES CHECK====")
    try:
        frame = sys._getframe(1)
        print(f"Got frame: {frame}")
        while frame is not None:
            for val in frame.f_locals.values():
                if isinstance(val, _AssertRaisesContext):
                    print("====FOUND IN ASSERT RAISES CHECK====")
                    return True
            frame = frame.f_back
        
        print("====NOT FOUND IN ASSERT RAISES CHECK====")
        return False
    except BaseException as exc:
        print(f"Exception raised during check: {exc}")
        return False

try:
    import pydevd
    from _pydevd_bundle.pydevd_api import PyDevdAPI
    from debugpy._vendored import force_pydevd

    py_db = pydevd.get_global_debugger()
    if py_db is not None:
        _orig_send = py_db.send_caught_exception_stack

        def _is_inside_assert_raises(frame, exc_type):
            print("====IN ASSET RAISES CHECK====")
            print(f"frame: {frame}")
            while frame is not None:
                print("=========FRAME=========")
                print(f"frame is {type(frame)} ({frame.f_locals.get("self")})")
                print(dir(frame))
                if frame.f_locals:
                    print("=====VALS=====")
                for key, val in frame.f_locals.items():
                    print(f"{key}: {type(val)}")
                    if isinstance(val, unittest.case._AssertRaisesContext):
                        print("===FOUND ASSERT RAISES CONTEXT")
                        print(f"exc_type: {exc_type}, expected: {val.expected}")
                        if issubclass(exc_type, val.expected):
                            return True
                # TOREMOVE either clear up the older try or incorporate it
                frame = frame.f_back
                continue
                
                # Trying with local self back to root
                local_self = frame.f_locals.get("self")
                print(f"AR local self: {local_self}")
                if isinstance(local_self, unittest.case._AssertRaisesContext):
                    if issubclass(exc_type, local_self.expected):
                        return True

                #print("\n".join([
                #    f"back: {frame.f_back}",
                #    f"locals: {frame.f_locals}",
                #    f"line: {frame.f_lineno}",
                #    f"opcodes: {frame.f_trace_opcodes}",
                #    f"trace_lines: {frame.f_trace_lines}",
                #]))
                frame = frame.f_back
                if local_self is not None:
                    print(f"local self is {type(local_self)}")
                    #print(dir(local_self))
            return False

        if any(hasattr(py_db, attr) for attr in ["stop_on_handled_exception", "break_on_caught_exceptions"]):
            if hasattr(py_db, "stop_on_handled_exception"):
                _orig = py_db.stop_on_handled_exception
                print("================= CREATING FILTERED STOP ==================")
                def _filtered_stop(thread, frame, frames_byid, arg):
                    _msg = "IN FILTERED STOP"
                    _ml = (12+len(_msg) + len(_msg) % 2)
                    print(f"{' {_msg} ':*^ml}")
                    print("================ IN FILTERED STOP ===================")
                    exc_type, exc_val, exc_tb = arg
                    if _is_inside_assert_raises(exc_tb.tb_frame if exc_tb else frame, exc_type):
                        return  # Prevents the thread from suspending at all!
                    return _orig_stop(thread, frame, frames_byid, arg)
            else:
                _orig = py_db.break_on_caught_exceptions
                print("================= CREATING FILTERED [break]STOP ==================")
                def _filtered_stop(thread, frame, fames_byid, arg):
                    
                    print("================ IN FILTERED [break] STOP ===================")
                
                PyDevdAPI().remove_all_exception_breakpoints(py_db)
            py_db.stop_on_handled_exception = _filtered_stop
            py_db.add_break_on_exception(
                exception="BaseException",
                condition="not __import__('tests').in_assert_raises_stack()",
                expression="f'Failed on item={item_id} with args={args} and vars={vars(self)}'",
                notify_on_handled_exceptions=True,
                notify_on_unhandled_exceptions=False,
                notify_on_user_unhandled_exceptions= _orig["BaseException"].notify_on_user_unhandled_exceptions,
                notify_on_first_raise_only = _orig["BaseException"].notify_on_first_raise_only,
                ignore_libraries=True,
            )
        else:
            raise ValueError("whut")

except ImportError:
    pass
