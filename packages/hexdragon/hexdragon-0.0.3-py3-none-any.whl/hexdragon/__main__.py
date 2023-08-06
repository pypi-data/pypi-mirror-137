import argparse, sys


def main():
    parser = argparse.ArgumentParser(
        description="Print a file as coloured hexadecimal values to console"
    )
    parser.add_argument("inputfile", action="store", help="Input file")
    parser.add_argument("--fill", action="store", help="byte to fill [default: 0xff]")
    parser.add_argument("-w", action="store", help="width")
    args = parser.parse_args()

    with open(args.inputfile, "rb") as in_file:
        data_array = []
        data = in_file.read(1)
        data_array.append(data)
        while data:
            data = in_file.read(1)
            data_array.append(data)

        hex_array = [hex(int.from_bytes(byte, "big")) for byte in data_array]
        if not args.w:
            length = len(hex_array)

            n = length
            while n % n ** 0.5 != 0:
                n += 1
            sqrt_n = int(n ** 0.5)

            padding = n - length
            for i in range(padding):
                hex_array.append(args.fill if args.fill is not None else hex(0xFF))

        width = int(args.w or sqrt_n)
        chunks = [hex_array[i : i + width] for i in range(0, len(hex_array), width)]

        for chunk in chunks:
            for i in chunk:
                hexa = i if len(i) != 3 else i[0:2] + "0" + i[2]
                sys.stdout.write(f"\033[38;5;{int(i, 16)}m{hexa}\u001b[0m")
            sys.stdout.write("\n")


if __name__ == "__main__":
    main()
