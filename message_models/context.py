import yaml

from os.path import join, dirname
from typing import *
from pydantic import create_model, ConfigDict, ValidationError
from ovos_bus_client.message import Message
from pydantic.fields import FieldInfo

models = {}
_pydantic_config = ConfigDict(arbitrary_types_allowed=True)
_model_names = ["UserProfile", "IntentContext", "SessionContext", "Session",
                "Context"]


def _parse_model_from_spec(model_name: str, spec_path: str):
    with open(join(dirname(__file__), spec_path)) as f:
        user_profile = yaml.safe_load(f)
        pydantic_model = dict()
        for k, v in user_profile.items():
            v_type = eval(v['type'])
            if 'default' not in v and not v['required']:
                v['default'] = v_type()
            default = v['default'] if not v['required'] \
                else Ellipsis
            if v_type != str and isinstance(default, str):
                default = eval(default)
            field_info = FieldInfo(default=default, alias=v.get('alias'),
                                   description=v['description'],
                                   annotation=v_type)
            pydantic_model[k] = (v_type, field_info)
    models[model_name] = create_model(model_name, __config__=_pydantic_config,
                                      **pydantic_model)
    globals()[model_name] = models[model_name]


for model in _model_names:
    _parse_model_from_spec(model,
                           f"context/{model}.yaml")

__all__ = _model_names


