class compoundLexemeController:
    """Compound Lexeme Controller"""

    _controller_name = "compoundLexemeController"
    _gracie = None

    def __init__(self, gracie):
        self._gracie = gracie

    def add(self, config, enabled, name):
        """

        Args:
            config: (type): config
            enabled: (boolean): Enable/disable new compound lexeme
            name: (string): Name of new compound lexeme, must be unique

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'config': {'name': 'config', 'required': True, 'in': 'body'}, 'enabled': {'name': 'enabled', 'required': True, 'in': 'query'}, 'name': {'name': 'name', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/compoundLexeme/add'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def addLabel(self, id, label):
        """

        Args:
            id: (string): Id of compound lexeme to assign label
            label: (string): Label to apply to compound lexeme

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'id': {'name': 'id', 'required': True, 'in': 'query'}, 'label': {'name': 'label', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/compoundLexeme/addLabel'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def delete(self, id):
        """

        Args:
            id: (string): Id of compound lexeme to delete

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'id': {'name': 'id', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/compoundLexeme/delete'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def edit(self, id, **kwargs):
        """

        Args:
            config: (type): config
            enabled: (boolean): Enable/disable compound lexeme
            id: (string): Id of compound lexeme to edit
            name: (string): New name of compound lexeme, must be unique

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'config': {'name': 'config', 'required': False, 'in': 'body'}, 'enabled': {'name': 'enabled', 'required': False, 'in': 'query'}, 'id': {'name': 'id', 'required': True, 'in': 'query'}, 'name': {'name': 'name', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/compoundLexeme/edit'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def exportGet(self, taskId):
        """

        Args:
            taskId: (string): taskId of the export task

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'taskId': {'name': 'taskId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/compoundLexeme/export'
        actions = ['get']
        consumes = []
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def exportPost(self, **kwargs):
        """

        Args:
            ids: (array): Ids of existing compound lexemes. If empty then export all compound lexemes.

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'ids': {'name': 'ids', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/compoundLexeme/export'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def import_(self, file, **kwargs):
        """

        Args:
            conflictsResolving: (type, enum): Method to resolve import conflicts: STOP, OVERWRITE, SKIP
            file: (file): Name of JSON-file with compound lexemes

        Consumes:
            multipart/form-data

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'conflictsResolving': {'name': 'conflictsResolving', 'required': False, 'in': 'formData'}, 'file': {'name': 'file', 'required': True, 'in': 'formData'}}
        parameters_names_map = {}
        api = '/compoundLexeme/import'
        actions = ['post']
        consumes = ['multipart/form-data']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def list(self, **kwargs):
        """

        Args:
            label: (string): Limit list of compound lexemes to those with the specified label
            limit: (integer): Max number of results
            offset: (integer): Start offset of results
            orderAsc: (boolean): true = ascending (default); false = descending
            orderBy: (string): Sort results by order: NAME

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'label': {'name': 'label', 'required': False, 'in': 'query'}, 'limit': {'name': 'limit', 'required': False, 'in': 'query'}, 'offset': {'name': 'offset', 'required': False, 'in': 'query'}, 'orderAsc': {'name': 'orderAsc', 'required': False, 'in': 'query'}, 'orderBy': {'name': 'orderBy', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/compoundLexeme/list'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def listLabels(self):
        """"""

        all_api_parameters = {}
        parameters_names_map = {}
        api = '/compoundLexeme/listLabels'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def removeLabel(self, id, label):
        """

        Args:
            id: (string): Id of compound lexeme to remove label from
            label: (string): Label to remove from compound lexeme

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'id': {'name': 'id', 'required': True, 'in': 'query'}, 'label': {'name': 'label', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/compoundLexeme/removeLabel'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def retrieve(self, id):
        """

        Args:
            id: (string): Id of compound lexeme to retrieve

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'id': {'name': 'id', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/compoundLexeme/retrieve'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)
