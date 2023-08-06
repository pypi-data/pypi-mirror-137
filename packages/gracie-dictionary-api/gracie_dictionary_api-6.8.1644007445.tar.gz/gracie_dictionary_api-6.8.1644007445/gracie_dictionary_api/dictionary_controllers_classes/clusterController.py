class clusterController:
    """Cluster Controller"""

    _controller_name = "clusterController"
    _gracie = None

    def __init__(self, gracie):
        self._gracie = gracie

    def add(self, clusterGroupId, name):
        """

        Args:
            clusterGroupId: (string): Cluster group id to assign name
            name: (string): Cluster group name

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'clusterGroupId': {'name': 'clusterGroupId', 'required': True, 'in': 'query'}, 'name': {'name': 'name', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/cluster/add'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def copyDocuments(self, clusterId, targetId, **kwargs):
        """

        Args:
            clusterId: (string): Source cluster id
            languageId: (string): Language id of documents to copy to destination cluster
            targetId: (string): Destination cluster id

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'clusterId': {'name': 'clusterId', 'required': True, 'in': 'query'}, 'languageId': {'name': 'languageId', 'required': False, 'in': 'query'}, 'targetId': {'name': 'targetId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/cluster/copyDocuments'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def delete(self, id):
        """

        Args:
            id: (string): Id of existing cluster group

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'id': {'name': 'id', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/cluster/delete'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def findNames(self, clusterId, **kwargs):
        """

        Args:
            clusterId: (string): Cluster id to find names in
            languageId: (string): Language for results, default to user language
            maxNames: (integer): Max number of results

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'clusterId': {'name': 'clusterId', 'required': True, 'in': 'query'}, 'languageId': {'name': 'languageId', 'required': False, 'in': 'query'}, 'maxNames': {'name': 'maxNames', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/cluster/findNames'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def list(self, clusterGroupId, **kwargs):
        """

        Args:
            clusterGroupId: (string): Id of the cluster group to list
            limit: (integer): Max number of results
            offset: (integer): Start offset of results
            orderAsc: (boolean): true = ascending (default); false = descending
            orderBy: (string): Sort results by order: NAME

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'clusterGroupId': {'name': 'clusterGroupId', 'required': True, 'in': 'query'}, 'limit': {'name': 'limit', 'required': False, 'in': 'query'}, 'offset': {'name': 'offset', 'required': False, 'in': 'query'}, 'orderAsc': {'name': 'orderAsc', 'required': False, 'in': 'query'}, 'orderBy': {'name': 'orderBy', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/cluster/list'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def retrieve(self, id):
        """

        Args:
            id: (string): Id of existing cluster group

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'id': {'name': 'id', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/cluster/retrieve'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)
