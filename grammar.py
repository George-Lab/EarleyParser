class Rule:
    def __init__(self, left, right):
        self.left = left  # Левая часть правила (нетерминал)
        self.right = tuple(right)  # Правая часть правила (кортеж символов, пустой кортеж представляет ε)

    def __repr__(self):
        rhs = ''.join(self.right) if self.right else 'ε'
        return f"{self.left} -> {rhs}"


class Grammar:
    def __init__(self, non_terminals, terminals, rules, start_symbol):
        self.non_terminals = non_terminals  # Список нетерминальных символов
        self.terminals = terminals  # Список терминальных символов
        self.rules = rules  # Список объектов Rule
        self.start_symbol = start_symbol  # Стартовый символ

        self.check_input_accuracy()

    def check_input_accuracy(self):
        # Проверка корректности входных данных
        if self.start_symbol not in self.non_terminals:
            raise RuntimeError("Стартовый символ должен быть нетерминалом.")
        if set(self.non_terminals) & set(self.terminals):
            raise RuntimeError("Нетерминалы и терминалы не должны пересекаться.")
        for rule in self.rules:
            if rule.left not in self.non_terminals:
                raise RuntimeError(f"Левая часть правила должна быть нетерминалом, получено '{rule.left}'.")
            for symbol in rule.right:
                if symbol not in self.non_terminals and symbol not in self.terminals:
                    raise RuntimeError(f"Символ '{symbol}' в правиле '{rule.left} -> {''.join(rule.right)}' не определен в грамматике.")