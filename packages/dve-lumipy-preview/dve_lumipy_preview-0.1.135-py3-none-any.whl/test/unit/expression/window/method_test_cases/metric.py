metric_method_cases = {
    'window.metric.mean_squared_error': (
        lambda w, x, y: w.metric.mean_squared_error(x, y),
        lambda w, x, y: f"mean_squared_error({x.get_sql()}, {y.get_sql()}) {w.get_sql()}"
    ),
    'window.metric.mean_absolute_error': (
        lambda w, x, y: w.metric.mean_absolute_error(x, y),
        lambda w, x, y: f"mean_absolute_error({x.get_sql()}, {y.get_sql()}) {w.get_sql()}"
    ),
    'window.metric.mean_fractional_absolute_error': (
        lambda w, x, y: w.metric.mean_fractional_absolute_error(x, y),
        lambda w, x, y: f"mean_fractional_absolute_error({x.get_sql()}, {y.get_sql()}) {w.get_sql()}"
    ),
}