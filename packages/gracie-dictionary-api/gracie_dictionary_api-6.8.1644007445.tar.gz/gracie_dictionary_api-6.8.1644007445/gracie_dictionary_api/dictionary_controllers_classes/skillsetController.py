class skillsetController:
    """Skillset Controller"""

    _controller_name = "skillsetController"
    _gracie = None

    def __init__(self, gracie):
        self._gracie = gracie

    def add(self, name):
        """

        Args:
            name: (string): Name of new skillset

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'name': {'name': 'name', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/skillset/add'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def delete(self, id):
        """

        Args:
            id: (string): Id of skillset to delete

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'id': {'name': 'id', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/skillset/delete'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def list(self, **kwargs):
        """

        Args:
            filter: (string): Filter expression.The expression supports parentheses `['(', ')']` for operation order, logical operations `['not', 'and', 'or']`, and comparison operations `['=', '!=', '<', '<=', '>', '>=']`.Item name is referenced as `name(<prefix>)` (will match all names starting with `<prefix>`), item tag is referenced as `tag(<key>)` (returns value if tag exists, `false` otherwise).Following attributes can be referenced for skillsets/skills in user language: `['corpusDocumentsCount', 'keywordsCount', 'blacklistKeywordsCount', 'averageProximity']`Example: `name('doctype') and corpusDocumentsCount < 20` - Take all skills with the names that start with `doctype` and with less than 20 documents in user's language.
            orderAsc: (boolean): Sort result in ascending order
            orderBy: (string): Sort order of returned skillsets, one of [NAME]

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'filter': {'name': 'filter', 'required': False, 'in': 'query'}, 'orderAsc': {'name': 'orderAsc', 'required': False, 'in': 'query'}, 'orderBy': {'name': 'orderBy', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/skillset/list'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def retrieve(self, id):
        """

        Args:
            id: (string): Id of skillset to retrieve

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'id': {'name': 'id', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/skillset/retrieve'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def visualize(self, skillsetId, **kwargs):
        """

        Args:
            languageId: (string): Id of language for visualization, default is caller's language
            skillsetId: (string): Id of skillset to visualize

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'languageId': {'name': 'languageId', 'required': False, 'in': 'query'}, 'skillsetId': {'name': 'skillsetId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/skillset/visualize'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)
