%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

extern int yylineno;
extern char *yytext;

int yyparse(void);
int yylex(void);
void yyerror(const char *s);
%}

%union {
    int num;
    char* id;
}

%token <num> NUMBER
%token <id> IDENTIFIER

%token RANGE TO
%token GOAL INCOME EXPENSE SAVE LOAN INVEST
%token IF TAG

%token MONTH_TGT
%token MONTHLY DAILY BIMESTRAL TRIMESTRAL SEMESTRAL ANUAL
%token AT IN

%token LPAREN RPAREN LBRACE RBRACE COMMA PERCENT DOLLAR

%token JANUARY FEBRUARY MARCH APRIL MAY JUNE
%token JULY AUGUST SEPTEMBER OCTOBER NOVEMBER DECEMBER

%%

program:
    range statements
;

range:
    RANGE month year TO month year
;

month:
      JANUARY | FEBRUARY | MARCH | APRIL | MAY | JUNE
    | JULY | AUGUST | SEPTEMBER | OCTOBER | NOVEMBER | DECEMBER
;

year:
    NUMBER
;

statements:
    /* vazio */
    | statements statement
;

statement:
      goal
    | income
    | expense
    | save
    | loan
    | invest
    | if_statement
;

goal:
    GOAL DOLLAR NUMBER
;

income:
    INCOME IDENTIFIER DOLLAR NUMBER repeat_or_target opt_tag
;

expense:
    EXPENSE IDENTIFIER DOLLAR NUMBER repeat_or_target opt_tag
;

save:
    SAVE IDENTIFIER DOLLAR NUMBER repeat_or_target opt_tag
;

loan:
    LOAN IDENTIFIER DOLLAR NUMBER AT DOLLAR NUMBER repeat_or_target opt_tag
;

invest:
    INVEST IDENTIFIER DOLLAR NUMBER COMMA NUMBER PERCENT repeat_or_target opt_tag
;

opt_tag:
    /* vazio */
    | TAG IDENTIFIER
;

if_statement:
    IF condition LBRACE statements RBRACE
;

condition:
    MONTH_TGT IN LPAREN interval RPAREN
;

repeat_or_target:
      repeat
    | month_target
;

repeat:
      MONTHLY LPAREN interval RPAREN
    | DAILY LPAREN NUMBER COMMA MONTHLY LPAREN interval RPAREN RPAREN
    | BIMESTRAL LPAREN interval RPAREN
    | TRIMESTRAL LPAREN interval RPAREN
    | SEMESTRAL LPAREN interval RPAREN
    | ANUAL LPAREN interval RPAREN
;

month_target:
    MONTH_TGT LPAREN NUMBER RPAREN
;

interval:
    NUMBER TO NUMBER
;

%%


