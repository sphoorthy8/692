#include <stdio.h>
#include <stdlib.h>
#define SIZE 10000  // Matrix size
#define NNZ 100000  // Non-zero elements

typedef struct {
    int row, col;
    double val;
} Triplet;

int main() {
    Triplet mat[NNZ];
    double vec[SIZE], result[SIZE] = {0};

    // Initialize sparse matrix and vector
    for (int i = 0; i < NNZ; i++) {
        mat[i].row = rand() % SIZE;
        mat[i].col = rand() % SIZE;
        mat[i].val = (double)rand()/RAND_MAX;
    }
    for (int i = 0; i < SIZE; i++)
        vec[i] = (double)rand()/RAND_MAX;

    // Sparse matrix-vector multiply
    for (int i = 0; i < NNZ; i++)
        result[mat[i].row] += mat[i].val * vec[mat[i].col];

    return 0;
}
