from src.evalb.scorer import Scorer


def evaluate():
    gold_name = "../../data/heb-ctrees_"
    gold_suffix = ".gold"

    test_path = "../../output/"
    preco = "ParserWithPrecolation_"
    no_preco = "ParserWithoutPrecolation_"
    optimizied = "NP1VC2HC/NP1VC2HC_"
    test_suffix = ".txt"

    batches = ["0-10", "11-20", "21-25", "25-30", "30-35", "35-40"]

    for batch in batches:
        batch_gold = gold_name + batch + gold_suffix
        batch_preco = test_path + preco + batch + test_suffix
        preco_score = (Scorer().evalb(batch_gold, batch_preco))
        batch_no_preco = test_path + no_preco + batch + test_suffix
        no_preco_score = (Scorer().evalb(batch_gold, batch_no_preco))
        batch_optimizied = test_path + optimizied + batch + test_suffix
        opt_score = (Scorer().evalb(batch_gold, batch_optimizied))
        with open(test_path + "result" + batch + ".txt", 'w') as f:
            f.write(preco + batch)
            f.write(preco_score)
            f.write('\n\n\n')
            f.write(no_preco + batch)
            f.write(no_preco_score)
            f.write('\n\n\n')
            f.write(optimizied + batch)
            f.write(opt_score)


if __name__ == "__main__":
    evaluate()