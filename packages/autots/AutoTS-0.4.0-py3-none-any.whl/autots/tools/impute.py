"""Fill NA."""
# import numpy as np
import pandas as pd


def fill_zero(df):
    """Fill NaN with zero."""
    df = df.fillna(0)
    return df


def fill_forward(df):
    """Fill NaN with previous values."""
    df = df.fillna(method='ffill')
    df = df.fillna(method='bfill').fillna(0)
    return df


def fill_mean(df):
    """Fill NaN with mean."""
    df = df.fillna(df.mean().fillna(0).to_dict())
    return df


def fill_median(df):
    """Fill NaN with median."""
    df = df.fillna(df.median().fillna(0).to_dict())
    return df


def rolling_mean(df, window: int = 10):
    """Fill NaN with mean of last window values."""
    df = fill_forward(df.fillna(df.rolling(window=window, min_periods=1).mean()))
    return df


def biased_ffill(df, mean_weight: float = 1):
    """Fill NaN with average of last value and mean."""
    df_mean = fill_mean(df)
    df_ffill = fill_forward(df)
    df = ((df_mean * mean_weight) + df_ffill) / (1 + mean_weight)
    return df


def fake_date_fill(df, back_method: str = 'slice'):
    """
    Return a dataframe where na values are removed and values shifted forward.

    Warnings:
        Thus, values will have incorrect timestamps!

    Args:
        back_method (str): how to deal with tails left by shifting NaN
            - 'bfill' -back fill the last value
            - 'slice' - drop any rows with any na
            - 'keepna' - keep the lagging na
    """
    df_index = df.index.to_series().copy()
    df2 = df.sort_index(ascending=False).copy()
    df2 = df2.apply(lambda x: pd.Series(x.dropna().values))
    df2 = df2.sort_index(ascending=False)
    df2.index = df_index.tail(len(df2.index))
    df2 = df2.dropna(how='all', axis=0)
    if df2.empty:
        df2 = df.fillna(0)

    if back_method == 'bfill':
        df2 = fill_forward(df2)
        return df
    elif back_method == 'slice':
        thresh = int(df.shape[1] * 0.5)
        thresh = thresh if thresh > 1 else 1
        df3 = df2.dropna(thresh=thresh, axis=0)
        if df3.empty or df3.shape[0] < 8:
            df3 = fill_forward(df2)
        else:
            df3 = fill_forward(df3)
        return df3
    elif back_method == 'keepna':
        return df2
    else:
        print('back_method not recognized in fake_date_fill')
        return df2


df_interpolate = {
    'linear': 0.1,
    'time': 0.1,
    'pad': 0.1,
    'nearest': 0.1,
    'zero': 0.1,
    'quadratic': 0.1,
    'cubic': 0.1,
    'spline': 0.1,
    'barycentric': 0.01,  # this parallelizes and is noticeably slower
    'piecewise_polynomial': 0.01,
    'spline': 0.1,
    'pchip': 0.1,
    'akima': 0.1,
    # these seem to cause more harm than good usually
    'polynomial': 0.0,
    'krogh': 0.0,
    'cubicspline': 0.0,
    'from_derivatives': 0.0,
    'slinear': 0.0,
}
df_interpolate_full = list(df_interpolate.keys())


def FillNA(df, method: str = 'ffill', window: int = 10):
    """Fill NA values using different methods.

    Args:
        method (str):
            'ffill' - fill most recent non-na value forward until another non-na value is reached
            'zero' - fill with zero. Useful for sales and other data where NA does usually mean $0.
            'mean' - fill all missing values with the series' overall average value
            'median' - fill all missing values with the series' overall median value
            'rolling mean' - fill with last n (window) values
            'ffill mean biased' - simple avg of ffill and mean
            'fake date' - shifts forward data over nan, thus values will have incorrect timestamps
            also most `method` values of pd.DataFrame.interpolate()
        window (int): length of rolling windows for filling na, for rolling methods
    """
    method = str(method).replace(" ", "_")

    if method == 'zero':
        return fill_zero(df)

    elif method == 'ffill':
        return fill_forward(df)

    elif method == 'mean':
        return fill_mean(df)

    elif method == 'median':
        return fill_median(df)

    elif method == 'rolling_mean':
        return rolling_mean(df, window=window)

    elif method == 'rolling_mean_24':
        return rolling_mean(df, window=24)

    elif method == 'ffill_mean_biased':
        return biased_ffill(df)

    elif method == 'fake_date':
        return fake_date_fill(df, back_method='slice')

    elif method in df_interpolate_full:
        df = df.interpolate(method=method, order=5).fillna(method='bfill')
        if df.isnull().values.any():
            df = fill_forward(df)
        return df

    elif method == 'IterativeImputer':
        cols = df.columns
        indx = df.index
        try:
            from sklearn.experimental import enable_iterative_imputer  # noqa
        except Exception:
            pass
        from sklearn.impute import IterativeImputer

        df = IterativeImputer(random_state=0, max_iter=100).fit_transform(df)
        if not isinstance(df, pd.DataFrame):
            df = pd.DataFrame(df)
            df.index = indx
            df.columns = cols
        return df

    elif method == 'IterativeImputerExtraTrees':
        cols = df.columns
        indx = df.index
        try:
            from sklearn.experimental import enable_iterative_imputer  # noqa
        except Exception:
            pass
        from sklearn.ensemble import ExtraTreesRegressor
        from sklearn.impute import IterativeImputer

        df = IterativeImputer(
            ExtraTreesRegressor(n_estimators=10, random_state=0),
            random_state=0,
            max_iter=100,
        ).fit_transform(df)
        if not isinstance(df, pd.DataFrame):
            df = pd.DataFrame(df)
            df.index = indx
            df.columns = cols
        return df

    elif method == 'KNNImputer':
        cols = df.columns
        indx = df.index
        from sklearn.impute import KNNImputer

        df = KNNImputer(n_neighbors=5).fit_transform(df)
        if not isinstance(df, pd.DataFrame):
            df = pd.DataFrame(df)
            df.index = indx
            df.columns = cols
        return df

    elif method is None or method == 'None':
        return df

    else:
        print(f"FillNA method `{str(method)}` not known, returning original")
        return df
