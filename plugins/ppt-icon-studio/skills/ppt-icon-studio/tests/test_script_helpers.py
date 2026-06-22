from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path
import sys
import unittest


SCRIPT_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))


def load_script(name: str):
    path = SCRIPT_DIR / name
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class ScriptHelperTests(unittest.TestCase):
    def test_crop_and_trace_hex_parser_accepts_hash_and_plain_values(self):
        module = load_script("color_utils.py")

        self.assertEqual(module.parse_hex_color("#00ff00"), (0, 255, 0))
        self.assertEqual(module.parse_hex_color("336699"), (51, 102, 153))

    def test_crop_and_trace_hex_parser_rejects_invalid_values(self):
        module = load_script("color_utils.py")

        with self.assertRaises(argparse.ArgumentTypeError):
            module.parse_hex_color("bad")

    def test_chroma_key_distance_uses_largest_channel_delta(self):
        module = load_script("color_utils.py")

        self.assertEqual(module.channel_distance((0, 255, 0), (0, 240, 10)), 15)
        self.assertEqual(module.channel_distance((10, 20, 30), (40, 10, 30)), 30)

    def test_chroma_key_soft_alpha_bounds(self):
        module = load_script("chroma_alpha.py")

        self.assertEqual(module.alpha_for_distance(0, 12.0, 96.0), 0)
        self.assertEqual(module.alpha_for_distance(120, 12.0, 96.0), 255)
        middle = module.alpha_for_distance(54, 12.0, 96.0)
        self.assertGreater(middle, 0)
        self.assertLess(middle, 255)


if __name__ == "__main__":
    unittest.main()
