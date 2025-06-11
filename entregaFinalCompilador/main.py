import sys
import re
import traceback

class SymbolTable:
    def __init__(self):
        self.table = {}
    
    def create(self, key, type):
        if key in self.table:
            raise Exception(f"Erro de execução: variável \'{key}\' já declarada")
        self.table[key] = (type, None)
    
    def getter(self, key):
        return self.table[key]

    def setter(self, key, value):
        if key not in self.table:
            raise Exception(f"Erro de execução: variável \'{key}\' não declarada")
        declared_type, _ = self.table[key]
        value_type, value_val = value
        
        if declared_type == "INT" and value_type != "INT":
            raise Exception(f"Erro de tipo: variável \'{key}\' declarada como INT recebeu {value_type}")
        elif declared_type == "STR" and value_type != "STR":
            raise Exception(f"Erro de tipo: variável \'{key}\' declarada como STR recebeu {value_type}")
        elif declared_type == "BOOL" and value_type != "BOOL":
            raise Exception(f"Erro de tipo: variável \'{key}\' declarada como BOOL recebeu {value_type}")
        
        self.table[key] = (declared_type, value)

class PrePro:
    @staticmethod
    def filter(source):
        # Remove single-line comments starting with //
        return re.sub(r'//.*(?=\n|$)', '', source)

class Node(object):
    id = 0
    
    @staticmethod
    def newId():
        Node.id += 1
        return Node.id
    
    def __init__(self, value):
        self.value = value
        self.children = []
        self.node_id = Node.newId()
    
    def Evaluate(self, st, context):
        pass

    def Generate(self):
        # This method is for assembly generation and will be removed.
        pass

# The Code class and its methods are for assembly generation and will be removed.
# class Code:
#     instructions = []
#     var_offset = {}
#     current_offset = 0

#     @staticmethod
#     def append(code):
#         Code.instructions.append(code)

#     staticmethod
#     def dump(filename):
#         with open(filename, "w") as f:
#             f.write(\'section .data\\n\
# format_out: db "%d", 10, 0\\n\
# format_in: db "%d", 0\\n\
# scan_int: dd 0\\n\\n\
# section .text\\n\
# extern printf\\n\
# extern scanf\\n\
# global _start\\n\\n\
# \\\\\\\\'\\\'_start:\\\\n\
#  push ebp\\n\
#  mov ebp, esp\\n\
#  mov ebp, esp\\n\\n\
# \
#             f.write("\\n".join(Code.instructions))
            
#             f.write(\'\\n\\n mov esp, ebp\\n\
#  pop ebp\\n\
#  mov eax, 1\\n\
#  xor ebx, ebx\\n\
#  int 0x80\\n\
# \
#         f.close()
        
class BinOp(Node):
    def __init__(self, value, left, right):
        super().__init__(value)
        self.children = [left, right]
    
    def Evaluate(self,st, context):
        # This class will likely be removed or heavily modified for CashScript
        # as it doesn\'t seem to have binary operations in its grammar.
        # Keeping it for now to avoid breaking other parts of the code.
        leftType, leftValue = self.children[0].Evaluate(st, context)
        rightType, rightValue = self.children[1].Evaluate(st, context)
        if self.value == '+':
            if leftType == "BOOL":
                leftValue = str(leftValue).lower()
            elif rightType == "BOOL":
                rightValue = str(rightValue).lower()
            if leftType == "INT" and rightType == "INT":
                return ("INT", leftValue + rightValue)
            else:
                return ("STR", str(leftValue) + str(rightValue))

        elif self.value == '-' and leftType == "INT" and rightType == "INT":    
            return ("INT", leftValue - rightValue)
        elif self.value == '*' and leftType == "INT" and rightType == "INT":
            return ("INT", leftValue * rightValue)
        elif self.value == '/' and leftType == "INT" and rightType == "INT":
            return ("INT", leftValue // rightValue)
        elif self.value == '==' and leftType == rightType:
            return ("BOOL", leftValue == rightValue)
        elif self.value == '<' and leftType == rightType:
            return ("BOOL", leftValue < rightValue)
        elif self.value == '>' and leftType == rightType:
            return ("BOOL", leftValue > rightValue)
        elif self.value == '&&' and leftType == rightType:
            return ("BOOL", leftValue and rightValue)
        elif self.value == '||' and leftType == rightType:
            return ("BOOL", leftValue or rightValue)
        

class UnOp(Node):
    def __init__(self, value, child):
        super().__init__(value)
        self.children = [child]
    
    def Evaluate(self, st, context):
        # This class will likely be removed or heavily modified for CashScript
        # as it doesn\'t seem to have unary operations in its grammar.
        child_type, child_val = self.children[0].Evaluate(st, context)
        if self.value == '!':
            if child_type != "BOOL":
                raise Exception("Erro de tipo: operador \'!\' requer BOOL")
            return ("BOOL", not child_val)
        elif self.value in '+-':
            if child_type != "INT":
                raise Exception(f"Erro de tipo: operador \'{self.value}\' requer INT")
            return ("INT", child_val if self.value == '+' else -child_val)


class IntVal(Node):
    def __init__(self, value):
        super().__init__(value)
    
    def Evaluate(self,st, context):
        return ("INT", self.value)


class StrVal(Node):
    def __init__(self, value):
        super().__init__(value)
    
    def Evaluate(self,st, context):
        return ("STR", self.value)
    

class BoolVal(Node):
    def __init__(self, value):
        super().__init__(value)
    
    def Evaluate(self,st, context):
        return ("BOOL", (self.value))
    

class NoOp(Node):
    def __init__(self):
        super().__init__(None) # Explicitly pass None as value
    def Evaluate(self,st, context):
        pass
    

class Ident(Node):
    def __init__(self, value):
        super().__init__(value)
    
    def Evaluate(self,st, context):
        _, value = st.getter(self.value)
        return value


class Print(Node):
    def __init__(self, child):
        super().__init__(None)
        self.children = [child]
    
    def Evaluate(self,st, context):
        # This class will likely be removed or heavily modified for CashScript
        # as it doesn\'t seem to have a direct \'print\' statement.
        type, value = self.children[0].Evaluate(st, context)
        if type == "BOOL":
            value = "true" if value else "false"
        print(value)


class Assign(Node):
    def __init__(self, value, child):
        super().__init__(value)
        self.children = [child]

    def Evaluate(self,st, context):
        # This class will likely be removed or heavily modified for CashScript
        # as it doesn\'t seem to have direct variable assignment.
        evaluated_value = self.children[0].Evaluate(st, context)
        st.setter(self.value, evaluated_value)


class Block(Node):
    def __init__(self):
        super().__init__(None)
    
    def Evaluate(self,st, context):
        block_income = 0
        block_expense = 0
        block_save = 0
        block_loan_payment = 0
        block_invest = 0

        for child in self.children:
            if isinstance(child, IncomeNode):
                block_income += child.Evaluate(st, context)
            elif isinstance(child, ExpenseNode):
                block_expense += child.Evaluate(st, context)
            elif isinstance(child, SaveNode):
                block_save += child.Evaluate(st, context)
            elif isinstance(child, LoanNode):
                block_loan_payment += child.Evaluate(st, context)
            elif isinstance(child, InvestNode):
                invest_result = child.Evaluate(st, context)
                block_invest += invest_result.get('debit', 0)
            elif isinstance(child, IfNode):
                # If an IfNode is inside a block, its evaluation should contribute to the block\'s totals
                if_results = child.Evaluate(st, context)
                block_income += if_results.get('income', 0)
                block_expense += if_results.get('expense', 0)
                block_save += if_results.get('save', 0)
                block_loan_payment += if_results.get('loan_payment', 0)
                block_invest += if_results.get('invest', 0)
            else:
                child.Evaluate(st, context) # Evaluate other nodes that don\'t contribute to financial totals
        
        return {
            'income': block_income,
            'expense': block_expense,
            'save': block_save,
            'loan_payment': block_loan_payment,
            'invest': block_invest
        }



class If(Node):
    def __init__(self, condition, block, elseBlock=None):
        super().__init__(None)
        self.children = [condition, block]
        if elseBlock:
            self.children.append(elseBlock)

    def Evaluate(self, st, context):
        cond_type, cond_val = self.children[0].Evaluate(st, context)
        if cond_type != "BOOL":
            raise Exception("Erro de tipo: condição do 'if' deve ser BOOL")

        selected_block = None
        if cond_val:
            selected_block = self.children[1]
        elif len(self.children) > 2:
            selected_block = self.children[2]

        result = {
            'income': 0,
            'expense': 0,
            'save': 0,
            'loan_payment': 0,
            'invest': 0,
            'investment_return': 0,
            'investment_return_transactions': []
        }

        if selected_block:
            for child in selected_block.children:
                if isinstance(child, IncomeNode):
                    result['income'] += child.Evaluate(st, context)
                elif isinstance(child, ExpenseNode):
                    result['expense'] += child.Evaluate(st, context)
                elif isinstance(child, SaveNode):
                    result['save'] += child.Evaluate(st, context)
                elif isinstance(child, LoanNode):
                    result['loan_payment'] += child.Evaluate(st, context)
                elif isinstance(child, InvestNode):
                    invest_result = child.Evaluate(st, context)
                    result['invest'] += invest_result.get('debit', 0)
                    result['investment_return'] += invest_result.get('return', 0)
                    result['investment_return_transactions'].append({
                        'amount': invest_result.get('return', 0),
                        'tag': invest_result.get('tag')
                    })

        return result

class While(Node):
    def __init__(self, condition, block):
        super().__init__(None)
        self.children = [condition, block]
    
    def Evaluate(self, st, context):
        # This class will likely be removed or heavily modified for CashScript
        # as it doesn\'t seem to have a \'while\' loop.
        while True:
            cond_type, cond_val = self.children[0].Evaluate(st, context)
            if cond_type != "BOOL":
                raise Exception("Erro de tipo: condição do \'while\' deve ser BOOL")
            if not cond_val:
                break
            self.children[1].Evaluate(st, context)
    

class Read(Node):
    def __init__(self, value):
        super().__init__(value)
    
    def Evaluate(self, st, context):
        # This class will likely be removed or heavily modified for CashScript
        # as it doesn\'t seem to have a direct \'read\' statement.
        value = int(input())
        return ("INT", value)


class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

class VarDec(Node):
    def __init__(self, value, type, child=None):
        super().__init__(value)
        self.type = type
        if child:
            self.children.append(child)

    def Evaluate(self, st, context):
        # This class will likely be removed or heavily modified for CashScript
        # as it doesn\'t seem to have explicit variable declarations.
        st.create(self.value, self.type)
        if self.children:
            value = self.children[0].Evaluate(st, context)
            st.setter(self.value, value)


class Tokenizer:
    def __init__(self, source):
        self.source = source
        self.position = 0
        self.next = None
        self.selectNext()

    def selectNext(self):
        # Skip whitespace including newlines
        while self.position < len(self.source) and self.source[self.position].isspace():
            self.position += 1

        if self.position >= len(self.source):
            self.next = Token("EOF", None)
            return

        # Check for numbers
        if self.source[self.position].isdigit():
            num_str = ""
            while self.position < len(self.source) and self.source[self.position].isdigit():
                num_str += self.source[self.position]
                self.position += 1
            self.next = Token("NUMBER", int(num_str))
            return

        # Check for identifiers and keywords
        if self.source[self.position].isalpha():
            ident_str = ""
            while self.position < len(self.source) and (self.source[self.position].isalnum() or self.source[self.position] == '_'):
                ident_str += self.source[self.position]
                self.position += 1
            
            keywords = {
                "RANGE": "RANGE", "to": "TO",
                "GOAL": "GOAL", "INCOME": "INCOME", "EXPENSE": "EXPENSE", "SAVE": "SAVE", "LOAN": "LOAN", "INVEST": "INVEST",
                "IF": "IF", "TAG": "TAG",
                "month": "MONTH_TGT",
                "monthly": "MONTHLY", "daily": "DAILY", "bimestral": "BIMESTRAL", "trimestral": "TRIMESTRAL", "semestral": "SEMESTRAL", "anual": "ANUAL",
                "in": "IN", "at": "AT",
                "January": "JANUARY", "February": "FEBRUARY", "March": "MARCH", "April": "APRIL", "May": "MAY", "June": "JUNE",
                "July": "JULY", "August": "AUGUST", "September": "SEPTEMBER", "October": "OCTOBER", "November": "NOVEMBER", "December": "DECEMBER"
            }
            if ident_str in keywords:
                self.next = Token(keywords[ident_str], ident_str)
            else:
                self.next = Token("IDENTIFIER", ident_str)
            return

        # Check for single character tokens
        char = self.source[self.position]
        if char == '(': self.next = Token("LPAREN", char)
        elif char == ')': self.next = Token("RPAREN", char)
        elif char == '{': self.next = Token("LBRACE", char)
        elif char == '}': self.next = Token("RBRACE", char)
        elif char == ',': self.next = Token("COMMA", char)
        elif char == '%': self.next = Token("PERCENT", char)
        elif char == '$': self.next = Token("DOLLAR", char)
        else:
            raise Exception(f"Caractere inesperado: {char}")
        
        self.position += 1

class Parser:
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer
    
    def parseFactor(self):
        if self.tokenizer.next.type == "NUMBER":
            node = IntVal(self.tokenizer.next.value)
            self.tokenizer.selectNext()
        elif self.tokenizer.next.type == "IDENTIFIER":
            node = Ident(self.tokenizer.next.value)
            self.tokenizer.selectNext()
        elif self.tokenizer.next.type == "LPAREN":
            self.tokenizer.selectNext()
            # The original parseExpression is for arithmetic, which CashScript doesn\'t have in this context.
            # This needs to be adapted based on CashScript grammar.
            # For now, raising an error as a placeholder.
            raise Exception("Erro de sintaxe: Expressões aritméticas não esperadas aqui.")
        else:
            raise Exception(f"Erro de sintaxe: token inesperado {self.tokenizer.next.type}")
        return node

    def parseTerm(self):
        # This method is for arithmetic operations and will be removed or heavily modified.
        raise Exception("Erro: parseTerm não implementado para CashScript.")

    def parseExpression(self):
        # This method is for arithmetic operations and will be removed or heavily modified.
        raise Exception("Erro: parseExpression não implementado para CashScript.")

    def parseComparison(self):
        # This method is for comparison operations and will be removed or heavily modified.
        raise Exception("Erro: parseComparison não implementado para CashScript.")

    def parseBoolean(self):
        # This method is for boolean operations and will be removed or heavily modified.
        raise Exception("Erro: parseBoolean não implementado para CashScript.")

    def parseUnary(self):
        # This method is for unary operations and will be removed or heavily modified.
        raise Exception("Erro: parseUnary não implementado para CashScript.")

    def parseStatement(self):
        # This part needs to be completely rewritten for CashScript grammar
        # The grammar defines: goal | income | expense | save | loan | invest | if_statement
        if self.tokenizer.next.type == "GOAL":
            return self.parseGoal()
        elif self.tokenizer.next.type == "INCOME":
            return self.parseIncome()
        elif self.tokenizer.next.type == "EXPENSE":
            return self.parseExpense()
        elif self.tokenizer.next.type == "SAVE":
            return self.parseSave()
        elif self.tokenizer.next.type == "LOAN":
            return self.parseLoan()
        elif self.tokenizer.next.type == "INVEST":
            return self.parseInvest()
        elif self.tokenizer.next.type == "IF":
            return self.parseIfStatement()
        else:
            # Consume current token if it\'s not a recognized statement start
            # This is a temporary measure to allow parsing to continue for now
            # Proper error handling will be implemented later.
            # self.tokenizer.selectNext() # Removed as NEWLINE is now skipped by selectNext
            return NoOp()

    def parseBlock(self):
        block = Block()
        while self.tokenizer.next.type != "RBRACE" and self.tokenizer.next.type != "EOF":
            block.children.append(self.parseStatement())
        if self.tokenizer.next.type == "RBRACE":
            self.tokenizer.selectNext()
        return block

    def parseProgram(self):
        # CashScript program starts with 'range' followed by 'statements'
        program_node = Block() # Using Block as a root for now
        
        # Parse RANGE
        if self.tokenizer.next.type == "RANGE":
            program_node.children.append(self.parseRange())
        else:
            raise Exception("Erro de sintaxe: \'RANGE\' esperado no início do programa.")

        # Parse statements
        while self.tokenizer.next.type != "EOF":
            program_node.children.append(self.parseStatement())
        return program_node

    # New parsing methods for CashScript grammar
    def parseRange(self):
        self.tokenizer.selectNext() # Consume RANGE
        month1 = self.tokenizer.next.value
        self.tokenizer.selectNext() # Consume month1
        year1 = self.tokenizer.next.value
        self.tokenizer.selectNext() # Consume year1
        if self.tokenizer.next.type != "TO":
            raise Exception("Erro de sintaxe: \'to\' esperado em RANGE.")
        self.tokenizer.selectNext() # Consume TO
        month2 = self.tokenizer.next.value
        self.tokenizer.selectNext() # Consume month2
        year2 = self.tokenizer.next.value
        self.tokenizer.selectNext() # Consume year2
        return RangeNode(month1, year1, month2, year2)

    def parseGoal(self):
        self.tokenizer.selectNext() # Consume GOAL
        if self.tokenizer.next.type != "DOLLAR":
            raise Exception("Erro de sintaxe: \'$\' esperado em GOAL.")
        self.tokenizer.selectNext() # Consume DOLLAR
        number = self.tokenizer.next.value
        self.tokenizer.selectNext() # Consume NUMBER
        return GoalNode(number)

    def parseIncome(self):
        self.tokenizer.selectNext() # Consume INCOME
        identifier = self.tokenizer.next.value
        self.tokenizer.selectNext() # Consume IDENTIFIER
        if self.tokenizer.next.type != "DOLLAR":
            raise Exception("Erro de sintaxe: \'$\' esperado em INCOME.")
        self.tokenizer.selectNext() # Consume DOLLAR
        number = self.tokenizer.next.value
        self.tokenizer.selectNext() # Consume NUMBER
        repeat_or_target = self.parseRepeatOrTarget()
        opt_tag = self.parseOptTag()
        return IncomeNode(identifier, number, repeat_or_target, opt_tag)

    def parseExpense(self):
        self.tokenizer.selectNext() # Consume EXPENSE
        identifier = self.tokenizer.next.value
        self.tokenizer.selectNext() # Consume IDENTIFIER
        if self.tokenizer.next.type != "DOLLAR":
            raise Exception("Erro de sintaxe: \'$\' esperado em EXPENSE.")
        self.tokenizer.selectNext() # Consume DOLLAR
        number = self.tokenizer.next.value
        self.tokenizer.selectNext() # Consume NUMBER
        repeat_or_target = self.parseRepeatOrTarget()
        opt_tag = self.parseOptTag()
        return ExpenseNode(identifier, number, repeat_or_target, opt_tag)

    def parseSave(self):
        self.tokenizer.selectNext() # Consume SAVE
        identifier = self.tokenizer.next.value
        self.tokenizer.selectNext() # Consume IDENTIFIER
        if self.tokenizer.next.type != "DOLLAR":
            raise Exception("Erro de sintaxe: \'$\' esperado em SAVE.")
        self.tokenizer.selectNext() # Consume DOLLAR
        number = self.tokenizer.next.value
        self.tokenizer.selectNext() # Consume NUMBER
        repeat_or_target = self.parseRepeatOrTarget()
        opt_tag = self.parseOptTag()
        return SaveNode(identifier, number, repeat_or_target, opt_tag)

    def parseLoan(self):
        self.tokenizer.selectNext() # Consume LOAN
        identifier = self.tokenizer.next.value
        self.tokenizer.selectNext() # Consume IDENTIFIER
        if self.tokenizer.next.type != "DOLLAR":
            raise Exception("Erro de sintaxe: \'$\' esperado em LOAN.")
        self.tokenizer.selectNext() # Consume DOLLAR
        number1 = self.tokenizer.next.value
        self.tokenizer.selectNext() # Consume NUMBER
        if self.tokenizer.next.type != "AT":
            raise Exception("Erro de sintaxe: \'at\' esperado em LOAN.")
        self.tokenizer.selectNext() # Consume AT
        if self.tokenizer.next.type != "DOLLAR":
            raise Exception("Erro de sintaxe: \'$\' esperado em LOAN.")
        self.tokenizer.selectNext() # Consume DOLLAR
        number2 = self.tokenizer.next.value
        self.tokenizer.selectNext() # Consume NUMBER
        repeat_or_target = self.parseRepeatOrTarget()
        opt_tag = self.parseOptTag()
        return LoanNode(identifier, number1, number2, repeat_or_target, opt_tag)

    def parseInvest(self):
        self.tokenizer.selectNext() # Consume INVEST
        identifier = self.tokenizer.next.value
        self.tokenizer.selectNext() # Consume IDENTIFIER
        if self.tokenizer.next.type != "DOLLAR":
            raise Exception("Erro de sintaxe: \'$\' esperado em INVEST.")
        self.tokenizer.selectNext() # Consume DOLLAR
        amount = self.tokenizer.next.value
        self.tokenizer.selectNext() # Consume NUMBER (amount)
        if self.tokenizer.next.type != "COMMA":
            raise Exception("Erro de sintaxe: \',\' esperado em INVEST.")
        self.tokenizer.selectNext() # Consume COMMA
        percentage = self.tokenizer.next.value
        self.tokenizer.selectNext() # Consume NUMBER (percentage)
        if self.tokenizer.next.type != "PERCENT":
            raise Exception("Erro de sintaxe: \'%\' esperado em INVEST.")
        self.tokenizer.selectNext() # Consume PERCENT
        # Expecting 'monthly' keyword followed by an interval
        if self.tokenizer.next.type != "MONTH_TGT":
            print(self.tokenizer.next.type)
            raise Exception("Erro de sintaxe: \'month\' esperado em INVEST.")
        self.tokenizer.selectNext() # Consume MONTH_TGT
        if self.tokenizer.next.type != "LPAREN":
            raise Exception("Erro de sintaxe: \'(\' esperado após monthly em INVEST.")
        self.tokenizer.selectNext() # Consume LPAREN
        interval = self.parseInterval() # This will give us the month of investment
        if self.tokenizer.next.type != "RPAREN":
            raise Exception("Erro de sintaxe: \')\' esperado após intervalo em INVEST.")
        self.tokenizer.selectNext() # Consume RPAREN
        opt_tag = self.parseOptTag()
        return InvestNode(identifier, amount, percentage, interval, opt_tag)

    def parseOptTag(self):
        if self.tokenizer.next.type == "TAG":
            self.tokenizer.selectNext() # Consume TAG
            identifier = self.tokenizer.next.value
            self.tokenizer.selectNext() # Consume IDENTIFIER
            return TagNode(identifier)
        return NoOp() # No tag

    def parseIfStatement(self):
        self.tokenizer.selectNext() # Consume IF
        condition = self.parseCondition()
        if self.tokenizer.next.type != "LBRACE":
            raise Exception("Erro de sintaxe: \'{\' esperado após condição do if.")
        self.tokenizer.selectNext() # Consume LBRACE
        statements = Block() # Create a new block for statements inside IF
        while self.tokenizer.next.type != "RBRACE" and self.tokenizer.next.type != "EOF":
            statements.children.append(self.parseStatement())
        if self.tokenizer.next.type != "RBRACE":
            raise Exception("Erro de sintaxe: \'}\' esperado para fechar o bloco do if.")
        self.tokenizer.selectNext() # Consume RBRACE
        return IfNode(condition, statements)

    def parseCondition(self):
        if self.tokenizer.next.type != "MONTH_TGT":
            raise Exception("Erro de sintaxe: \'month\' esperado na condição.")
        self.tokenizer.selectNext() # Consume MONTH_TGT
        if self.tokenizer.next.type != "IN":
            raise Exception("Erro de sintaxe: \'in\' esperado na condição.")
        self.tokenizer.selectNext() # Consume IN
        if self.tokenizer.next.type != "LPAREN":
            raise Exception("Erro de sintaxe: \'(\' esperado na condição.")
        self.tokenizer.selectNext() # Consume LPAREN
        interval = self.parseInterval()
        if self.tokenizer.next.type != "RPAREN":
            raise Exception("Erro de sintaxe: \')\' esperado na condição.")
        self.tokenizer.selectNext() # Consume RPAREN
        return ConditionNode(interval)

    def parseRepeatOrTarget(self):
        if self.tokenizer.next.type in ["MONTHLY", "DAILY", "BIMESTRAL", "TRIMESTRAL", "SEMESTRAL", "ANUAL"]:
            return self.parseRepeat()
        elif self.tokenizer.next.type == "MONTH_TGT":
            return self.parseMonthTarget()
        else:
            raise Exception("Erro de sintaxe: \'repeat\' ou \'month\' esperado.")

    def parseRepeat(self):
        repeat_type = self.tokenizer.next.type
        self.tokenizer.selectNext() # Consume repeat type
        if repeat_type == "DAILY":
            if self.tokenizer.next.type != "LPAREN":
                raise Exception("Erro de sintaxe: \'(\' esperado em repeat DAILY.")
            self.tokenizer.selectNext() # Consume LPAREN
            daily_num = self.tokenizer.next.value
            self.tokenizer.selectNext() # Consume NUMBER
            if self.tokenizer.next.type != "COMMA":
                raise Exception("Erro de sintaxe: \',\' esperado em repeat DAILY.")
            self.tokenizer.selectNext() # Consume COMMA
            if self.tokenizer.next.type != "MONTHLY":
                raise Exception("Erro de sintaxe: \'monthly\' esperado em repeat DAILY.")
            self.tokenizer.selectNext() # Consume MONTHLY
            if self.tokenizer.next.type != "LPAREN":
                raise Exception("Erro de sintaxe: \'(\' esperado em repeat DAILY monthly.")
            self.tokenizer.selectNext() # Consume LPAREN
            interval = self.parseInterval()
            if self.tokenizer.next.type != "RPAREN":
                raise Exception("Erro de sintaxe: \')\' esperado em repeat DAILY monthly.")
            self.tokenizer.selectNext() # Consume RPAREN
            if self.tokenizer.next.type != "RPAREN":
                raise Exception("Erro de sintaxe: \')\' esperado em repeat DAILY.")
            self.tokenizer.selectNext() # Consume RPAREN
            return RepeatNode(repeat_type, daily_num, interval)
        else:
            if self.tokenizer.next.type != "LPAREN":
                raise Exception("Erro de sintaxe: \'(\' esperado em repeat.")
            self.tokenizer.selectNext() # Consume LPAREN
            interval = self.parseInterval()
            if self.tokenizer.next.type != "RPAREN":
                raise Exception("Erro de sintaxe: \')\' esperado em repeat.")
            self.tokenizer.selectNext() # Consume RPAREN
            return RepeatNode(repeat_type, None, interval)

    def parseMonthTarget(self):
        self.tokenizer.selectNext() # Consume MONTH_TGT
        if self.tokenizer.next.type != "LPAREN":
            raise Exception("Erro de sintaxe: \'(\' esperado em month_target.")
        self.tokenizer.selectNext() # Consume LPAREN
        number = self.tokenizer.next.value
        self.tokenizer.selectNext() # Consume NUMBER
        if self.tokenizer.next.type != "RPAREN":
            raise Exception("Erro de sintaxe: \')\' esperado em month_target.")
        self.tokenizer.selectNext() # Consume RPAREN
        return MonthTargetNode(number)

    def parseInterval(self):
        # Handles both month names and numbers for interval
        val1 = self.tokenizer.next.value
        self.tokenizer.selectNext() # Consume first value
        
        if self.tokenizer.next.type == "TO":
            self.tokenizer.selectNext() # Consume TO
            val2 = self.tokenizer.next.value
            self.tokenizer.selectNext() # Consume second value
            return IntervalNode(val1, val2)
        else:
            # If 'TO' is not present, it's a single value interval
            return IntervalNode(val1, val1)


# Define new Node classes for CashScript grammar
class RangeNode(Node):
    def __init__(self, month1, year1, month2, year2):
        super().__init__("RANGE")
        self.month1 = month1
        self.year1 = year1
        self.month2 = month2
        self.year2 = year2
    
    def Evaluate(self, st, context):
        month_map = {
            "January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6,
            "July": 7, "August": 8, "September": 9, "October": 10, "November": 11, "December": 12
        }
        context["start_month_num"] = month_map[self.month1]
        context["start_year"] = self.year1
        context["end_month_num"] = month_map[self.month2]
        context["end_year"] = self.year2

class GoalNode(Node):
    def __init__(self, amount):
        super().__init__("GOAL")
        self.amount = amount
    
    def Evaluate(self, st, context):
        context["goal"] = self.amount

class IncomeNode(Node):
    def __init__(self, identifier, amount, repeat_or_target, opt_tag):
        super().__init__("INCOME")
        self.identifier = identifier
        self.amount = amount
        self.repeat_or_target = repeat_or_target
        self.opt_tag = opt_tag
    
    def Evaluate(self, st, context):
        tag_info = f" TAG {self.opt_tag.value}" if isinstance(self.opt_tag, TagNode) else ""
        
        monthly_amount = 0
        if isinstance(self.repeat_or_target, RepeatNode):
            repeat_info = self.repeat_or_target.Evaluate(st, context)
            current_month_num = context["current_month_num"]
            
            if repeat_info["type"] == "MONTHLY":
                start_month, end_month = repeat_info["interval"]
                if start_month <= end_month:
                    if start_month <= current_month_num <= end_month:
                        monthly_amount = self.amount
                else: # e.g., Dec to Feb (12 to 2)
                    if current_month_num >= start_month or current_month_num <= end_month:
                        monthly_amount = self.amount
            elif repeat_info["type"] == "DAILY":
                daily_num = repeat_info["daily_num"]
                start_month, end_month = repeat_info["monthly_interval"]
                if start_month <= end_month:
                    if start_month <= current_month_num <= end_month:
                        monthly_amount = self.amount * daily_num
                else: # e.g., Dec to Feb (12 to 2)
                    if current_month_num >= start_month or current_month_num <= end_month:
                        monthly_amount = self.amount * daily_num
            # Add logic for BIMESTRAL, TRIMESTRAL, SEMESTRAL, ANUAL
            # For simplicity, let\'s assume they apply if the current month is the start month of their interval
            elif repeat_info["type"] == "BIMESTRAL":
                start_month, end_month = repeat_info["interval"]
                if current_month_num == start_month:
                    monthly_amount = self.amount
            elif repeat_info["type"] == "TRIMESTRAL":
                start_month, end_month = repeat_info["interval"]
                if current_month_num == start_month:
                    monthly_amount = self.amount
            elif repeat_info["type"] == "SEMESTRAL":
                start_month, end_month = repeat_info["interval"]
                if current_month_num == start_month:
                    monthly_amount = self.amount
            elif repeat_info["type"] == "ANUAL":
                start_month, end_month = repeat_info["interval"]
                if current_month_num == start_month:
                    monthly_amount = self.amount

        elif isinstance(self.repeat_or_target, MonthTargetNode):
            target_month = self.repeat_or_target.Evaluate(st, context)
            if context["current_month_num"] == target_month:
                monthly_amount = self.amount
        
        return monthly_amount

class ExpenseNode(Node):
    def __init__(self, identifier, amount, repeat_or_target, opt_tag):
        super().__init__("EXPENSE")
        self.identifier = identifier
        self.amount = amount
        self.repeat_or_target = repeat_or_target
        self.opt_tag = opt_tag
    
    def Evaluate(self, st, context):
        tag_info = f" TAG {self.opt_tag.value}" if isinstance(self.opt_tag, TagNode) else ""
        
        monthly_amount = 0
        if isinstance(self.repeat_or_target, RepeatNode):
            repeat_info = self.repeat_or_target.Evaluate(st, context)
            current_month_num = context["current_month_num"]
            
            if repeat_info["type"] == "MONTHLY":
                start_month, end_month = repeat_info["interval"]
                if start_month <= end_month:
                    if start_month <= current_month_num <= end_month:
                        monthly_amount = self.amount
                else: # e.g., Dec to Feb (12 to 2)
                    if current_month_num >= start_month or current_month_num <= end_month:
                        monthly_amount = self.amount
            elif repeat_info["type"] == "DAILY":
                daily_num = repeat_info["daily_num"]
                start_month, end_month = repeat_info["monthly_interval"]
                if start_month <= end_month:
                    if start_month <= current_month_num <= end_month:
                        monthly_amount = self.amount * daily_num
                else: # e.g., Dec to Feb (12 to 2)
                    if current_month_num >= start_month or current_month_num <= end_month:
                        monthly_amount = self.amount * daily_num
            elif repeat_info["type"] == "BIMESTRAL":
                start_month, end_month = repeat_info["interval"]
                if current_month_num == start_month:
                    monthly_amount = self.amount
            elif repeat_info["type"] == "TRIMESTRAL":
                start_month, end_month = repeat_info["interval"]
                if current_month_num == start_month:
                    monthly_amount = self.amount
            elif repeat_info["type"] == "SEMESTRAL":
                start_month, end_month = repeat_info["interval"]
                if current_month_num == start_month:
                    monthly_amount = self.amount
            elif repeat_info["type"] == "ANUAL":
                start_month, end_month = repeat_info["interval"]
                if current_month_num == start_month:
                    monthly_amount = self.amount

        elif isinstance(self.repeat_or_target, MonthTargetNode):
            target_month = self.repeat_or_target.Evaluate(st, context)
            if context["current_month_num"] == target_month:
                monthly_amount = self.amount
        
        return monthly_amount

class SaveNode(Node):
    def __init__(self, identifier, amount, repeat_or_target, opt_tag):
        super().__init__("SAVE")
        self.identifier = identifier
        self.amount = amount
        self.repeat_or_target = repeat_or_target
        self.opt_tag = opt_tag
    
    def Evaluate(self, st, context):
        tag_info = f" TAG {self.opt_tag.value}" if isinstance(self.opt_tag, TagNode) else ""
        
        monthly_amount = 0
        if isinstance(self.repeat_or_target, RepeatNode):
            repeat_info = self.repeat_or_target.Evaluate(st, context)
            current_month_num = context["current_month_num"]
            
            if repeat_info["type"] == "MONTHLY":
                start_month, end_month = repeat_info["interval"]
                if start_month <= end_month:
                    if start_month <= current_month_num <= end_month:
                        monthly_amount = self.amount
                else: # e.g., Dec to Feb (12 to 2)
                    if current_month_num >= start_month or current_month_num <= end_month:
                        monthly_amount = self.amount
            elif repeat_info["type"] == "DAILY":
                daily_num = repeat_info["daily_num"]
                start_month, end_month = repeat_info["monthly_interval"]
                if start_month <= end_month:
                    if start_month <= current_month_num <= end_month:
                        monthly_amount = self.amount * daily_num
                else: # e.g., Dec to Feb (12 to 2)
                    if current_month_num >= start_month or current_month_num <= end_month:
                        monthly_amount = self.amount * daily_num
            elif repeat_info["type"] == "BIMESTRAL":
                start_month, end_month = repeat_info["interval"]
                if current_month_num == start_month:
                    monthly_amount = self.amount
            elif repeat_info["type"] == "TRIMESTRAL":
                start_month, end_month = repeat_info["interval"]
                if current_month_num == start_month:
                    monthly_amount = self.amount
            elif repeat_info["type"] == "SEMESTRAL":
                start_month, end_month = repeat_info["interval"]
                if current_month_num == start_month:
                    monthly_amount = self.amount
            elif repeat_info["type"] == "ANUAL":
                start_month, end_month = repeat_info["interval"]
                if current_month_num == start_month:
                    monthly_amount = self.amount

        elif isinstance(self.repeat_or_target, MonthTargetNode):
            target_month = self.repeat_or_target.Evaluate(st, context)
            if context["current_month_num"] == target_month:
                monthly_amount = self.amount
        
        return monthly_amount

class LoanNode(Node):
    def __init__(self, identifier, total_amount, monthly_amount, repeat_or_target, opt_tag):
        super().__init__("LOAN")
        self.identifier = identifier
        self.total_amount = total_amount
        self.monthly_amount = monthly_amount
        self.repeat_or_target = repeat_or_target
        self.opt_tag = opt_tag
    
    def Evaluate(self, st, context):
        tag_info = f" TAG {self.opt_tag.value}" if isinstance(self.opt_tag, TagNode) else ""
        
        loan_payment_this_month = 0
        if isinstance(self.repeat_or_target, RepeatNode):
            repeat_info = self.repeat_or_target.Evaluate(st, context)
            current_month_num = context["current_month_num"]
            
            if repeat_info["type"] == "MONTHLY":
                start_month, end_month = repeat_info["interval"]
                if start_month <= end_month:
                    if start_month <= current_month_num <= end_month:
                        loan_payment_this_month = self.monthly_amount
                else: # e.g., Dec to Feb (12 to 2)
                    if current_month_num >= start_month or current_month_num <= end_month:
                        loan_payment_this_month = self.monthly_amount
            elif repeat_info["type"] == "DAILY":
                daily_num = repeat_info["daily_num"]
                start_month, end_month = repeat_info["monthly_interval"]
                if start_month <= end_month:
                    if start_month <= current_month_num <= end_month:
                        loan_payment_this_month = self.monthly_amount * daily_num
                else: # e.g., Dec to Feb (12 to 2)
                    if current_month_num >= start_month or current_month_num <= end_month:
                        loan_payment_this_month = self.monthly_amount * daily_num
            elif repeat_info["type"] == "BIMESTRAL":
                start_month, end_month = repeat_info["interval"]
                if current_month_num == start_month:
                    loan_payment_this_month = self.monthly_amount
            elif repeat_info["type"] == "TRIMESTRAL":
                start_month, end_month = repeat_info["interval"]
                if current_month_num == start_month:
                    loan_payment_this_month = self.monthly_amount
            elif repeat_info["type"] == "SEMESTRAL":
                start_month, end_month = repeat_info["interval"]
                if current_month_num == start_month:
                    loan_payment_this_month = self.monthly_amount
            elif repeat_info["type"] == "ANUAL":
                start_month, end_month = repeat_info["interval"]
                if current_month_num == start_month:
                    loan_payment_this_month = self.monthly_amount

        elif isinstance(self.repeat_or_target, MonthTargetNode):
            target_month = self.repeat_or_target.Evaluate(st, context)
            if context["current_month_num"] == target_month:
                loan_payment_this_month = self.monthly_amount
        
        return loan_payment_this_month


class InvestNode(Node):
    def __init__(self, identifier, amount, percentage, interval, opt_tag):
        super().__init__("INVEST")
        self.identifier = identifier
        self.amount = amount
        self.percentage = percentage
        self.interval = interval
        self.opt_tag = opt_tag
        # Mover o estado do investimento para o contexto global
        # Isso permite que o estado persista entre chamadas
        self.investment_key = f"investment_{identifier}"
    
    def Evaluate(self, st, context):
        current_month_num = context['current_month_num']
        current_year = context['current_year']
        
        # Inicializa ou recupera o estado do investimento do contexto
        if self.investment_key not in context:
            context[self.investment_key] = {
                'start_month': None,
                'start_year': None,
                'balance': 0,
                'initial_investment_processed': False
            }
        
        investment_state = context[self.investment_key]
        
        start_month, end_month = self.interval.Evaluate(st, context)
        
        monthly_invest_debit = 0
        monthly_investment_return = 0
        effective_total_value = 0

        if current_month_num == start_month and not investment_state['initial_investment_processed']:
            monthly_invest_debit = self.amount
            investment_state['balance'] += self.amount
            investment_state['start_month'] = current_month_num
            investment_state['start_year'] = current_year
            investment_state['initial_investment_processed'] = True
        
        elif investment_state['initial_investment_processed'] and (
            (current_year > investment_state['start_year']) or
            (current_year == investment_state['start_year'] and current_month_num > investment_state['start_month'])
        ):
            monthly_investment_return = investment_state['balance'] * (self.percentage / 100)
            investment_state['balance'] += monthly_investment_return
            effective_total_value = investment_state['balance']

        return {
            'debit': monthly_invest_debit,
            'return': effective_total_value,
            'tag': self.opt_tag.value if isinstance(self.opt_tag, TagNode) else None
        }

class TagNode(Node):
    def __init__(self, value):
        super().__init__(value)
    
    def Evaluate(self, st, context):
        return self.value

class ConditionNode(Node):
    def __init__(self, interval):
        super().__init__("CONDITION")
        self.interval = interval
    
    def Evaluate(self, st, context):
        current_month_num = context.get("current_month_num", 1) # Default to January (1)
        
        start_val, end_val = self.interval.Evaluate(st, context) # IntervalNode now returns numbers

        is_in_interval = False
        if start_val <= end_val:
            is_in_interval = start_val <= current_month_num <= end_val
        else: # Handles cases like December to February (12 to 2)
            is_in_interval = current_month_num >= start_val or current_month_num <= end_val

        return ("BOOL", is_in_interval)

class RepeatNode(Node):
    def __init__(self, repeat_type, daily_num, interval):
        super().__init__(repeat_type)
        self.daily_num = daily_num
        self.interval = interval
    
    def Evaluate(self, st, context):
        interval_start, interval_end = self.interval.Evaluate(st, context)
        
        if self.daily_num is not None:
            return {
                "type": self.value,
                "daily_num": self.daily_num,
                "monthly_interval": (interval_start, interval_end)
            }
        else:
            return {
                "type": self.value,
                "interval": (interval_start, interval_end)
            }

class MonthTargetNode(Node):
    def __init__(self, number):
        super().__init__("MONTH_TARGET")
        self.number = number
    
    def Evaluate(self, st, context):
        return self.number

class IntervalNode(Node):
    def __init__(self, start_val, end_val):
        super().__init__("INTERVAL")
        self.start_val = start_val
        self.end_val = end_val

    def Evaluate(self, st, context):
        month_map = {
            "January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6,
            "July": 7, "August": 8, "September": 9, "October": 10, "November": 11, "December": 12
        }
        start_num = month_map.get(self.start_val, self.start_val)
        end_num = month_map.get(self.end_val, self.end_val)
        return (start_num, end_num)

class IfNode(Node):
    def __init__(self, condition, statements):
        super().__init__("IF")
        self.children = [condition, statements]

    def Evaluate(self, st, context):
        cond_type, cond_val = self.children[0].Evaluate(st, context)
        if cond_type != "BOOL":
            raise Exception("Erro de tipo: condição do 'if' deve ser BOOL")
        
        if cond_val:
            results = {
                'income': 0,
                'expense': 0,
                'save': 0,
                'loan_payment': 0,
                'invest': 0,
                'return': 0,
                'income_tags': [],
                'expense_tags': [],
                'save_tags': [],
                'invest_tags': []
            }
            
            for child in self.children[1].children:
                if isinstance(child, IncomeNode):
                    amount = child.Evaluate(st, context)
                    results['income'] += amount
                    if isinstance(child.opt_tag, TagNode):
                        results['income_tags'].append({
                            'amount': amount,
                            'tag': child.opt_tag.value
                        })
                elif isinstance(child, ExpenseNode):
                    amount = child.Evaluate(st, context)
                    results['expense'] += amount
                    if isinstance(child.opt_tag, TagNode):
                        results['expense_tags'].append({
                            'amount': amount,
                            'tag': child.opt_tag.value
                        })
                elif isinstance(child, SaveNode):
                    amount = child.Evaluate(st, context)
                    results['save'] += amount
                    if isinstance(child.opt_tag, TagNode):
                        results['save_tags'].append({
                            'amount': amount,
                            'tag': child.opt_tag.value
                        })
                elif isinstance(child, LoanNode):
                    amount = child.Evaluate(st, context)
                    results['loan_payment'] += amount
                elif isinstance(child, InvestNode):
                    invest_result = child.Evaluate(st, context)
                    results['invest'] += invest_result['debit']
                    results['return'] += invest_result['return']
                    if isinstance(child.opt_tag, TagNode):
                        results['invest_tags'].append({
                            'debit': invest_result['debit'],
                            'return': invest_result['return'],
                            'tag': child.opt_tag.value
                        })
            
            return results
        
        return {
            'income': 0,
            'expense': 0,
            'save': 0,
            'loan_payment': 0,
            'invest': 0,
            'return': 0,
            'income_tags': [],
            'expense_tags': [],
            'save_tags': [],
            'invest_tags': []
        }

# Main part of the program
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python main.py <arquivo_de_entrada>")
        sys.exit(1)

    input_filename = sys.argv[1]
    try:
        with open(input_filename, 'r') as file:
            code = file.read()
        
        processed_code = PrePro.filter(code)
        
        tokenizer = Tokenizer(processed_code)
        parser = Parser(tokenizer)
        
        tree = parser.parseProgram()
        
        st = SymbolTable()
        
        # Initialize context for evaluation
        evaluation_context = {
            'current_month_num': 1, # January
            'current_year': 2025,
            'income': [],
            'expense': [],
            'save': [],
            'loan': [],
            'invest': [],
            'goal': None,
            'financial_summary': [], # To store monthly financial summaries
            'investment_balance': 0 # Initialize investment balance
        }

        # Extract range and goal information first
        range_node = None
        goal_node = None
        for child in tree.children:
            if isinstance(child, RangeNode):
                range_node = child
            elif isinstance(child, GoalNode):
                goal_node = child
        
        if range_node:
            range_node.Evaluate(st, evaluation_context)
            start_month_num = evaluation_context['start_month_num']
            start_year = evaluation_context['start_year']
            end_month_num = evaluation_context['end_month_num']
            end_year = evaluation_context['end_year']

        if goal_node:
            goal_node.Evaluate(st, evaluation_context)

        month_map_reverse = {
            1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June",
            7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"
        }

        current_month = start_month_num
        current_year = start_year

        # Initialize total sums
        total_income_all_months = 0
        total_expense_all_months = 0
        total_save_all_months = 0
        total_loan_payment_all_months = 0
        total_invest_all_months = 0 # This will be for initial debits
        total_investment_return_all_months = 0 # This will be for compounded returns
        total_balance_all_months = 0

        while True:
            evaluation_context['current_month_num'] = current_month
            evaluation_context['current_year'] = current_year
            
            monthly_income = 0
            monthly_expense = 0
            monthly_save = 0
            monthly_loan_payment = 0
            monthly_invest_debit = 0 # Initial investment debit for the month
            monthly_investment_return = 0 # Compounded return for the month

            # New lists to store transaction details including tags for the current month
            current_month_income_transactions = []
            current_month_expense_transactions = []
            current_month_save_transactions = []
            current_month_loan_transactions = []
            current_month_invest_transactions = [] # For initial investment debit
            current_month_investment_return_transactions = [] # For investment returns


            for child in tree.children:
                if not isinstance(child, RangeNode) and not isinstance(child, GoalNode):
                    # Evaluate each statement for the current month
                    # This is where the core financial logic will be applied
                    
                    if isinstance(child, IncomeNode):
                        amount = child.Evaluate(st, evaluation_context)
                        if amount > 0: # Only add if there was an actual income for the month
                            monthly_income += amount
                            tag = child.opt_tag.value if isinstance(child.opt_tag, TagNode) else None
                            current_month_income_transactions.append({'amount': amount, 'tag': tag})
                    elif isinstance(child, ExpenseNode):
                        amount = child.Evaluate(st, evaluation_context)
                        if amount > 0:
                            monthly_expense += amount
                            tag = child.opt_tag.value if isinstance(child.opt_tag, TagNode) else None
                            current_month_expense_transactions.append({'amount': amount, 'tag': tag})
                    elif isinstance(child, SaveNode):
                        amount = child.Evaluate(st, evaluation_context)
                        if amount > 0:
                            monthly_save += amount
                            tag = child.opt_tag.value if isinstance(child.opt_tag, TagNode) else None
                            current_month_save_transactions.append({'amount': amount, 'tag': tag})
                    elif isinstance(child, LoanNode):
                        amount = child.Evaluate(st, evaluation_context)
                        if amount > 0:
                            monthly_loan_payment += amount
                            tag = child.opt_tag.value if isinstance(child.opt_tag, TagNode) else None
                            current_month_loan_transactions.append({'amount': amount, 'tag': tag})
                    elif isinstance(child, InvestNode):
                        invest_results = child.Evaluate(st, evaluation_context)
                        if invest_results['debit'] > 0:
                            monthly_invest_debit += invest_results['debit']
                            current_month_invest_transactions.append({'amount': invest_results['debit'], 'tag': invest_results['tag']})
                        if invest_results['return'] > 0:
                            monthly_investment_return += invest_results['return']
                            current_month_investment_return_transactions.append({'amount': invest_results['return'], 'tag': invest_results['tag']})
                    elif isinstance(child, IfNode):
                        if_results = child.Evaluate(st, evaluation_context)
                        monthly_income += if_results.get('income', 0)
                        monthly_expense += if_results.get('expense', 0)
                        monthly_save += if_results.get('save', 0)
                        monthly_loan_payment += if_results.get('loan_payment', 0)
                        monthly_invest_debit += if_results.get('invest', 0)
                        monthly_investment_return += if_results.get('return', 0)
                        
                        # Adiciona as transações com tags
                        for income in if_results.get('income_tags', []):
                            current_month_income_transactions.append({'amount': income['amount'], 'tag': income['tag']})
                        for expense in if_results.get('expense_tags', []):
                            current_month_expense_transactions.append({'amount': expense['amount'], 'tag': expense['tag']})
                        for save in if_results.get('save_tags', []):
                            current_month_save_transactions.append({'amount': save['amount'], 'tag': save['tag']})
                        for invest in if_results.get('invest_tags', []):
                            if invest['debit'] > 0:
                                current_month_invest_transactions.append({'amount': invest['debit'], 'tag': invest['tag']})
                            if invest['return'] > 0:
                                current_month_investment_return_transactions.append({'amount': invest['return'], 'tag': invest['tag']})
                    elif isinstance(child, Block):
                        block_results = child.Evaluate(st, evaluation_context)
                        monthly_income += block_results.get('income', 0)
                        monthly_expense += block_results.get('expense', 0)
                        monthly_save += block_results.get('save', 0)
                        monthly_loan_payment += block_results.get('loan_payment', 0)
                        monthly_invest_debit += block_results.get('invest', 0) # This might need refinement if InvestNode is inside Block
                    else:
                        child.Evaluate(st, evaluation_context) # Evaluate other nodes that don\'t contribute to financial totals

            current_month_balance = monthly_income + monthly_investment_return - monthly_expense - monthly_save - monthly_loan_payment - monthly_invest_debit
            # Store monthly summary, now including transaction details
            evaluation_context['financial_summary'].append({
                'month': current_month,
                'year': current_year,
                'income': monthly_income,
                'expense': monthly_expense,
                'save': monthly_save,
                'loan_payment': monthly_loan_payment,
                'invest_debit': monthly_invest_debit,
                'investment_return': monthly_investment_return,
                'balance': current_month_balance,
                'income_transactions': current_month_income_transactions,
                'expense_transactions': current_month_expense_transactions,
                'save_transactions': current_month_save_transactions,
                'loan_transactions': current_month_loan_transactions,
                'invest_transactions': current_month_invest_transactions,
                'investment_return_transactions': current_month_investment_return_transactions
            })

            # Accumulate totals
            total_income_all_months += monthly_income
            total_expense_all_months += monthly_expense
            total_save_all_months += monthly_save
            total_loan_payment_all_months += monthly_loan_payment
            total_invest_all_months += monthly_invest_debit
            total_investment_return_all_months += monthly_investment_return
            total_balance_all_months += current_month_balance

            # Advance to next month
            current_month += 1
            if current_month > 12:
                current_month = 1
                current_year += 1
            
            if current_year > end_year or (current_year == end_year and current_month > end_month_num):
                break

        # Open report.txt for writing
        with open("report.txt", "w") as report_file:
            report_file.write("\n--- Monthly Financial Summary ---\n")
            
            for summary in evaluation_context['financial_summary']:
                month_str = f"Month: {month_map_reverse[summary['month']]} {summary['year']}"
                report_file.write(f"{month_str}\n")

                # Income (Adds to Balance)
                if summary['income_transactions']:
                    income_details = []
                    for t in summary['income_transactions']:
                        tag_str = f" (TAG: {t['tag']})" if t['tag'] else ""
                        income_details.append(f"${t['amount']}{tag_str}")
                    report_file.write(f"  Income (+): {', '.join(income_details)} (Total: ${summary['income']})\n")
                else:
                    report_file.write(f"  Income (+): $0 (Total: $0)\n")

                # Expense (Removes from Balance)
                if summary['expense_transactions']:
                    expense_details = []
                    for t in summary['expense_transactions']:
                        tag_str = f" (TAG: {t['tag']})" if t['tag'] else ""
                        expense_details.append(f"${t['amount']}{tag_str}")
                    report_file.write(f"  Expense (-): {', '.join(expense_details)} (Total: ${summary['expense']})\n")
                else:
                    report_file.write(f"  Expense (-): $0 (Total: $0)\n")

                # Save (Removes from Balance)
                if summary['save_transactions']:
                    save_details = []
                    for t in summary['save_transactions']:
                        tag_str = f" (TAG: {t['tag']})" if t['tag'] else ""
                        save_details.append(f"${t['amount']}{tag_str}")
                    report_file.write(f"  Save (-): {', '.join(save_details)} (Total: ${summary['save']})\n")
                else:
                    report_file.write(f"  Save (-): $0 (Total: $0)\n")

                # Loan Payment (Removes from Balance)
                if summary['loan_transactions']:
                    loan_details = []
                    for t in summary['loan_transactions']:
                        tag_str = f" (TAG: {t['tag']})" if t['tag'] else ""
                        loan_details.append(f"${t['amount']}{tag_str}")
                    report_file.write(f"  Loan Payment (-): {', '.join(loan_details)} (Total: ${summary['loan_payment']})\n")
                else:
                    report_file.write(f"  Loan Payment (-): $0 (Total: $0)\n")

                # Invest (Removes from Balance) - Initial Debit
                if summary['invest_transactions']:
                    invest_details = []
                    for t in summary['invest_transactions']:
                        tag_str = f" (TAG: {t['tag']})" if t['tag'] else ""
                        invest_details.append(f"${t['amount']}{tag_str}")
                    report_file.write(f"  Invest (-): {', '.join(invest_details)} (Total: ${summary['invest_debit']})\n")
                else:
                    report_file.write(f"  Invest (-): $0 (Total: $0)\n")

                # Total Investment Return (+) (with compound principal)
                if summary['investment_return_transactions']:
                    return_details = []
                    for t in summary['investment_return_transactions']:
                        tag_str = f" (TAG: {t['tag']})" if t['tag'] else ""
                        return_details.append(f"${t['amount']:.2f}{tag_str}")
                    report_file.write(f"  Total Investment Return (+) (with compound principal): {', '.join(return_details)} (Total: ${summary['investment_return']:.2f})\n")
                else:
                    report_file.write(f"  Total Investment Return (+) (with compound principal): $0.00 (Total: $0.00)\n")

                    report_file.write(f"  Monthly Balance: ${summary['balance']:.2f}\n\n")

            report_file.write("\n--- Total Financial Summary ---\n")
            report_file.write(f"Total Income: ${total_income_all_months}\n")
            report_file.write(f"Total Expense: ${total_expense_all_months}\n")
            report_file.write(f"Total Save: ${total_save_all_months}\n")
            report_file.write(f"Total Loan Payment: ${total_loan_payment_all_months}\n")
            report_file.write(f"Total Invest (Debit): ${total_invest_all_months}\n")
            report_file.write(f"Total Investment Return: ${total_investment_return_all_months:.2f}\n")
            report_file.write(f"Total Balance: ${total_balance_all_months:.2f}\n")

            # Goal comparison
            if evaluation_context['goal'] is not None:
                goal = evaluation_context['goal']
                report_file.write(f"\n--- Goal Comparison ---\n")
                if total_balance_all_months >= goal:
                    report_file.write(f"Congratulations! Your total balance (${total_balance_all_months:.2f}) met or exceeded your goal of ${goal}.\n")
                elif total_balance_all_months > 0:
                    report_file.write(f"Your total balance was ${total_balance_all_months:.2f}. You needed ${goal - total_balance_all_months:.2f} more to reach your goal of ${goal}.\n")
                else:
                    report_file.write(f"Your total balance was ${total_balance_all_months:.2f}. You have a negative balance compared to your goal of ${goal}.\n")
            else:
                report_file.write("\n--- Goal Not Defined ---\n")
                report_file.write("No goal was defined in the CashScript for comparison.\n")


    except Exception as e:
        traceback.print_exc()
        sys.stdout.flush()
        print(f"Erro: {e}")
        sys.exit(1)