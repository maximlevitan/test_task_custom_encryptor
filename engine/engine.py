from engine.tokens import Token
from engine.parser import Parser
from engine.renderer import render

from rules.char_substitution import CharacterSubstitutionRule
from rules.substring_rearrangement import SubstringRearrangementRule
from rules.index_encoding import IndexBasedEncodingRule
from rules.special_symbol import SpecialSymbolInsertionRule
from rules.number_encoding import NumberEncodingRule


class EncryptionEngine:

    def __init__(self):
        self.rules_encrypt = [
            CharacterSubstitutionRule(),
            SubstringRearrangementRule(),
            IndexBasedEncodingRule(),
            SpecialSymbolInsertionRule(),
            NumberEncodingRule(),
        ]

        self.rules_decrypt = list(reversed(self.rules_encrypt))

    def encrypt(self, text: str, verbose=False) -> str:
        parser = Parser()
        tokens = parser.parse_for_encrypt(text)

        if verbose:
            print(f"[Parser] {tokens}")

        for rule in self.rules_encrypt:
            tokens = rule.encrypt(tokens)
            if verbose:
                print(f"[{rule.__class__.__name__}] {tokens}")

        return render(tokens)

    def decrypt(self, text: str, verbose=False) -> str:
        parser = Parser()
        tokens = parser.parse_for_decrypt(text)

        if verbose:
            print(f"[Parser] {tokens}")

        for rule in self.rules_decrypt:
            tokens = rule.decrypt(tokens)
            if verbose:
                print(f"[{rule.__class__.__name__}] {tokens}")

        return render(tokens)
