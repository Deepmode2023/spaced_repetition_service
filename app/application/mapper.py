from dataclasses import dataclass


@dataclass
class APIMapper:
    @classmethod
    def from_input_to_domain(cls, model):
        pass

    @classmethod
    def from_domain_to_input(cls, model):
        pass
