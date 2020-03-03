#!/usr/bin/env python3

import os
import subprocess

def generate_directories(start_dir, max_levels):

    max_level_string = 'directory_level_0'

    for i in range(1, max_levels):
        max_level_string = '{}/directory_level_{}'.format(max_level_string, i)


    full_path = os.path.join(start_dir, max_level_string)
    if not os.path.isdir(full_path):
        os.makedirs(full_path)

    return full_path


def generate_library(base_dir, library_path, lib_number):
    lib_header = open('library{}.h'.format(lib_number), 'w+')
    header = "void library_call_{}(const int level);\n".format(lib_number)
    lib_header.write(header)
    lib_header.close()

    lib_source = open('library{}.c'.format(lib_number), 'w+')
    if lib_number > 0:
        source  = "#include \"library{}.h\"\n\n".format(lib_number-1)
    else:
        source = "#include \"base.h\"\n\n"

    source += "void library_call_{}(const int level){{\n".format(lib_number)
    if lib_number > 0:
        source += "    library_call_{}(level);\n".format(lib_number-1)
    else:
        source += "    base_call(level);\n"

    source += "}\n\n"
    lib_source.write(source)
    lib_source.close()

    makefile = open('Makefile', 'w+')
    source  = "CC = icc\n"
    source += "CFLAGS = -ipo -fPIC -shared\n"
    source += "SRCS = library{}.c\n".format(lib_number)
    source += "LIBRARY = liblibrary{}.so\n".format(lib_number)
    if lib_number > 0:
        source += "INC = -I{}/library_{}\n".format(library_path, lib_number-1)
        source += "LIBS = -L{}/library_{} -llibrary{}\n".format(library_path, lib_number-1, lib_number-1)
        source += "CFLAGS += -Wl,-rpath {}/library_{}\n".format(library_path, lib_number-1)
    else:
        source += "INC = -I{}/base_library\n".format(base_dir)
        source += "LIBS = -L{}/base_library -lbase\n".format(base_dir)
        source += "CFLAGS += -Wl,-rpath {}/base_library\n".format(base_dir)

    source += "lib:\n"
    source += "\t$(CC) $(CFLAGS) $(INC) $(SRCS) -o $(LIBRARY) $(LIBS)\n\n"
    source += "clean:\n"
    source += "\trm -f *.so *.o\n"
    makefile.write(source)
    makefile.close()

    subprocess.check_call(['make', 'clean'])
    subprocess.check_call(['make', 'lib'])

def generate_libraries(lib_path, num_libs):

    start_dir = os.getcwd()

    for i in range(0, num_libs):
        library_path = os.path.join(lib_path, 'library_{}'.format(i))
        if not os.path.isdir(library_path):
            os.makedirs(library_path)
        os.chdir(library_path)

        generate_library(start_dir, lib_path, i)

def generate_tester(start_dir, lib_path, num_libs):
    os.chdir(start_dir)
    tester_dir = "{}/tester".format(start_dir)
    if not os.path.isdir(tester_dir):
        os.makedirs(tester_dir)

    source  = "#include <stdio.h>\n"
    source += "#include \"library{}.h\"\n\n".format(num_libs)
    source += "int main(int *argc, char **argv){{\n"
    source += "    printf(\"Main call. Level 0\\n\");\n"
    source += "    library_call_{}(0);\n".format(num_libs)
    source += "    return 0;\n"
    source += "}\n\n"
    source_file = open('test.cc', 'w+')
    source_file.write(source)
    source_file.close()

    source  = "CC = icc\n"
    source += "CFLAGS = -ipo -fPIC\n"
    source += "SRCS = test.cc\n"
    source += "EXEC = testing.x\n\n"
    source += "LIBS = -L{}/library_{} -llibrary{}\n".format(lib_path, num_libs, num_libs)
    source += "INC  = -I{}/library_{}\n".format(lib_path, num_libs)
    source += "all:\n"
    source += "\t$(CC) $(CFLAGS) $(INC) $(SRCS) -o $(EXEC) $(LIBS)\n"
    source += "clean:\n"
    source += "\trm -f *.o $(EXEC)\n"
    makefile = open('Makefile', 'w+')
    makefile.write(source)
    makefile.close()

    subprocess.check_call(['make', 'clean'])
    subprocess.check_call(['make'])

if __name__ == "__main__":
    start_dir = os.getcwd()
    base_lib_dir = '{}/{}'.format(start_dir, 'base_library')

    num_levels = 15

    lib_path = generate_directories(start_dir, num_levels)
    generate_libraries(lib_path, num_levels)
    generate_tester(start_dir, lib_path, num_levels)



