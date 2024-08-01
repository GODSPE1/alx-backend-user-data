#!/usr/bin/env python3
"""
filtered_logger function
"""
import logging
import re
import os
import mysql.connector
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """
    Returns the log message obfuscated by replacing the values of
    specified fields.

    Args:
        fields (List[str]): A list of str representing all fields to obfuscate.
        redaction (str): A str repr by what the field will be obfuscated.
        message (str): A str repr the log line.
        separator (str): A str repr the character separating all fields
                         in the log line.

    Returns:
        str: The obfuscated log message.
    """
    pattern = '|'.join(
        f'(?<={field}=)[^{separator}]+' for field in fields)
    return re.sub(pattern, redaction, message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Initialize the formatter with the given fields.

        Args:
            fields (List[str]): A list of str repr all fields to obfuscate.
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record by obfuscating the specified fields.

        Args:
            record (logging.LogRecord): The log record to format.

        Returns:
            str: The formatted and obfuscated log message.
        """
        record.msg = filter_datum(self.fields, self.REDACTION, record.msg,
                                  self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)


PII_FIELDS = ("name", "email", "phone", "ssn", "password")




if __name__ == "__main__":
    main()
