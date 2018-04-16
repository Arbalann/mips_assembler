import re


class MipsParsingError(Exception):

    current_parsed_line = None

    def __init__(self, message):
        message += "\nCurrent line: <{}>".format(MipsParsingError.current_parsed_line)
        super().__init__(message)


class _MipsAssembly(object):

    def __init__(self, assembly):
        self._original_assembly = assembly
        self._parse_instruction(assembly)

    def _parse_instruction(self, assembly):
        parts = assembly.split(maxsplit=1)
        self._instruction = parts[0]
        if len(parts) > 1:
            arguments = parts[1]
        else:
            arguments = ""

        # -----------------------------
        # ---------- J Types ----------
        # -----------------------------

        if self._instruction == "j":
            self._parse_arguments(arguments, instruction_type="J", argument_format_string="j", opcode=0x2)
        elif self._instruction == "jal":
            self._parse_arguments(arguments, instruction_type="J", argument_format_string="j", opcode=0x3)

        # -----------------------------
        # ---------- I Types ----------
        # -----------------------------

        elif self._instruction == "beq":
            self._parse_arguments(arguments, instruction_type="I", argument_format_string="sti", opcode=0x4)
        elif self._instruction == "bne":
            self._parse_arguments(arguments, instruction_type="I", argument_format_string="sti", opcode=0x5)
        elif self._instruction == "blez":
            self._parse_arguments(arguments, instruction_type="I", argument_format_string="si", opcode=0x6)
        elif self._instruction == "bgtz":
            self._parse_arguments(arguments, instruction_type="I", argument_format_string="si", opcode=0x7)
        elif self._instruction == "addi":
            self._parse_arguments(arguments, instruction_type="I", argument_format_string="(ts)i,tsi", opcode=0x8)
        elif self._instruction == "addiu":
            self._parse_arguments(arguments, instruction_type="I", argument_format_string="(ts)i,tsi", opcode=0x9)
        elif self._instruction == "slti":
            self._parse_arguments(arguments, instruction_type="I", argument_format_string="(ts)i,tsi", opcode=0xA)
        elif self._instruction == "sltiu":
            self._parse_arguments(arguments, instruction_type="I", argument_format_string="(ts)i,tsi", opcode=0xB)
        elif self._instruction == "andi":
            self._parse_arguments(arguments, instruction_type="I", argument_format_string="(ts)i,tsi", opcode=0xC)
        elif self._instruction == "ori":
            self._parse_arguments(arguments, instruction_type="I", argument_format_string="(ts)i,tsi", opcode=0xD)
        elif self._instruction == "xori":
            self._parse_arguments(arguments, instruction_type="I", argument_format_string="(ts)i,tsi", opcode=0xE)
        elif self._instruction == "lui":
            self._parse_arguments(arguments, instruction_type="I", argument_format_string="ti", opcode=0xF)
        elif self._instruction == "lb":
            self._parse_arguments(arguments, instruction_type="I", argument_format_string="*tis", opcode=0x20)
        elif self._instruction == "lh":
            self._parse_arguments(arguments, instruction_type="I", argument_format_string="*tis", opcode=0x21)
        elif self._instruction == "lwl":
            self._parse_arguments(arguments, instruction_type="I", argument_format_string="*tis", opcode=0x22)
        elif self._instruction == "lw":
            self._parse_arguments(arguments, instruction_type="I", argument_format_string="*tis", opcode=0x23)
        elif self._instruction == "lbu":
            self._parse_arguments(arguments, instruction_type="I", argument_format_string="*tis", opcode=0x24)
        elif self._instruction == "lhu":
            self._parse_arguments(arguments, instruction_type="I", argument_format_string="*tis", opcode=0x25)
        elif self._instruction == "lwr":
            self._parse_arguments(arguments, instruction_type="I", argument_format_string="*tis", opcode=0x26)
        elif self._instruction == "sb":
            self._parse_arguments(arguments, instruction_type="I", argument_format_string="*tis", opcode=0x28)
        elif self._instruction == "sh":
            self._parse_arguments(arguments, instruction_type="I", argument_format_string="*tis", opcode=0x29)
        elif self._instruction == "swl":
            self._parse_arguments(arguments, instruction_type="I", argument_format_string="*tis", opcode=0x2a)
        elif self._instruction == "sw":
            self._parse_arguments(arguments, instruction_type="I", argument_format_string="*tis", opcode=0x2b)
        elif self._instruction == "swr":
            self._parse_arguments(arguments, instruction_type="I", argument_format_string="*tis", opcode=0x2e)

        # -------- Opcode 0x1 Extension --------

        elif self._instruction == "bltz":
            self._parse_arguments(arguments, instruction_type="I", argument_format_string="si",
                                  opcode=0x1, rt="$0")
        elif self._instruction == "bgez":
            self._parse_arguments(arguments, instruction_type="I", argument_format_string="si",
                                  opcode=0x1, rt="$1")
        elif self._instruction == "tgei":
            self._parse_arguments(arguments, instruction_type="I", argument_format_string="si",
                                  opcode=0x1, rt="$8")
        elif self._instruction == "tgeiu":
            self._parse_arguments(arguments, instruction_type="I", argument_format_string="si",
                                  opcode=0x1, rt="$9")
        elif self._instruction == "tlti":
            self._parse_arguments(arguments, instruction_type="I", argument_format_string="si",
                                  opcode=0x1, rt="$10")
        elif self._instruction == "tltiu":
            self._parse_arguments(arguments, instruction_type="I", argument_format_string="si",
                                  opcode=0x1, rt="$11")
        elif self._instruction == "teqi":
            self._parse_arguments(arguments, instruction_type="I", argument_format_string="si",
                                  opcode=0x1, rt="$12")
        elif self._instruction == "tnei":
            self._parse_arguments(arguments, instruction_type="I", argument_format_string="si",
                                  opcode=0x1, rt="$14")
        elif self._instruction == "bltzal":
            self._parse_arguments(arguments, instruction_type="I", argument_format_string="si",
                                  opcode=0x1, rt="$16")
        elif self._instruction == "bgezal":
            self._parse_arguments(arguments, instruction_type="I", argument_format_string="si",
                                  opcode=0x1, rt="$17")

        # -----------------------------
        # ---------- R Types ----------
        # -----------------------------

        elif self._instruction == "sll":
            self._parse_arguments(arguments, instruction_type="R", argument_format_string="(dt)a,dta", funct=0x0)
        elif self._instruction == "srl":
            self._parse_arguments(arguments, instruction_type="R", argument_format_string="(dt)a,dta", funct=0x2)
        elif self._instruction == "sra":
            self._parse_arguments(arguments, instruction_type="R", argument_format_string="(dt)a,dta", funct=0x3)
        elif self._instruction == "sllv":
            self._parse_arguments(arguments, instruction_type="R", argument_format_string="(dt)s,dts", funct=0x4)
        elif self._instruction == "srav":
            self._parse_arguments(arguments, instruction_type="R", argument_format_string="(dt)s,dts", funct=0x6)
        elif self._instruction == "srlv":
            self._parse_arguments(arguments, instruction_type="R", argument_format_string="(dt)s,dts", funct=0x7)
        elif self._instruction == "jr":
            self._parse_arguments(arguments, instruction_type="R", argument_format_string="s", funct=0x8)
        elif self._instruction == "jalr":
            self._parse_arguments(arguments, instruction_type="R", argument_format_string="s,sd", funct=0x9, rd="$ra")
        elif self._instruction == "mult":
            self._parse_arguments(arguments, instruction_type="R", argument_format_string="st", funct=0x18)
        elif self._instruction == "multu":
            self._parse_arguments(arguments, instruction_type="R", argument_format_string="st", funct=0x19)
        elif self._instruction == "div":
            self._parse_arguments(arguments, instruction_type="R", argument_format_string="st", funct=0x1A)
        elif self._instruction == "divu":
            self._parse_arguments(arguments, instruction_type="R", argument_format_string="st", funct=0x1B)
        elif self._instruction == "add":
            self._parse_arguments(arguments, instruction_type="R", argument_format_string="(ds)t,dst", funct=0x20)
        elif self._instruction == "addu":
            self._parse_arguments(arguments, instruction_type="R", argument_format_string="(ds)t,dst", funct=0x21)
        elif self._instruction == "sub":
            self._parse_arguments(arguments, instruction_type="R", argument_format_string="(ds)t,dst", funct=0x22)
        elif self._instruction == "subu":
            self._parse_arguments(arguments, instruction_type="R", argument_format_string="(ds)t,dst", funct=0x23)
        elif self._instruction == "and":
            self._parse_arguments(arguments, instruction_type="R", argument_format_string="(ds)t,dst", funct=0x24)
        elif self._instruction == "or":
            self._parse_arguments(arguments, instruction_type="R", argument_format_string="(ds)t,dst", funct=0x25)
        elif self._instruction == "xor":
            self._parse_arguments(arguments, instruction_type="R", argument_format_string="(ds)t,dst", funct=0x26)
        elif self._instruction == "nor":
            self._parse_arguments(arguments, instruction_type="R", argument_format_string="(ds)t,dst", funct=0x27)
        elif self._instruction == "slt":
            self._parse_arguments(arguments, instruction_type="R", argument_format_string="(ds)t,dst", funct=0x2A)
        elif self._instruction == "sltu":
            self._parse_arguments(arguments, instruction_type="R", argument_format_string="(ds)t,dst", funct=0x2B)
        elif self._instruction == "tge":
            self._parse_arguments(arguments, instruction_type="R", argument_format_string="st", funct=0x30)
        elif self._instruction == "tgeu":
            self._parse_arguments(arguments, instruction_type="R", argument_format_string="st", funct=0x31)
        elif self._instruction == "tlt":
            self._parse_arguments(arguments, instruction_type="R", argument_format_string="st", funct=0x32)
        elif self._instruction == "tltu":
            self._parse_arguments(arguments, instruction_type="R", argument_format_string="st", funct=0x33)
        elif self._instruction == "teq":
            self._parse_arguments(arguments, instruction_type="R", argument_format_string="st", funct=0x34)
        elif self._instruction == "tne":
            self._parse_arguments(arguments, instruction_type="R", argument_format_string="st", funct=0x36)

        # -------- Opcode 0x1C Extension --------

        elif self._instruction == "madd":
            self._parse_arguments(arguments, instruction_type="R", argument_format_string="st",
                                  opcode=0x1C, funct=0x0)
        elif self._instruction == "maddu":
            self._parse_arguments(arguments, instruction_type="R", argument_format_string="st",
                                  opcode=0x1C, funct=0x1)
        elif self._instruction == "mul":
            self._parse_arguments(arguments, instruction_type="R", argument_format_string="(ds)t,dst",
                                  opcode=0x1C, funct=0x2)
        elif self._instruction == "msub":
            self._parse_arguments(arguments, instruction_type="R", argument_format_string="st",
                                  opcode=0x1C, funct=0x4)
        elif self._instruction == "msubu":
            self._parse_arguments(arguments, instruction_type="R", argument_format_string="st",
                                  opcode=0x1C, funct=0x5)
        elif self._instruction == "clz":
            self._parse_arguments(arguments, instruction_type="R", argument_format_string="(ds)t,dst",
                                  opcode=0x1C, funct=0x20)
        elif self._instruction == "clo":
            self._parse_arguments(arguments, instruction_type="R", argument_format_string="(ds)t,dst",
                                  opcode=0x1C, funct=0x21)

        else:
            raise MipsParsingError("The '{}' instruction is not valid or is not yet supported by this assembler"
                                   .format(self._instruction))

    def _parse_arguments(self, arguments,  instruction_type, argument_format_string, opcode=0, funct=0,
                         rs="$0", rt="$0", rd="$0", sa="0", immediate="0", jump_target="0"):

        self._instruction_type = instruction_type
        self._opcode = opcode
        self._funct = funct

        # Set default values
        self._rs = rs
        self._rt = rt
        self._rd = rd
        self._sa = sa
        self._immediate = immediate
        self._jump_target = jump_target

        # Split the argument string into a list of the arguments passed in
        arguments = self._split_arguments(arguments, argument_format_string)
        argument_format_string = argument_format_string.replace("*", "")

        # Match the argument format string with the amount of arguments passed in
        argument_format_string = self._determine_argument_format(len(arguments), argument_format_string)

        # Override the default values with the arguments that were passed in
        self._set_argument_values(arguments, argument_format_string)

        # Turn registers into their numerical equivalent
        self._rs = self._get_register_id(self._rs)
        self._rt = self._get_register_id(self._rt)
        self._rd = self._get_register_id(self._rd)

        # Validate that the supplied equations can be solved once we get all labels
        self._test_evaluate(self._sa)
        self._test_evaluate(self._immediate)
        self._test_evaluate(self._jump_target)

    def _split_arguments(self, arguments, argument_format_string):
        arguments = arguments.split(",")
        if argument_format_string.startswith("*"):
            last_arg = arguments[-1]
            if "(" in last_arg and last_arg[-1] == ")":
                last_arg = last_arg.rsplit("(", maxsplit=1)
                arguments[-1] = last_arg[0]
                arguments.append(last_arg[1][:-1])
            else:
                raise MipsParsingError("The '{}' instruction should be in the format '{} $0, 0($0)'"
                                       .format(self._instruction, self._instruction))
        return arguments

    def _determine_argument_format(self, argument_count, argument_format_string):
        argument_formats = argument_format_string.split(",")
        argument_counts = []
        for argument_format in argument_formats:
            argument_counts.append(0)
            inside_parenthesis = False
            for char in argument_format:
                if char == "(" and not inside_parenthesis:
                    inside_parenthesis = True
                    argument_counts[-1] += 1
                elif char == ")" and inside_parenthesis:
                    inside_parenthesis = False
                elif not inside_parenthesis:
                    argument_counts[-1] += 1

        if argument_count not in argument_counts:
            raise MipsParsingError("The instruction '{}' accepts {} arguments but was provided {}"
                                   .format(self._instruction, " or ".join(map(str, argument_counts)), argument_count))
        argument_index = argument_counts.index(argument_count)
        return argument_formats[argument_index]

    def _set_argument_values(self, arguments, argument_format_string):
        inside_parenthesis = False
        argument_index = 0
        for char in argument_format_string:
            if char == "(" and not inside_parenthesis:
                inside_parenthesis = True
            elif char == ")" and inside_parenthesis:
                inside_parenthesis = False
                argument_index += 1
            else:
                if char == "s":
                    self._rs = arguments[argument_index]
                elif char == "t":
                    self._rt = arguments[argument_index]
                elif char == "d":
                    self._rd = arguments[argument_index]
                elif char == "a":
                    self._sa = arguments[argument_index]
                elif char == "i":
                    self._immediate = arguments[argument_index]
                elif char == "j":
                    self._jump_target = arguments[argument_index]

                if not inside_parenthesis:
                    argument_index += 1

    def _get_register_id(self, register):
        register = register.strip()
        if register in ["$zero", "$0"]:
            register_id = 0
        elif register in ["$at", "$1"]:
            register_id = 1
        elif register in ["$v0", "$2"]:
            register_id = 2
        elif register in ["$v1", "$3"]:
            register_id = 3
        elif register in ["$a0", "$4"]:
            register_id = 4
        elif register in ["$a1", "$5"]:
            register_id = 5
        elif register in ["$a2", "$6"]:
            register_id = 6
        elif register in ["$a3", "$7"]:
            register_id = 7
        elif register in ["$t0", "$8"]:
            register_id = 8
        elif register in ["$t1", "$9"]:
            register_id = 9
        elif register in ["$t2", "$10"]:
            register_id = 10
        elif register in ["$t3", "$11"]:
            register_id = 11
        elif register in ["$t4", "$12"]:
            register_id = 12
        elif register in ["$t5", "$13"]:
            register_id = 13
        elif register in ["$t6", "$14"]:
            register_id = 14
        elif register in ["$t7", "$15"]:
            register_id = 15
        elif register in ["$s0", "$16"]:
            register_id = 16
        elif register in ["$s1", "$17"]:
            register_id = 17
        elif register in ["$s2", "$18"]:
            register_id = 18
        elif register in ["$s3", "$19"]:
            register_id = 19
        elif register in ["$s4", "$20"]:
            register_id = 20
        elif register in ["$s5", "$21"]:
            register_id = 21
        elif register in ["$s6", "$22"]:
            register_id = 22
        elif register in ["$s7", "$23"]:
            register_id = 23
        elif register in ["$t8", "$24"]:
            register_id = 24
        elif register in ["$t9", "$25"]:
            register_id = 25
        elif register in ["$k0", "$26"]:
            register_id = 26
        elif register in ["$k1", "$27"]:
            register_id = 27
        elif register in ["$gp", "$28"]:
            register_id = 28
        elif register in ["$sp", "$29"]:
            register_id = 29
        elif register in ["$fp", "$30", "$s8"]:
            register_id = 30
        elif register in ["$ra", "$31"]:
            register_id = 31
        else:
            raise MipsParsingError("The value '{}' is not a valid register".format(register))

        return register_id

    def _test_evaluate(self, expression):
        # Replace labels with 0 for the test
        while True:
            match = re.search("[A-Za-z_][A-Za-z0-9_]*", expression)
            if match is None:
                break
            if match.start() != 0 and ord("0") <= ord(expression[match.start() - 1]) <= ord("9"):
                raise MipsParsingError("Label '{}' is not allowed to be prefixed with a number".format(match.group()))
            expression = expression.replace(match.group(), "0", 1)

        # Validate that only math related characters are in the expression
        # eval() has potential security implications so this lessens the chance eval can cause harm
        match = re.match("^[0-9+\-/*^. ]+$", expression)
        if match is None:
            raise MipsParsingError("Found illegal characters in the '{}' expression".format(expression))

        # Attempt to calculate the result
        try:
            int(eval(expression))
        except:
            raise MipsParsingError("Failed to calculate the '{}' expression".format(expression))


class _MipsLabel(object):

    def __init__(self, label):
        self._label = label
        self._validate_label()

    def _validate_label(self):
        match = re.match("^[A-Za-z_][A-Za-z0-9_]*$", self._label)
        if match is None:
            raise MipsParsingError("The label '{}' contains invalid characters".format(self._label))

    def get_label(self):
        return self._label


class _MipsDirective(object):

    def __init__(self, directive):
        self._parse_directive(directive)

    def _parse_directive(self, directive):
        parts = directive.split(maxsplit=1)
        self._directive = parts[0]
        if len(parts) > 1:
            arguments = parts[1]
        else:
            arguments = ""

        if self._directive == ".section":
            self._parse_section_arguments(arguments)
        elif self._directive == ".set":
            self._parse_set_arguments(arguments)
        elif self._directive == ".align":
            raise MipsParsingError("The directive '{}' is unsupported".format(self._directive))
        elif self._directive == ".ascii":
            raise MipsParsingError("The directive '{}' is unsupported".format(self._directive))
        elif self._directive == ".asciiz":
            raise MipsParsingError("The directive '{}' is unsupported".format(self._directive))
        elif self._directive == ".space":
            raise MipsParsingError("The directive '{}' is unsupported".format(self._directive))
        elif self._directive == ".word":
            raise MipsParsingError("The directive '{}' is unsupported".format(self._directive))
        elif self._directive == ".hword":
            raise MipsParsingError("The directive '{}' is unsupported".format(self._directive))
        elif self._directive == ".byte":
            raise MipsParsingError("The directive '{}' is unsupported".format(self._directive))
        else:
            raise MipsParsingError("The directive '{}' is unsupported".format(self._directive))

    def _parse_set_arguments(self, arguments):
        if arguments not in ["reorder", "noreorder"]:
            raise MipsParsingError("The .set directive doesn't support the '{}' argument".format(arguments))
        self._arguments = arguments

    def _parse_section_arguments(self, arguments):
        match = re.match("^(\.[A-Za-z][A-Za-z0-9]*)+$", arguments)
        if match is None:
            raise MipsParsingError("Section name '{}' is invalid".format(arguments))
        self._arguments = arguments

    def get_directive(self):
        return self._directive

    def get_arguments(self):
        return self._arguments


class _MipsSection(object):

    def __init__(self):
        pass

    def add(self, line):
        pass


class MipsAssembler(object):

    def __init__(self, code=None):
        self._default_section = ".text"
        self._default_reorder = True

        self._sections = {}

        if code is not None:
            self.add(code)

    @staticmethod
    def _strip_comments(line):
        i = 0
        in_quotes = False
        while i < len(line):
            if line[i] == "\"":
                in_quotes = not in_quotes
            elif line[i] == "\\" and in_quotes:
                i += 1
            elif line[i] == "#":
                line = line[:i]
            i += 1
        return line

    def _parse_line(self, line):
        MipsParsingError.current_parsed_line = line
        line = line.strip()
        line = self._strip_comments(line)

        parsed_items = []
        while len(line) > 0:
            if line.startswith("."):
                parsed_items.append(_MipsDirective(line))
                line = ""
            elif ":" in line:
                parts = line.split(":", maxsplit=1)
                parsed_items.append(_MipsLabel(parts[0]))
                line = parts[1].strip()
            else:
                parsed_items.append(_MipsAssembly(line))
                line = ""

        return parsed_items

    def _add_to_section(self, section, item):
        if section not in self._sections.keys():
            self._sections[section] = []
        self._sections[section].append(item)

    def add(self, code):
        current_section = self._default_section

        code = code.split("\n")
        for line in code:
            parsed = self._parse_line(line)
            for item in parsed:
                if type(item) is _MipsDirective and item.get_directive() == ".section":
                    current_section = item.get_arguments()
                else:
                    self._add_to_section(current_section, item)


if __name__ == "__main__":
    assembler = MipsAssembler()
    assembler.add("""
        lui   $t0, 1
        ori $t0, 2
        label: label2: .set noreorder
        .section .text.start
        lw  $t1, 1+ label1 + 0($t9)
        ori $t0, 2
        .section .text
        label: label2: .set noreorder
    """)
    for section, items in assembler._sections.items():
        print(section)
        for item in items:
            print("\t" + str(item))
