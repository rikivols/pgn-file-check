import unittest
import check_tag_syntax
import check_move_syntax


class TestTagSyntax(unittest.TestCase):

    def test_all_tags_ok(self):

        message = "Wrong execution of testing tags function, when there are optional tags"
        inp = ['[Event "F/S Return Match"]', '[Site "Belgrade, Serbia JUG"]', '[Date "1992.11.04"]', '[Round "29"]',
               '[White "Fischer, Robert J."]', '[Black "Spassky, Boris V."]', '[Result "1/2-1/2"]', '[ECO "E35"]']
        result = check_tag_syntax.check_tag_syntax(inp)
        self.assertEqual('1/2-1/2', result, message)

        # --------------------------------------------------------------------------------------------------

        message = "Wrong execution of testing tags function, when there are only basic tags"
        inp = ['[Event "F/S Return Match"]', '[Site "Belgrade, Serbia JUG"]', '[Date "1992.11.04"]', '[Round "29"]',
               '[White "Fischer, Robert J."]', '[Black "Spassky, Boris V."]', '[Result "1/2-1/2"]']
        result = check_tag_syntax.check_tag_syntax(inp)
        self.assertEqual('1/2-1/2', result, message)

    def test_missing_all_tags(self):

        with self.assertRaises(SystemExit):
            check_tag_syntax.check_tag_syntax([''])

    def test_missing_first_tag(self):

        with self.assertRaises(SystemExit):
            inp = ['[Site "Belgrade, Serbia JUG"]', '[Date "1992.11.04"]', '[Round "29"]',
                   '[White "Fischer, Robert J."]', '[Black "Spassky, Boris V."]', '[Result "1/2-1/2"]', '[ECO "E35"]']
            check_tag_syntax.check_tag_syntax(inp)

    def test_missing_tags(self):

        with self.assertRaises(SystemExit):
            # missing second tag (Site)
            inp = ['[Event "F/S Return Match"]', '[Date "1992.11.04"]', '[Round "29"]', '[White "Fischer, Robert J."]',
                   '[Black "Spassky, Boris V."]', '[Result "1/2-1/2"]', '[ECO "E35"]']
            check_tag_syntax.check_tag_syntax(inp)

        with self.assertRaises(SystemExit):
            # missing date tag
            inp = ['[Event "F/S Return Match"]', '[Site "Belgrade, Serbia JUG"]', '[Round "29"]',
                   '[White "Fischer, Robert J."]', '[Black "Spassky, Boris V."]', '[Result "1/2-1/2"]', '[ECO "E35"]']
            check_tag_syntax.check_tag_syntax(inp)

        with self.assertRaises(SystemExit):
            # missing result (last tag)
            inp = ['[Event "F/S Return Match"]', '[Site "Belgrade, Serbia JUG"]', '[Date "1992.11.04"]', '[Round "29"]',
                   '[White "Fischer, Robert J."]', '[Black "Spassky, Boris V."]']
            check_tag_syntax.check_tag_syntax(inp)

    def test_bad_enclosing_of_tags(self):

        with self.assertRaises(SystemExit):
            # bad start of 1st tag
            inp = ['Event "F/S Return Match"]', '[Site "Belgrade, Serbia JUG"]', '[Date "1992.11.04"]', '[Round "29"]',
                   '[White "Fischer, Robert J."]', '[Black "Spassky, Boris V."]', '[Result "1/2-1/2"]', '[ECO "E35"]']
            check_tag_syntax.check_tag_syntax(inp)

        with self.assertRaises(SystemExit):
            # date tag has no brackets
            inp = ['[Event "F/S Return Match"]', '[Site "Belgrade, Serbia JUG"]', 'Date "1992.11.04"', '[Round "29"]',
                   '[White "Fischer, Robert J."]', '[Black "Spassky, Boris V."]', '[Result "1/2-1/2"]', '[ECO "E35"]']
            check_tag_syntax.check_tag_syntax(inp)

        with self.assertRaises(SystemExit):
            # result has no ending
            inp = ['[Event "F/S Return Match"]', '[Site "Belgrade, Serbia JUG"]', '[Date "1992.11.04"]', '[Round "29"]',
                   '[White "Fischer, Robert J."]', '[Black "Spassky, Boris V."]', '[Result "1/2-1/2"', '[ECO "E35"]']
            check_tag_syntax.check_tag_syntax(inp)

        with self.assertRaises(SystemExit):
            # result has one space more at the end
            inp = ['[Event "F/S Return Match"]', '[Site "Belgrade, Serbia JUG"]', '[Date "1992.11.04"]', '[Round "29"]',
                   '[White "Fischer, Robert J."]', '[Black "Spassky, Boris V."]', '[Result "1/2-1/2" ]', '[ECO "E35"]']
            check_tag_syntax.check_tag_syntax(inp)

        with self.assertRaises(SystemExit):
            # event has space more at start
            inp = ['[ Event "F/S Return Match"]', '[Site "Belgrade, Serbia JUG"]', '[Date "1992.11.04"]',
                   '[Round "29"]', '[White "Fischer, Robert J."]', '[Black "Spassky, Boris V."]', '[Result "1/2-1/2"]',
                   '[ECO "E35"]']
            check_tag_syntax.check_tag_syntax(inp)

    def test_bad_enclosing_of_optional_tag(self):

        with self.assertRaises(SystemExit):
            # optional tag space more at start
            inp = ['[Event "F/S Return Match"]', '[Site "Belgrade, Serbia JUG"]', '[Date "1992.11.04"]', '[Round "29"]',
                   '[White "Fischer, Robert J."]', '[Black "Spassky, Boris V."]', '[Result "1/2-1/2"]', '[ ECO "E35"]']
            check_tag_syntax.check_tag_syntax(inp)

        with self.assertRaises(SystemExit):
            # optional tag space more at end
            inp = ['[Event "F/S Return Match"]', '[Site "Belgrade, Serbia JUG"]', '[Date "1992.11.04"]', '[Round "29"]',
                   '[White "Fischer, Robert J."]', '[Black "Spassky, Boris V."]', '[Result "1/2-1/2"]', '[ECO "E35" ]']
            check_tag_syntax.check_tag_syntax(inp)

        with self.assertRaises(SystemExit):
            # optional tag space has no start
            inp = ['[Event "F/S Return Match"]', '[Site "Belgrade, Serbia JUG"]', '[Date "1992.11.04"]', '[Round "29"]',
                   '[White "Fischer, Robert J."]', '[Black "Spassky, Boris V."]', '[Result "1/2-1/2"]', 'ECO "E35"]']
            check_tag_syntax.check_tag_syntax(inp)

        with self.assertRaises(SystemExit):
            # optional tag space has no end
            inp = ['[Event "F/S Return Match"]', '[Site "Belgrade, Serbia JUG"]', '[Date "1992.11.04"]', '[Round "29"]',
                   '[White "Fischer, Robert J."]', '[Black "Spassky, Boris V."]', '[Result "1/2-1/2"]', '[ECO "E35"']
            check_tag_syntax.check_tag_syntax(inp)

    def test_ignoring_if_not_tags_in_end(self):

        # optional tag space has no start, no end
        inp = ['[Event "F/S Return Match"]', '[Site "Belgrade, Serbia JUG"]', '[Date "1992.11.04"]', '[Round "29"]',
               '[White "Fischer, Robert J."]', '[Black "Spassky, Boris V."]', '[Result "1/2-1/2"]', 'ECO "E35"']
        self.assertEqual('1/2-1/2', check_tag_syntax.check_tag_syntax(inp))

    def test_bad_content(self):

        with self.assertRaises(SystemExit):
            # missing "
            inp = ['[Event "F/S Return Match]', '[Site "Belgrade, Serbia JUG"]', '[Date "1992.11.04"]', '[Round "29"]',
                   '[White "Fischer, Robert J."]', '[Black "Spassky, Boris V."]', '[Result "1/2-1/2"]', '[ECO "E35"]']
            check_tag_syntax.check_tag_syntax(inp)

    def test_empty_content(self):

        message = "Empty content event"
        inp = ['[Event ""]', '[Site "Belgrade, Serbia JUG"]', '[Date "1992.11.04"]', '[Round "29"]',
               '[White "Fischer, Robert J."]', '[Black "Spassky, Boris V."]', '[Result "1-0"]', '[ECO "E35"]']
        self.assertEqual('1-0', check_tag_syntax.check_tag_syntax(inp), message)

    def test_tags_wrong_order(self):

        with self.assertRaises(SystemExit):
            # missing "
            inp = ['[Event "F/S Return Match"]', '[Date "1992.11.04"]', '[Site "Belgrade, Serbia JUG"]', '[Round "29"]',
                   '[White "Fischer, Robert J."]', '[Black "Spassky, Boris V."]', '[Result "1/2-1/2"]', '[ECO "E35"]']
            check_tag_syntax.check_tag_syntax(inp)

    def test_bad_date_format(self):

        self.assertEqual(False, check_tag_syntax.is_date_tag_ok("1999.13.08"))
        self.assertEqual(False, check_tag_syntax.is_date_tag_ok("-1999.12.08"))
        self.assertEqual(False, check_tag_syntax.is_date_tag_ok("199913.08"))
        self.assertEqual(False, check_tag_syntax.is_date_tag_ok("1999.13.08."))
        self.assertEqual(False, check_tag_syntax.is_date_tag_ok("a.13.08."))

    """ ------------ """


class TestMoveSyntax(unittest.TestCase):

    def test_short_pawn_moves_ok(self):

        result = check_move_syntax.Move('e4').move
        self.assertEqual("e4", result)

        result = check_move_syntax.Move('f8').move
        self.assertEqual("f8", result)

        result = check_move_syntax.Move('a1').move
        self.assertEqual("a1", result)

        result = check_move_syntax.Move('h8').move
        self.assertEqual("h8", result)

        result = check_move_syntax.Move('Ph8').move
        self.assertEqual("h8", result)

    def test_long_pawn_moves_that_should_be_shorten_ok(self):

        result = check_move_syntax.Move('ee4').move
        self.assertEqual('e4', result)

        message = "Pawn move by 2 up"
        result = check_move_syntax.Move('a2a4').move
        self.assertEqual('a4', result, message)

        message = "Pawn move by 2 down"
        result = check_move_syntax.Move('g7g5').move
        self.assertEqual('g5', result, message)

        message = "Pawn move by 1 long"
        result = check_move_syntax.Move('g7g6').move
        self.assertEqual('g6', result, message)

        message = "Pawn move by 1 long"
        result = check_move_syntax.Move('a4a5').move
        self.assertEqual('a5', result, message)

    def test_pawn_takings_short_ok(self):

        result = check_move_syntax.Move('exf5').move
        self.assertEqual('exf5', result)

        result = check_move_syntax.Move('cxb5').move
        self.assertEqual('cxb5', result)

    def test_pawn_takings_long_should_be_shorten_ok(self):

        result = check_move_syntax.Move('e4xf5').move
        self.assertEqual('exf5', result)

        result = check_move_syntax.Move('c7xb8').move
        self.assertEqual('cxb8', result)

    def test_check_move_mate(self):

        result = check_move_syntax.Move('e4xf5#').move
        self.assertEqual('exf5#', result)

        result = check_move_syntax.Move('e4x#f5').move
        self.assertEqual('', result)

    def test_check_move_check(self):

        result = check_move_syntax.Move('cxb5+').move
        self.assertEqual('cxb5+', result)

        result = check_move_syntax.Move('c+xb5').move
        self.assertEqual('', result)

    def test_check_move_check_and_mate(self):

        result = check_move_syntax.Move('b2b4+#').move
        self.assertEqual('b4+#', result)

        result = check_move_syntax.Move('b+#2b4').move
        self.assertEqual('', result)

    def test_pawn_short_moves_wrong(self):

        result = check_move_syntax.Move('b9').move
        self.assertEqual('', result)

        result = check_move_syntax.Move('b0').move
        self.assertEqual('', result)

        result = check_move_syntax.Move('A4').move
        self.assertEqual('', result)

        result = check_move_syntax.Move('q8').move
        self.assertEqual('', result)

        result = check_move_syntax.Move('f9').move
        self.assertEqual('', result)

    def test_pawn_long_moves_wrong(self):

        result = check_move_syntax.Move('ba4').move
        self.assertEqual('', result)

        result = check_move_syntax.Move('bb9').move
        self.assertEqual('', result)

        result = check_move_syntax.Move('b3b5').move
        self.assertEqual('', result)

        result = check_move_syntax.Move('i7i5').move
        self.assertEqual('', result)

    def test_pawn_taking_wrong(self):

        result = check_move_syntax.Move('e4xf6').move
        self.assertEqual('', result)

        result = check_move_syntax.Move('c7xb1').move
        self.assertEqual('', result)

        result = check_move_syntax.Move('cx1b2').move
        self.assertEqual('', result)

    def test_piece_move_ok(self):

        result = check_move_syntax.Move('Bb1').move
        self.assertEqual('Bb1', result)

        result = check_move_syntax.Move('Nh8').move
        self.assertEqual('Nh8', result)

        result = check_move_syntax.Move('Kf4').move
        self.assertEqual('Kf4', result)

        result = check_move_syntax.Move('Bcb1').move
        self.assertEqual('Bcb1', result)

        result = check_move_syntax.Move('Rcf4').move
        self.assertEqual('Rcf4', result)

        result = check_move_syntax.Move('Qc1d2').move
        self.assertEqual('Qc1d2', result)

    def test_piece_move_wrong(self):

        result = check_move_syntax.Move('Bb9').move
        self.assertEqual('', result)

        result = check_move_syntax.Move('Wh8').move
        self.assertEqual('', result)

        result = check_move_syntax.Move('Kr4').move
        self.assertEqual('', result)

        result = check_move_syntax.Move('Bcr1').move
        self.assertEqual('', result)

        result = check_move_syntax.Move('R4cf').move
        self.assertEqual('', result)

        result = check_move_syntax.Move('Qc1d28').move
        self.assertEqual('', result)

        result = check_move_syntax.Move('####').move
        self.assertEqual('', result)

    def test_castle(self):

        result = check_move_syntax.Move('O-O+').move
        self.assertEqual('O-O+', result)

        result = check_move_syntax.Move('O-O-O').move
        self.assertEqual('O-O-O', result)

        result = check_move_syntax.Move('O-O-O+#').move
        self.assertEqual('O-O-O+#', result)





if __name__ == '__main__':
    # please run in console like this: python test_ugen.py -b (-b to ignore printing)
    unittest.main(buffer=True)
