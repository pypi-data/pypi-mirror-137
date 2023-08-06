from askdata import complex_query_calculator

if __name__ == "__main__":
    dialect = "MySQL"
    instruction = "difference between PURCHASE_DATE (date) and INVOICE_DATE (date)"

    # Complex field
    res = complex_query_calculator.complex_field_calculator(instruction=instruction, dialect=dialect)
    print(res)

    # Complex filter
    res = complex_query_calculator.complex_filter_calculator(instruction=instruction, dialect=dialect)
    print(res)

    # Smartjoin
    tables = {
        "table_left":
            {
                "columns": [
                    {"label": "person ID", "type": "numeric"},
                    {"label": "name", "type": "string"},
                    {"label": "surname", "type": "string"},
                    {"label": "work name", "type": "string"},
                    {"label": "salary", "type": "numeric"},
                    {"label": "city ID", "type": "string"}
                ],
                "values": [
                    ["10", "Francesco", "De Gaio", "engineer", "3000", "NA"],
                    ["22", "Giacomo", "Martin", "employer", "1300", "BO"],
                    ["43", "Luigia", "Mazzi", "chef", "1400", "CA"],
                    ["90", "Martina", "Di Giuseppe", "doctor", "2500", "RM"],
                    ["3", "Rindina", "Dindi", "butcher", "1200", "CT"]
                ]
            },
        "table_right":
            {
                "columns":
                    [
                        {"label": "city", "type": "string"},
                        {"label": "state id", "type": "numeric"},
                        {"label": "population number", "type": "numeric"}
                    ],
                "values":
                    [
                        ["RM", "01", "10101"],
                        ["RI", "04", "93727"],
                        ["PL", "12", "2917283"],
                        ["NA", "01", "9172648"],
                        ["ML", "01", "2818"]
                    ]
            }
    }
    res = complex_query_calculator.smartjoin(tables=tables)
    print(res)
