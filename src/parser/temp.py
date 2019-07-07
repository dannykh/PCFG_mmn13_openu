def _build_tree_from_backtrack(cky_table: Dict[Tuple[int, int], Dict[MultiSymbol, CkyTableEntry]], n: int):
    head_symbol = MultiSymbol((NonTerminal("S"),))
    assert head_symbol in cky_table[n, 0]
    head = Node(str(head_symbol))
    node_list = [(head, n, cky_table[n, 0][head_symbol])]
    while node_list:
        node, span, tbl_entry = node_list.pop()
        if span == -1:
            continue
        for child_entry in [cky_table[tbl_entry.start, tbl_entry.partition][tbl_entry.RHS.symbol_list[0]],
                            cky_table[n - tbl_entry.partition, tbl_entry.start + tbl_entry.partition]]:
            child_node = Node

def cky(grammar: ProbGrammar, sentence: str, include_unary=False) -> Node:
    """
    An implementation of CKY algorithm in it's wikipedia version.
    :param grammar: The probabilistic grammar to use.
    :param sentence: A sentence of lexical tokens separated by white space.
    :param include_unary: True if to support unary rules in run, False otherwise.
    :return: Most probable parse tree for given sentence.
    """
    sentence = sentence.split(" ")
    n = len(sentence)
    cky_table: Dict[Tuple[int, int], Dict[MultiSymbol, CkyTableEntry]] = {(i, j): dict() for i in range(n + 1) for j in
                                                                          range(n + 1)}
    for j in range(0, n):
        rhs = MultiSymbol((Terminal(sentence[j]),))
        terminal_node = Node(sentence[j])
        cky_table[0, j][rhs] = CkyTableEntry(-1, -1, None, - 0.0)
        # Check if symbol exists as some rule's RHS in grammar
        if rhs in grammar.rhs_to_lhs_map:
            # Iterate all rules generating this as rhs
            for rule in grammar.rhs_to_lhs_map[rhs]:
                assert rule.is_lexical()  # Sanity check
                cky_table[1, j][rule.lhs] = CkyTableEntry(0, j, rhs, grammar[rule].minus_log_prob)
        else:
            # Initiate assuming no match in lexical rules in grammar, and therefore UNK symbol most probable
            # (See note near definition of UNK_SYMBOL )
            node = Node(str(UNK_SYMBOL))
            node.add_child(terminal_node)
            cky_table[1, j][MultiSymbol((UNK_SYMBOL,))] = CkyTableEntry(0, j, rhs, -0.0)

    for span_length in range(2, n + 1):
        for span_start in range(0, n - span_length + 1):
            for partition in range(1, span_length):
                # Name current entries in table as B, C for possible derivation " _ -> B C "
                for rhs_B, rhs_B_entry in cky_table[partition, span_start].items():
                    for rhs_C, rhs_C_entry in \
                            cky_table[span_length - partition, span_start + partition].items():
                        # Build RHS as concatenation of B and C
                        rhs = rhs_B + rhs_C
                        # Skip if no rule exists such that -> B C
                        if rhs not in grammar.rhs_to_lhs_map:
                            continue
                        # There are rules A -> B C in grammar, add all such rules as possible derivations
                        for rule in grammar.rhs_to_lhs_map[rhs]:
                            rule_prob = rhs_B_entry.minus_log_prob + rhs_C_entry.minus_log_prob + grammar[
                                rule].minus_log_prob
                            if rule.lhs not in cky_table[span_length, span_start] or rule_prob < \
                                    cky_table[span_length, span_start][rule.lhs].minus_log_prob:
                                cky_table[span_length, span_start][rule.lhs] = CkyTableEntry(partition, span_start, rhs,
                                                                                             rule_prob)

    return min([(node, prob) for _, (node, prob) in cky_table[n, 0].items() if
                node.tag in map(str, grammar.start_symbols)], key=lambda x: x[1])[0]

CkyTableEntry = NamedTuple("CkyTableEntry", [("partition", int), ("start", int), ("RHS", MultiSymbol),
                                             ("minus_log_prob", float)])