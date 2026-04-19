#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main() {
    int mystere, guess, essais = 0;

    // Initialisation du générateur de nombres aléatoires
    srand(time(NULL));
    mystere = rand() % 101; // nombre entre 0 et 100

    printf("Devine le nombre entre 0 et 100 !\n");

    do {
        printf("Ton essai : ");
        scanf("%d", &guess);
        essais++;

        if (guess < mystere) {
            printf("C'est plus grand !\n");
        } else if (guess > mystere) {
            printf("C'est plus petit !\n");
        } else {
            printf("Bravo ! Tu as trouvé en %d essais.\n", essais);
        }

    } while (guess != mystere);

    return 0;
}