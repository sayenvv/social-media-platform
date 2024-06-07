from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


def manual_params(
    params: list = [],
    description: str = None,
    enums=None,
    data_type: str = openapi.TYPE_STRING,
    required: bool = False,
):
    params_ = []
    for i in params:

        params_.append(
            openapi.Parameter(
                i,
                openapi.IN_QUERY,
                description=description,
                type=data_type,
                enum=[enum.value for enum in enums],
                required=required,
            )
        )
    return params_
