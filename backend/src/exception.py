import sys
import traceback


def error_message_detail(error, error_detail):
    exc_type, exc_value, exc_tb = error_detail.exc_info()

    if exc_tb is None:
        return str(error)

    file_name = exc_tb.tb_frame.f_code.co_filename
    line_number = exc_tb.tb_lineno

    return (
        f"Error occurred in script [{file_name}] "
        f"at line number [{line_number}] "
        f"error message [{error}]"
    )


class CustomException(Exception):
    def __init__(self, error_message, error_detail=sys):
        super().__init__(str(error_message))

        self.error_message = error_message_detail(
            error_message,
            error_detail
        )

        self.traceback = traceback.format_exc()

    def __str__(self):
        return f"{self.error_message}\n\n{self.traceback}"