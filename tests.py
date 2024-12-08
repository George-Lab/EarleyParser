import unittest
from grammar import Grammar, Rule
from earley_parser import EarleyParser


class TestEarleyParser(unittest.TestCase):

    def test_simple_grammar(self):
        # Грамматика: S -> a
        non_terminals = ['S']
        terminals = ['a']
        rules = [Rule('S', ['a'])]
        start_symbol = 'S'
        grammar = Grammar(non_terminals, terminals, rules, start_symbol)
        parser = EarleyParser()
        parser.fit(grammar)
        self.assertTrue(parser.predict('a'))
        self.assertFalse(parser.predict('b'))
        self.assertFalse(parser.predict('aa'))

    def test_epsilon_rule(self):
        # Грамматика: S -> ε
        non_terminals = ['S']
        terminals = []
        rules = [Rule('S', [])]  # Пустой список представляет ε
        start_symbol = 'S'
        grammar = Grammar(non_terminals, terminals, rules, start_symbol)
        parser = EarleyParser()
        parser.fit(grammar)
        self.assertTrue(parser.predict(''))
        self.assertFalse(parser.predict('a'))

    def test_recursive_grammar(self):
        # Грамматика: S -> aSb | ε
        non_terminals = ['S']
        terminals = ['a', 'b']
        rules = [Rule('S', ['a', 'S', 'b']), Rule('S', [])]
        start_symbol = 'S'
        grammar = Grammar(non_terminals, terminals, rules, start_symbol)
        parser = EarleyParser()
        parser.fit(grammar)
        self.assertTrue(parser.predict(''))
        self.assertTrue(parser.predict('ab'))
        self.assertTrue(parser.predict('aabb'))
        self.assertTrue(parser.predict('aaabbb'))
        self.assertFalse(parser.predict('aabbb'))
        self.assertFalse(parser.predict('aaabb'))
        self.assertFalse(parser.predict('aabbba'))

    def test_complex_grammar(self):
        # Грамматика для арифметических выражений
        # E -> E+T | T
        # T -> T*F | F
        # F -> (E) | i
        non_terminals = ['E', 'T', 'F']
        terminals = ['+', '*', '(', ')', 'i']
        rules = [
            Rule('E', ['E', '+', 'T']),
            Rule('E', ['T']),
            Rule('T', ['T', '*', 'F']),
            Rule('T', ['F']),
            Rule('F', ['(', 'E', ')']),
            Rule('F', ['i'])
        ]
        start_symbol = 'E'
        grammar = Grammar(non_terminals, terminals, rules, start_symbol)
        parser = EarleyParser()
        parser.fit(grammar)
        self.assertTrue(parser.predict('i'))
        self.assertTrue(parser.predict('i+i'))
        self.assertTrue(parser.predict('i+i*i'))
        self.assertTrue(parser.predict('(i)'))
        self.assertTrue(parser.predict('(i+i)*i'))
        self.assertFalse(parser.predict('i+'))
        self.assertFalse(parser.predict('i*(i+)'))
        self.assertFalse(parser.predict('i*+i'))

    def test_left_recursion(self):
        # Грамматика: S -> S a | a
        non_terminals = ['S']
        terminals = ['a']
        rules = [Rule('S', ['S', 'a']), Rule('S', ['a'])]
        start_symbol = 'S'
        grammar = Grammar(non_terminals, terminals, rules, start_symbol)
        parser = EarleyParser()
        parser.fit(grammar)
        self.assertTrue(parser.predict('a'))
        self.assertTrue(parser.predict('aa'))
        self.assertTrue(parser.predict('aaa'))
        self.assertFalse(parser.predict(''))
        self.assertFalse(parser.predict('b'))

    def test_invalid_grammar(self):
        non_terminals = ['S']
        terminals = ['a']
        rules = [Rule('S', ['B'])]  # 'B' не определен
        start_symbol = 'S'
        with self.assertRaises(RuntimeError):
            Grammar(non_terminals, terminals, rules, start_symbol)

    def test_nonexistent_symbol_in_rule(self):
        non_terminals = ['S']
        terminals = ['a']
        rules = [Rule('S', ['a', 'B'])]  # 'B' не определен
        start_symbol = 'S'
        with self.assertRaises(RuntimeError):
            Grammar(non_terminals, terminals, rules, start_symbol)


if __name__ == '__main__':
    unittest.main()