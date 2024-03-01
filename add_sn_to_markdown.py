import argparse


def parse_args():
    arg_parser = argparse.ArgumentParser(description="This script will add Series number to markdown file")
    arg_parser.add_argument("--file", type=str, help="The markdown file to be add", required=True)
    arg_parser.add_argument("--encoding", type=str, default="utf-8", help="Encoding of src file")
    arg_parser.add_argument("--overwrite", action="store_true", default=False, help="whether to overwrite origin file")
    arg_parser.add_argument(
        "--savePath", type=str, help="Path to save new file, can skip if argument overwrite is provided"
    )
    arg_parser.add_argument("--startLevel", type=int, default=1, help="From which level to encode sn")
    arg_parser.add_argument("--startValue", type=int, default=1, help="From which value to encode sn")
    args = arg_parser.parse_args()
    return args


def read_file(src_file_path: str, encoding: str) -> list[str]:
    with open(src_file_path, mode="r", encoding=encoding) as f:
        lines = f.readlines()
    return lines


def save_file(lines: list[str], save_file_path: str, encoding: str):
    with open(save_file_path, "w+", encoding=encoding) as f:
        for line in lines:
            f.write(line)
    return 0


class CSnCounter:
    def __init__(self, start_level: int, start_value: int):
        self.counter: list[int] = []
        self.start_level: int = start_level
        self.start_value: int = start_value

    @property
    def levels(self) -> int:
        return len(self.counter)

    def reset(self):
        self.counter.clear()

    def update(self, sign: str):
        if (level_sign := len(sign)) < 1:
            pass

        if level_sign >= self.levels + 2:
            raise ValueError("level wrong")
        elif level_sign == self.levels + 1:
            self.counter.append(self.start_value)
        elif level_sign == self.levels:
            self.counter[-1] += 1
        else:  # level_sign < self.levels:
            self.counter = self.counter[0:level_sign]
            self.counter[-1] += 1
        return 0

    def get_sn(self) -> str:
        return ".".join([str(_) for _ in self.counter[self.start_level :]])


def update_lines(lines: list[str], start_level: int, start_value: int):
    sn_counter = CSnCounter(start_level=start_level, start_value=start_value)
    for i, line in enumerate(lines):
        if line[0] == "#":
            sign, description = line.split()
            sn_counter.update(sign=sign)
            sn = sn_counter.get_sn()
            if sn:
                new_line = f"{sign} {sn} {description}"
            else:
                new_line = f"{sign} {description}"
            old_line = line.replace("\n", "")
            print(f"{old_line:<60s} -> {new_line:<60s}")
            lines[i] = new_line + "\n"
    return 0


if __name__ == "__main__":
    args = parse_args()
    print(args)
    src_file_path, src_file_encoding, overwrite, save_file_path = (
        args.file,
        args.encoding,
        args.overwrite,
        args.savePath,
    )
    start_level, start_value = args.startLevel, args.startValue
    if overwrite:
        save_file_path = src_file_path
    elif not save_file_path:
        raise ValueError(f"save path is not provided")

    lines = read_file(src_file_path=src_file_path, encoding=src_file_encoding)
    update_lines(lines, start_level=start_level, start_value=start_value)
    save_file(lines, save_file_path=save_file_path, encoding=src_file_encoding)
