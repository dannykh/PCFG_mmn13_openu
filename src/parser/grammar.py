import copy
import pickle
from typing import Set, Dict

from math import inf, log

from src.parser.rule import Rule
from src.parser.symbol import Terminal, NonTerminal, MultiSymbol


class CountAndProbability:
    def __init__(self, count=0, minus_log_prob=inf):
        self.count = count
        self.minus_log_prob = minus_log_prob


class ProbGrammar:
    """
    A probabilistic grammar, holding the set of it's rules, symbols (start symbols, terminals and non-terminals), and
    counts and log-probabilities of it's rules.
    """

    def __init__(self):
        # Rule (lexical/syntactical) maps, mapping rules to their counts and probabilities
        self.syntactic_rule_map: Dict[Rule, CountAndProbability] = dict()
        self.lexical_rule_map: Dict[Rule, CountAndProbability] = dict()
        # Unary rules : Note !!! disjoint from syntactic rule map !
        self.unary_rule_map: Dict[Rule, CountAndProbability] = dict()
        # Symbol sets
        self.start_symbols: Set[NonTerminal] = set(MultiSymbol((NonTerminal("S"),)))
        self.terminals: Set[Terminal] = set()
        self.non_terminals: Set[NonTerminal] = set()
        # Mapping LHS to RHS and vice versa for easy computation
        self.rhs_to_lhs_map: Dict[MultiSymbol, Set[Rule]] = dict()
        self.lhs_to_rhs_map: Dict[MultiSymbol, Set[Rule]] = dict()
        # Track lhs counts
        self.lhs_counts: Dict[MultiSymbol, int] = dict()

    def get_relevant_rule_map(self, rule):
        return self.lexical_rule_map if rule.is_lexical() else self.unary_rule_map if rule.is_unary() else \
            self.syntactic_rule_map

    def add_rule(self, rule: Rule):
        # Add newly seen symbols
        self.terminals.update({sym for sym in rule.lhs.symbol_list + rule.rhs.symbol_list if type(sym) is Terminal})
        self.non_terminals.update(
            {sym for sym in rule.lhs.symbol_list + rule.rhs.symbol_list if type(sym) is NonTerminal})
        # Find relevant rule map to update
        rules_to_update = self.get_relevant_rule_map(rule)
        # Add rule to relevant map if first seen
        if rule not in rules_to_update:
            rules_to_update[rule] = CountAndProbability()
        self.increment_rule_count(rule)
        # Map LHS and RHS to rule
        if rule.rhs not in self.rhs_to_lhs_map:
            self.rhs_to_lhs_map[rule.rhs] = set()
        if rule.lhs not in self.lhs_to_rhs_map:
            self.lhs_counts[rule.lhs] = 0
            self.lhs_to_rhs_map[rule.lhs] = set()
        self.rhs_to_lhs_map[rule.rhs].update({rule})
        self.lhs_to_rhs_map[rule.lhs].update({rule})
        self.lhs_counts[rule.lhs] += 1

    def set_rule_count_and_probability(self, rule, count: int, minus_log_prob: float):
        relevant_rule_map = self.get_relevant_rule_map(rule)
        if rule not in relevant_rule_map:
            raise ValueError("Rule doesn't exist in grammar.")
        relevant_rule_map[rule].count = count
        relevant_rule_map[rule].minus_log_prob = minus_log_prob

    def __getitem__(self, item: Rule):
        return self.get_relevant_rule_map(item)[item]

    def __contains__(self, item: Rule):
        return item in self.get_relevant_rule_map(item)

    def increment_rule_count(self, rule):
        """
        ! NOTE : Using this nullifies rule's probability if such already exists.
        """
        relevant_rule_map = self.get_relevant_rule_map(rule)
        self.set_rule_count_and_probability(rule, relevant_rule_map[rule].count + 1, inf)

    def generate_rule_probabilities(self):
        """
        Attach a probability ( - log of probability ) to every rule in the grammar.
        :return: None.
        """
        for rule_map in (self.syntactic_rule_map, self.unary_rule_map, self.lexical_rule_map):
            for rule, count_and_prob in rule_map.items():
                count_and_prob.minus_log_prob = -log(
                    float(count_and_prob.count) / float(self.lhs_counts[rule.lhs]))


def precolate_grammar(grammar: ProbGrammar):
    """
    Collapse unit rules in the grammar.
    :param grammar: The grammar to collapse unit rules in.
    :return: None.

    Collapses all unit rules in BINARY (!) grammar: For each A ->* BC, the rule A->BC is added.
    !Notes :
    1. Rules must have probability already generated !
    2. Rules added in this function shall have no count.
    3. Although all possible rules are added recursively, new unit rules ARE NOT added.
    """
    # Keep track of unhandled unary rules
    unit_rules = [urule for urule in grammar.unary_rule_map]
    # Generate local copy of unary rules, ATM we do not wish to alter grammar's instance
    unit_rule_map = copy.deepcopy(grammar.unary_rule_map)
    # While unhandled unary rules remain
    while unit_rules:
        # Pop A --> B
        unit_rule = unit_rules.pop()
        # Find all unit rules with current rule's RHS as LHS:
        # i.e all rules B --> C
        for urule in unit_rules:
            if urule.lhs == unit_rule.rhs:
                # Shortcut A and C : Create a rule A --> C
                new_rule = Rule(unit_rule.lhs, urule.rhs)
                # If this is a new rule, add it as a new unit rule to local copy of unit rule map
                if new_rule not in unit_rule_map:
                    # TODO : Currently count is disregarded and only probability is generated.
                    unit_rule_map[new_rule] = CountAndProbability(0, unit_rule_map[unit_rule].minus_log_prob +
                                                                  unit_rule_map[unit_rule].minus_log_prob)
                    # Add the new unit rule for further handling
                    unit_rules.append(new_rule)
        # Expand unary rule to all immediate binary rules
        # Traverse all non-unary rules with current (unary) rule's RHS as LHS : B --> C D
        for rule in grammar.lhs_to_rhs_map[unit_rule.rhs]:
            if rule.is_unary() and not rule.is_lexical():
                continue
            # Create a rule A --> C D
            new_rule = Rule(unit_rule.lhs, rule.rhs)
            # TODO : If rule already exists in grammar, how to choose probability ?
            if new_rule not in grammar:
                grammar.add_rule(new_rule)
                # Take the unit rule's probability from the local copy as it might have unit rules which do not exist
                # in the grammar
                grammar[new_rule].minus_log_prob = grammar[rule].minus_log_prob + unit_rule_map[
                    unit_rule].minus_log_prob


def write_grammar_to_files(grammar: ProbGrammar, gram_path: str, lex_path: str):
    """
    Write a grammar to gram,lex files.
    :param grammar: The grammar to save.
    :param gram_path: Path to gram file.
    :param lex_path: Path to .lex file.
    :return: None.
    """

    def __write_rules(p_rule_map, p_fp):
        for rule, count_and_prob in p_rule_map.items():
            p_fp.write("{} {} {} {}\n".format(count_and_prob.count, count_and_prob.minus_log_prob, rule.lhs, rule.rhs))

    with open(gram_path, "w") as fp:
        for rule_map in (grammar.unary_rule_map, grammar.syntactic_rule_map):
            __write_rules(rule_map, fp)

    with open(lex_path, "w") as fp:
        __write_rules(grammar.lexical_rule_map, fp)


def pickle_grammar(grammar: ProbGrammar, pkl_path: str):
    """
    Pickle grammar.
    :param grammar: Grammar to pickle.
    :param pkl_path: Path to pickle file.
    :return: None.
    """
    with open(pkl_path, "wb") as fp:
        pickle.dump(grammar, fp)


def unpickle_grammar(pkl_path: str) -> ProbGrammar:
    with open(pkl_path, "rb") as fp:
        grammar = pickle.load(fp)

    return grammar


def load_grammar_from_files(gram_path: str, lex_path: str):
    """
    Load grammar from .lex, .gram files.
    :return: The loaded grammar.
    """
    grammar = ProbGrammar()
    for fpath in (gram_path, lex_path):
        with open(fpath, "r") as fp:
            for line in fp:
                count = int(line[0])
                probability = float(line[1])
                lhs = MultiSymbol((NonTerminal(line[2]),))
                rhs = MultiSymbol(tuple(map(NonTerminal, line[3:])))
                rule = Rule(lhs, rhs)
                grammar.add_rule(rule)
                grammar.set_rule_count_and_probability(rule, count, probability)
