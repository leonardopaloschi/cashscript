# CashScript

#### CashScript se trata de uma solução para a organização do seu dinheiro. A ideia principal por trás dessa linguagem de programação é tornar fácil a catalogação de gastos e ganhos para poder se organizar financeiramente. Por meio de scripts fáceis, é possível montar planilhas organizadas e receber um resumo geral de toda a situação financeira dentro do escopo delimitado.

Para executar o programa, apenas rode ./cashscript e depois digite o nome do arquivo de entrada quando for solicitado.
---
Alguns exemplos dos comandos implementados são:

- RANGE, para declarar o escopo a ser utilizado (RANGE January 2025 to June 2025);
- GOAL, para estabelecer uma meta a ser cumprida (GOAL $10000);
- INCOME, para marcar fontes de renda (INCOME Salary $3000 monthly(0 to 5));
- EXPENSE, para marcar fontes de gasto (EXPENSE Rent $1200 monthly(0 to 5));
- TAG, para categorizar seus gastos (EXPENSE Vacation $2000 month(5) TAG Leisure);
- SAVE, para colocar valores que foram guardados(SAVE Retirement $500 monthly(0 
to 5));
- LOAN, para demonstrar parcelas de empréstimo(LOAN CarLoan $15000 at $500 monthly(0 to 5));
- INVEST, para calcular o rendimento de investimentos(INVEST Stocks $200 , 5% monthly(0 to 5));

---
### Para isso, tem-se o diagrama EBNF definido abaixo:
program         = range, { statement } ;

range           = "RANGE", month, year, "to", month, year ;

statement       = goal
                | income
                | expense
                | save
                | loan
                | invest
                | if_statement ;

goal            = "GOAL", "$", number ;

income          = "INCOME", identifier, "$", number, repeat_or_target, [ tag ] ;

expense         = "EXPENSE", identifier, "$", number, repeat_or_target, [ tag ] ;

save            = "SAVE", identifier, "$", number, repeat_or_target, [ tag ] ;

loan            = "LOAN", identifier, "$", number, "at", "$", number, repeat_or_target , [ tag ] ;

invest          = "INVEST", identifier, "$", number, ",", number "%", repeat_or_target, [ tag ] ;

if_statement    = "IF", condition, "{", { statement }, "}" ;

condition       = "month", "in", "(", interval ")" ;

repeat_or_target = repeat
                 | month_target ;

repeat          = "monthly", "(", interval ")" 
                | "daily", "(", number, ",", "monthly", "(", interval ")" ")" 
                | "bimestral", "(", interval ")" 
                | "trimestral", "(", interval ")" 
                | "semestral", "(", interval ")" 
                | "anual", "(", interval ")" ;

month_target    = "month", "(", number ")" ;

interval        = number, "to", number ;

tag             = "TAG", identifier ;

identifier      = letter, { letter | digit } ;

month           = "January" | "February" | "March" | "April" | "May" | "June" 
                | "July" | "August" | "September" | "October" | "November" | "December" ;

year            = digit, digit, digit, digit ;

number          = digit, { digit } ;

letter          = "A".."Z" | "a".."z" ;

digit           = "0".."9" ;
