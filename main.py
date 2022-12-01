import time
import os
from colorama import Fore, Style

from cleaningModel import CleaningModel


def clearConsole():
    if os.name == "posix":
        os.system("clear")
    elif os.name == "ce" or os.name == "nt" or os.name == "dos":
        os.system("cls")


if __name__ == "__main__":

    clearConsole()
    M = int(input("Height: "))
    N = int(input("Width: "))

    CANT_AGENTS = int(input("Number of agents: "))

    DIRT_PERCENTAGE_CELLS = float(
        input("Percentage of dirt cells (0-1): "))
    while (DIRT_PERCENTAGE_CELLS > 1):
        print("Percentage of dirt cells must be between 0 and 1")
        DIRT_PERCENTAGE_CELLS = float(
            input("Percentage of dirt cells (0-1): "))

    MAX_TIME = int(input("Max execution time (seconds): "))

    def main():
        model = CleaningModel(
            CANT_AGENTS, N, M, DIRT_PERCENTAGE_CELLS, MAX_TIME)
        while (model.dirt_cells > 0 and ((time.time() - model.init_time) < model.final_time)):
            model.step()
            clearConsole()
            for i in range(M):
                for j in range(N):
                    if model.dirty_matrix[i][j]:
                        print(Fore.GREEN + "1", end=" ")
                    else:
                        print(Fore.RED + "0", end=" ")
                print()
            print(Style.RESET_ALL)
            print(f"Clean cells percentage: {model.total_movements()}%")
            time.sleep(1)

        print("\nTotal movements:", model.total_movements())
        print("Total time:", model.final_time, "seconds")

    main()
