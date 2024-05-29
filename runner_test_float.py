import sys
import time
from core import *
from parse_test_float import *

TEST_FILE_PATH = "tmp.v"
# CHUNK_SIZE = 100000
CHUNK_SIZE = 500000
# CHUNK_SIZE = 1

def int_to_hex(n: int, format: str):
    match format:
        case "b32":
            return f'{n:08X}'
        case "b64":
            return f'{n:016X}'
        case _:
            raise ValueError(f"Invalid format 'int_to_hex': {format}")

def run_tests(test_vectors, test_path):
    output = run_coqc(test_path)
    result = parse_coq(output)

    assert(len(test_vectors) == len(result))

    converted_result = [int_to_hex(num, format) for num in result]

    failed_counter = 0

    for i in range(len(converted_result)):
        if not test_vectors[i].check(converted_result[i]):
            failed_counter += 1
            print(f"Test failed. Case: ({test_vectors[i]}) Result: {converted_result[i]}")
            # print(f"Test {i+count_from} failed. Expected: {test_vectors[i].expct}, Result: {converted_result[i]}")
        # else:
        #     print(f"Test {i+count_from} passed.")

    return failed_counter


def testing(path, format, operation, rm):
    start_time = time.time()
    test_counter, failed_counter = 0, 0
    test_vectors, test_input = [], COQ_IMPORTS

    with open(path, 'r') as vector_file:
        while True:
            line = vector_file.readline()

            if line == "": 
                with open(TEST_FILE_PATH, 'w') as test_file:
                    test_file.write(test_input)
                failed_counter += run_tests(test_vectors, TEST_FILE_PATH)
                break

            test_counter += 1
            test = parse_test_vector(line, operation, format, rm)
            test_vectors.append(test)
            test_input += "\n" + test.to_flocq()

            if len(test_vectors) == CHUNK_SIZE:
                with open(TEST_FILE_PATH, 'w') as test_file:
                    test_file.write(test_input)

                failed_counter += run_tests(test_vectors, TEST_FILE_PATH)
                test_vectors, test_input = [], COQ_IMPORTS

    print(f"Ran {test_counter} tests ({path}). {failed_counter} tests failed. Time elapsed: {round(time.time() - start_time, 2)}")

def main(path, format, operation, rm):
    testing(path, format, operation, rm)

if __name__ == "__main__":

    VALID_OPERATIONS = ["add", "div", "mul", "sqrt", "sub", "mulAdd"]
    VALID_FORMATS = ["f32", "f64"]
    VALID_ROUNDING = ["rnear_even", "rnear_maxMag", "rminMag", "rmin", "rmax"]
    if len(sys.argv) != 5:
        print("Usage: python runner_test_float.py <format> <file_path> <operation> <rounding>")
    else:
        format, path, operation, rm = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
        if format not in VALID_FORMATS:
            print(f"Invalid format: {format}")
        elif operation not in VALID_OPERATIONS:
            print(f"Invalid operation: {operation}")
        elif rm not in VALID_ROUNDING:
            print(f"Invalid rounding mode: {rm}")
        else: 
            match format:
                case "f32": format = "b32"
                case "f64": format = "b64"
                case _: raise ValueError(f"Invalid format: {format}")
            match operation:
                case "add": operation = "plus"
                case "sub": operation = "minus"
                case "mul": operation = "mult"
                case "mulAdd": operation = "fma"
                case _: operation = operation
            match rm:
                case "rnear_even": rm = "mode_NE"
                case "rnear_maxMag": rm = "mode_NA"
                case "rminMag": rm = "mode_ZR"
                case "rmin": rm = "mode_DN"
                case "rmax": rm = "mode_UP"

            assert(rm in ROUNDING_MODES)

            main(path, format, operation, rm)