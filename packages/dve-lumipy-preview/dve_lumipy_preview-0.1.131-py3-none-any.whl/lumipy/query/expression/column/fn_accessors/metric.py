from lumipy.query.expression.column.column_base import BaseColumnExpression
from lumipy.query.expression.column_op.aggregation_op import (
    MeanSquaredError, MeanAbsoluteError, MeanFractionalAbsoluteError
)


class MetricColumnFunctionAccessor:
    """MetricColumnFunctionAccessor contains a collection of metrics and statistical similarity measures between the
    expression and another column expression. These are all aggregate functions that map two columns of data to a single
    value.

    This and the other accessor classes behave like a namespace and keep the different column methods organised.

    They are presented as methods on an accessor attribute in each column class inheritor instance analogous to the
    string and datetime accessor methods in pandas, e.g
    https://pandas.pydata.org/pandas-docs/stable/reference/series.html#api-series-dt

    Try hitting tab to see what functions you can use.
    """

    def __init__(self, x):
        self.__x = x

    def mean_squared_error(self, y: BaseColumnExpression) -> MeanSquaredError:
        """Apply a mean squared error calculation to this expression and another.

        Args:
            y (BaseColumnExpression): an expression corresponding to the other series.

        Returns:
            MeanSquaredError: a MeanSquaredError instance representing the mean square error metric calculation.
        """
        return MeanSquaredError(self.__x, y)

    def mean_absolute_error(self, y: BaseColumnExpression) -> MeanAbsoluteError:
        """Apply a mean absolute error calculation to this expression and another.

        Args:
            y (BaseColumnExpression): an expression corresponding to the other series.

        Returns:
            MeanAbsoluteError: a MeanAbsoluteError instance representing the mean absolute error metric calculation.
        """
        return MeanAbsoluteError(self.__x, y)

    def mean_fractional_absolute_error(self, y: BaseColumnExpression) -> MeanFractionalAbsoluteError:
        """Apply a mean fractional absolute error calculation to this expression and another.

        Args:
            y (BaseColumnExpression): an expression corresponding to the other series.

        Returns:
            MeanFractionalAbsoluteError: a MeanAbsoluteFractionalError instance representing the mean fractional
            absolute error calculation.
        """
        return MeanFractionalAbsoluteError(self.__x, y)
