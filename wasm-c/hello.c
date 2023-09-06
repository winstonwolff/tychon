#include <stdio.h>
#include "lib/hamt/hamt.h"

int main() {
    printf("Hello San Fred\n");
    int i;

    struct hamt_t *hamt = create_hamt();

    hamt = hamt_set(hamt, "hello", "world");
    hamt = hamt_set(hamt, "hey", "over there");
    hamt = hamt_set(hamt, "hey2", "over there again");
    char *value1 = (char *)hamt_get(hamt, "hello");
    char *value2 = (char *)hamt_get(hamt, "hey");
    char *value3 = (char *)hamt_get(hamt, "hey2");
    printf("value1: %s\n", value1);
    printf("value2: %s\n", value2);
    printf("value3: %s\n", value3);
}
