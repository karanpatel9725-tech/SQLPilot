few_shots = [
    {
        "Question": "How many small size t-shirts do we have of Nike brand?",
        "SQLQuery": "SELECT SUM(stock_quantity) FROM t_shirts WHERE brand = 'Nike' AND size = 'S';",
        "SQLResult": "Result of this SQL query",
        "Answer": "178"
    },
    {
        "Question": "If we sell all Levi's t-shirts today, how much revenue will we generate?",
        "SQLQuery": "SELECT SUM(price * stock_quantity) FROM t_shirts WHERE brand='Levi';",
        "SQLResult": "Result of the SQL query",
        "Answer": "876.600000"
    },
    {
        "Question": "How much total revenue will we generate after applying discounts on all t-shirts?",
        "SQLQuery": "SELECT SUM(T1.price * T1.stock_quantity * (1 - IFNULL(T2.pct_discount,0)/100)) FROM t_shirts AS T1 LEFT JOIN discounts AS T2 ON T1.t_shirt_id = T2.t_shirt_id;",
        "SQLResult": "Result of the SQL query",
        "Answer": "13730.000000"
    },
    {
        "Question": "How many t-shirts do not have any discount applied?",
        "SQLQuery": "SELECT COUNT(*) FROM t_shirts WHERE t_shirt_id NOT IN (SELECT t_shirt_id FROM discounts);",
        "SQLResult": "Result of the SQL query",
        "Answer": "70"
    },
    {
        "Question": "Find the total discounted revenue for each brand.",
        "SQLQuery": "SELECT T1.brand, SUM(T1.price * T1.stock_quantity * (1 - IFNULL(T2.pct_discount,0)/100)) AS total_revenue FROM t_shirts AS T1 LEFT JOIN discounts AS T2 ON T1.t_shirt_id = T2.t_shirt_id GROUP BY T1.brand ORDER BY total_revenue DESC;",
        "SQLResult": "Result of the SQL query",
        "Answer": "[('Levi', '876.600000'), ('Nike', '6911.300000'), ('Van Huesen', '5942.100000')]"
}
]




clean_metadata = [
    {
        "Question": fs["Question"],
        "SQLQuery": fs["SQLQuery"],
        "SQLResult": fs["SQLResult"],
        "Answer": str(fs["Answer"])
    }
    for fs in few_shots
]