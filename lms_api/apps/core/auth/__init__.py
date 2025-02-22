from abc import ABC, abstractmethod


class AuthAbstract(ABC):
    @abstractmethod
    def login(self, data):
        raise NotImplemented("`login()` must be implemented.")

    @abstractmethod
    def sign_up(self, data):
        raise NotImplemented("`sign_up()` must be implemented.")

class AuthHandler:
    def __init__(self, instance: AuthAbstract):
        self.__instance = instance
        
    def sign_up(self, data):
        username = data.get("username")
