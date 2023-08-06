class autotuneIterationController:
    """Autotune Iteration Controller"""

    _controller_name = "autotuneIterationController"
    _gracie = None

    def __init__(self, gracie):
        self._gracie = gracie

    def getAccuracySpreadsheet(self, id):
        """

        Args:
            id: (string): Id of existing autotune-iteration

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'id': {'name': 'id', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/autotuneIteration/getAccuracySpreadsheet'
        actions = ['get']
        consumes = []
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def list(self, autotuneRunId):
        """

        Args:
            autotuneRunId: (string): Id of existing autotune-run

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'autotuneRunId': {'name': 'autotuneRunId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/autotuneIteration/list'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def restore(self, id):
        """

        Args:
            id: (string): Id of existing autotune-iteration

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'id': {'name': 'id', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/autotuneIteration/restore'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def resume(self, id, maxIterations, **kwargs):
        """

        Args:
            firstIterationRerunsTesting: (boolean): true - in first resumed iteration run backup and test. false - make documents movement based on previous iteration result.
            firstIterationUpdatesSkills: (boolean): firstIterationUpdatesSkills
            id: (string): Id of existing autotune-iteration
            maxIterations: (integer): Max number of iterations to run.

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'firstIterationRerunsTesting': {'name': 'firstIterationRerunsTesting', 'required': False, 'in': 'query'}, 'firstIterationUpdatesSkills': {'name': 'firstIterationUpdatesSkills', 'required': False, 'in': 'query'}, 'id': {'name': 'id', 'required': True, 'in': 'query'}, 'maxIterations': {'name': 'maxIterations', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/autotuneIteration/resume'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def retrieve(self, id, **kwargs):
        """

        Args:
            id: (string): Id of existing autotune-iteration
            includeClassificationAccuracy: (boolean): includeClassificationAccuracy
            includeSummaryDocumentsMovement: (boolean): includeSummaryDocumentsMovement

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'id': {'name': 'id', 'required': True, 'in': 'query'}, 'includeClassificationAccuracy': {'name': 'includeClassificationAccuracy', 'required': False, 'in': 'query'}, 'includeSummaryDocumentsMovement': {'name': 'includeSummaryDocumentsMovement', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/autotuneIteration/retrieve'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)
