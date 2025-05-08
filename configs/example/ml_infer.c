// ml_infer.c
#include <stdio.h>
#include <stdlib.h>

#define IN   256
#define H    128
#define OUT  10

int main(int argc, char *argv[]) {
    // Static arrays so they go in BSS/data, not stack
    static float x[IN];
    static float W1[IN][H], b1[H], h[H];
    static float W2[H][OUT], b2[OUT], y[OUT];

    // Initialize input vector
    for (int i = 0; i < IN; i++) {
        x[i] = i * 0.01f;
    }

    // Initialize weights and biases
    for (int i = 0; i < IN; i++)
        for (int j = 0; j < H; j++)
            W1[i][j] = ((i + j) % 100) * 0.001f;
    for (int j = 0; j < H; j++)
        b1[j] = 0.1f;

    for (int i = 0; i < H; i++)
        for (int j = 0; j < OUT; j++)
            W2[i][j] = ((i * j + 3) % 100) * 0.002f;
    for (int k = 0; k < OUT; k++)
        b2[k] = 0.2f;

    // Layer 1: fully-connected + ReLU
    for (int j = 0; j < H; j++) {
        float sum = b1[j];
        for (int i = 0; i < IN; i++) {
            sum += W1[i][j] * x[i];
        }
        h[j] = (sum > 0.0f) ? sum : 0.0f;
    }

    // Layer 2: fully-connected
    for (int k = 0; k < OUT; k++) {
        float sum = b2[k];
        for (int j = 0; j < H; j++) {
            sum += W2[j][k] * h[j];
        }
        y[k] = sum;
    }

    // Print first and last output to verify
    printf("y[0] = %f, y[%d] = %f\n", y[0], OUT-1, y[OUT-1]);
    return 0;
}
