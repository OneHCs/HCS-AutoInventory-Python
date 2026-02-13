class EndpointHandler:
    @staticmethod
    def get_API_endpoint(api):
        return api.split(" ")[1]
    @staticmethod
    def get_API_method(api):
        return api.split(" ")[0]