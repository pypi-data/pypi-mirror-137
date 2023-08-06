class downloadController:
    """Download Controller"""

    _controller_name = "downloadController"
    _gracie = None

    def __init__(self, gracie):
        self._gracie = gracie

    def download(self, downloadToken):
        """

        Args:
            downloadToken: (string): downloadToken

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'downloadToken': {'name': 'downloadToken', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/download'
        actions = ['get']
        consumes = []
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)
