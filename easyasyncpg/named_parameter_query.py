import re


class NamedParameterQuery:
    def __init__(self, query: str, params: dict | list[dict]):
        self.query = query
        self.params = params
        (
            self.positional_query,
            self.positional_params,
        ) = self._convert_to_positional_parameters()

    def _convert_to_positional_parameters(self) -> tuple:
        regex = r":(\w+)"
        positional_param_names = []
        positional_param_values = []
        counter = 1

        def replace_named_params(match):
            nonlocal counter
            positional_param_names.append(match.group(1))
            counter += 1
            return f"${counter - 1}"

        query = re.sub(regex, replace_named_params, self.query)

        if isinstance(self.params, dict):
            positional_param_values = self._get_positional_param_values(
                positional_param_names, self.params
            )
        elif isinstance(self.params, list):
            positional_param_values = [
                self._get_positional_param_values(positional_param_names, param)
                for param in self.params
            ]
        else:
            raise ValueError(
                f"params must be a dict or a list of dicts, not {type(self.params)}"
            )

        return query, positional_param_values

    def _get_positional_param_values(self, param_names: list, params: dict) -> list:
        positional_param_values = []
        for param_name in param_names:
            if param_name not in params:
                raise ValueError(f"Missing parameter: {param_name}")
            positional_param_values.append(params[param_name])
        return positional_param_values
