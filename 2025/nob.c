#define NOB_IMPLEMENTATION
#include "nob.h"

int main(int argc, char **argv) {
    NOB_GO_REBUILD_URSELF(argc, argv);
    Nob_Cmd cmd = {0};

    nob_cmd_append(&cmd, "clang++");
    nob_cc_flags(&cmd);
    nob_cc_output(&cmd, "mondex.exe");

    nob_cmd_append(&cmd, "main.cpp");
    nob_cmd_append(&cmd, "-lraylib");

    nob_cmd_append(&cmd, "-O2", "-Wno-unused-const-variable");

    if (!nob_cmd_run_sync(cmd)) return 1;
    return 0;
}
