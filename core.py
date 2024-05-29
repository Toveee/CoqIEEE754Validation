import subprocess
import re

FORMATS = ["b32", "b64"]

SQRT, PLUS, MINUS, MULT, DIV, FMA = "sqrt", "plus", "minus", "mult", "div", "fma"
OPERATIONS = [SQRT, PLUS, MINUS, MULT, DIV, FMA]

COQ_IMPORTS = "Require Import BinNums BinInt ZArith Floats. \nFrom Flocq Require Import Core FLT Operations Bits BinarySingleNaN Binary PrimFloat.\n"

ROUNDING_MODES = ["mode_NE", "mode_ZR", "mode_DN", "mode_UP", "mode_NA" ]

ARG_3 = [FMA]
ARG_2 = [PLUS, MINUS, MULT, DIV]
ARG_1 = [SQRT]

EVAL = "Eval vm_compute in "

class _binary_float:
    def __init__(self, bin: str):
        assert(bin[:2] == "0x")
        self.bin = bin

    def to_flocq(self, format: str):
        assert(format in FORMATS)
        arg = "Z0" if int(self.bin, 16) == 0 else f"(Zpos ({self.bin})%positive)"
        match format:
            case "b32":
                return f" (b32_of_bits {arg}) "
            case "b64":
                return f" (b64_of_bits {arg}) "
        
class b32(_binary_float):
    def __init__(self, bin: str):
        super().__init__(bin)

    def __str__(self):
        return self.bin
    
    def to_flocq(self):
        return super().to_flocq("b32")    

class b64(_binary_float):
    def __init__(self, bin: str):
        super().__init__(bin)

    def __str__(self):
        return self.bin

    def to_flocq(self):
        return super().to_flocq("b64")

class test_vector:
    def __init__(self, rm: str, op: str, args, expct: str, format):
        # rounding mode and operation must have the same name as the operation in flocq
        self.rm = rm
        self.op = op 
        self.args = args
        self.expct = expct
        self.format = format
    
    def __str__(self):
        args = " "
        for arg in self.args:
            args += arg.bin + " "

        return f"{self.format} {self.rm} {self.op} [{args}] {self.expct}"

    def to_flocq(self):
        str_args = ""
        for n in self.args:
            str_args += n.to_flocq()
        return f"{EVAL} bits_of_{self.format} ({self.format}_erase ({self.format}_{self.op} {self.rm} {str_args}))."
    
    def check(self, result: str):
        if is_nan(self.expct, self.format) and is_nan(result, self.format):
            return True
        else:
            return self.expct == result
        
    def check_no_nan(self, result: str):
        return self.expct == result

def run_coqc(file_path):
    # Call coqc with the file path and argument
    process = subprocess.Popen(['coqc', file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # Get output
    stdout, stderr = process.communicate()

    stdout_str = stdout.decode('utf-8')
    stderr_str = stderr.decode('utf-8')

    if stderr_str != "":
        print(stderr)
        raise ValueError("Error in Coq occurred.")

    return stdout_str 

def is_nan(bin: str, format):
    n = int(bin, 16)
    match format:
        case "b32":
            e = f'{n:032b}'[1:9]
            
        case "b64":
            e = f'{n:064b}'[1:12]
        case _:
            raise ValueError(f"Unknown format: {format}")
    for bit in e:
        if bit != "1":
            return False
        
    return True

def parse_coq(s: str):
    numbers = re.findall(r'= (\d+)%Z', s)
    return [int(num) for num in numbers]
