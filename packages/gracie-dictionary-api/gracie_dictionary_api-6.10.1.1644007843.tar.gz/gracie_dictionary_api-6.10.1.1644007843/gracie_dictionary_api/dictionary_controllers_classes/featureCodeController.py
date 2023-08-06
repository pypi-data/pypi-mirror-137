class featureCodeController:
    """Feature Code Controller"""

    _controller_name = "featureCodeController"
    _gracie = None

    def __init__(self, gracie):
        self._gracie = gracie

    def add(self, featureClassId, name, subCode, **kwargs):
        """

        Args:
            description: (string): Feature description (https://www.geonames.org/statistics/total.html)
            featureClassId: (string): Id of existing feature class to assign new feature code.
            name: (string): Feature code name (https://www.geonames.org/statistics/total.html)
            subCode: (string): Feature code subcode (https://www.geonames.org/statistics/total.html)

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'description': {'name': 'description', 'required': False, 'in': 'query'}, 'featureClassId': {'name': 'featureClassId', 'required': True, 'in': 'query'}, 'name': {'name': 'name', 'required': True, 'in': 'query'}, 'subCode': {'name': 'subCode', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/featureCode/add'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def delete(self, id):
        """

        Args:
            id: (string): Id of existing features code

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'id': {'name': 'id', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/featureCode/delete'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def edit(self, id, **kwargs):
        """

        Args:
            description: (string): Feature description (https://www.geonames.org/statistics/total.html)
            id: (string): Id of existing features code
            name: (string): Feature code name (https://www.geonames.org/statistics/total.html)

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'description': {'name': 'description', 'required': False, 'in': 'query'}, 'id': {'name': 'id', 'required': True, 'in': 'query'}, 'name': {'name': 'name', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/featureCode/edit'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def list(self, **kwargs):
        """

        Args:
            featureClassId: (string): Id of existing feature class
            orderAsc: (boolean): true = ascending (default); false = descending
            orderBy: (string): Sort results by order: NAME, FEATURE_CLASS, SUBCODE

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'featureClassId': {'name': 'featureClassId', 'required': False, 'in': 'query'}, 'orderAsc': {'name': 'orderAsc', 'required': False, 'in': 'query'}, 'orderBy': {'name': 'orderBy', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/featureCode/list'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def retrieve(self, id):
        """

        Args:
            id: (string): Id of existing geo features code

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'id': {'name': 'id', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/featureCode/retrieve'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)
