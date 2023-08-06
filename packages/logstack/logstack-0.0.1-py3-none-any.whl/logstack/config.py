SCHEME = 'http'
ENDPOINT = '54.93.244.57'
PORT = '24225'

REMOTE_LOGSTACK_SERVER = f"{SCHEME}://{ENDPOINT}:{PORT}/"

# DJANGO_CONFIG = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         'backend': {
#             'format': '{asctime} {levelname} {message}',
#             'style': '{',
#         },
#         'json':{
#             '()': 'json_log_formatter.JSONFormatter',
#         },
#     },
#     'filters': {
#         'require_debug_true': {
#             '()': 'django.utils.log.RequireDebugTrue',
#         },
#     },
#     'handlers': {
#         'file_debug': self.file_debug_handler_setting,
#         'file_error': self.file_error_handler_setting,
#         'console': self.console_handler_setting
#     },
#     'loggers': {
#         '': {
#             'handlers': ['file_debug'],
#             'level': 'DEBUG',
#             'propagate': False,
#         },
#         'file_error_logger': {
#             'handlers': ['file_error'],
#             'level': 'ERROR',
#             'propagate': False
#         },
#     }
# }