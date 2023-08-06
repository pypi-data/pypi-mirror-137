from injecta.container.ContainerInterface import ContainerInterface
from daipecore.decorator.BaseDecorator import BaseDecorator
from daipecore.decorator.DecoratedFunctionInjector import DecoratedFunctionInjector
from daipecore.decorator.InputDecorator import InputDecorator


class CallbackDecorator(BaseDecorator, metaclass=DecoratedFunctionInjector):
    def run_callback(self, input_decorator: InputDecorator, container: ContainerInterface):
        pass
