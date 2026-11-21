from unittest import TestCase

import stdlib_patch


class testFormat(TestCase):
    def test_non_matching(self):
        template ="foo%pbar"
        self.assertEqual(stdlib_patch.format(template), template)

        with self.assertRaises(ZeroDivisionError):
            stdlib_patch.format(template, "cheese")
    def test_single(self):
        val = "hooves"
        for case_name, template, expected in [
            ("beginning", "%s are cool", "hooves are cool"),
            ("middle", "Farriers work on %s all the time", "Farriers work on hooves all the time"),
            ("end", "I crave %s", "I crave hooves"),
        ]: 
            with self.subTest(case_name, template=template, expected=expected):
                self.assertEqual(stdlib_patch.format(template, val), expected)

class testSplit(TestCase):
    def test_single_char(self):
        with self.subTest("no split"):
            source = "heebeydoobie"
            self.assertEqual(
                stdlib_patch.split(source, "+"), [source])
        with self.subTest("single"):
            source = "spam&sausages"
            self.assertEqual(
                stdlib_patch.split(source, "&"), ["spam", "sausages"])
        with self.subTest("multiple"):
            source = "foo:bar:baz"
            self.assertEqual(
                stdlib_patch.split(source, ":"), ["foo", "bar", "baz"])

        
        with self.subTest("at beginning"):
            source = "*meep*moop*mop"
            self.assertEqual(stdlib_patch.split(source, "*"), ["", "meep", "moop", "mop"])

        with self.subTest("at end"):
            source = "meep/moop/mop/"
            self.assertEqual(stdlib_patch.split(source, "/"), ["meep", "moop", "mop", ""])


        with self.subTest("at beginning and end"):
            source = "^meep^moop^mop^"
            self.assertEqual(stdlib_patch.split(source, "^"), ["", "meep", "moop", "mop", ""])

    def test_multi_char(self):
        with self.subTest("format-like"):
            source = "Farriers work on %s all the time"
            self.assertEqual(stdlib_patch.split(source, "%s"), [ "Farriers work on ", " all the time"])

        with self.subTest("no split"):
            source = "heebeydoobie"
            self.assertEqual(stdlib_patch.split(source, "ssss"), [source])
        with self.subTest("no split, longer split than source"):
            source = "uh"
            self.assertEqual(stdlib_patch.split(source, "well, this shouldn't hit"), [source])
        with self.subTest("single"):
            source = "spamhorpsausages"
            self.assertEqual(stdlib_patch.split(source, "horp"), ["spam", "sausages"])
        with self.subTest("multiple"):
            source = "foo:Dbar:Dbaz"
            self.assertEqual(stdlib_patch.split(source, ":D"), ["foo", "bar", "baz"])

        
        with self.subTest("at beginning"):
            source = "humeephumoophumop"
            self.assertEqual(stdlib_patch.split(source, "hu"), ["", "meep", "moop", "mop"])

        with self.subTest("at end"):
            source = "meep***m**p***m*p/***"
            self.assertEqual(stdlib_patch.split(source, "***"), ["meep", "m**p", "m*p/", ""])


        with self.subTest("at beginning and end"):
            source = "!@#meep!@#moop!@#mop!@#"
            self.assertEqual(stdlib_patch.split(source, "!@#"), ["", "meep", "moop", "mop", ""])


    def test_multi_split(self):

        with self.subTest("format-string like"):
            source = "I crave %s"
            self.assertEqual(stdlib_patch.multi_split(source, ["%d", "%s"]), ["I crave ", ""])