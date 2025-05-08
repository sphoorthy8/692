// add.c
#include <stdio.h>
#include <stdlib.h>

#define DEFAULT_N 10000000

int main(int argc, char *argv[]) {
    size_t n = DEFAULT_N;
    if (argc > 1) {
        n = strtoull(argv[1], NULL, 10);
        if (n == 0) n = DEFAULT_N;
    }

    double *a = malloc(n * sizeof(double));
    double *b = malloc(n * sizeof(double));
    double *c = malloc(n * sizeof(double));
    if (!a || !b || !c) {
        perror("malloc");
        return 1;
    }

    // Initialize
    for (size_t i = 0; i < n; i++) {
        a[i] = (double)i;
        b[i] = (double)(2 * i);
    }

    // Compute c = a + b
    for (size_t i = 0; i < n; i++) {
        c[i] = a[i] + b[i];
    }

    // Prevent compiler optimizing away the loop
    printf("c[%zu] = %f\n", n/2, c[n/2]);

    free(a);
    free(b);
    free(c);
    return 0;
}
