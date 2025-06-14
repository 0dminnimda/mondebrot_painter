#define NOB_IMPLEMENTATION
#define NOB_STRIP_PREFIX
#include "nob.h"

#define cxx(cmd) cmd_append((cmd), "clang++")
#define common_flags(cmd) cmd_append((cmd), "-O3", "-Wno-unused-const-variable")
// , "-march=native"
#define get_arg(argv, argc) (argc > 0? shift(argv, argc) : "")

#define SRC "main.cpp"
#define EXE "mondex.exe"


bool set_enviroment_variable(const char *name, const char *value) {
    nob_log(NOB_INFO, "ENV: %s=%s", name, value);
#ifdef _WIN32
    if (_putenv_s(name, value) != 0) {
        nob_log(NOB_ERROR, "Failed to set environment variable: %s", nob_win32_error_message(GetLastError()));
        return false;
    }
#else
    if (setenv(name, value, /*overwrite=*/true) != 0) {
        nob_log(NOB_ERROR, "Failed to set environment variable: %s", strerror(errno));
        return false;
    }
#endif
    return true;
}


typedef enum {
    OPTIMIZED,
    COVERAGE,
    ASSEMBLY,
} Compilation_Mode;


bool compile(Compilation_Mode mode) {
    Cmd cmd = {0};

    cxx(&cmd);

    if (mode == ASSEMBLY) {
        nob_cc_output(&cmd, "mondex.asm");
        cmd_append(&cmd, "-c", SRC);

        cmd_append(&cmd, "-S", "-mllvm", "--x86-asm-syntax=intel");
    } else {
        nob_cc_output(&cmd, EXE);
        cmd_append(&cmd, SRC);

        nob_cc_flags(&cmd);
        cmd_append(&cmd, "-lraylib");
    }

    common_flags(&cmd);

    if (mode == COVERAGE) {
        cmd_append(&cmd, "-g", "-fprofile-instr-generate", "-fcoverage-mapping");
    }

    return cmd_run_sync(cmd);
}

bool compile_and_run(Compilation_Mode mode) {
    if (!compile(mode)) return 1;

    Cmd cmd = {0};
    cmd_append(&cmd, EXE);
    return cmd_run_sync_and_reset(&cmd);
}

bool analyze_perf() {
    set_enviroment_variable("LLVM_PROFILE_FILE", "mondex.profraw");
    if (!compile_and_run(COVERAGE)) return 1;

    Cmd cmd = {0};
    cmd_append(&cmd, "llvm-profdata", "merge", "-sparse", "mondex.profraw", "-o", "mondex.profdata");
    if (!cmd_run_sync_and_reset(&cmd)) return 1;

    cmd_append(&cmd, "llvm-cov", "show", EXE, "-instr-profile=mondex.profdata");
    if (!cmd_run_sync_and_reset(&cmd)) return 1;

    return 0;
}

int help(char *program) {
    printf("\n");
    printf("Usage: %s [COMMAND]\n", program);
    printf("COMMAND:\n");
    printf("    help         show this message and exit\n");
    printf("    asm          compile the program and output assembly\n");
    printf("    perf         compile the program then run it and output performance insights\n");
    printf("    run          compile and run the program\n");
    printf("\n");
    printf("The default action is to just compile the program\n");
    return 0;
}

int main(int argc, char **argv) {
    NOB_GO_REBUILD_URSELF(argc, argv);

    char *program = get_arg(argv, argc);
    char *target = get_arg(argv, argc);

    if (strcmp(target, "help") == 0) {
        return help(program);
    } else if (strcmp(target, "asm") == 0) {
        if (!compile(ASSEMBLY)) return 1;
    } else if (strcmp(target, "perf") == 0) {
        if (!analyze_perf()) return 1;
    } else if (strcmp(target, "run") == 0) {
        if (!compile_and_run(OPTIMIZED)) return 1;
    } else {
        if (!compile(OPTIMIZED)) return 1;
    }

    return 0;
}
