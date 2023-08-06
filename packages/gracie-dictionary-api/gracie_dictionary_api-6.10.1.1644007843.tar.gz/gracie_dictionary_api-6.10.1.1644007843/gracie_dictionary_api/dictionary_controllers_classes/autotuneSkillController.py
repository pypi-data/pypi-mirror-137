class autotuneSkillController:
    """Autotune Skill Controller"""

    _controller_name = "autotuneSkillController"
    _gracie = None

    def __init__(self, gracie):
        self._gracie = gracie

    def addSkills(self, autotuneRunId, **kwargs):
        """

        Args:
            autotuneRunId: (string): Id of existing autotune-run
            classId: (string): Id of { skill, skillset }. If unset then add all skills from all skillsets.

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'autotuneRunId': {'name': 'autotuneRunId', 'required': True, 'in': 'query'}, 'classId': {'name': 'classId', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/autotuneSkill/addSkills'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def bulkAdd(self, autotuneRunId, **kwargs):
        """

        Args:
            autotuneRunId: (string): Id of existing autotune-run
            skillIds: (array): Ids of existing skills
            skillsetIds: (array): Ids of existing skillsets

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'autotuneRunId': {'name': 'autotuneRunId', 'required': True, 'in': 'query'}, 'skillIds': {'name': 'skillIds', 'required': False, 'in': 'query'}, 'skillsetIds': {'name': 'skillsetIds', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/autotuneSkill/bulkAdd'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def delete(self, autotuneRunId, skillId):
        """

        Args:
            autotuneRunId: (string): Id of existing autotune-run to delete
            skillId: (string): Id of skill

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'autotuneRunId': {'name': 'autotuneRunId', 'required': True, 'in': 'query'}, 'skillId': {'name': 'skillId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/autotuneSkill/delete'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def list(self, autotuneRunId, **kwargs):
        """

        Args:
            autotuneRunId: (string): Id of existing autotune-run
            orderAsc: (boolean): true = ascending (default); false = descending
            orderBy: (string): Sort results by order: NAME

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'autotuneRunId': {'name': 'autotuneRunId', 'required': True, 'in': 'query'}, 'orderAsc': {'name': 'orderAsc', 'required': False, 'in': 'query'}, 'orderBy': {'name': 'orderBy', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/autotuneSkill/list'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)
