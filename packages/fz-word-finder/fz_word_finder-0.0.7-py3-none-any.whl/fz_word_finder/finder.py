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

from fz_word_finder.tries import trie
from fz_word_finder.helpers import is_alpha_numeric, is_punct, ss_len_manager, search_nodes_manager, search_results_manager
from importlib import import_module


class fz_finder():
    def __init__(self):
        self.trie = trie()
        self.use_punct_as_variant = False

    def add_target_words(self, target_words):
        self.trie.add_target_words(target_words)

    def add_target_word(self, target_word):
        self.trie.add(word)

    def delete_target_word(self, target_word):
        self.trie.delete(word)

    def delete_target_words(self, target_words):
        self.trie.delete_target_words

    def add_variants(self, variants):
        self.trie.add_variants(variants)

    def delete_variant(self, variant):
        self.trie.delete_variant(variant)

    def delete_variants(self, variants):
        self.trie.delete_variants(variants)

    def set_match_case(self, value):
        self.trie.set_match_case(value)

    def set_match_punct_ws(self, value):
        self.trie.set_match_punct_ws(value)

    def set_match_punct(self, value):
        self.trie.set_match_punct(value)

    def set_match_ws(self, value):
        self.trie.set_match_ws(value)
    
    def has_key(self, key, ss_len, search_nodes, srm):
        return self.trie.has_key(key, ss_len, search_nodes, srm)

    def has_next_key(self, key, ss_len, search_nodes, srm):
        return self.trie.has_next_key(key, ss_len, search_nodes, srm)

    def get_partial_matches(self, key, ss_len, search_nodes, srm):
        return self.trie.get_partial_matches(key, ss_len, search_nodes, srm)

    def set_use_punct_as_variant(self, value):
        self.use_punct_as_variant = value
        self.trie.set_use_punct_as_variant(value)
        
    def clear_variants(self):
        self.trie.clear_variants()

    def clear_target_words(self):
        self.trie.clear_target_words()

    def get_variant_dict(self):
        return self.trie.get_variant_dict()

    def get_target_words(self):
        return self.trie.get_target_words()

    def load_default_variants(self, offline = True, mode = "", file_path = None):
        tools = import_module("fz_word_finder.variant_tools")

        for name in tools.get_variant_names():
            self.add_variants(tools.get_variant_dict(name, offline, mode, file_path))

    def download_variants(self, file_path = None):
        tools = import_module("fz_word_finder.variant_tools")
        tools.download_variants(file_path)

    def update_variant_list(self, file_path = None):
        tools = import_module("fz_word_finder.variant_tools")
        tools.update_variant_list(file_path)

    def find_matches(self, input_str, fast_search = True):
        results = {"whole words" : [], "substrings" : []}

        if type(input_str) != str:
            return results

        start = 0
        end = 0
        index = 0
        str_len = len(input_str)
        ss_len = ss_len_manager()
        search_nodes = search_nodes_manager()
        srm = search_results_manager()
        while  start <= len(input_str) - 1:
            start_search = self.has_key(input_str[start], ss_len, search_nodes, srm)

            if start_search:
                end = start+1

                while True:
                    search_result = self.has_next_key(input_str[end], ss_len, search_nodes, srm) if  end <= str_len - 1 else srm.get_results()

                    if search_result == True:
                        end+=1

                    else:
                        if search_result == False:
                            start+=1
                            break
                            
                        else:

                            start_word_boundary = True if start == 0 else True if not is_alpha_numeric(input_str[start-1]) else False
                            
                            for result in search_result:
                                target_word = result[0]
                                index = result[1]
                                substring = input_str[start: start + index]
                                result_dict = {"target word" : target_word, "match" : substring}
                                if start_word_boundary == False:
                                    results["substrings"].append(result_dict)
                                else:
                                    end_word_boundary = True if end == str_len else True if not is_alpha_numeric(input_str[start + index]) else False
                                    if end_word_boundary:
                                        results["whole words"].append(result_dict)
                                    else:
                                        results["substrings"].append(result_dict)
                                
                            start+=(index if fast_search == True else 1) 
                
                        break

            else:
                start+=1


        return results    


    def get_word_indices(self, input_str, whole_words_only = True, fast_search = True):
        results = {}

        if type(input_str) != str:
            return results

        start = 0
        end = 0
        index = 0
        str_len = len(input_str)
        ss_len = ss_len_manager()
        search_nodes = search_nodes_manager()
        srm = search_results_manager()
        while  start <= len(input_str) - 1:
            start_search = self.has_key(input_str[start], ss_len, search_nodes, srm)

            if start_search:
                end = start+1

                while True:
                    
                    search_result = self.has_next_key(input_str[end], ss_len, search_nodes, srm) if  end <= str_len - 1 else srm.get_results()

                    if search_result == True:
                        end+=1

                    else:
                        if search_result == False:
                            start+=1
                            break
                            
                        else:
                            
                            start_word_boundary = True if start == 0 else True if not is_alpha_numeric(input_str[start-1]) else False

                            for result in search_result:
                                target_word = result[0]
                                index = result[1]
                                end_index = start + index
                                substring = input_str[start: end_index]
                                if start_word_boundary == False and whole_words_only == False:
                                    if target_word not in results:
                                        results[target_word] = {substring: [[start, end]]}
                                    else:
                                        if substring in results[target_word]:
                                            results[target_word][substring].append([start, end])
                                        else:
                                            results[target_word] = {substring: [[start, end]]}
                                            
                                        
                                else:
                                    end_word_boundary = True if end == str_len else True if not is_alpha_numeric(input_str[start + index]) else False
                                    if end_word_boundary or whole_words_only == False:

                                        if target_word not in results:
                                            results[target_word] = {substring: [[start, end_index]]}
                                        else:
                                            if substring in results[target_word]:
                                                results[target_word][substring].append([start, end_index])
                                            else:
                                                results[target_word] = {substring: [[start, end_index]]}

                                
                            start+=(index if fast_search == True else 1)

                        break

            else:
                start+=1


        return results


    def has_any_target_word(self, input_str, whole_words_only = True):

        if type(input_str) != str:
            return False

        start = 0
        end = 0
        index = 0
        str_len = len(input_str)
        ss_len = ss_len_manager()
        search_nodes = search_nodes_manager()
        srm = search_results_manager()
        while  start <= len(input_str) - 1:
            start_search = self.has_key(input_str[start], ss_len, search_nodes, srm)

            if start_search:
                end = start+1

                while True:
                    
                    search_result = self.has_next_key(input_str[end], ss_len, search_nodes, srm) if  end <= str_len - 1 else srm.get_results()

                    if search_result == True:
                        end+=1

                    else:
                        if search_result == False:
                            start+=1
                            break
                            
                        else:
                            
                            start_word_boundary = True if start == 0 else True if not is_alpha_numeric(input_str[start-1]) else False

                            for result in search_result:
                                target_word = result[0]
                                index = result[1]
                                end_index = start + index
                                substring = input_str[start: end_index]
                                if start_word_boundary == False and whole_words_only == False:
                                    return True
                                            
                                else:
                                    end_word_boundary = True if end == str_len else True if not is_alpha_numeric(input_str[start + index]) else False
                                    if end_word_boundary or whole_words_only == False:
                                        return True
  
                            start+= index

                        break

            else:
                start+=1


        return False 


    def find_partial_matches(self, input_str, fast_search = True, partial_matches = False, partial_matches_fast_search = True):
        results = {"whole words" : [], "substrings" : [], "partial" : []}

        if type(input_str) != str:
            return results

        start = 0
        end = 0
        index = 0
        str_len = len(input_str)
        ss_len = ss_len_manager()
        search_nodes = search_nodes_manager()
        srm = search_results_manager()
        input_str_len = len(input_str) - 1
        while  start <= input_str_len:
            start_search = self.has_key(input_str[start], ss_len, search_nodes, srm)

            if start_search:
                end = start+1

                while True:
                    search_result = self.has_next_key(input_str[end], ss_len, search_nodes, srm) if  end <= str_len - 1 else srm.get_results()

                    if search_result == True:
                        end+=1

                    else:
                        if search_result == False:

                            past_chars = input_str[start:end]
                            srm.enable_partial_matches(past_chars)
                            fake_end = end

                            run = False if (end == input_str_len + 1 and all([is_punct(char) for char in past_chars])) else True                        
                                
                            while run == True:
                                current_key = input_str[fake_end] if fake_end <= input_str_len else None
                                partial_string_search_result = self.get_partial_matches(current_key, ss_len, search_nodes, srm)

                                if partial_string_search_result == True:
                                    fake_end+=1
                                    
                                elif partial_string_search_result == False:
                                    break

                                else:
                                    for result in partial_string_search_result:
                                        target_word = result[0]
                                        index = result[1]
                                        substring = input_str[start: start + index]
                                        result_dict = {"target word" : target_word, "match" : substring}
                                        results["partial"].append(result_dict)
                                    break
                                        
                            start+=(fake_end if partial_matches_fast_search == True and (type(partial_string_search_result) != bool and len(partial_string_search_result) > 0) else 1)
                            break

                        else:

                            start_word_boundary = True if start == 0 else True if not is_alpha_numeric(input_str[start-1]) else False
                            
                            for result in search_result:
                                target_word = result[0]
                                index = result[1]
                                substring = input_str[start: start + index]
                                result_dict = {"target word" : target_word, "match" : substring}
                                if start_word_boundary == False:
                                    results["substrings"].append(result_dict)
                                else:
                                    end_word_boundary = True if end == str_len else True if not is_alpha_numeric(input_str[start + index]) else False
                                    if end_word_boundary:
                                        results["whole words"].append(result_dict)
                                    else:
                                        results["substrings"].append(result_dict)
                                
                            start+=(index if fast_search == True else 1) 
                
                        break

            else:
                start+=1


        return results    
