#include <stdio.h>
#include <stdlib.h>

int yyparse(void); 
extern FILE *yyin; 
extern int yylineno; 

void yyerror(const char *s) {
    fprintf(stderr, "Erro de sintaxe na linha %d: %s\n", yylineno, s);
}

int main() {
    char filename[256];
    
    printf("Digite o nome do arquivo a ser analisado: ");
    scanf("%s", filename);
    
    yyin = fopen(filename, "r");
    if (!yyin) {
        perror("Erro ao abrir o arquivo");
        return 1;
    }

    if (yyparse() == 0) {
        printf("Programa válido!\n");
    } else {
        printf("Erro na análise, programa não é válido.\n");
    }

    fclose(yyin);
    return 0;
}
