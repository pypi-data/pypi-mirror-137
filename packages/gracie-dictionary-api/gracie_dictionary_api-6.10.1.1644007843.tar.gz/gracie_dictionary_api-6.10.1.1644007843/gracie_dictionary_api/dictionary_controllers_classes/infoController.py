class infoController:
    """Info Controller"""

    _controller_name = "infoController"
    _gracie = None

    def __init__(self, gracie):
        self._gracie = gracie

    def retrieve(self):
        """"""

        all_api_parameters = {}
        parameters_names_map = {}
        api = '/info/retrieve'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)
