class entityRiskRuleController:
    """Entity Risk Rule Controller"""

    _controller_name = "entityRiskRuleController"
    _gracie = None

    def __init__(self, gracie):
        self._gracie = gracie

    def addLabel(self, id, label):
        """

        Args:
            id: (string): id of rule to assign label to
            label: (string): Label to assign to rule

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'id': {'name': 'id', 'required': True, 'in': 'query'}, 'label': {'name': 'label', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/entityRiskRules/addLabel'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def create(self, entityRefs, minQuantity, requireUnique, riskLabel, riskValue):
        """

        Args:
            entityRefs: (array): List of entities to include, can be any combination of [CompoundLexemeId, RegexId, CompoundLexemeLabel, RegexLabel]
            minQuantity: (integer): Minimum number of matches required to trigger rule
            requireUnique: (boolean): Only count unique matches (case-insensitive) toward minQuantity
            riskLabel: (string): Risk label to apply if rule matches
            riskValue: (number): Risk value to assign to riskLabel if rule matches

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'entityRefs': {'name': 'entityRefs', 'required': True, 'in': 'query'}, 'minQuantity': {'name': 'minQuantity', 'required': True, 'in': 'query'}, 'requireUnique': {'name': 'requireUnique', 'required': True, 'in': 'query'}, 'riskLabel': {'name': 'riskLabel', 'required': True, 'in': 'query'}, 'riskValue': {'name': 'riskValue', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/entityRiskRules/create'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def edit(self, id, **kwargs):
        """

        Args:
            entityRefs: (array): New list of entities to include
            id: (string): Id of rule to edit
            minQuantity: (integer): New minimum number of matches
            requireUnique: (boolean): New requirement for unique matches
            riskLabel: (string): New risk label
            riskValue: (number): New risk value

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'entityRefs': {'name': 'entityRefs', 'required': False, 'in': 'query'}, 'id': {'name': 'id', 'required': True, 'in': 'query'}, 'minQuantity': {'name': 'minQuantity', 'required': False, 'in': 'query'}, 'requireUnique': {'name': 'requireUnique', 'required': False, 'in': 'query'}, 'riskLabel': {'name': 'riskLabel', 'required': False, 'in': 'query'}, 'riskValue': {'name': 'riskValue', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/entityRiskRules/edit'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def list(self, **kwargs):
        """

        Args:
            label: (string): Limit list of rules to those with the specified label
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
        api = '/entityRiskRules/list'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def listLabels(self):
        """"""

        all_api_parameters = {}
        parameters_names_map = {}
        api = '/entityRiskRules/listLabels'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def remove(self, id):
        """

        Args:
            id: (string): Id of rule to remove

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'id': {'name': 'id', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/entityRiskRules/remove'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def removeLabel(self, id, label):
        """

        Args:
            id: (string): Id of rule to remove label from
            label: (string): Label to remove from rule

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'id': {'name': 'id', 'required': True, 'in': 'query'}, 'label': {'name': 'label', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/entityRiskRules/removeLabel'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def retrieve(self, id):
        """

        Args:
            id: (string): Id of entity risk rule to retrieve

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'id': {'name': 'id', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/entityRiskRules/retrieve'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)
