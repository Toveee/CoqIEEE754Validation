import sys
from core import *

DEFAULT_RM = "mode_NE"

def parse_test_vectors(file_path, op, frmt, rm):

    if op in ARG_1:
        fun = parse_args_1
    elif op in ARG_2:
        fun = parse_args_2
    elif op in ARG_3:
        fun = parse_args_3

    return _parse_test_vectors(file_path, op, frmt, fun, rm)

def parse_test_vector(line, op, frmt, rm):
    if op in ARG_1:
        fun = parse_args_1
    elif op in ARG_2:
        fun = parse_args_2
    elif op in ARG_3:
        fun = parse_args_3

    return _parse_test_vector(line, op, frmt, fun, rm)

def _parse_test_vector(line, op, frmt, fun, rm):
    (nums, expected) = fun(line)
    return create_test_vector(nums, expected, op, frmt, rm)

def _parse_test_vectors(file_path, op, frmt, parse_fun, rm):
    test_vectors = []
    with open(file_path, 'r') as file:
        for line in file:
            (nums, expected) = parse_fun(line)
            test_vectors.append(create_test_vector(nums, expected, op, frmt, rm))
    return test_vectors

def create_test_vector(nums, expected, op, frmt, rm):
    float_func = globals().get(f"{frmt}") # get the right function
    args = []
    for n in nums: # NOTE: nums should always be 1 or 2, at best 3 (but probably not)
        args.append(float_func("0x" + str(n)))

    return test_vector(rm, op, args, expected, frmt)

def parse_args_3(line):
    parts = line.strip().split()
    nums = parts[:3]
    expected = parts[3]
    return (nums, expected)

def parse_args_2(line):
    parts = line.strip().split()
    nums = parts[:2]
    expected = parts[2]
    return (nums, expected)

def parse_args_1(line):
    parts = line.strip().split()
    nums = [parts[0]]
    expected = parts[1]
    return (nums, expected)

def main(path, format, operation):
    vectors = parse_test_vectors(path, operation, format)
    for vector in vectors:
        print(vector.to_flocq(format))

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python parse_test_float.py <format> <file_path> <operation>")
    else:
        format, path, operation = sys.argv[1], sys.argv[2], sys.argv[3]
        if format not in FORMATS:
            print(f"Invalid format: {format}")
        elif operation not in OPERATIONS:
            print(f"Invalid operation: {operation}")
        else: 
            main(path, format, operation)