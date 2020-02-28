#include <stdio.h>

void base_call(const int level){
    printf(" Finally called base, with %d levels above it.\n", level);
    return;
}
