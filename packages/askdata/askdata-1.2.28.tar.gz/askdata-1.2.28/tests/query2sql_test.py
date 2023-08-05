from askdata import query2sql
from askdata.smartquery import SmartQuery, Query, Field, Condition, Sorting, SQLSorting, SQLOperator, TimeOperator, \
    BooleanOperator, CompositeCondition

if __name__ == "__main__":

    # # Query2SQL
    smartquery = SmartQuery(
        queries=[
            Query(
                fields=[
                    Field(aggregation="SUM", column="incidents", alias="sum_incidents",
                          internalDataType="NUMERIC",
                          sourceDataType="INT64"),
                    Field(column="customer_name", alias="Customer",
                          internalDataType="STRING",
                          sourceDataType="VARCHAR"),
                    Field(aggregation="YEAR", column="acquired", alias="Acquired Date",
                          internalDataType="DATE",
                          sourceDataType="DATE")
                ],
                where=[
                    CompositeCondition(conditions=[
                        Condition(field=Field(column="customer_name", alias="Customer",
                                              internalDataType="STRING",
                                              sourceDataType="VARCHAR"), operator=SQLOperator.IN,
                                  value=["Franceaco Doe", "Claude Rudolf"]),
                        Condition(field=Field(aggregation="YEAR", column="acquired", alias="Acquired Date",
                                              internalDataType="DATE",
                                              sourceDataType="DATE"), operator=TimeOperator.RANGE,
                                  value=["2018-01-01", "2019-12-31"])
                    ], operator=BooleanOperator.AND)

                ],
                orderBy=[
                    Sorting(field="Acquired Date", order=SQLSorting.DESC)
                ],
                limit=6
            )
        ]
    )

    response = query2sql.query_to_sql(smartquery=smartquery, db_driver="MySQL")
    print(response)

    # Query 2 OLAP
    nl = "list all the revenue by player"
    df = ""
    schema = {
        "SerieA.Revenue": {
            "name":"revenue",
            "synonyms": ["revenues"]
        },
        "SerieA.Player": {
            "name": "player",
            "synonyms": ["players", "soccer player"],
            "example_of_values": ["Cristiano Ronaldo", "Ciro Immobile", "Alessandro del Piero"]
        }
    }
    db_driver = "olap"

    # Function call
    result_nl = query2sql.query_to_olap(nl=nl, df=df, schema=schema, db_driver=db_driver)

    # Print the DataFrame result
    print("Answer: ")
    print(result_nl)
