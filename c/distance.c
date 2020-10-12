#include <math.h>
#include <stdio.h>

const double k = 1.3806488;
const double Na = 6.02214129;
const double g = 1.40;
const double M = 29.98E-3;

double calc_speed(double T) { return sqrt(g * k * Na * T / M); }

int main(void) {
    double T, v, d;
    unsigned int t;

    printf("Введите температуру (градусы цельсия): ");
    scanf("%lf", &T);
    printf("Введите время (сек): ");
    scanf("%u", &t);
    T += 273.15;
    v = calc_speed(T);
    d = v * t;
    printf("Скорость звука в воздухе ~ %lf м/с\n", v);
    printf("Расстояние до точки попадания молнии ~ %lf м\n", d);
    return 0;
}