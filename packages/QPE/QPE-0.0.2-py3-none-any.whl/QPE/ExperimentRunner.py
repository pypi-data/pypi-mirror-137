from QPE.Kitaev import Kitaev
from QPE.Iterative import Iterative
from QPE.QFT import QFT
from QPE.HelpFunctions import phase_to_exp
from QPE.Unitary import Unitary
import json
import numpy as np
import os
import re

class ExperimentSet():
    def __init__(self, instructions, draw_params:dict = {"NT":0, "T":0}):
        self.draw_params = draw_params 
        self.get_specs(instructions)
        self.PE_dicts = self.get_PE_dicts()
        self.generate_filenames()
        self.result_dicts = []
    
    def get_specs(self, instructions):
        self.path = instructions.pop("path")
        self.name = instructions.pop("name")
        self.filename_flags = instructions.pop("filename_flags")
        self.instructions = instructions

    def get_PE_dicts(self):
        PE_dicts = [{}]
        non_defaults = list(self.instructions.keys())

        def generate_combinations(PE_dicts, key, param_list):
            new_PE_dicts = []
            for old_dict in PE_dicts:
                for param in param_list:
                    new_d = old_dict.copy()
                    new_d[key] = param
                    new_PE_dicts.append(new_d)
            return new_PE_dicts

        while len(non_defaults) > 0:
            key = non_defaults.pop(-1)
            param_list = self.instructions[key]
            PE_dicts = generate_combinations(PE_dicts, key, param_list)
        
        print(f"Using {len(PE_dicts)} different combinations")
        return PE_dicts

    def generate_filenames(self):

        keys = list(self.PE_dicts[0].keys())
        estimator_pattern = r"[A-Za-z]+"
        estimator_pattern = r"QPE\.([A-Za-z]+)"

        # print(keys)
        # print(self.filename_flags)
        for d in self.PE_dicts:
            filename = ""
            for flag in self.filename_flags:
                if flag == "estimator":
                    full_e_string = str(d["estimator"])
                    match = re.search(estimator_pattern, full_e_string)

                    s = match.groups()[0]
                    filename += f"_{s}"
                elif flag == "U":
                    unitary_name = d["U"].name
                    if unitary_name != "":
                        filename += f"_{unitary_name}"
                elif flag == "backend_name":
                    filename += f"_{d['backend_params']['backend_name']}"
                elif flag == "backend_service":
                        filename += f"_{d['backend_params']['service']}"
                elif flag == "n_rotations":
                    filename += f"_n_rotations{d['method_specific_params']['n_rotations']}" 
                elif flag in ["m_digits","n_shots"]:
                    filename += f"_{flag}{d[flag]}"                   

            d["filename"] = filename



    def one_run(self, index:int, draw_params = {"T":-1, "NT":-1}):
        PE_dict = self.PE_dicts[index]
        filename = PE_dict.pop("filename")
        estimator = PE_dict.pop("estimator")
        e = estimator(**PE_dict)
        e.run_circuit()
        e.post_process()

        if (draw_params["T"] != 0) or (draw_params["NT"] != 0):
            plot_path = self.path + f"/plots/{filename}"
            if not os.path.isdir(plot_path):
                os.makedirs(plot_path, exist_ok=True)
                print(f"Created directory {plot_path}")
            
            drawing_path = plot_path + f"{filename}_{index}"
            e.draw_circuits(drawing_path, self.draw_params["NT"], self.draw_params["T"])

        dicts = e.get_dicts()
        json_path = self.path + "/data"

        if not os.path.isdir(json_path):
            os.makedirs(json_path, exist_ok=True)
            print(f"Created directory {json_path}")

        for d_i, d in enumerate(dicts):
            d["Experiment"] = self.name
            d["name"] = filename
            json_filepath = json_path + f"/{filename}-{index}_{d_i+1}.json"
            with open(json_filepath, "w") as write_file:
                json.dump(d, write_file, indent = True)
        
    def run(self):
        for i in range(len(self.PE_dicts)):
            self.one_run(i, self.draw_params)

if __name__ == "__main__":
    pass