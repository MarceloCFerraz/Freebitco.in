if __name__ == '__main__':
    vezes = int(
        input("Quantas vezes? ")
    )
    # ------------------------------
    onlose1 = float(
        input("OnLose 1 (%): ")
    )
    onlose1 = (onlose1 / 100)
    # ------------------------------
    onlose2 = float(
        input("OnLose 2 (%): ")
    )
    onlose2 = (onlose2 / 100)
    # ------------------------------
    bet = 1.0
    resultado1 = [bet]
    resultado2 = [bet]
    # ------------------------------
    soma1 = 0.0
    soma2 = 0.0
    # ------------------------------
    for i in range(1, vezes):
        bet = bet + (bet * onlose1)
        resultado1.append(divmod(bet, 1)[0])
    # ------------------------------
    bet = 1.0
    # ------------------------------
    for i in range(1, vezes):
        bet = bet + (bet * onlose2)
        resultado2.append(divmod(bet, 1)[0])
    # ------------------------------
    print("\nOnLose 1\tOnLose 2")
    for i in range(0, vezes):
        soma1 = soma1 + resultado1[i]
        soma2 = soma2 + resultado2[i]
        print("Bet {0}: {1:,} ({2:,})\t{3:,} ({4:,})"
              .format(
                    i + 1,
                    divmod(resultado1[i], 1)[0],
                    divmod(soma1, 1)[0],
                    divmod(resultado2[i], 1)[0],
                    divmod(soma2, 1)[0])
              )
    # ------------------------------
    input("press enter to quit")
