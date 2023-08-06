import numpy as np
import gaussianprocess as gp
import matplotlib.pyplot as plt
import genutils as gu


class fitderiv:
    """
    to smooth data and estimate the time derivative of the data using Gaussian processes.

    Summary statistics - the maximal time derivative, the time at which the maximal time
    derivative occurs, the timescale found from inverting the maximal time derivative, the
    maximal value of the smoothed data, and the lag time (the time when the tangent from the
    point with the maximal time derivative crosses a line parallel to the time-axis that
    passes through the first data point) - are found and their errors estimated using
    bootstrapping. All statistics can be postfixed by ' err' to find this error.

    A summary statistic is given as the median of a distribution of the statistic calculated
    from time series sampled from the optimal Gaussian process. Its error is estimated as the
    interquartile range of this distribution.

    After a successful optimisation, the following attributes are generated:
        t: array
            The times specified as input.
        origd: array
            The original data.
        d: array
            The data used in the smoothing, either the original data or its logarithm.
        f: array
            The mean of the Gaussian process with the optimal hyperparmeters at each time point.
        fvar: array
            The variance of the optimal Gaussian process at each time point.
        df: array
            The inferred first time-derivative.
        dfvar: array
            The inferred variance of the first time-derivative.
        ddf: array
            The inferred second time-derivative.
        ddfvar: array
            The inferred variance of the second time-derivative.
        ds: dictionary
            The summary statistics and their estimated errors.


    Examples
    --------
    A typical work flow is:

    >>> from fitderiv import fitderiv
    >>> q= fitderiv(t, od, figs= True)
    >>> q.plotfit('df')

    or potentially

    >>> import matplotlib.pyplot as plt
    >>> plt.plot(q.t, q.d, 'r.', q.t, q.y, 'b')

    Reference
    ---------
    PS Swain, K Stevenson, A Leary, LF Montano-Gutierrez, IBN Clark, J Vogel, and T Pilizota.
    Inferring time derivatives including growth rates using Gaussian processes
    Nat Commun 7 (2016) 13766
    """

    def __init__(
        self,
        t,
        d,
        cvfn="sqexp",
        logs=True,
        noruns=5,
        noinits=100,
        exitearly=False,
        figs=False,
        bd=False,
        esterrs=False,
        optmethod="l_bfgs_b",
        nosamples=100,
        gui=False,
        figtitle=False,
        ylabel="y",
        stats=True,
        statnames=False,
        showstaterrors=True,
        warn=False,
        linalgmax=3,
        iskip=False,
    ):
        """
        Runs a Gaussian process to both smooth time-series data and estimate its time-derivatives.

        Parameters
        ----------
        t: array
            The time points.
        d: array
            The data corresponding to the time points with any replicates given as columns.
        cvfn: string
            The type of kernel function for the Gaussian process either 'sqexp' (squared exponential)
            or 'matern' (Matern with nu= 5/2) or 'nn' (neural network).
        logs: boolean
            If True, the Gaussian process is used to smooth the natural logarithm of the data
            and the time-derivative is therefore of the logarithm of the data.
        noruns: integer, optional
            The number of attempts to be made at optimising the kernel's hyperparmeters.
        noinits: integer, optional
            The number of random attempts made to find good initial choices for the
            hyperparameters before running their optimisation.
        exitearly: boolean, optional
            If True, stop at the first successful attempt at optimising the hyperparameters
            otherwwise take the best choice from all successful optimisations.
        figs: boolean, optional
            If True, plot the data and the mean of the Gaussian process with the optimal
            hyperparameters.
        bd: dictionary, optional
            Specifies the limits on the hyperparameters for the Gaussian process.
            For example, bd= {0: [-1, 4], 2: [2, 6]})
            sets confines the first hyperparameter to be between 1e-1 and 1e^4 and confines the
            third hyperparmater between 1e2 and 1e6.
        esterrs: boolean, optional
            If True, measurement errors are empirically estimated by the variance across replicates
            at each time point.
            If False, the variance of the measurement error is assumed to be the same for all time
            points and its magnitude is a hyperparameter that is optimised.
        optmethod: string, optional
            The algorithm used to optimise the hyperparameters, either 'l_bfgs_b' or 'tnc'.
        nosamples: integer, optional
            The number of bootstrap samples taken to estimate errors in statistics.
        gui: boolean, optional
            If True, extra output is generated and printed for the GUI.
        figtitle: string, optional
            A title for the figure generated if figs= True.
        ylabel: string, optional
            A label of the y-axis for the figure generated if figs= True.
        stats: boolean, optional
            If True, calcuate summary statistics for both the smoothed data and the inferred
            time- derivative.
        statnames: list of strings
            To customise the names of the statistics.
            The default names are:
                    'max df' for the maximal time derivative;
                    'time of max df' for the time at which the maximal time derivative occurs;
                    'inverse max df' for the timescale found from inverting the maximal time
                    derivative;
                    'max f' for the maximal value of the smoothed data;
                    'lag time' for the lag time defined as the time when the tangent from the point
                    with the maximal time derivative crosses a line parallel to the time-axis that
                    passes through the first data point.
        showstaterrors: boolean, optional
            If True, display estimated errors for the statistics.
        warn: boolean, optional
            If False, warnings created by covariance matrices that are not positive semi-definite
            are suppressed.
        linalgmax: integer, optional
            The number of times errors generated by underlying linear algebra modules during the
            optimisation by poor choices of the hyperparameters should be ignored.
        iskip: integer, optional
            If non-zero, only every iskip'th data point is used to increase speed.
        """
        self.__version__ = "1.1.3"
        self.ylabel = ylabel
        self.logs = logs
        if not warn:
            # warning generated occasionally when sampling from the Gaussian process likely because of numerical errors
            import warnings

            warnings.simplefilter("ignore", RuntimeWarning)
        try:
            noreps = d.shape[1]
        except:
            noreps = 1
        self.noreps = noreps
        self.origd = d
        pt = t
        self.pt = t
        if iskip:
            self.t = t[::iskip]
            self.d = d[::iskip]
            t, d = self.t, self.d
        else:
            self.t = t
            self.d = d
        # bounds for hyperparameters
        bnn = {0: (-1, 5), 1: (-7, -2), 2: (-6, 2)}
        bsqexp = {0: (-5, 5), 1: (-6, 2), 2: (-5, 2)}
        bmatern = {0: (-5, 5), 1: (-4, 4), 2: (-5, 2)}
        # take log of data
        if logs:
            print("Taking natural logarithm of the data.")
            if np.any(np.nonzero(d < 0)):
                raise (
                    SystemExit(
                        "Negative data found, but all data must be positive if taking logs."
                    )
                )
            else:
                # replace zeros by machine error
                d[d == 0] = np.finfo(float).eps
                d = np.log(np.asarray(d))
        # run checks and define measurement errors
        merrors = False
        if np.any(esterrs):
            if type(esterrs) == type(True):
                # errors must be empirically estimated.
                if noreps > 1:
                    lod = [
                        len(np.nonzero(~np.isnan(d[:, i]))[0]) for i in range(noreps)
                    ]
                    if np.sum(np.diff(lod)) != 0:
                        print("The replicates have different number of data points.")
                        print(
                            "Equal numbers of data points are needed for empirically estimating errors."
                        )
                    else:
                        # estimate errors empirically
                        merrors = gu.findsmoothvariance(d)
                        if figs:
                            plt.figure()
                            plt.errorbar(t, np.mean(d, 1), np.sqrt(merrors))
                            plt.plot(t, d, ".")
                            plt.show(block=False)
                else:
                    print("Not enough replicates to estimate errors.")
            else:
                # esterrs given as an array of errors
                if len(esterrs) != len(t):
                    print("Each time point requires an estimated error.")
                else:
                    merrors = esterrs
        if not np.any(merrors):
            print("Fitting measurement errors.")
        # display details of covariance functions
        try:
            if bd:
                bds = gu.mergedicts(original=eval("b" + cvfn), update=bd)
            else:
                bds = eval("b" + cvfn)
            if not gui:
                gt = getattr(gp, cvfn + "GP")(bds, t, d)
                print("Using a " + gt.description + ".")
                gt.info()
        except NameError:
            print("Gaussian process not recognized.")
            from sys import exit

            exit()
        self.bds = bds
        # combine data into one array
        tb = np.tile(t, noreps)
        db = np.reshape(d, np.size(d), order="F")
        if np.any(merrors):
            mb = np.tile(merrors, noreps)
        # remove any nans
        da = db[~np.isnan(db)]
        ta = tb[~np.isnan(db)]
        if np.any(merrors):
            ma = mb[~np.isnan(db)]
        else:
            ma = False
        # run Gaussian process
        g = getattr(gp, cvfn + "GP")(bds, ta, da, merrors=ma)
        g.findhyperparameters(
            noruns,
            noinits=noinits,
            exitearly=exitearly,
            optmethod=optmethod,
            linalgmax=linalgmax,
        )
        # display results
        if gui:
            print("log(max likelihood)= %e" % (-g.nlml_opt))
            for el in g.hparamerr:
                if el[1] == "l":
                    print(
                        "Warning: hyperparameter "
                        + str(el[0])
                        + " is at a lower bound."
                    )
                else:
                    print(
                        "Warning: hyperparameter "
                        + str(el[0])
                        + " is at an upper bound."
                    )
                print(
                    "\tlog10(hyperparameter %d)= %4.2f"
                    % (el[0], np.log10(np.exp(g.lth_opt[el[0]])))
                )
        else:
            g.results()
        g.predict(pt, derivs=2, addnoise=True)
        # results
        self.g = g
        self.logmaxlike = -g.nlml_opt
        self.hparamerr = g.hparamerr
        self.lth = g.lth_opt
        self.f = g.f
        self.df = g.df
        self.ddf = g.ddf
        self.fvar = g.fvar
        self.dfvar = g.dfvar
        self.ddfvar = g.ddfvar
        self.merrors = merrors
        if stats:
            self.calculatestats(nosamples, statnames, showstaterrors)
        if figs:
            plt.figure()
            self.plotfit()
            plt.xlabel("time")
            if logs:
                plt.ylabel("log " + ylabel)
            else:
                plt.ylabel(ylabel)
            if figtitle:
                plt.title(figtitle)
            else:
                plt.title("mean fit +/- standard deviation")
            plt.show(block=False)

    ###
    def fitderivsample(self, nosamples, newt=None):
        """
        Generate sample values for the latent function and its first two derivatives.
         (returned as a tuple).

        Parameters
        ----------
        nosamples: integer
            The number of samples.
        newt: array, optional
            Time points for which the samples should be made.
            If None, the orginal time points are used.

        Returns
        -------
        samples: a tuple of arrays
            The first element of the tuple gives samples of the latent function; the second
            element gives samples of the first time derivative; and the third element gives
            samples of the second time derivative.
        """
        if np.any(newt):
            newt = np.asarray(newt)
            import copy

            # make prediction for new time points
            gps = copy.deepcopy(g)
            gps.predict(newt, derivs=2, addnoise=True)
        else:
            gps = self.g
        samples = gps.sample(nosamples, derivs=2)
        return samples

    ###
    def plotfit(
        self, char="f", errorfac=1, xlabel="time", ylabel=False, figtitle=False
    ):
        """
        Plots either the data and the mean of the optimal Gaussian process or the inferred time
        derivatives.

        Parameters
        ----------
        char: string
            The variable to plot either 'f' or 'df' or 'ddf'.
        errorfac: float, optional
            The size of the errorbars are errorfac times the standard deviation of the optimal
            Gaussian process.
        ylabel: string, optional
            A label for the y-axis.
        figtitle: string, optional
            A title for the figure.
        """
        x = getattr(self, char)
        xv = getattr(self, char + "var")
        if char == "f":
            d = np.log(self.origd) if self.logs else self.origd
            plt.plot(self.pt, d, "r.")
        plt.plot(self.pt, x, "b")
        plt.fill_between(
            self.pt,
            x - errorfac * np.sqrt(xv),
            x + errorfac * np.sqrt(xv),
            facecolor="blue",
            alpha=0.2,
        )
        if ylabel:
            plt.ylabel(ylabel)
        else:
            plt.ylabel(char)
        plt.xlabel(xlabel)
        if figtitle:
            plt.title(figtitle)

    ###
    def calculatestats(self, nosamples=100, statnames=None, showerrors=True):
        """
        Calculates the statistics from the smoothed data and the inferred time derivative.
        The default names are 'max df', 'time of max df', 'inverse max grad', 'max f', and
        'lag time'.

        Parameters
        ----------
        nosamples: integer
            The number of bootstrap samples used to estimate errors.
        statnames: list of strings, optional
            A list of alternative names for the statistics.
        showerrors: boolean, optional
            If True, display the estimated errors.
        """
        print("\nCalculating statistics with " + str(nosamples) + " samples")
        if showerrors:
            print("\t(displaying median +/- half interquartile range)\n")
        if statnames:
            self.stats = statnames
        else:
            self.stats = [
                "max df",
                "time of max df",
                "inverse max df",
                "max " + self.ylabel,
                "lag time",
            ]
        t, noreps = self.pt, self.noreps
        fs, gs, hs = self.fitderivsample(nosamples)
        # calculate stats
        im = np.argmax(gs, 0)
        # max df
        mgr = gs[im, np.arange(nosamples)]
        # time of max df
        tmgr = np.array([t[i] for i in im])
        # inverse max df
        dt = np.log(2) / mgr
        # max f
        if self.logs:
            md = np.exp(np.max(fs, axis=0))
        else:
            md = np.max(fs, axis=0)
        # lag time
        lagtime = (
            tmgr + (fs[0, np.arange(nosamples)] - fs[im, np.arange(nosamples)]) / mgr
        )
        # store stats
        ds = {}
        for stname, st in zip(self.stats, [mgr, tmgr, dt, md, lagtime]):
            ds[stname] = np.median(st)
            ds[stname + " err"] = gu.findiqr(st) / 2
        self.ds = ds
        self.nosamples = nosamples
        self.printstats(showerrors=showerrors)

    ###
    def printstats(self, showerrors=True, performprint=True):
        """
        Creates and potentially displays a dictionary of the statistics calculated from
        the smoothed data and its inferred time-derivatives.

        Parameters
        ----------
        showerrors: boolean, optional
            If True, display the errors.
        performprint: boolean optional
            If True, display the statistics.

        Returns
        -------
        statd: dictionary
            The statistics and their errors.
        """
        ds = self.ds
        statd = {}
        lenstr = np.max([len(s) for s in self.stats])
        for s in self.stats:
            statd[s] = ds[s]
            statd[s + " err"] = ds[s + " err"]
            if performprint:
                stname = s.rjust(lenstr + 1)
                if showerrors:
                    print(
                        "{:s}= {:6e} +/- {:6e}".format(stname, statd[s], ds[s + " err"])
                    )
                else:
                    print("{:s}= {:6e}".format(stname, statd[s]))
        return statd

    ###
    def plotstats(self):
        """
        Produces a bar chart of the statistics.
        """
        try:
            ds, stats = self.ds, self.stats
            data = []
            errs = []
            for s in stats:
                data.append(ds[s])
                errs.append(ds[s + " err"])
            fig = plt.figure()
            barwidth = 0.5
            ax = fig.add_subplot(111)
            plt.bar(np.arange(len(stats)), data, barwidth, yerr=errs)
            ax.set_xticks(np.arange(len(stats)) + barwidth / 2.0)
            ax.set_xticklabels(stats)
            plt.tight_layout()
            plt.show(block=False)
        except AttributeError:
            print(" Statistics have not been calculated.")

    ###
    def plotfvsdf(self, ylabel="f", title=""):
        """
        Plots the mean of the optimal Gaussion process versus the inferred time-derivative
        using ellipses with axes lengths proportional to the estimated errors.

        Parameters
        --
        ylabel: string, optional
            A label for the y-axis.
        title: string, optional.
            A title
        """
        if self.logs:
            xlabel = "fitted log " + ylabel
        else:
            xlabel = "fitted " + ylabel
        ylabel = "deriv " + ylabel
        gu.plotxyerr(
            self.f,
            self.df,
            np.sqrt(self.fvar),
            np.sqrt(self.dfvar),
            xlabel,
            ylabel,
            title,
        )

    ###
    def export(self, fname, rows=False):
        """
        Exports the smoothed data and inferred time-derivative.

        Parameters
        ----------
        fname: string
            The name of the file appended with '.csv' or '.txt' or '.tsv' or '.xlsx'.
        rows: boolean, optional
            If True, data are exported in rows otherwise they are exported as columns.
        """
        import pandas as pd

        ods = self.origd
        data = [self.pt, self.f, np.sqrt(self.fvar), self.df, np.sqrt(self.dfvar), ods]
        if ods.ndim == 1:
            labels = ["t", "log(OD)", "log(OD) error", "gr", "gr error", "od"]
        else:
            labels = ["t", "log(OD)", "log(OD) error", "gr", "gr error"] + [
                "od"
            ] * ods.shape[1]
        orgdata = np.column_stack(data)
        # make dataframes
        if rows:
            df = pd.DataFrame(np.transpose(orgdata), index=labels)
        else:
            df = pd.DataFrame(orgdata, columns=labels)
        statd = self.printstats(performprint=False)
        dfs = pd.DataFrame(statd, index=[0], columns=statd.keys())
        # export in appropriate format
        ftype = fname.split(".")[-1]
        if ftype == "csv" or ftype == "txt" or ftype == "tsv":
            if ftype == "txt" or ftype == "tsv":
                sep = " "
            else:
                sep = ","
            if rows:
                df.to_csv(fname, sep=sep, header=False)
            else:
                df.to_csv(fname, sep=sep, index=False)
            dfs.to_csv(
                ".".join(fname.split(".")[:-1]) + "_stats." + ftype,
                sep=sep,
                index=False,
            )
        elif ftype == "xls" or ftype == "xlsx":
            if rows:
                df.to_excel(fname, sheet_name="Sheet1", header=False)
            else:
                df.to_excel(fname, sheet_name="Sheet1", index=False)
            dfs.to_excel(
                ".".join(fname.split(".")[:-1]) + "_stats.xlsx",
                sheet_name="Sheet1",
                index=False,
            )
        else:
            print(
                "!! File type is either not recognized or not specified. Cannot save as",
                fname,
            )


#####

if __name__ == "__main__":
    print(fitderiv.__doc__)
