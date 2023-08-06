#usage
##install
```
pip install xdj-utils
```
##setting
###additional
```
USERNAME_FIELD = 'username'
ROLE_MODEL = 'xdj_system.Role'
DEFAULT_ROLE = ['']
ANONYMOUS_ROLE = ['']
```
###modification
```
USERNAME_FIELD = 'username'
ROLE_MODEL = 'xdj_system.Role'
DEFAULT_ROLE = ['']
ANONYMOUS_ROLE = ['']

#settings for modifying
MIDDLEWARE = [
    ...
    xdj_utils.middleware.ApiLoggingMiddleware
]

REST_FRAMEWORK = {
    ...
    'DEFAULT_FILTER_BACKENDS':(
        'xdj_utils.filters.CustomDjangoFilterBackend',
        ...
    ),
    'DEFAULT_PAGINATION_CLASS': 'xdj_utils.pagination.CustomPagination',
    'DEFAULT_AUTHENTICATION_CLASSES':(
        ...
        'xdj_utils.authentications.AnonymousAuthenticated',
    ),
    'EXCEPTION_HANDLER': 'xdj_utils.exception.CustomExceptionHandler',
}

AUTHENTICATION_BACKENDS = [
    'xdj_utils.backends.CustomBackend',
    ...
]

SWAGGER_SETTINGS = {
    ...
    'DEFAULT_AUTO_SCHEMA_CLASS': 'xdj_utils.swagger.CustomSwaggerAutoSchema',
}
```