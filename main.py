import multiprocessing
import port_scanner

if __name__ == "__main__":

    # number of targets
    num_targets = int(input("How many targets: "))

    # list of targets
    targets = input("list targets with space in between: ").split()
    print(targets)

    # scan type
    option = -1
    while option < 0 or option > 3:
        option = int(input(
                "\nSelect scan type:\n"
                "1. Common ports\n"
                "2. Full scan (1–65535)\n"
                "3. Get Mac Address\n"
                "Enter option: "
            ))

    process_array = []
    for i in range(0, num_targets):
        p = multiprocessing.Process(target=port_scanner.main, args=(targets[i], option,))
        process_array.append(p)
    
    # execute
    for i in range(0, len(process_array)):
        process_array[i].start()

    # clean up
    for i in range(0, len(process_array)):
        process_array[i].join()
