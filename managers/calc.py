class Calculator:
    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b

    def divide(self, a, b):
        if b == 0:
            raise ValueError("Ошибка: деление на ноль невозможно.")
        return a / b

    def calculate(self, expression):
        try:
            parts = expression.split()
            if len(parts) != 3:
                raise ValueError("Ошибка: выражение должно содержать два числа и оператор.")
            
            a = float(parts[0])
            operator = parts[1]
            b = float(parts[2])

            if operator == '+':
                return self.add(a, b)
            elif operator == '-':
                return self.subtract(a, b)
            elif operator == '*':
                return self.multiply(a, b)
            elif operator == '/':
                return self.divide(a, b)
            else:
                raise ValueError("Ошибка: неподдерживаемый оператор. Используйте +, -, * или /.")
        
        except ValueError as e:
            return str(e)
        except Exception as e:
            return "Ошибка: " + str(e)

def calculate(calculator: Calculator) -> None:
    expression = input("Введите выражение (например, \"2 + 2\"): ")
    result = calculator.calculate(expression)
    if result is not None:
        print(result)
