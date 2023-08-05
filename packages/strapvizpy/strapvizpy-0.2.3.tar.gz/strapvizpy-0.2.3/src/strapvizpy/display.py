import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from strapvizpy.bootstrap import calculate_boot_stats


def plot_ci(sample, rep, bin_size=30, estimator="mean" ,n="auto", level=0.95,
            random_seed=None, title="", y_axis="Count", path=None):
    
    """Makes a histogram of a boostrapped sampling distribution 
    with its confidence interval and oberserved mean.
     
    Parameters
    ----------
    sample : list or numpy.ndarray or pandas.core.series.Series 
        sample to bootstrap
    rep : int
        number of replicates of the distribution
    bin_size = int
        a number of bins representing intervals of equal size
        over the range
    estimator: {"mean", "median", "var", "sd"}
        sampling distributor's estimator
    n : str or int, default="auto"
        bootstrap sample size, "auto" specifies using the
        same size as the sample
    level : float, default=0.95
        confidence level
    random_seed : None or int, default=None
        seed for random state
    title : str, default = ""
        title of the histogram
    y_axis : str, default = "Count"
        name of the y axis
    path : None or str, default = None
        specify the directory to save the figure as .png
    
    Returns
    -------
    plot: histogram
        histogram of bootstrap distribution with confidence interval
        and oberserved mean
    
    Examples
    --------
    >>> plot_ci([1, 2, 3, 4, 5, 6, 7], 1000, n=100, level=0.95,
                random_seed=123, title="Bootstrap")
    """

    if not isinstance(title, str):
        raise TypeError(
            "The value of the argument 'title' must be type of str."
        )
        
    if not isinstance(y_axis, str):
        raise TypeError(
            "The value of the argument 'y_axis' must be type of str."
        )

    if not (isinstance(path, str) or path == None):
        raise TypeError(
            "The value of the argument 'path' must be type of str or None."
        )
        
    if path is not None :
        if os.path.isdir(path) is False:
            raise NameError("The folder path you specified is invalid.")
    
    if estimator not in {"mean", "median", "var", "sd"}:
        raise ValueError("Supported estimators are mean, median, var, sd")

    sample_stat_dict = calculate_boot_stats(sample, rep, level=level, 
                                            n=n, estimator=estimator,
                                            random_seed=random_seed,
                                            pass_dist=True)
        
    plt.hist(sample_stat_dict[1], density=False, bins=bin_size)
    plt.axvline(sample_stat_dict[0]["lower"], color='k', linestyle='--')
    plt.axvline(sample_stat_dict[0]["sample_"+estimator], color='r', linestyle='-')
    plt.axvline(sample_stat_dict[0]["upper"], color='k', linestyle='--')
    axes = plt.gca()
    _, y_max = axes.get_ylim()
    plt.text(sample_stat_dict[0]["sample_"+estimator], 
             y_max * 0.9 , 
             (str(round(sample_stat_dict[0]["sample_"+estimator], 2))+
              '('+u"\u00B1"+str(round(sample_stat_dict[0]['std_err'],2))+')'), 
             ha='center', va='center',rotation='horizontal', 
             color = "k", bbox={'facecolor':'white', 'pad':5})
    plt.text(sample_stat_dict[0]["upper"], 
             y_max * 0.9 , 
             (str(round(sample_stat_dict[0]["upper"], 2))), 
             ha='center', va='center',rotation='horizontal', 
             color = "k", bbox={'facecolor':'white', 'pad':5})
    plt.text(sample_stat_dict[0]["lower"], 
             y_max * 0.9 , 
             (str(round(sample_stat_dict[0]["lower"], 2))), 
             ha='center', va='center',rotation='horizontal', 
             color = "k", bbox={'facecolor':'white', 'pad':5})
    plt.title(title)
    plt.xlabel("Bootstrap sample "+estimator)
    plt.ylabel(y_axis)

    if path is not None:
        plt.savefig(f"{path}bootstrap_histogram.png")

    return plt
    


def tabulate_stats(stat, precision=2, estimator=True, alpha=True, path=None):
    """Makes two tables that summerize the statistics from the bootstrapped 
    samples and the parameters for creating the bootstrapped samples. It also allows you
    to save the tables in latex format.


    Parameters
    ----------
    stat : dict or tuple
        summary statistics produced by the `calculate_boot_stats()` function 
    precision : int, default=2
        the precision of the table values
    estimator : boolean, default=True
        include the bootstrap estimate in the summary statistics table
    alpha : boolean, default=True
        include the significance level in the summary statistics table
    path : str, default = None
        specify a path to where the tex files of tables should be saved.

    Returns
    -------
    tuple :
        summary statistics: style object
            table summerizing the lower bound and upper bound of the confidence
            interval,the standard error, the sampling statitic (if estimator = True),
            and the significance level (if alpha = True). Style objects do not display
            well in a python shell.
        bootstrap parameters: style object
            table  summerizing the parameters of the bootstrap sampling spficiying
            the original sample size, number of repititions, the significance level,
            and the number of samples in each bootstrap if its different from the
            original sample size. Style objects do not display well in a python shell.
        
    Examples
    --------
    >>> st = calculate_boot_stats([1, 2, 3, 4], 1000, level=0.95, random_seed=123)
    >>> stats_table, parameter_table  = tabulate_stats(st)
    >>> stats_table
    >>> parameter_table
    """

    if not(isinstance(stat, tuple) | isinstance(stat, dict)):
        raise TypeError(
            "The stats parameter must be created from "
            "calculate_boot_stats() function."
        )
    if not isinstance(precision, int):
        raise TypeError("The precision parameter must be of type int.")
    if not (isinstance(estimator, bool) & isinstance(alpha, bool)):
        raise TypeError(
            "The estimator and alpha parameters must be of type boolean."
        )
    if not (isinstance(path, str) or path is None):
        raise TypeError("The path parameter must be a character string.")
        
    if path is not None :
         if os.path.isdir(path) is False:
            raise NameError("The folder path you specified is invalid.")
    
    if isinstance(stat, tuple):
        stat = stat[0]
        
    dic_keys = stat.keys()
    
    if not (("lower" in dic_keys) &
            ("upper" in dic_keys) &
            ("std_err" in dic_keys) &
            ("estimator" in dic_keys) &
            ("level" in dic_keys) &
            ("sample_size" in dic_keys) &
            ("n" in dic_keys) &
            ("rep" in dic_keys)):
        raise TypeError(
            "The statistics dictionary is missing a key. "
            "Please rerun calculate_boot_stats() function"
        )
        
    # define the statistics table
    df = pd.DataFrame(data=np.array([(stat["lower"], stat["upper"],
                                      stat["std_err"])]),
                      columns=["Lower Bound CI", "Upper Bound CI",
                               "Standard Error"])

    if estimator is True:
        s_name = "Sample " + stat["estimator"]
        df[s_name] = stat["sample_" + stat["estimator"]]

    if alpha is True:
        df["Significance Level"] = 1 - stat["level"]
        stats_table = df.style.format(
            precision=precision, formatter={("Significance Level"): "{:.3f}"}
        )
    else:
        stats_table = df.style.format(precision=precision)

    stats_table = stats_table.hide(axis="index")

    # set formatting and caption for table
    stats_table.set_caption(
        "Bootstrapping sample statistics from sample with "+
        str(stat["sample_size"]) + " records"
    ).set_table_styles(
        [{"selector": "caption",
          "props": "caption-side: bottom; font-size: 1.00em;"}],
        overwrite=False)
            
    # create bootstrapping parameter summary table
    df_bs = pd.DataFrame(
        data=np.array(
            [(stat["sample_size"], stat["rep"], (1 - stat["level"]))]),
        columns=["Sample Size", "Repetition", "Significance Level"])
    
    if stat["n"] != "auto":
        df_bs["Samples per bootstrap"] = round(stat["n"], 0)

    # set formatting and caption for table
    bs_params = df_bs.style.format(
        precision=0,
        formatter={("Significance Level"): "{:.3f}"}
    ).hide(axis="index")
    
    (bs_params
    .set_caption("Parameters used for bootstrapping")
    .set_table_styles(
        [{"selector": "caption",
          "props": "caption-side: bottom;font-size:1.00em;"}],
        overwrite=False)
    )

    if path is not None:
        with open(f"{path}sampling_statistics.tex", "w") as tf:
            tf.write(stats_table.to_latex())

        with open(f"{path}bootstrap_params.tex", "w") as tf:
            tf.write(bs_params.to_latex())
        
    return stats_table, bs_params
