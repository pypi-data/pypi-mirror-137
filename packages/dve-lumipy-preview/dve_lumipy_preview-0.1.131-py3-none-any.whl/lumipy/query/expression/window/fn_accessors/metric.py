from .base import BaseWindowFunctionAccessor
from ..function import WindowAggregate
from ...column.column_base import BaseColumnExpression


class MetricWindowFunctionAccessor(BaseWindowFunctionAccessor):
    """MetricWindowFunctionAccessor contains a collection of metrics and statistical similarity measures between the
    expression and another column expression applied in a window. These are all aggregate functions that map two columns
    of data to a single value.

    This and the other accessor classes behave like a namespace and keep the different window methods organised.

    They are presented as methods on an accessor attribute in each column class inheritor instance analogous to the
    string and datetime accessor methods in pandas, e.g
    https://pandas.pydata.org/pandas-docs/stable/reference/series.html#api-series-dt

    Try hitting tab to see what functions you can use.
    """

    def mean_squared_error(self, x: BaseColumnExpression, y: BaseColumnExpression) -> WindowAggregate:
        """Apply a mean squared error calculation in this window to the given expressions.

        Args:
            x (BaseColumnExpression): an expression corresponding to the first series.
            y (BaseColumnExpression): an expression corresponding to the second series.

        Returns:
            WindowAggregate: a WindowAggregate instance representing the mean square error metric calculation.
        """
        return self._apply(x.metric.mean_squared_error(y))

    def mean_absolute_error(self, x: BaseColumnExpression, y: BaseColumnExpression) -> WindowAggregate:
        """Apply a mean absolute error calculation in this window to the given expressions.

        Args:
            x (BaseColumnExpression): an expression corresponding to the first series.
            y (BaseColumnExpression): an expression corresponding to the second series.

        Returns:
            WindowAggregate: a WindowAggregate instance representing the mean absolute error metric calculation.
        """
        return self._apply(x.metric.mean_absolute_error(y))

    def mean_fractional_absolute_error(self, x: BaseColumnExpression, y: BaseColumnExpression) -> WindowAggregate:
        """Apply a mean fractional absolute error calculation in this window to the given expressions.

        Args:
            x (BaseColumnExpression): an expression corresponding to the first series.
            y (BaseColumnExpression): an expression corresponding to the second series.

        Returns:
            WindowAggregate: a MeanAbsoluteFractionalError instance representing the mean fractional absolute error
            calculation.
        """
        return self._apply(x.metric.mean_fractional_absolute_error(y))
