from grammar import Grammar, Rule
from earley_parser import EarleyParser


def read_input():
    # Чтение входных данных
    N, Sigma, P = map(int, input().split())
    non_terminals = list(input().strip())
    terminals = list(input().strip())
    rules = []
    for _ in range(P):
        line = input().strip()
        if '->' not in line:
            raise RuntimeError("Неверный формат правила. Правила должны содержать '->'.")
        left_part, right_part = line.split('->')
        left_part = left_part.strip()
        right_part = right_part.strip()
        if right_part == '':
            right_symbols = []  # Представляет пустое слово
        else:
            right_symbols = list(right_part)  # Разделение на отдельные символы
        rules.append(Rule(left_part, right_symbols))
    start_symbol = input().strip()
    m = int(input())
    words = [input().strip() for _ in range(m)]
    return non_terminals, terminals, rules, start_symbol, words


if __name__ == "__main__":
    try:
        non_terminals, terminals, rules, start_symbol, words = read_input()
        grammar = Grammar(non_terminals, terminals, rules, start_symbol)
        parser = EarleyParser()
        parser.fit(grammar)
        for word in words:
            result = parser.predict(word)
            print("Yes" if result else "No")
    except RuntimeError as e:
        print(f"Ошибка: {e}")