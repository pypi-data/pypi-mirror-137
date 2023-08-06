from tracepointdebug.tracepoint.coded_error import CodedError

UNKNOWN = CodedError(0, "Unknown")

TRACEPOINT_ALREADY_EXIST = CodedError(1004, "Tracepoint has been already added in file {} on line {} from client {}")

INSTRUMENTATION_IS_NOT_ACTIVE = CodedError(1000,
                                           "Couldn't activate instrumentation support." +
                                           " So custom tracepoints is not supported")
UNABLE_TO_FIND_MODULE = CodedError(1002, "Unable to find module")

LINE_NO_IS_NOT_AVAILABLE = CodedError(1005, "Line {} is not available in {} for tracepoint")
LINE_NO_IS_NOT_AVAILABLE_2 = CodedError(1005, "Line {} is not available in {} for tracepoint. Try line {}")
LINE_NO_IS_NOT_AVAILABLE_3 = CodedError(1005, "Line {} is not available in {} for tracepoint. Try lines {} or {}")
NO_TRACEPOINT_EXIST = CodedError(1006, "No tracepoint could be found in file {} on line {} from client {}")
NO_TRACEPOINT_EXIST_WITH_ID = CodedError(1009, "No tracepoint could be found with id {} from client {}")
CLIENT_HAS_NO_ACCESS_TO_TRACEPOINT = CodedError(1010, "Client {} has no access to tracepoint with id {}")

PUT_TRACEPOINT_FAILED = CodedError(
    1050,
    "Error occurred while putting tracepoint to file {} on line {} from client {}: {}")

SOURCE_CODE_MISMATCH_DETECTED = CodedError(
    1051,
    "Source code mismatch detected while putting tracepoint to file {} on line {} from client {}")

UPDATE_TRACEPOINT_FAILED = CodedError(
    1100,
    "Error occurred while updating tracepoint to file {} on line {} from client {}: {}")

UPDATE_TRACEPOINT_WITH_ID_FAILED = CodedError(
    1101,
    "Error occurred while updating tracepoint with id {} from client {}: {}")

REMOVE_TRACEPOINT_FAILED = CodedError(
    1150,
    "Error occurred while removing tracepoint from file {} on line {} from client {}: {}")

REMOVE_TRACEPOINT_WITH_ID_FAILED = CodedError(
    1151,
    "Error occurred while removing tracepoint with id {} from client {}: {}")

ENABLE_TRACEPOINT_FAILED = CodedError(
    1200,
    "Error occurred while enabling tracepoint to file {} on line {} from client {}: {}")

ENABLE_TRACEPOINT_WITH_ID_FAILED = CodedError(
    1201,
    "Error occurred while enabling tracepoint with id {} from client {}: {}")

DISABLE_TRACEPOINT_FAILED = CodedError(
    1250,
    "Error occurred while disabling tracepoint to file {} on line {} from client {}: {}")

DISABLE_TRACEPOINT_WITH_ID_FAILED = CodedError(
    1251,
    "Error occurred while disabling tracepoint with id {} from client {}: {}")

CONDITION_CHECK_FAILED = CodedError(
    1900,
    "Error occurred while checking condition '{}': {}")

CONDITION_EXPRESSION_SYNTAX_CHECK_FAILED = CodedError(
    1901,
    "Syntax check failed while checking condition '{}': {}")

UNABLE_TO_FIND_PROPERTY_FOR_CONDITION = CodedError(
    1904,
    "Unable to find property over file {} while evaluating condition: {}")
