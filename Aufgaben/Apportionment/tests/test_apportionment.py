from collections.abc import Container

class TestInput:

    def test_type(self, submission, cases, verbosity):
        assert isinstance(submission, dict), 'Es soll sich um ein Dictionary handeln.'

    def test_length(self, submission, cases, verbosity):
        example = cases.inputs[0][1]
        assert len(example) == len(submission), 'Das Dictionary hat die falsche Anzahl Einträge.'

    def test_key_type(self, submission, cases, verbosity):
        for value in submission:
            assert isinstance(value, str), f'Der Schlüssel {value} ist kein String.'

    def test_value_type(self, submission, cases, verbosity):
        for key, value in submission.items():
            assert isinstance(value, int), f'Der Wert {value} zum Schlüssel {key} ist kein Integer.'
    
    def test_dictionary(self, submission, cases, verbosity):
        example = cases.inputs[0][1]
        assert submission == example, f'Das Dictionary ist nicht korrekt.'

class TestResult:

    def test_return_quantity(self, submission, cases, verbosity):
        args, kwargs = cases.inputs[0]
        return_tuple = submission(args, kwargs)
        assert len(return_tuple) == 2, "Es sollen genau zwei Objekte zurückgegeben werden."

    def test_return_first_type(self, submission, cases, verbosity):
        args, kwargs = cases.inputs[0]
        return_tuple = submission(args, kwargs)
        seats, lots = return_tuple
        assert isinstance(seats, dict), "Das erste Rückgabeobjekt soll das Dictionary mit der Sitzverteilung sein."

    def test_return_first_type_key(self, submission, cases, verbosity):
        args, kwargs = cases.inputs[0]
        return_tuple = submission(args, kwargs)
        seats, lots = return_tuple
        for key, value in seats.items():
            assert isinstance(key, str), f"Warum ist der key {key} kein String?"

    def test_return_first_type_value(self, submission, cases, verbosity):
        args, kwargs = cases.inputs[0]
        return_tuple = submission(args, kwargs)
        seats, lots = return_tuple
        for key, value in seats.items():
            assert isinstance(value, int), f"Warum ist der Wert zum key {key} kein Integer?"

    def test_return_second_type_container(self, submission, cases, verbosity):
        args, kwargs = cases.inputs[0]
        return_tuple = submission(args, kwargs)
        seats, lots = return_tuple
        assert isinstance(lots, Container | None), "Das zweite Rückgabeobjekt soll das Set mit den Parteien sein, die an der Losverteilung teilnehmen."

    def test_return_second_type(self, submission, cases, verbosity):
        args, kwargs = cases.inputs[0]
        return_tuple = submission(args, kwargs)
        seats, lots = return_tuple
        assert isinstance(lots, set | None), "Das zweite Rückgabeobjekt soll das Set mit den Parteien sein, die an der Losverteilung teilnehmen."

    def test_return_second_type_values(self, submission, cases, verbosity):
        args, kwargs = cases.inputs[0]
        return_tuple = submission(args, kwargs)
        seats, lots = return_tuple
        if lots:
            for key in lots:
                assert isinstance(key, str), f"Warum ist der key {key} kein String?"
        
    def test_dictionary_length(self, submission, cases, verbosity):
        args, kwargs = cases.inputs[0]
        return_tuple = submission(args, kwargs)
        seats, lots = return_tuple
        solution_seats, solution_lots = cases.expected[0][0]
        assert len(seats) == len(solution_seats), 'Das ausgegebene Dictionary mit der Sitzverteilung hat nicht die korrekte Länge'
    
    def test_dictionary_keys(self, submission, cases, verbosity):
        args, kwargs = cases.inputs[0]
        return_tuple = submission(args, kwargs)
        seats, lots = return_tuple
        solution_seats, solution_lots = cases.expected[0][0]
        assert seats.keys() == solution_seats.keys(), 'Das ausgegebene Dictionary mit der Sitzverteilung ist nicht korrekt'
    
    def test_dictionary_complete(self, submission, cases, verbosity):
        args, kwargs = cases.inputs[0]
        return_tuple = submission(args, kwargs)
        seats, lots = return_tuple
        solution_seats, solution_lots = cases.expected[0][0]
        assert seats == solution_seats, 'Das ausgegebene Dictionary mit der Sitzverteilung ist nicht korrekt'

    def test_set_length(self, submission, cases, verbosity):
        args, kwargs = cases.inputs[0]
        return_tuple = submission(args, kwargs)
        seats, lots = return_tuple
        solution_seats, solution_lots = cases.expected[0][0]
        if lots:
            assert len(lots) == (len(solution_lots) if solution_lots else 0), 'Das ausgegebene Set mit den Parteien, die am Losverfahren teilnehmen hat die falsche Anzahl Einträge'
    
    def test_set_complete(self, submission, cases, verbosity):
        args, kwargs = cases.inputs[0]
        return_tuple = submission(args, kwargs)
        seats, lots = return_tuple
        solution_seats, solution_lots = cases.expected[0][0]
        if not solution_lots:
            assert lots in (tuple(), list(), set(), None), 'Das ausgegebene Set mit den Parteien, die am Losverfahren teilnehmen ist nicht korrekt'    
        else: 
            assert set(lots) == solution_lots, 'Das ausgegebene Set mit den Parteien, die am Losverfahren teilnehmen ist nicht korrekt'

class TestMinimum:

    def test_minimum(self, submission, cases, verbosity):
        args, kwargs = cases.inputs[0]
        return_tuple = submission(args, kwargs)
        seats, lots = return_tuple
        minimum_seats = cases.expected[0][0]
        for key, value in seats.items():
            assert value >= minimum_seats[key], f'Die Partei {key} erhält weniger Sitze als ihr nach der Grundverteilung zustehen.'

