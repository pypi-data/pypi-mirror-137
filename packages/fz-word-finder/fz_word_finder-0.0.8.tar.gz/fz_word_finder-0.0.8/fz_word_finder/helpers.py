
'''
Copyright 2021 Rairye
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

#Helper methods. Not suggested for use outside of this package.


def is_supported_target_word_type(target_words):
    supported_types = set([str, list])
    return type(target_words) in supported_types

def is_punct(char):
    if type(char) != str:
        return False
    
    if len(char) > 1 or char == "":
        return False

    return (char.isalpha() or (char.isdigit() or char.isspace())) == False


def is_alpha_numeric(char):

    return char.isalpha() or char.isdigit()


def generate_search_candidates(char):
    upper = char.upper() if char.islower() else char
    lower = char.lower() if char.upper() else char

    if upper == lower:
        return [char]

    return [upper, lower]

class ss_len_manager():
    def __init__(self):
        self.value = 0
        
    def increment(self):
        self.value+=1

    def reset(self):
        self.value = 0

class search_nodes_manager():
    def __init__(self):
        self.nodes = []

    def update(self, new_nodes):
        self.nodes = new_nodes

    def add(self, new_node):
        self.nodes.append(new_node)

class search_results_manager():
    def __init__(self):
        self.results = []
        self.past_chars = None
        self.differences = None

    def add(self, result):
        self.results.append(result)

    def reset(self):
        self.results = []

    def get_results(self):
        if len(self.results) > 0:
            return self.results
        
        return False

    def count(self):
        return len(self.results)

    def set_past_chars(self, chars):
        self.past_chars = set([char for char in chars if not char.isspace()])

    def enable_partial_matches(self, chars):
        self.set_past_chars(chars)
        self.difference = 0
        self.steps = 0

    def increment_difference(self):
        self.difference+=1

    def increment_steps(self):
        self.steps+=1

    def is_move_or_duplicate(self, chars, match_ws, match_punct):
        return any ([char in self.past_chars for char in chars if not ((char.isspace() and match_ws == False) or (is_punct(char) and match_punct == False)) ])

    def add_past_char(self, char, match_ws, match_punct):
        if char == None:
            return
        
        if  not ((char.isspace() and match_ws == False) or (is_punct(char) and match_punct == False)):
            self.past_chars.add(char)

    def is_good_match(self):
        if self.difference == 1 and self.steps == 1:
            return True
        
        return (self.difference / self.steps) <= 0.5

    def is_current_good_match(self):
        return ((self.difference + 1)/ self.steps) <= 0.5
