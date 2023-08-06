from pathlib import Path

from lark import Lark, Transformer
from rich import print_json

package_path = Path(__file__).parent

parser = Lark.open(
    package_path / "grammars/common.lark", rel_to=__file__, parser="lalr"
)

result = parser.parse("Testing")
print(result)
