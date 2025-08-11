# run_parser_demo.py

from lark import LarkError
from aegis_v2.language.parser import TlSafeParser

# --- Example TL-SAFE Specifications to Test ---

valid_specs = [
    # 1. Simple predicate
    'IsHighImpact("some_action")',
    # 2. Globally operator with negation
    'G(¬HasLabel(data, "PII"))',
    # 3. Implication
    'RequiresCap(action, "deploy") → HasHumanApproval(action)',
    # 4. Nested operators and conjunction
    'G(¬(IsHighImpact("action") ∧ ¬HasHumanApproval("action")))',
    # 5. More complex nested structure
    'G(PredicateA() → (PredicateB() ∧ G(PredicateC())))'
]

invalid_specs = [
    # 1. Mismatched parentheses
    'G(PredicateA()',
    # 2. Invalid operator (F is not in our grammar)
    'F(PredicateA())',
    # 3. Incomplete implication
    'PredicateA() →',
    # 4. Malformed predicate (no parentheses)
    'PredicateA',
    # 5. Gibberish
    'this is not a valid formula'
]


if __name__ == "__main__":
    print("--- Initializing TL-SAFE Parser Demonstration ---")
    parser = TlSafeParser()
    print("Parser initialized.\n")

    print("--- Testing Valid Specifications ---")
    success_count = 0
    for i, spec in enumerate(valid_specs):
        print(f"[{i+1}] Parsing: {spec}")
        try:
            ast = parser.parse(spec)
            print(f"    ✅ SUCCESS. AST: {ast}")
            success_count += 1
        except LarkError as e:
            print(f"    ❌ FAILED. Parser failed unexpectedly! {e}")
    print("-" * 40)

    print("\n--- Testing Invalid Specifications ---")
    failure_count = 0
    for i, spec in enumerate(invalid_specs):
        print(f"[{i+1}] Parsing: {spec}")
        try:
            parser.parse(spec)
            print(f"    ❌ FAILED. Parser succeeded unexpectedly!")
        except LarkError:
            print(f"    ✅ SUCCESS. Parser correctly identified spec as invalid.")
            failure_count += 1
    print("-" * 40)

    print("\n--- Parser Demonstration Complete ---")
    print(f"Results: {success_count}/{len(valid_specs)} valid specs parsed correctly.")
    print(f"         {failure_count}/{len(invalid_specs)} invalid specs rejected correctly.")
    if success_count == len(valid_specs) and failure_count == len(invalid_specs):
        print("All tests passed!")
    else:
        print("Some tests failed.")
