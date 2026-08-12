#!/usr/bin/env python3

if __name__ == "__main__":
    print("=== Kaboom 1 ===\nAccess to alchemy/grimoire/dark_spellbook.py "
          "directly\nTest import now - THIS WILL RAISE AN UNCAUGHT EXCEPTION")
    from alchemy.grimoire.dark_spellbook import dark_spell_record
    dark_spell_record("Fantasy", "Earth, wind, fire")
