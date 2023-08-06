class logoutController:
    """Logout Controller"""

    _controller_name = "logoutController"
    _gracie = None

    def __init__(self, gracie):
        self._gracie = gracie

    def doLogout(self):
        """"""

        all_api_parameters = {}
        parameters_names_map = {}
        api = '/doLogout'
        actions = ['get']
        consumes = []
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)
