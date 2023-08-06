class performanceController:
    """Performance Controller"""

    _controller_name = "performanceController"
    _gracie = None

    def __init__(self, gracie):
        self._gracie = gracie

    def enable(self, enabled):
        """

        Args:
            enabled: (boolean): Enable/disable runtime server engine performance logging

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'enabled': {'name': 'enabled', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/performance/enable'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def retrieve(self):
        """"""

        all_api_parameters = {}
        parameters_names_map = {}
        api = '/performance/retrieve'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)
