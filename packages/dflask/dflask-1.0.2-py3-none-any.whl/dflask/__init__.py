from flask import *
from typing import Union
class DirectFlask(Flask):
    def add_response(self, path: str, response: Union[str, Response]) -> Flask:
        for rule in self.url_rule_class(path, endpoint=path).get_rules(self.url_map):
            rule.bind(self.url_map)
            self.url_map._rules.append(rule)
            self.url_map._rules_by_endpoint.setdefault(rule.endpoint, []).append(rule)
        self.view_functions[path] = lambda: response
        return self
