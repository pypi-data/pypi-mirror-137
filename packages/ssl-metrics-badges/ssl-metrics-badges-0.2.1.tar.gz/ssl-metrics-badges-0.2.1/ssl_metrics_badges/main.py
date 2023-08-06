from argparse import ArgumentParser, Namespace
from base64 import b64encode

from pybadges import badge


def getArgs() -> Namespace:
    parser: ArgumentParser = ArgumentParser(
        prog="SSL Metrics Badges",
        usage="This utility is an interface into the `pybadges` library's ability to create custom, embedable badges for each of the SSL tracked metrics.",
        epilog="Program created by Nicholas M. Synovic and George K. Thiruvathukal",
    )

    parser.add_argument(
        "-g",
        "--graph",
        required=True,
        type=str,
        help="The graph SVG file to be the badge logo",
    )
    parser.add_argument(
        "-lc",
        "--left-color",
        required=True,
        type=str,
        help="Left side color",
    )
    parser.add_argument(
        "-lt",
        "--left-text",
        required=True,
        type=str,
        help="Text to go on the left side of the badge",
    )
    parser.add_argument(
        "-u",
        "--link",
        required=True,
        type=str,
        help="Link to a specific URL that will open when the badge is clicked",
    )
    parser.add_argument(
        "-o",
        "--output",
        required=True,
        type=str,
        help="The output filename of the badge. NOTE: Must end in .svg",
    )
    parser.add_argument(
        "-rt",
        "--right-text",
        required=True,
        type=str,
        help="Text to go on the left side of the badge",
    )
    parser.add_argument(
        "-rc"
        "--right-color",
        required=True,
        type=str,
        help="Right side color",
    )
    parser.add_argument(
        "-t",
        "--title",
        required=True,
        type=str,
        help="Title of the badge",
    )

    return parser.parse_args()


def createBadge(
    leftText: str = "Hello",
    rightText: str = "World",
    link: str = "https://github.com/SoftwareSystemsLaboratory/",
    logo: str = "",
    leftColor: str = "maroon",
    rightColor: str = "gold",
    title: str = "SSL Metrics Badge",
) -> str:
    return badge(
        left_text=leftText,
        right_text=rightText,
        whole_link=link,
        logo=logo,
        left_color=leftColor,
        right_color=rightColor,
        embed_logo=True,
        whole_title=title,
    )


def main() -> None:
    args: Namespace = getArgs()

    if args.graph[-4::] != ".png":
        print("Invalid graph file extension. File must end in .png")
        quit(1)

    if args.output[-4::] != ".svg":
        print("Invalid output file extension. File must end in .svg")
        quit(2)

    base64EncodedStr: str
    with open(file=args.graph, mode="r", encoding="utf8") as file:
        byteStream: bytes = bytes(file.read(), "utf8")
        base64EncodedByteStream: bytes = b64encode(byteStream)
        base64EncodedStr: str = (
            "data:image/svg+xml;base64," + base64EncodedByteStream.decode("utf8")
        )
        file.close()

    badge: str = createBadge(
        leftText=args.left_text,
        rightText=args.right_text,
        link=args.link,
        logo=base64EncodedStr,
        leftColor=args.left_color,
        rightColor=args.right_color,
        title=args.title,
    )

    with open(file=args.output, mode="w") as svg:
        svg.write(badge)
        svg.close()


if __name__ == "__main__":
    main()
