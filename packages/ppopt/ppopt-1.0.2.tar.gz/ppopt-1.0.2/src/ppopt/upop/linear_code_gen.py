from typing import List

import numpy
import scipy.io as sio

from ..solution import Solution
from ..upop.language_generation import gen_array, gen_variable
from ..upop.lib_upop.upop_cpp_template import cpp_upop
from ..upop.lib_upop.upop_js_template import js_upop
from ..upop.upop_utils import find_unique_region_hyperplanes, find_unique_region_functions, get_descriptions


def generate_code_cpp(solution: Solution, float_type: str = 'float') -> str:
    """
    Generates C++17 code for point location and function evaluation on microcontrollers \n

    WARNING: This breaks down at high dimensions

    :param solution: a solution to a MPLP or MPQP solution
    :param float_type: the type of C++ float to export, e.g. 'double' or 'float'
    :return: List of the strings of the C++17 datafiles that integrate with uPOP
    """

    fundamental_c, original_c, parity_c = find_unique_region_hyperplanes(solution)

    fundamental_f, original_f, parity_f = find_unique_region_functions(solution)

    # get the list range
    region_boundary_index = list()
    region_boundary_index.append(0)

    for region in solution.critical_regions:
        region_boundary_index.append(region.E.shape[0] + region_boundary_index[-1])

    to_augment = list()

    to_augment.append(f"typedef {float_type} float_;")
    to_augment.append(gen_array(region_boundary_index, 'region_indicies', 'uint16_t'))

    to_augment.append("")

    to_augment.append(gen_array(original_c, "constraint_indices", "uint16_t"))
    bit_string_c = ''.join(["1" if i == 1 else "0" for i in parity_c])
    to_augment.append(
        f"const BitArray<{len(parity_c)}> constraint_parity = BitArray<{len(parity_c)}>(\"{bit_string_c}\");")
    to_augment.append("")

    to_augment.append(gen_array(original_f, "function_indices", "uint16_t"))
    bit_string_f = ''.join(["1" if i == 1 else "0" for i in parity_f])
    to_augment.append(
        f"const BitArray<{len(parity_f)}> function_parity = BitArray<{len(parity_f)}>(\"{bit_string_f}\");")

    desc = get_descriptions(solution)

    to_augment.append(gen_variable(desc['theta_dim'], "theta_dim", "int"))
    to_augment.append(gen_variable(desc['x_dim'], "x_dim", "int"))
    to_augment.append(gen_variable(desc['num_constraints'], "num_hyperplanes", "int"))
    to_augment.append(gen_variable(desc['num_functions'], "num_functions", "int"))
    to_augment.append(gen_variable(desc['num_regions'], "num_regions", "int"))

    to_augment.append(gen_variable(len(fundamental_c), "num_fundamental_hyper_planes", "int"))

    constraint_matrix = numpy.block([[region.E] for region in solution.critical_regions])
    constraint_matrix = constraint_matrix[fundamental_c].flatten().tolist()

    constraint_rhs = numpy.block([[region.f] for region in solution.critical_regions])
    constraint_rhs = constraint_rhs[fundamental_c].flatten().tolist()

    to_augment.append(gen_array(constraint_matrix, "constraint_matrix_data", float_type))
    to_augment.append(gen_array(constraint_rhs, "constraint_vector_data", float_type))

    function_matrix = numpy.block([[region.A] for region in solution.critical_regions])
    function_matrix = function_matrix[fundamental_f].flatten().tolist()

    function_rhs = numpy.block([[region.b] for region in solution.critical_regions])
    function_rhs = function_rhs[fundamental_f].flatten().tolist()

    to_augment.append(gen_array(function_matrix, "function_matrix_data", float_type))
    to_augment.append(gen_array(function_rhs, "function_vector_data", float_type))

    inset_data = "\n".join(to_augment)

    return cpp_upop.replace("<==PayloadHere==>", inset_data)


def generate_code_js(solution: Solution) -> List[str]:
    """
    Generates Javascript code for point location and function evaluation for Scripting Engines and IOT servers \n

    This is direct enumeration, and it is

    :param solution: a solution to a MPLP or MPQP solution
    :return: List of the strings of the C++17 datafiles that integrate with uPOP
    """

    fundamental_c, original_c, parity_c = find_unique_region_hyperplanes(solution)

    fundamental_f, original_f, parity_f = find_unique_region_functions(solution)

    # get the list range
    region_boundary_index = list()
    region_boundary_index.append(0)

    for region in solution.critical_regions:
        region_boundary_index.append(region.E.shape[0] + region_boundary_index[-1])

    float_type = "double"

    to_augment = list()

    # to_augment.append(f"typedef {float_type} float_;")
    to_augment.append(gen_array(region_boundary_index, 'region_indicies', 'uint16_t', lang='js'))

    to_augment.append("")

    to_augment.append(gen_array(original_c, "constraint_indices", "uint16_t", lang='js'))
    to_augment.append(gen_array([1 if i == 1 else 0 for i in parity_c], "constraint_parity", "uint16_t", lang='js'))

    to_augment.append(gen_array(original_f, "function_indices", "uint16_t", lang='js'))
    to_augment.append(gen_array([1 if i == 1 else 0 for i in parity_f], "function_parity", "uint16_t", lang='js'))

    desc = get_descriptions(solution)

    to_augment.append(gen_variable(desc['theta_dim'], "theta_dim", "int", lang='js'))
    to_augment.append(gen_variable(desc['x_dim'], "x_dim", "int", lang='js'))
    to_augment.append(gen_variable(desc['num_constraints'], "num_hyperplanes", "int", lang='js'))
    to_augment.append(gen_variable(desc['num_functions'], "num_functions", "int", lang='js'))
    to_augment.append(gen_variable(desc['num_regions'], "num_regions", "int", lang='js'))

    to_augment.append(gen_variable(len(fundamental_c), "num_fundamental_hyper_planes", "int", lang='js'))

    constraint_matrix = numpy.block([[region.E] for region in solution.critical_regions])
    constraint_matrix = constraint_matrix[fundamental_c].flatten().tolist()

    constraint_rhs = numpy.block([[region.f] for region in solution.critical_regions])
    constraint_rhs = constraint_rhs[fundamental_c].flatten().tolist()

    to_augment.append(gen_array(constraint_matrix, "constraint_matrix_data", float_type, lang='js'))
    to_augment.append(gen_array(constraint_rhs, "constraint_vector_data", float_type, lang='js'))

    function_matrix = numpy.block([[region.A] for region in solution.critical_regions])
    function_matrix = function_matrix[fundamental_f].flatten().tolist()

    function_rhs = numpy.block([[region.b] for region in solution.critical_regions])
    function_rhs = function_rhs[fundamental_f].flatten().tolist()

    to_augment.append(gen_array(function_matrix, "function_matrix_data", float_type, lang='js'))
    to_augment.append(gen_array(function_rhs, "function_vector_data", float_type, lang='js'))

    inset_data = "\n".join(to_augment)

    return js_upop.replace("<==PayloadHere==>", inset_data)


def generate_code_matlab(solution: Solution, path: str = '') -> None:
    """
    This code gen does not bother with memory compression as it is running in the matlab environment and takes ~1 gb to run anyways

    :param solution:
    :param path: File export path, if not specified will save in current working directory
    :return:
    """

    const_block = numpy.block([[k.E] for k in solution.critical_regions])
    const_vec = numpy.block([[k.f] for k in solution.critical_regions])

    func_block = numpy.block([[k.A] for k in solution.critical_regions])
    func_vec = numpy.block([[k.b] for k in solution.critical_regions])

    region_list = list()
    region_list.append(0)
    cursor = 0
    for i in solution.critical_regions:
        cursor += i.E.shape[0]
        region_list.append(cursor)

    num_regions = len(region_list) - 1
    region_list = numpy.array(region_list) + 1

    solution_information = {"constraint_block": const_block, "constraint_vector": const_vec,
                            "function_block": func_block, "function_vec": func_vec, "region_list": region_list,
                            "num_regions": num_regions}
    sio.savemat(path, {'upop_solution': solution_information})
