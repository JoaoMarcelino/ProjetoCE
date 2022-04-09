from main import gen_indiv, swap_mutation, create_table



def test_gen(x):
    print(gen_indiv(x))

def test_table(size, min, max):

    print("Unidirectional")

    table = create_table(size, min, max, bidirectional=False)
    for i, row in enumerate(table):
        print(row)

    print("Bidirectional")

    table = create_table(size, min, max)
    for i, row in enumerate(table):
        print(row)


if __name__ == "__main__":
    test_table(3, 1, 20)