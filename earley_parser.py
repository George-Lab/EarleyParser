from grammar import Grammar, Rule


class State:
    def __init__(self, left, right, dot_pos, origin):
        self.left = left  # Левая часть правила
        self.right = tuple(right)  # Правая часть правила (кортеж символов)
        self.dot_pos = dot_pos  # Позиция точки в правой части
        self.origin = origin  # Позиция в входной строке, где это состояние возникло
        self.is_complete = self.dot_pos == len(self.right)  # Завершено ли правило (точка в конце)

    def next_symbol(self):
        # Возвращает следующий символ после точки
        if self.dot_pos < len(self.right):
            return self.right[self.dot_pos]
        return None

    def advance(self):
        # Перемещает точку на один символ вправо
        return State(self.left, self.right, self.dot_pos + 1, self.origin)

    def __hash__(self):
        # Хеш-функция для использования состояния в множествах и словарях
        return hash((self.left, self.right, self.dot_pos, self.origin))

    def __eq__(self, other):
        # Проверка на равенство двух состояний
        return (self.left, self.right, self.dot_pos, self.origin) == (other.left, other.right, other.dot_pos, other.origin)

    def __repr__(self):
        # Представление состояния в виде строки
        right_with_dot = ''.join(self.right[:self.dot_pos]) + '.' + ''.join(self.right[self.dot_pos:])
        return f"({self.left} -> {right_with_dot}, {self.origin})"


class EarleyParser:
    def __init__(self):
        self.grammar = None
        self.rules = {}
        self.terminals = []
        self.non_terminals = []
        self.start_symbol = ''
        self.vertices = []

    def fit(self, grammar):
        # Инициализация парсера с заданной грамматикой
        self.grammar = grammar
        self.terminals = grammar.terminals
        self.non_terminals = grammar.non_terminals.copy()
        self.start_symbol = grammar.start_symbol

        # Инициализация словаря правил
        self.rules = {non_term: set() for non_term in self.non_terminals}
        for rule in grammar.rules:
            self.rules[rule.left].add(rule)

        # Добавление дополнительного стартового символа
        self.augmented_start = '&'
        self.non_terminals.append(self.augmented_start)
        self.rules[self.augmented_start] = {Rule(self.augmented_start, [self.start_symbol])}

    def predict(self, word):
        # Проверка принадлежности слова языку
        return self.parse(word)

    def parse(self, word):
        # Основной метод парсинга
        self.vertices = [set() for _ in range(len(word) + 1)]
        start_state = State(self.augmented_start, [self.start_symbol], 0, 0)
        self.vertices[0].add(start_state)
        self._closure(0)

        for i in range(len(word)):
            self._scan(i, word[i])
            self._closure(i + 1)

        # Проверка на наличие принимающего состояния
        for state in self.vertices[len(word)]:
            if (state.left == self.augmented_start and state.is_complete and state.origin == 0):
                return True
        return False

    def _closure(self, index):
        # Замыкание множества состояний
        changed = True
        while changed:
            changed = False
            new_states = set()
            for state in self.vertices[index]:
                next_symbol = state.next_symbol()
                if next_symbol is not None and next_symbol in self.non_terminals:
                    for rule in self.rules[next_symbol]:
                        new_state = State(rule.left, rule.right, 0, index)
                        if new_state not in self.vertices[index]:
                            new_states.add(new_state)
                            changed = True
                elif state.is_complete:
                    for prev_state in self.vertices[state.origin]:
                        if prev_state.next_symbol() == state.left:
                            advanced_state = prev_state.advance()
                            if advanced_state not in self.vertices[index]:
                                new_states.add(advanced_state)
                                changed = True
            self.vertices[index].update(new_states)

    def _scan(self, index, symbol):
        # Сканирование символа входной строки
        self.vertices[index + 1] = set()
        for state in self.vertices[index]:
            next_symbol = state.next_symbol()
            if next_symbol == symbol:
                advanced_state = state.advance()
                self.vertices[index + 1].add(advanced_state)