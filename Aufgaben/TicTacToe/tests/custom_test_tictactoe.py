import tempfile
import traceback

import pytest

from pytest_nbgrader.cases import execute, format_result


class TestParseTictactoe:
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

    def test_valid_boards(self, test_execution, verbosity):
        case, result = test_execution
        assert case.expected == result[:-1]
    
    def test_invalid_boards(self, test_execution, verbosity):
        case, result = test_execution

        if case.raises:
            assert isinstance(result, Exception)
        else:
            assert not isinstance(result, Exception)
