from functools import wraps

# TODO: Refactor
# def file_logger(function, project_name: str):
#     '''
#     Takes a function as argument, executes the function in a try catch block and logs the exception in error_log.log file if raise any or the function throws any.
#     Also logs the successful function execution with execution time.
#     Parameters:
#         function -> function
#         project_name -> str : Name of the project
#     retunrs:
#         result -> results returned from the executed function
#     '''
#     def wrapper(*args, **kwargs):
#         result = None
#         try:
#             t1 = time.time()
#             result = function(*args, **kwargs)
#             execution_time = time.time() - t1
#             file_error_logger.error(f'{str(function.__name__)}() executed successfully.', extra={'Project name': project_name,
#                                'Execution duration': execution_time, 'log_type': 'Successful execution'})
#         except Exception as e:
#             file_error_logger.error(traceback.format_exc(), extra={'Project name': project_name,
#                                'During': f'{str(function.__name__)}() execution.', 'log_type': 'Error'})
#         return result

#     return wrapper

# TODO: Refactor
# def http_logger(*args, **kwargs):
#     '''
#     Takes a function as argument, executes the function in a try catch block and logs the exception in remote server if raise any or the function throws any.
#     Also logs the successful function execution with execution time.
#     Parameters:
#         function -> function
#         project_name -> str : Name of the project
#     retunrs:
#         result -> results returned from the executed function
#     '''
#     def wrapper(func):
#         result = None
#         logger = RemoteLogger('54.93.244.57','24225', 'health_check.log')
#         try:
#             t1 = time.time()
#             result = func(*args, **kwargs)
#             execution_time = time.time() - t1
#             log = {'message': f'{str(func.__name__)}() executed successfully.', 'Execution duration': execution_time, 'log_type': 'Successful execution'}
#             logger.send_remote_log(log, 'post')
#         except Exception as e:
#             log = {'message': traceback.format_exc(), 'During': f'{str(func.__name__)}() execution.', 'log_type': 'Error'}
#             logger.send_remote_log(log, 'post')
#         return result

#     return wrapper


def log_to_remote():
    pass

def log_to_file():
    pass


def logger(function):
    pass


def file_logger(function, name):
    @wraps(function)
    def wrapper(*args, **kwargs):
        return function(*args, **kwargs)

    return wrapper

def remote_logger(function, name):
    @wraps(function)
    def wrapper(*args, **kwargs):
        return function(*args, **kwargs)

    return wrapper