#include <stdio.h>
#include <math.h>
#include <complex.h>

#define N 1024  // FFT size

void fft(complex double *x, int n) {
    if (n <= 1) return;

    complex double even[n/2], odd[n/2];
    for (int i = 0; i < n/2; i++) {
        even[i] = x[2*i];
        odd[i] = x[2*i + 1];
    }

    fft(even, n/2);
    fft(odd, n/2);

    for (int k = 0; k < n/2; k++) {
        complex double t = cexp(-2 * I * M_PI * k / n) * odd[k];
        x[k] = even[k] + t;
        x[k + n/2] = even[k] - t;
    }
}

int main() {
    complex double x[N];
    for (int i = 0; i < N; i++)
        x[i] = (double)i/N;

    fft(x, N);
    return 0;
}
