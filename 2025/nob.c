#define NOB_IMPLEMENTATION
#define NOB_STRIP_PREFIX
#include "nob.h"

int main(int argc, char **argv) {
    NOB_GO_REBUILD_URSELF(argc, argv);
    Cmd cmd = {0};

    cmd_append(&cmd, "clang++");
    nob_cc_flags(&cmd);
    nob_cc_output(&cmd, "mondex.exe");

    cmd_append(&cmd, "main.cpp");
    cmd_append(&cmd, "-lraylib");

    cmd_append(&cmd, "-O2", "-Wno-unused-const-variable");

    if (!cmd_run_sync(cmd)) return 1;
    return 0;
}
