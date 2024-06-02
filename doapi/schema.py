from drf_spectacular.extensions import OpenApiAuthenticationExtension


class MyBearerScheme(OpenApiAuthenticationExtension):
    target_class = 'doapi.core.auth.MyBearerAuthentication'
    name ='bearerAuth'
    priority = -1
    def get_security_definition(self, auto_schema):
        return {
            'type': 'http',
           'scheme': 'bearer',
        }