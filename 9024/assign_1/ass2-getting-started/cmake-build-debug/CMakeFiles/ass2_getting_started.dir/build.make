# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.15

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /Applications/CLion.app/Contents/bin/cmake/mac/bin/cmake

# The command to remove a file.
RM = /Applications/CLion.app/Contents/bin/cmake/mac/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /Users/huhawel/Documents/unsw_course/9024/assign_1/ass2-getting-started

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /Users/huhawel/Documents/unsw_course/9024/assign_1/ass2-getting-started/cmake-build-debug

# Include any dependencies generated for this target.
include CMakeFiles/ass2_getting_started.dir/depend.make

# Include the progress variables for this target.
include CMakeFiles/ass2_getting_started.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/ass2_getting_started.dir/flags.make

CMakeFiles/ass2_getting_started.dir/exTkns.c.o: CMakeFiles/ass2_getting_started.dir/flags.make
CMakeFiles/ass2_getting_started.dir/exTkns.c.o: ../exTkns.c
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/huhawel/Documents/unsw_course/9024/assign_1/ass2-getting-started/cmake-build-debug/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building C object CMakeFiles/ass2_getting_started.dir/exTkns.c.o"
	/Library/Developer/CommandLineTools/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -o CMakeFiles/ass2_getting_started.dir/exTkns.c.o   -c /Users/huhawel/Documents/unsw_course/9024/assign_1/ass2-getting-started/exTkns.c

CMakeFiles/ass2_getting_started.dir/exTkns.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/ass2_getting_started.dir/exTkns.c.i"
	/Library/Developer/CommandLineTools/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /Users/huhawel/Documents/unsw_course/9024/assign_1/ass2-getting-started/exTkns.c > CMakeFiles/ass2_getting_started.dir/exTkns.c.i

CMakeFiles/ass2_getting_started.dir/exTkns.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/ass2_getting_started.dir/exTkns.c.s"
	/Library/Developer/CommandLineTools/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /Users/huhawel/Documents/unsw_course/9024/assign_1/ass2-getting-started/exTkns.c -o CMakeFiles/ass2_getting_started.dir/exTkns.c.s

# Object files for target ass2_getting_started
ass2_getting_started_OBJECTS = \
"CMakeFiles/ass2_getting_started.dir/exTkns.c.o"

# External object files for target ass2_getting_started
ass2_getting_started_EXTERNAL_OBJECTS =

ass2_getting_started: CMakeFiles/ass2_getting_started.dir/exTkns.c.o
ass2_getting_started: CMakeFiles/ass2_getting_started.dir/build.make
ass2_getting_started: CMakeFiles/ass2_getting_started.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/Users/huhawel/Documents/unsw_course/9024/assign_1/ass2-getting-started/cmake-build-debug/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking C executable ass2_getting_started"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/ass2_getting_started.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/ass2_getting_started.dir/build: ass2_getting_started

.PHONY : CMakeFiles/ass2_getting_started.dir/build

CMakeFiles/ass2_getting_started.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/ass2_getting_started.dir/cmake_clean.cmake
.PHONY : CMakeFiles/ass2_getting_started.dir/clean

CMakeFiles/ass2_getting_started.dir/depend:
	cd /Users/huhawel/Documents/unsw_course/9024/assign_1/ass2-getting-started/cmake-build-debug && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /Users/huhawel/Documents/unsw_course/9024/assign_1/ass2-getting-started /Users/huhawel/Documents/unsw_course/9024/assign_1/ass2-getting-started /Users/huhawel/Documents/unsw_course/9024/assign_1/ass2-getting-started/cmake-build-debug /Users/huhawel/Documents/unsw_course/9024/assign_1/ass2-getting-started/cmake-build-debug /Users/huhawel/Documents/unsw_course/9024/assign_1/ass2-getting-started/cmake-build-debug/CMakeFiles/ass2_getting_started.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/ass2_getting_started.dir/depend
