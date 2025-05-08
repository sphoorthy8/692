// matmul.c
#include <stdio.h>
#include <stdlib.h>

#define DEFAULT_N 512

int main(int argc, char *argv[]) {
    int n = DEFAULT_N;
    if (argc > 1) {
        n = atoi(argv[1]);
        if (n <= 0) n = DEFAULT_N;
    }

    double *A = malloc(n*n * sizeof(double));
    double *B = malloc(n*n * sizeof(double));
    double *C = calloc(n*n, sizeof(double));
    if (!A || !B || !C) {
        perror("malloc");
        return 1;
    }

    // Initialize A and B
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            A[i*n + j] = (double)((i + j) % 100) * 0.01;
            B[i*n + j] = (double)((i * j + 3) % 100) * 0.02;
        }
    }

    // C = A × B
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            double sum = 0.0;
            for (int k = 0; k < n; k++) {
                sum += A[i*n + k] * B[k*n + j];
            }
            C[i*n + j] = sum;
        }
    }

    // Print one element to verify
    printf("C[%d][%d] = %f\n", n/2, n/2, C[(n/2)*n + (n/2)]);

    free(A);
    free(B);
    free(C);
    return 0;
}
