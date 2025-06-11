# CashScript

## 💡 O que é?

CashScript é uma linguagem de domínio específico criada para te ajudar a organizar sua vida financeira de forma clara, prática e automatizada. Com ela, você descreve receitas, despesas, economias, empréstimos e investimentos usando comandos intuitivos. A saída é um relatório em `report.txt` com um resumo mensal e total da sua situação financeira — pronto para leitura, sem precisar abrir Excel ou planilhas.

---

## ✨ Motivação

A ideia nasceu da frustração com planilhas desorganizadas e sistemas complicados de controle financeiro. Com CashScript, você escreve um pequeno script e recebe uma análise financeira completa, com:

- Renda mensal e extra
- Gastos fixos e variáveis com TAGs categorizadas
- Poupança e metas
- Financiamentos e pagamentos de empréstimos
- Investimentos com juros compostos
- Condicionais por mês (ex: só investir no fim do ano)

---

## 🔧 Características

- Sintaxe simples, inspirada em pseudo-código.
- Sistema de repetição (mensal, bimestral, trimestral, etc).
- Controle de fluxo com `IF` baseado em intervalo de meses.
- Suporte a juros compostos nos investimentos.
- Tags para categorização e rastreabilidade.
- Geração de relatório detalhado mês a mês e total (`report.txt`).

---

## 🔍 Curiosidades

- O sistema foi inicialmente feito com Flex e Bison, mas depois foi reescrito inteiramente em Python (`main.py`) por questões de portabilidade, manutenção e clareza.
- A linguagem não requer datas exatas: basta usar nomes de January a February para representar os meses no ano atual do `RANGE`.

---

## 📦 Estrutura do Projeto
Dentro da pasta entregaFinalCompilador, é possível encontrar a seguinte estrutura:
- `main.py` → Interpretador principal da linguagem
- `entrada_completa.txt` → Exemplo de entrada com todos os recursos da linguagem
- `report.txt` → Saída gerada após execução do interpretador com o exemplo presente no repositório.

---

## ▶️ Como rodar

1. Tenha o Python 3 instalado.
2. No terminal, vá até a pasta entregaFinalCompilador.
3. Rode:

```bash
python3 main.py entrada_completa.txt
```

4. O relatório será gerado como `report.txt` na mesma pasta.

---

## 🧠 Exemplo de sintaxe

```plaintext
RANGE January 2025 to December 2025
GOAL $10000

INCOME Salario $3000 monthly (1 to 12) TAG Trabalho
EXPENSE Aluguel $1500 monthly (1 to 12)
SAVE Emergencia $200 monthly (1 to 6)
LOAN Casa $150000 at $800 monthly (1 to 120)
INVEST Fundos $500, 2% month (9) TAG cdi

IF month in (12 to 2) {
    INVEST Natal $200, 1% month (12) TAG Natalino
}
```

---

## 🧬 Gramática EBNF

```ebnf
program         = range, { statement } ;
range           = "RANGE", month_literal, year, "to", month_literal, year ;

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

repeat_or_target = repeat | month_target ;
repeat          = "monthly", "(", interval ")" 
                | "daily", "(", number, ",", "monthly", "(", interval ")" ")" 
                | "bimestral", "(", interval ")" 
                | "trimestral", "(", interval ")" 
                | "semestral", "(", interval ")" 
                | "anual", "(", interval ")" ;

month_target    = "month", "(", number ")" ;
interval        = number, "to", number ;
month_literal  = "January" | "February" | "March" | "April" | "May" | "June" | "July" | "August" | "September" | "October" | "November" | "December" ;

tag             = "TAG", identifier ;
identifier      = letter, { letter | digit } ;
year            = digit, digit, digit, digit ;
number          = digit, { digit } ;
letter          = "A".."Z" | "a".."z" ;
digit           = "0".."9" ;
```