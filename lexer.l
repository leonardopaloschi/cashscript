%{
#include "parser.tab.h"
#include <stdlib.h>
#include <string.h>

%}

%%

"RANGE"         { return RANGE; }
"to"            { return TO; }

"GOAL"          { return GOAL; }
"INCOME"        { return INCOME; }
"EXPENSE"       { return EXPENSE; }
"SAVE"          { return SAVE; }
"LOAN"          { return LOAN; }
"INVEST"        { return INVEST; }

"IF"            { return IF; }
"TAG"           { return TAG; }

"month"         { return MONTH_TGT; }

"monthly"       { return MONTHLY; }
"daily"         { return DAILY; }
"bimestral"     { return BIMESTRAL; }
"trimestral"    { return TRIMESTRAL; }
"semestral"     { return SEMESTRAL; }
"anual"         { return ANUAL; }

"in"            { return IN; }
"at"            { return AT; }

"("             { return LPAREN; }
")"             { return RPAREN; }
"{"             { return LBRACE; }
"}"             { return RBRACE; }
","             { return COMMA; }
"%"             { return PERCENT; }
"$"             { return DOLLAR; }

"January"       { return JANUARY; }
"February"      { return FEBRUARY; }
"March"         { return MARCH; }
"April"         { return APRIL; }
"May"           { return MAY; }
"June"          { return JUNE; }
"July"          { return JULY; }
"August"        { return AUGUST; }
"September"     { return SEPTEMBER; }
"October"       { return OCTOBER; }
"November"      { return NOVEMBER; }
"December"      { return DECEMBER; }

[0-9]+          { yylval.num = atoi(yytext); return NUMBER; }
[a-zA-Z_][a-zA-Z0-9_]* { yylval.id = strdup(yytext); return IDENTIFIER; }

\n              { yylineno++; }
[ \t\r]+        ;
.               { printf("Caractere inválido na linha %d: %s\n", yylineno, yytext); exit(1); }

%%