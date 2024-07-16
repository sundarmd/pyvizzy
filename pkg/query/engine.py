import os
import string
from typing import Dict, Any, List, Union
from functools import partial

# Assuming prompt module is implemented similarly to the Go version
import prompt

# Simulating Go's embed functionality
class EmbeddedFS:
    def __init__(self, root_dir):
        self.root_dir = root_dir

    def read_file(self, path):
        with open(os.path.join(self.root_dir, path), 'r') as f:
            return f.read()

prompts_fs = EmbeddedFS('prompts')

def format_value(value: Any) -> str:
    if isinstance(value, str):
        return (value[:50] + '...') if len(value) > 50 else value
    elif isinstance(value, list):
        return ', '.join(format_value(v) for v in value)
    else:
        return str(value)

class Engine:
    def __init__(self):
        self.prompter = prompt.Engine()

    def with_session(self, id: str) -> 'Engine':
        new_engine = Engine()
        new_engine.prompter = self.prompter.with_session(id)
        return new_engine

    def query_with_template(self, template: str, data: Dict[str, Any]) -> str:
        return self.prompter.prompt_with_template(template, data)

def new() -> Engine:
    return Engine()

# Initialize the prompt module
prompt.set_fs(prompts_fs)
prompt.set_template_func_map({'format_value': format_value})