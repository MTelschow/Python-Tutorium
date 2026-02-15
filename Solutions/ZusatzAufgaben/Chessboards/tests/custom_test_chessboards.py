import tempfile
import traceback

import pytest

from pytest_nbgrader.cases import execute, format_result


class TestParseChessboard:
    @pytest.fixture
    def test_execution(cls, submission, cases, verbosity) -> tuple:
        """Run student submission on test cases."""
        
        contents = cases.inputs[1].pop('contents')
        filename = cases.inputs[0][0]
        
        with tempfile.NamedTemporaryFile(mode='w+t', suffix=filename) as f:
            f.write(contents)
            f.flush()
            cases.inputs = ((f.name,), cases.inputs[1])
            
            with open(f.name, 'rt') as g:
                print(*g.readlines())
            
            try:
                result = execute(submission, cases)
            except Exception as e:
                if cases.raises:
                    # forward the (expected) exception to be checked
                    result = e
                else:
                    result = pytest.ExitCode.INTERNAL_ERROR
                    limit = (verbosity > 0) - 1
                    exception = traceback.format_exc(limit=limit)
                    pytest.fail(
                        format_result(cases.inputs, result, exception=exception),
                        pytrace=False,
                    )
        return cases, result

    def test_piece_sequence(self, test_execution, verbosity):
        case, result = test_execution
        piece_sequence = str.maketrans({s: None for s in '/12345678'})
        translation_result = result[0][0].translate(piece_sequence)

        assert (translation_result == case.expected[0][0]), f'Error: {translation_result}'
    

    def test_line_breaks(self, test_execution, verbosity):
        case, result = test_execution
        empty = str.maketrans({s: None for s in '12345678'})
        translation_result = list(map(set, result[0][0].translate(empty).split('/')))

        assert (translation_result == case.expected[0][0]), f'Error: {translation_result}'
    
    def test_empty_squares(self, test_execution, verbosity):
        case, result = test_execution
        symbols = str.maketrans({s: '#' for s in 'pnbrqkPNBRQK'} | {'/': None})
        translation_result = result[0][0].translate(symbols)

        assert (translation_result == case.expected[0][0]), f'Error: {translation_result}'
