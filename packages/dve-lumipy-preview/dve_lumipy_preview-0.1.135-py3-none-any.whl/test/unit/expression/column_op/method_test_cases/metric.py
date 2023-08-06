metric_method_cases_happy = {
    'column.metric.mean_squared_error(column)': (
        lambda x, y: x.metric.mean_squared_error(x),
        lambda x, y: f"mean_squared_error({x.get_sql()}, {x.get_sql()})"
    ),
    'column.metric.mean_absolute_error(column)': (
        lambda x, y: x.metric.mean_absolute_error(x),
        lambda x, y: f"mean_absolute_error({x.get_sql()}, {x.get_sql()})"
    ),
    'column.metric.mean_fractional_error(column)': (
        lambda x, y: x.metric.mean_fractional_absolute_error(x),
        lambda x, y: f"mean_fractional_absolute_error({x.get_sql()}, {x.get_sql()})"
    ),
}
