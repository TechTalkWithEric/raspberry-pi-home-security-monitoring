

class ServiceFactory:
    def __init__(self, service_class):
        self.service_class = service_class

    def create_service(self, *args, **kwargs):
        return self.service_class(*args, **kwargs)
