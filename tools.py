import pandas
import numpy
import matplotlib.pyplot as plt 

class Average:
    def __init__(self, mean: float, total_error: float) -> None:
        self._series = None
        self._errors = []
        self._statistical_error = numpy.nan

        self.mean = mean
        self.total_error = total_error

    @classmethod
    def from_series(cls, series: pandas.Series, errors: list[float] | None = None) -> 'Average':
        mean = series.mean()
        statistical_error = series.sem()
        errors = errors or []

        total_error = numpy.sqrt(statistical_error**2+sum(error**2 for error in errors if errors is not None))

        obj = Average(mean=mean, total_error=total_error)

        obj._series = series
        obj._errors = errors
        obj._statistical_error = statistical_error
        return obj

def add_error_bar(plot: plt.Axes, x: list[Average], y: list[Average], bar_config: dict | None = None):
    x_values, y_values, x_errors, y_errors = [], [], [], []

    for x_avg, y_avg in zip(x, y):
        x_values.append(x_avg.mean)
        y_values.append(y_avg.mean)
        x_errors.append(x_avg.total_error)
        y_errors.append(y_avg.total_error)

    plot.errorbar(
        x=x_values,
        y=y_values,
        xerr=x_errors,
        yerr=y_errors,
        **(bar_config or {})
    )
