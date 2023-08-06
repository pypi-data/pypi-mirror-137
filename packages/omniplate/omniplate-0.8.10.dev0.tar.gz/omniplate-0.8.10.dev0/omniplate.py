#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.interpolate import interp1d
from scipy.optimize import minimize_scalar

try:
    from statsmodels.nonparametric.smoothers_lowess import lowess
except ModuleNotFoundError:
    raise (
        SystemExit(
            "The module statmodels is not installed - try: pip install statsmodels"
        )
    )
import gaussianprocess as gp
from fitderiv import fitderiv
import genutils as gu
import pandas as pd
import inspect

# from 0.87 to 0.8.7
version = "0.8.10"

plt.rcParams["figure.max_open_warning"] = 0
sns.set()


class platereader:
    """
    for analyzing plate-reader data, correcting for autofluorescence, and
    determining growth rates.

    All data is stored used Panda's dataframes and plotted using Seaborn.

    Three dataframes are created. If p is an instance of the platereader class,
    then p.r contains the raw data for each well in the plate; p.s contains the
    processed time-series using the data from all relevant wells; and p.sc
    constains any summary statistics, such as 'max gr'.

    For time series sampled from a Gaussian process, the mean is used as the statistic
    and errors are estimated by the standard deviation.
    For statistics calculated from time series, the median is used and errors are estimated
    by half the interquartile range, with the distribution of the statistic calculated by
    sampling time series.

    Examples
    -------
    A typical work flow is:

    >>> import omniplate as om

    then either

    >>> p= om.platereader('GALdata.xlsx', 'GALcontents.xlsx',
    ...                    wdir= 'data/')

    or

    >>> p= om.platereader()
    >>> p.load('GALdata.xls', 'GALcontents.xlsx')

    and to analyse OD data

    >>> p.plot('OD', plate= True)
    >>> p.correctOD()
    >>> p.correctmedia()
    >>> p.plot(y= 'OD')
    >>> p.plot(y= 'OD', hue= 'strain',
    ...        conditionincludes= ['Gal', 'Glu'],
    ...        strainexcludes= 'HXT7')
    >>> p.getstats('OD')

    and for fluorescence data

    >>> p.correctauto(['GFP', 'AutoFL'])
    >>> p.plot(y= 'c-GFPperOD', hue= 'condition')

    and to save the results

    >>> p.savefigs()
    >>> p.exportdf()

    General properties of the data and of previous processing are shown with:

    >>> p.info()
    >>> p.attributes()
    >>> p.corrections()
    >>> p.log()

    See also

        http://swainlab.bio.ed.ac.uk/software/omniplate/index.html

    for a tutorial, which can be opened directly using

    >>> p.webhelp()
    """

    #####
    def __init__(
        self,
        dnames=False,
        anames=False,
        wdir="",
        platereadertype="Tecan",
        dsheetnumbers=False,
        asheetnumbers=False,
        ODfname=None,
        info=True,
        ls=True,
    ):
        """
        Initiate and potentially immediately load data for processing.

        Parameters
        ----------
        dnames: string or list of strings, optional
            The name of the file containing the data from the plate reader or a list of file names.
        anames: string or list of strings, optional
            The name of file containing the corresponding annotation or a list of file names.
        wdir: string, optional
            The working directory where the data files are stored and where output will be saved.
            Append '/'.
        platereadertype: string
            The type of plate reader, currently either 'Tecan' or 'Sunrise' or 'old Tecan'.
        dsheetnumbers: integer or list of integers, optional
            The relevant sheets of the Excel files storing the data.
        asheetnumbers: integer or list of integers, optional
            The relevant sheets of the corresponding Excel files for the annotation.
        ODfname: string, optional
            The name of the file with the dilution data used to correct OD for its non-linear
            dependence on numbers of cells. If unspecified, data for haploid budding yeast growing
            in glucose is used.
        info: boolean
            If True (default), display summary information on the data once loaded.
        ls: boolean
            If True (default), display contents of working directory.
        """
        self.__version__ = version
        print("\nomniplate version=", self.__version__)
        self.wdir = wdir

        # enable logging
        self._initialiselogging()
        self._logmethod(self.logger)

        # general parameters
        self.gamma = 0.114  # ratio of 585 to 525 for eGFP
        self.overflow = -999.99

        if True:
            # warning generated occasionally when sampling from the Gaussian process likely because of numerical errors
            import warnings

            warnings.simplefilter("ignore", RuntimeWarning)

        # dictionary recording extent of analysis
        self.progress = {
            "ignoredwells": {},
            "negativevalues": {},
            "getstatsGP": {},
            "ODfname": {},
            "gc": {},
        }
        self.allexperiments = []
        self.allconditions = {}
        self.allstrains = {}
        self.datatypes = {}

        if dnames == False:
            # list all files in current directory
            if ls:
                self.ls()
        else:
            # immediately load data
            self.load(
                dnames,
                anames,
                platereadertype,
                dsheetnumbers,
                asheetnumbers,
                ODfname,
                info,
            )

    def __repr__(self):
        repstr = "{} v{}: ".format(self.__class__.__name__, self.__version__)
        for e in self.allexperiments:
            repstr += e + " ; "
        if repstr[-2:] == "; ":
            repstr = repstr[:-3]
        return repstr

    #####
    def ls(self):
        """
        List all files in the working directory.

        Example
        -------
        >>> p.ls()
        """
        import os

        wdir = os.getcwd() + "/" + self.wdir
        print("Working directory is", wdir)
        print("Files available are:", "\n---")
        datafiles = sorted(
            [
                f
                for f in os.listdir(wdir)
                if os.path.isfile(wdir + "/" + f)
                and ("xls" in f or "json" in f or "tsv" in f or "csv" in f)
            ]
        )
        for f in datafiles:
            if f:
                print(f)
        print()

    def changewdir(self, wdir):
        """
        Change working directory.

        Parameters
        ----------
        wdir: string
            The new working directory specified from the current directory.

        Example
        -------
        >>> p.changewdir('newdata/')
        """
        self.wdir = wdir
        self.ls()

    #####
    def load(
        self,
        dnames,
        anames=False,
        platereadertype="Tecan",
        dsheetnumbers=False,
        asheetnumbers=False,
        ODfname=None,
        info=True,
    ):
        """
        Loads raw data files generated by the plate reader and the corresponding annotation files.

        Parameters
        ----------
        dnames: string or list of strings, optional
            The name of the file containing the data from the plate reader or a list of file names.
        anames: string or list of strings, optional
            The name of file containing the corresponding annotation or a list of file names.
        platereadertype: string
            The type of plate reader, currently either 'Tecan' or 'Sunrise' or 'old Tecan'.
        dsheetnumbers: integer or list of integers, optional
            The relevant sheets of the Excel files storing the data.
        asheetnumbers: integer or list of integers, optional
            The relevant sheets of the corresponding Excel files for the annotation.
        ODfname: string, optional
            The name of the file with the dilution data used to correct OD for its non-linear
            dependence on numbers of cells. If unspecified, data for haploid budding yeast growing
            in glucose is used.
        info: boolean
            If True (default), display summary information on the data once loaded.

        Examples
        -------
        >>> p.load('Data.xlsx', 'DataContents.xlsx')
        >>> p.load('Data.xlsx', 'DataContents.xlsx', info= False)
        >>> p.load('Data.xlsx', 'DataContents.xlsx',
        ...         ODfname= 'ODcorrection_Glucose_Diploid.txt')
        """
        dnames = gu.makelist(dnames)
        if not anames:
            anames = [dname.split(".")[0]
                      + "Contents.xlsx" for dname in dnames]
        else:
            anames = gu.makelist(anames)
        if not dsheetnumbers:
            dsheetnumbers = [0 for dname in dnames]
        if not asheetnumbers:
            asheetnumbers = [0 for dname in dnames]

        alldata = {}
        for i, dname in enumerate(dnames):
            # get dataframe for raw data
            # defines self.allexperiments, self.allconditions, self.allstrains
            rdf, alldatasingle = self._importdatafromplate(
                platereadertype, dname, dsheetnumbers[i], anames[i], asheetnumbers[i]
            )
            alldata.update(alldatasingle)
            self.r = pd.merge(self.r, rdf, how="outer") if hasattr(
                self, "r") else rdf
            # update progress dictionary
            experiment = dname.split(".")[0]
            self._initialiseprogress(experiment)

        # define ODfname in progress dictionary
        if ODfname:
            if isinstance(ODfname, str):
                self.progress["ODfname"] = {
                    exp: ODfname for exp in self.allexperiments}
            else:
                self.progress["ODfname"] = {
                    exp: ODfname[i] for i, exp in enumerate(self.allexperiments)
                }
        else:
            self.progress["ODfname"] = {
                exp: None for exp in self.allexperiments}

        # dataframe for summary stats and corrections
        alldfs = []
        # for exp in self.allexperiments:
        for exp in alldata:
            strs, cons = [], []
            for cs in alldata[exp]:
                strs.append(cs.split(" in ")[0])
                cons.append(cs.split(" in ")[1])
            corrdict = {
                "experiment": exp,
                "strain": strs,
                "condition": cons,
                "OD corrected": False,
            }
            corrdict.update(
                {dtype
                    + " corrected for media": False for dtype in self.datatypes[exp]}
            )
            corrdict.update(
                {
                    dtype + " corrected for autofluorescence": False
                    for dtype in self.datatypes[exp]
                    if dtype not in ["AutoFL", "OD"]
                }
            )
            alldfs.append(pd.DataFrame(corrdict))
        self.sc = pd.concat(alldfs)

        # dataframe of original data
        self.origr = self.r.copy()
        # dataframe for well content
        self.wellsdf = self._makewellsdf()
        # dataframe for summary data
        self.s = self._make_s()

        # display info on experiment, conditions and strains
        if info:
            self.info()
        print(
            '\nWarning: "null" has been changed to "Null" to avoid confusion with pandas.\n'
        )

    #####
    def _initialiseprogress(self, experiment):
        """
        Internal function: initialises progress dictionary.
        """
        self.progress["ignoredwells"][experiment] = []
        self.progress["negativevalues"][experiment] = False
        self.progress["getstatsGP"][experiment] = {
            c: {} for c in self.allconditions[experiment]
        }
        self.progress["gc"][experiment] = None

    #####
    def _importdatafromplate(
        self, platereadertype, dname, dsheetnumber, aname, asheetnumber
    ):
        """
        Internal function: Creates dataframe from input files created by the plate reader.
        """
        experiment = dname.split(".")[0]

        # import and process plate contents file
        alldata, rcontents = self._analyseContentsofWells(
            experiment, aname, asheetnumber
        )

        # import data created by plate reader
        try:
            print("loading", dname)
            dfd = pd.read_excel(self.wdir + dname, sheet_name=dsheetnumber)
            self.allexperiments.append(experiment)
        except FileNotFoundError:
            raise _FileNotFound(self.wdir + dname)

        # extract data from the plate reader file
        if platereadertype == "Tecan":
            rdict, datatypes = self._analyseTecan(
                dfd, rcontents, experiment, old=False)
        elif platereadertype == "old Tecan":
            rdict, datatypes = self._analyseTecan(
                dfd, rcontents, experiment, old=True)
        elif platereadertype == "Sunrise":
            rdict, datatypes = self._analyseSunrise(
                dfd,
                rcontents,
                experiment,
            )
        else:
            raise _UnknownPlateReader(platereadertype)
        self.datatypes[experiment] = list(datatypes)
        # return dataframes for raw and processed data, error
        return pd.DataFrame(rdict), alldata

    #####
    def _analyseContentsofWells(self, exp, aname, asheetnumber):
        """
        Internal function: loads and parses ContentsofWells file.
        Creates allconditions and allstrains attributes.
        Returns rcontents, a dictionary with the contents of each well indexed by well,
        and alldata, a dictionary describing the contents of each well indexed by experiment.
        """
        try:
            alldata = {}
            # import contents of the wells
            anno = pd.read_excel(
                self.wdir + aname, index_col=0, sheet_name=asheetnumber
            )
            alldata[exp] = []
            rcontents = {}
            # run through and parse content of each well
            for x in np.arange(1, 13):
                for y in "ABCDEFGH":
                    well = y + str(x)
                    if isinstance(anno[x][y], str) and anno[x][y] != "contaminated":
                        s, c = anno[x][y].split(" in ")
                        rcontents[well] = [
                            c.strip(), s.strip().replace("null", "Null")]
                        alldata[exp].append(
                            rcontents[well][1] + " in " + rcontents[well][0]
                        )
                    else:
                        rcontents[well] = [None, None]
            # create summary descriptions of the well contents
            alldata[exp] = list(np.unique(alldata[exp]))
            self.allconditions[exp] = list(
                np.unique(
                    [
                        rcontents[well][0]
                        for well in rcontents
                        if rcontents[well][0] != None
                    ]
                )
            )
            self.allstrains[exp] = list(
                np.unique(
                    [
                        rcontents[well][1]
                        for well in rcontents
                        if rcontents[well][0] != None
                    ]
                )
            )
            return alldata, rcontents
        except FileNotFoundError:
            raise _FileNotFound(self.wdir + aname)

    #####
    def _analyseTecan(self, dfd, rcontents, experiment, old=False):
        """
        Internal function: extracts data from an imported Excel file generated by
        a Tecan F200 or M200 plate reader.

        Parameters
        --
        dfd: dataframe
            Created by importing the data from a file using Panda's read_excel.
        rcontents: dataframe
            Created by analyseContentsofWells.
        experiment: string
            The name of the experiment.
        old: boolean
            If True, assume the format of the data produced by older Tecan plate readers.

        Returns
        ------
        rdict: list of dictionaries
            Describes the contents of the plate by experiment, condition, strain, time,
            and well.
        datatypes: list of strings
            Delineates all the types of data in the experiment and is minimally ['OD'].
        """
        if old:
            # extract datatypes
            datatypes = [
                dfd[dfd.columns[0]]
                .iloc[
                    np.nonzero(
                        dfd[dfd.columns[0]].str.startswith(
                            "Label", na=False).to_numpy()
                    )[0]
                ]
                .to_numpy()[0]
                .split(": ")[1]
            ]
            # extract times of measurements
            t = (
                dfd.loc[
                    dfd[dfd.columns[0]].str.startswith("Time [s]", na=False),
                    dfd.columns[1]:,
                ]
                .dropna(axis="columns")
                .mean()
                .to_numpy()
                .astype("float")
                / 3600.0
            )
        else:
            # extract datatypes
            datatypes = (
                dfd[dfd.columns[0]]
                .iloc[
                    np.nonzero(
                        dfd[dfd.columns[0]]
                        .str.startswith("Cycle Nr", na=False)
                        .to_numpy()
                    )[0]
                    - 1
                ]
                .to_numpy()
            )
            # if only OD data measured
            if not isinstance(datatypes[0], str):
                datatypes = ["OD"]
            # extract times of measurements
            t = (
                dfd.loc[
                    dfd[dfd.columns[0]].str.startswith("Time [s]", na=False),
                    dfd.columns[1]:,
                ]
                .dropna(axis="columns")
                .mean()
                .to_numpy()
                .astype("float")
                / 3600.0
            )
        # deal with overflows
        df = dfd.replace("OVER", self.overflow)
        cols = df.columns
        ## extract data
        # add to dataframe
        df.index = df[cols[0]]
        rdict = []
        for x in np.arange(1, 13):
            for y in "ABCDEFGH":
                well = y + str(x)
                if well in df.index:
                    data = df.loc[well, cols[1]:].to_numpy(dtype="float")
                    if data.ndim == 1:
                        data = data[None, :]
                    if rcontents[well][0] != None and rcontents[well][1] != None:
                        for j in range(len(t)):
                            cons = {
                                "experiment": experiment,
                                "condition": rcontents[well][0],
                                "strain": rcontents[well][1],
                                "time": t[j],
                                "well": well,
                            }
                            dats = {
                                datatype: data[i, j]
                                for i, datatype in enumerate(datatypes)
                            }
                            cons.update(dats)
                            rdict.append(cons)
        return rdict, datatypes

    def _analyseSunrise(self, dfd, rcontents, experiment):
        """
        Internal function: extracts data from an imported Excel file generated by a
        Tecan Sunrise plate reader.

        Parameters
        --
        dfd: dataframe
            Created by importing the data from a file using Panda's read_excel.
        rcontents: dataframe
            Created by analyseContentsofWells.
        experiment: string
            The name of the experiment.

        Returns
        ------
        rdict: list of dictionaries
            Describes the contents of the plate by experiment, condition, strain, time,
            and well.
        datatypes: list of strings
            Delineates all the types of data in the experiment and is minimally ['OD'].
        """
        # extract datatypes
        datatypes = np.array(["OD"], dtype=object)
        # extract times of measurements
        t = (
            gu.rmnans([float(str(ts).split("s")[0])
                       for ts in dfd.to_numpy()[0]])
            / 3600.0
        )
        ## data
        # add to dataframe
        rdict = []
        for index, row in dfd.iterrows():
            if isinstance(row[-1], str) and row[-1][0] in "ABCDEFGH":
                well = row[-1]
                data = row.to_numpy(dtype="float")[:-1]
                if rcontents[well][0] != None and rcontents[well][1] != None:
                    for j in range(len(t)):
                        cons = {
                            "experiment": experiment,
                            "condition": rcontents[well][0],
                            "strain": rcontents[well][1],
                            "time": t[j],
                            "well": well,
                        }
                        dats = {"OD": data[j]}
                        cons.update(dats)
                        rdict.append(cons)
        return rdict, datatypes

    #####
    # Routines to display information on data and state of data processing
    #####
    def info(self):
        """
        Displays conditions, strains, and datatypes.

        Example
        -------
        >>> p.info()
        """
        for exp in self.allexperiments:
            print("\nExperiment:", exp, "\n---")
            print("Conditions:")
            for c in sorted(self.allconditions[exp], key=gu.natural_keys):
                print("\t", c)
            print("Strains:")
            for s in sorted(self.allstrains[exp], key=gu.natural_keys):
                print("\t", s)
            print("Data types:")
            for d in self.datatypes[exp]:
                print("\t", d)
            if self.progress["ignoredwells"]:
                print("Ignored wells:")
                if self.progress["ignoredwells"][exp]:
                    for d in self.progress["ignoredwells"][exp]:
                        print("\t", d)
                else:
                    print("\t", "None")
        print()

    def webhelp(self, browser=None):
        """
        Opens detailed examples of how to use in omniplate in a web browser.

        Parameters
        ----------
        browser: string, optional
            The browser to use - either the default if unspecified or 'firefox', 'chrome', etc.

        Example
        -------
        >>> p.webhelp()
        """
        import webbrowser

        url = "https://swainlab.bio.ed.ac.uk/software/omniplate/index.html"
        webbrowser.get(browser).open_new(url)

    def attributes(self):
        """
        Displays the names of the attributes of the current instance of platereader and
        acts as a check to see what variables have been calculated or determined.

        Example
        -------
        >>> p.attributes()
        """
        ignore = [
            "d",
            "consist",
            "t",
            "nosamples",
            "gamma",
            "ODfname",
            "overflow",
            "nooutchannels",
            "nodata",
            "__doc__",
        ]
        for a in self.__dict__:
            if "corrected" not in a and "processed" not in a and a not in ignore:
                print(a)

    def rename(self, translatedict):
        """
        Uses a dictionary to replace all occurrences of a strain or a condition with an alternative.
        Note that instances of self.progress will not be updated.

        Parameters
        ----------
        translatedict: dictionary
            A dictionary of old name - new name pairs

        Example
        -------
        >>> p.rename({'77.WT' : 'WT', '409.Hxt4' : 'Hxt4'})
        """
        # replace in dataframes
        for df in [self.r, self.s, self.sc]:
            df.replace(translatedict, inplace=True)
        # rename in attributes

        def applydict(a):
            return translatedict[a] if a in translatedict else a

        for e in self.allexperiments:
            self.allconditions[e] = list(map(applydict, self.allconditions[e]))
            self.allstrains[e] = list(map(applydict, self.allstrains[e]))
            olddict = self.progress["getstatsGP"][e]
            # rename any conditions
            self.progress["getstatsGP"][e] = dict(
                zip(list(map(applydict, list(olddict.keys()))),
                    list(olddict.values()))
            )
            for c in self.progress["getstatsGP"][e]:
                # rename any strains
                olddict = self.progress["getstatsGP"][e][c]
                self.progress["getstatsGP"][e][c] = dict(
                    zip(
                        list(map(applydict, list(olddict.keys()))),
                        list(olddict.values()),
                    )
                )

    def corrections(
        self,
        experiments="all",
        conditions="all",
        strains="all",
        experimentincludes=False,
        experimentexcludes=False,
        conditionincludes=False,
        conditionexcludes=False,
        strainincludes=False,
        strainexcludes=False,
    ):
        """
        Displays the status of corrections made for the specified strains, conditions,
        and experiments.

        Parameters
        ----------
        experiments: string or list of strings
            The experiments to include.
        conditions: string or list of strings
            The conditions to include.
        strains: string or list of strings
            The strains to include.
        experimentincludes: string, optional
            Selects only experiments that include the specified string in their name.
        experimentexcludes: string, optional
            Ignores experiments that include the specified string in their name.
        conditionincludes: string, optional
            Selects only conditions that include the specified string in their name.
        conditionexcludes: string, optional
            Ignores conditions that include the specified string in their name.
        strainincludes: string, optional
            Selects only strains that include the specified string in their name.
        strainexcludes: string, optional
            Ignores strains that include the specified string in their name.

        Returns
        -------
        df: dataframe
            Contains the status of the corrections for the specified strains, conditions,
            and experiments.

        Examples
        --------
        >>> p.corrections()
        >>> p.corrections(strainincludes= 'GAL')
        """
        exps, cons, strs = self._getall(
            experiments,
            experimentincludes,
            experimentexcludes,
            conditions,
            conditionincludes,
            conditionexcludes,
            strains,
            strainincludes,
            strainexcludes,
        )
        df = self.sc.query(
            "experiment == @exps and condition == @cons and strain == @strs"
        )
        # only show corrections and not stats
        df = df[
            ["experiment", "strain", "condition"]
            + [col for col in df.columns if "correct" in col]
        ]
        df = df.T
        return df

    def addcolumn(self, newcolumnname, oldcolumn, newcolumnvalues):
        """
        Adds a new column to all dataframes by parsing an existing column.
        All possible entries for the new column are specified as strings and the entry in
        the new column will be whichever of these strings is present in the entry of the
        existing column.

        Parameters
        ----------
        newcolumnname: string
            The name of the new column.
        oldcolumn: string
            The name of the column to be parsed to create the new column.
        newcolumnvalues: list of strings
            All of the possible values for the entries in the new column.

        Example
        -------
        >>> p.addcolumn('medium', 'condition', ['Raffinose',
        ...                                     'Geneticin'])

        will parse each entry in 'condition' to create a new column called 'medium' that has
        either a value 'Raffinose' if 'Raffinose' is in the entry from 'condition' or a value
        'Geneticin' if 'Geneticin' is in the entry from 'condition'.
        """
        for df in [self.r, self.s, self.sc]:
            newcol = np.array(
                ("",) * len(df[oldcolumn].to_numpy()), dtype="object")
            for i, oldcolvalue in enumerate(df[oldcolumn].to_numpy()):
                for newcolvalue in newcolumnvalues:
                    if newcolvalue in oldcolvalue:
                        newcol[i] = newcolvalue
            df[newcolumnname] = newcol

    def addnumericcolumn(
        self,
        newcolumnname,
        oldcolumn,
        picknumber=0,
        leftsplitstr=None,
        rightsplitstr=None,
        asstr=False,
    ):
        """
        Adds a new numeric column by parsing the numbers from the entries of an existing column.
        It is best to run this command only after the basic analyses - ignorewells, correctOD,
        and correctmedia - have been performed because it changes the structure of the dataframes
        and may cause errors.


        Parameters
        ----------
        newcolumnname: string
            The name of the new column.
        oldcolumn: string
            The name of column to be parsed.
        picknumber: integer
            The number to pick from the list of numbers extracted from the existing column's entry.
        leftsplitstr: string, optional
            Split the entry of the column using whitespace and parse numbers from the substring
            to the immediate left of leftsplitstr rather than the whole entry.
        rightsplitstr: string, optional
            Split the entry of the column using whitespace and parse numbers from the substring
            to the immediate right of rightsplitstr rather than the whole entry.
        asstr: boolean
            If True, convert the numeric value to a string to improve plots with seaborn.

        Examples
        --------
        To extract concentrations from conditions use

        >>> p.addnumericcolumn('concentration', 'condition')

        For a condition like '0.5% Raf 0.05ug/mL Cycloheximide', use

        >>> p.addnumericcolumn('raffinose', 'condition',
        ...                     picknumber= 0)
        >>> p.addnumericcolumn('cycloheximide', 'condition',
        ...                     picknumber= 1)
        """
        import re

        # process splitstrs
        if leftsplitstr or rightsplitstr:
            splitstr = leftsplitstr if leftsplitstr else rightsplitstr
            locno = -1 if leftsplitstr else 1
        else:
            splitstr = False
        # change each dataframe
        for df in [self.r, self.s, self.sc]:
            if asstr:
                # new column of strings
                newcol = np.full_like(
                    df[oldcolumn].to_numpy(), "", dtype="object")
            else:
                # new column of floats
                newcol = np.full_like(
                    df[oldcolumn].to_numpy(), np.nan, dtype="float")
            # parse old column
            for i, oldcolvalue in enumerate(df[oldcolumn].to_numpy()):
                if oldcolvalue:
                    # split string first on spaces and then find substring adjacent to specified splitstring
                    if splitstr:
                        if splitstr in oldcolvalue:
                            # oldcolvalue contains leftsplitstring or rightsplitstring
                            bits = oldcolvalue.split()
                            for k, bit in enumerate(bits):
                                if splitstr in bit:
                                    loc = k + locno
                                    break
                            # adjacent string
                            oldcolvalue = bits[loc]
                        else:
                            # oldcolvalue does not contain leftsplitstring or rightsplitstring
                            oldcolvalue = ""
                    # loop through all floats in oldcolvalue
                    nocount = 0
                    for ci in re.split(
                        r"[+-]?([0-9]+(?:[.][0-9]*)?|[.][0-9]+)", oldcolvalue
                    ):
                        try:
                            no = float(ci)
                            if nocount == picknumber:
                                newcol[i] = ci if asstr else no
                                break
                            nocount += 1
                        except ValueError:
                            pass
            df[newcolumnname] = newcol

    def addcommonvar(
        self,
        var="time",
        dvar=None,
        varmin=None,
        varmax=None,
        figs=True,
        experiments="all",
        experimentincludes=False,
        experimentexcludes=False,
        conditions="all",
        conditionincludes=False,
        conditionexcludes=False,
        strains="all",
        strainincludes=False,
        strainexcludes=False,
    ):
        """
        Adds to time-dependent dataframes a common variable whose values only come from a fixed
        array so that they are from the same array for all experiments.
        This common variable allows averaging across experiments and typically is time.

        For example, the plate reader often does not perfectly increment time between measurements
        and different experients can have slightly different time points despite the plate reader
        having the same settings. These unique times prevent seaborn from taking averages.

        If experiments have measurements that start at the same time point and have the same
        interval between measurements, then setting a commontime for all experiments will allow
        seaborn to perform averaging.

        The array of the common variable runs from varmin to varmax with an interval dvar.
        These parameters are automatically calculated, but may be specified.

        Each instance of var is assigned a common value - the closest instance of the common variable to the instance of var.
        Measurements are assumed to the same for the true instance of var and for the assigned common value,
        which may generate errors if these two are sufficiently distinct.

        An alternative method is averageoverexpts.

        Parameters
        ----------
        var: string
            The variable from which the common variable is generated, typically 'time'.
        dvar: float, optional
            The interval between the values comprising the common array.
        varmin: float, optional
            The minimum of the common variable.
        varmax: float, optional
            The maximum of the common variable.
        figs: boolean
            If True, generate plot to check if the variable and the common variable generated
            from it are sufficiently close in value.
        experiments: string or list of strings
            The experiments to include.
        conditions: string or list of strings
            The conditions to include.
        strains: string or list of strings
            The strains to include.
        experimentincludes: string, optional
            Selects only experiments that include the specified string in their name.
        experimentexcludes: string, optional
            Ignores experiments that include the specified string in their name.
        conditionincludes: string, optional
            Selects only conditions that include the specified string in their name.
        conditionexcludes: string, optional
            Ignores conditions that include the specified string in their name.
        strainincludes: string, optional
            Selects only strains that include the specified string in their name.
        strainexcludes: string, optional
            Ignores strains that include the specified string in their name.

        Example
        -------
        To plot averages of time-dependent variables over experiments, use for example

        >>> p.addcommonvar('time')
        >>> p.plot(x= 'commontime', y= 'c-GFPperOD',
        ...        hue= 'condition', style= 'strain')
        """
        exps, cons, strs = self._getall(
            experiments,
            experimentincludes,
            experimentexcludes,
            conditions,
            conditionincludes,
            conditionexcludes,
            strains,
            strainincludes,
            strainexcludes,
            nonull=True,
        )
        print("Finding common" + var)
        for df in [self.r, self.s]:
            if var in df:
                loc = (
                    df.experiment.isin(exps)
                    & df.condition.isin(cons)
                    & df.strain.isin(strs)
                )
                print("r dataframe") if df.equals(
                    self.r) else print("s dataframe")
                if dvar == None:
                    # calculated for tidy printing
                    elen = np.max([len(e) for e in exps]) + 5
                    # find median increment in var
                    for e in exps:
                        evar = df[loc][var].to_numpy()
                        print(
                            " {:{}} {}_min= {:.2e} ; d{}= {:.2e}".format(
                                e,
                                elen,
                                var,
                                np.min(evar),
                                var,
                                np.median(np.diff(evar)),
                            )
                        )
                    ldvar = np.median(np.diff(df[loc][var].to_numpy()))
                else:
                    ldvar = dvar
                print(" Using d{}= {:.2e}".format(var, ldvar))
                lvarmin = df[loc][var].min() if varmin == None else varmin
                print(" Using {}_min= {:.2e}\n".format(var, lvarmin))
                lvarmax = df[loc][var].max() if varmax == None else varmax
                # define common var
                cvar = np.arange(lvarmin, lvarmax, ldvar)
                df.loc[loc, "common" + var] = df[loc][var].apply(
                    lambda x: cvar[np.argmin((x - cvar) ** 2)]
                )
                if figs:
                    plt.figure()
                    sl = np.linspace(df[loc][var].min(),
                                     1.05 * df[loc][var].max(), 100)
                    plt.plot(sl, sl, alpha=0.4)
                    plt.plot(
                        df[loc][var].to_numpy(), df[loc]["common"
                                                         + var].to_numpy(), "."
                    )
                    plt.xlabel(var)
                    plt.ylabel("common" + var)
                    title = "r dataframe" if df.equals(
                        self.r) else "s dataframe"
                    plt.title(title)
                    plt.suptitle(
                        "comparing "
                        + var
                        + " with common"
                        + var
                        + " – the line y= x is expected"
                    )
                    plt.tight_layout()
                    plt.show()

    #####
    # Routines to examine and ignore individual wells
    #####
    def _makewellsdf(self):
        """
        Internal function: makes a dataframe that stores the contents of the wells
        """
        df = self.r[["experiment", "condition",
                     "strain", "well"]].drop_duplicates()
        df = df.reset_index(drop=True)
        return df

    def contentsofwells(self, wlist):
        """
        Displays contents of wells

        Parameters
        ----------
        wlist: string or list of string
            Specifies the well or wells of interest.

        Examples
        --------
        >>> p.contentsofwells(['A1', 'E4'])
        """
        wlist = gu.makelist(wlist)
        for w in wlist:
            print("\n" + w + "\n--")
            print(
                self.wellsdf.query("well == @w")
                .drop(["well"], axis=1)
                .to_string(index=False)
            )

    def showwells(
        self,
        concise=False,
        sortby=False,
        experiments="all",
        conditions="all",
        strains="all",
        experimentincludes=False,
        experimentexcludes=False,
        conditionincludes=False,
        conditionexcludes=False,
        strainincludes=False,
        strainexcludes=False,
    ):
        """
        Displays wells for specified experiments, conditions, and strains.

        Parameters
        ----------
        concise: boolean
            If True, display as experiment: condition: strain.
        sortby: list of strings, optional
            List of column names on which to sort the results.
        experiments: string or list of strings
            The experiments to include.
        conditions: string or list of strings
            The conditions to include.
        strains: string or list of strings
            The strains to include.
        experimentincludes: string, optional
            Selects only experiments that include the specified string in their name.
        experimentexcludes: string, optional
            Ignores experiments that include the specified string in their name.
        conditionincludes: string, optional
            Selects only conditions that include the specified string in their name.
        conditionexcludes: string, optional
            Ignores conditions that include the specified string in their name.
        strainincludes: string, optional
            Selects only strains that include the specified string in their name.
        strainexcludes: string, optional
            Ignores strains that include the specified string in their name.

        Examples
        --------
        >>> p.showwells()
        >>> p.showwells(strains= 'Mal12:GFP', conditions= '1% Mal')
        """
        exps, cons, strs = self._getall(
            experiments,
            experimentincludes,
            experimentexcludes,
            conditions,
            conditionincludes,
            conditionexcludes,
            strains,
            strainincludes,
            strainexcludes,
            nonull=False,
        )
        if not hasattr(self, "wellsdf"):
            self.wellsdf = self._makewellsdf()
        df = self.wellsdf.query(
            "experiment == @exps and condition == @cons and strain == @strs"
        )
        if sortby:
            df = df.sort_values(by=gu.makelist(sortby))
        print()
        for e in exps:
            if concise:
                print(
                    df[["experiment", "condition", "strain"]]
                    .drop_duplicates()
                    .query("experiment == @e")
                    .to_string(index=False)
                )
            else:
                print(df.query("experiment == @e").to_string(index=False))
            print()

    def ignorewells(
        self,
        exclude=[],
        experiments="all",
        experimentincludes=False,
        experimentexcludes=False,
        clearall=False,
    ):
        """
        Allows wells to be ignored in any future processing.
        If called several times, the default behaviour is for any previously ignored wells
        not to be re-instated.

        Parameters
        ---------
        exclude: list of strings
            List of labels of wells on the plate to be excluded.
        experiments: string or list of strings
            The experiments to include.
        experimentincludes: string, optional
            Selects only experiments that include the specified string in their name.
        experimentexcludes: string, optional
            Ignores experiments that include the specified string in their name.
        clearall: boolean
            If True, all previously ignored wells are re-instated.

        Example
        -------
        >>> p.ignorewells(['A1', 'C2'])
        """
        self._logmethod(self.logger)
        if clearall:
            # forget any previously ignoredwells
            self.r = self.origr.copy()
            self.progress["ignoredwells"] = {exp: []
                                             for exp in self.allexperiments}
            self._update_s()
            print(
                "Warning: all corrections and analysis to raw data have been lost. No wells have been ignored."
            )
        else:
            if gu.islistempty(exclude):
                return
            else:
                # exclude should be a list of lists
                if isinstance(exclude, str):
                    exclude = [gu.makelist(exclude)]
                elif isinstance(exclude[0], str):
                    exclude = [exclude]
                # check consistency
                if len(self.allexperiments) == 1:
                    exps = self.allexperiments
                else:
                    exps = self._getexps(
                        experiments, experimentincludes, experimentexcludes
                    )
                if len(exclude) != len(exps) and not clearall:
                    raise _IgnoreWells(
                        "Either a list of wells to exclude for a particular experiment or a list of experiments must be given"
                    )
                else:
                    # drop wells
                    for ex, exp in zip(exclude, exps):
                        # wells cannot be ignored twice
                        wex = list(
                            set(ex) - set(self.progress["ignoredwells"][exp]))
                        # delete wells
                        df = self.r
                        filt = ~((df["experiment"] == exp)
                                 & (df["well"].isin(wex)))
                        df = df.loc[filt]
                        df = df.reset_index(drop=True)
                        self.r = df
                        # store ignoredwells
                        self.progress["ignoredwells"][exp] += ex
                        # remove any duplicates
                        self.progress["ignoredwells"][exp] = list(
                            set(self.progress["ignoredwells"][exp])
                        )
                # remake summary data
                self._update_s()

    #####
    # Routines to make and update the dataframe of summary data (over wells)
    #####
    def _make_s(self, tmin=None, tmax=None):
        """
        Internal function: Calculates means and variances of all datatypes from raw data
        """
        # restrict time
        if tmin and not tmax:
            rdf = self.r[self.r.time >= tmin]
        elif tmax and not tmin:
            rdf = self.r[self.r.time <= tmax]
        elif tmin and tmax:
            rdf = self.r[(self.r.time >= tmin) & (self.r.time <= tmax)]
        else:
            rdf = self.r
        # find means
        df1 = (
            rdf.groupby(["experiment", "condition", "strain", "time"])
            .mean()
            .reset_index()
        )
        for exp in self.allexperiments:
            for dtype in self.datatypes[exp]:
                df1 = df1.rename(columns={dtype: dtype + " mean"})
        # find errors
        df2 = (
            rdf.groupby(["experiment", "condition", "strain", "time"])
            .std()
            .reset_index()
        )
        for exp in self.allexperiments:
            for dtype in self.datatypes[exp]:
                df2 = df2.rename(columns={dtype: dtype + " err"})
        return pd.merge(df1, df2)

    def _update_s(self):
        """
        Internal function: Updates means and errors of all datatypes from raw data
        """
        # find tmin and tmax in case restrict_time has been called
        tmin = self.s.time.min()
        tmax = self.s.time.max()
        # recalculate s dataframe
        self.s.update(self._make_s(tmin, tmax))

    def restricttime(self, tmin=None, tmax=None):
        """
        Restrict the processed data to a range of time, ignoring points outside this
        time range.
        Data is removed from the .s dataframe, but not from the .r dataframe containing
        the raw data.

        Parameters
        ----------
        tmin: float
            The minimum value of time, with data kept only for t >= tmin.
        tmax: float
            The maximum value of time, with data kept only for t <= tmax.

        Example
        -------
        >>> p.restrictime(tmin= 5)
        """
        self.s = self._make_s(tmin, tmax)

    #####
    # Routines for plotting
    #####
    def plot(
        self,
        x="time",
        y="OD",
        hue="strain",
        style="condition",
        size=None,
        kind="line",
        col=None,
        row=None,
        height=5,
        aspect=1,
        ymin=False,
        figsize=False,
        returnfacetgrid=False,
        noshow=False,
        title=False,
        plate=False,
        wells=False,
        nonull=False,
        messages=False,
        sortby=None,
        experiments="all",
        conditions="all",
        strains="all",
        experimentincludes=False,
        experimentexcludes=False,
        conditionincludes=False,
        conditionexcludes=False,
        strainincludes=False,
        strainexcludes=False,
        **kwargs,
    ):
        """
        Plots from the underlying dataframes (chosen automatically) using Seaborn's relplot,
        which is described at
        https://seaborn.pydata.org/generated/seaborn.relplot.html

        Parameters
        ----------
        x: string
            The variable - column of the dataframe - for the x-axis.
        y: string
            The variable - column of the dataframe - for y-axis.
        hue: string
            The variable whose variation will determine the colours of the lines plotted.
            From Seaborn.
        style: string
            The variable whose variation will determine the style of each line.
            From Seaborn.
        size: string
            The variable whose vairation will determine the size of each marker.
            From Seaborn.
        kind: string
            Either 'line' or 'scatter', which determines the type of plot.
            From Seaborn.
        col: string, optional
            The variable that varies over the columns in a multipanel plot.
            From Seaborn.
        row: string, optional
            The variable that varies over the rows in a multipanel plot.
            From Seaborn.
        height: float, optional
            The height of the individual panels in a multipanel plot.
            From Seaborn.
        aspect: float, optional
            The aspect ratio of the individual panels in a multipanel plot.
            From Seaborn.
        ymin: float, optional
            The minimum y-value
        figsize: tuple, optional
            A tuple of (width, height) for the size of figure.
            Ignored if wells= True or plate= True.
        returnfacetgrid: boolean, optional
            If True, return Seaborn's facetgrid object created by relplot
        noshow: boolean, optional
            If True, matplotlib's show is not called when plotting enabling the plots
            to be modified in Jupyter.
        title: float, optional
            The title of the plot (overwrites any default titles).
        plate: boolean, optional
            If True, data for each well for a whole plate are plotted in one figure.
        wells: boolean, optional
            If True, multiple figures are generated that are grouped by wells in the
            plate that have the same strain and condition per experiment.
        nonull: boolean, optional
            If True, 'Null' strains are not plotted.
        sortby: list of strings, optional
            A list of columns to sort the data in the dataframe and passed to
            pandas sort_values.
        messsages: boolean, optional
            If True, print warnings for any data requested but not found.
        experiments: string or list of strings
            The experiments to include.
        conditions: string or list of strings
            The conditions to include.
        strains: string or list of strings
            The strains to include.
        experimentincludes: string, optional
            Selects only experiments that include the specified string in their name.
        experimentexcludes: string, optional
            Ignores experiments that include the specified string in their name.
        conditionincludes: string, optional
            Selects only conditions that include the specified string in their name.
        conditionexcludes: string, optional
            Ignores conditions that include the specified string in their name.
        strainincludes: string, optional
            Selects only strains that include the specified string in their name.
        strainexcludes: string, optional
            Ignores strains that include the specified string in their name.
        kwargs: for Seaborn's relplot
            https://seaborn.pydata.org/generated/seaborn.relplot.html

        Returns
        -------
        sfig: Seaborn's facetgrid object generated by relplot if returnfacetgrid= True

        Examples
        --------
        >>> p.plot(y= 'OD', plate= True)
        >>> p.plot(y= 'OD', wells= True, strainincludes= 'Gal10:GFP')
        >>> p.plot(y= 'OD')
        >>> p.plot(x= 'OD', y= 'gr')
        >>> p.plot(y= 'c-GFPperOD', nonull= True, ymin= 0)
        >>> p.plot(y= 'c-GFPperOD', conditionincludes= '2% Mal',
        ...        hue= 'strain')
        >>> p.plot(y= 'c-mCherryperOD', conditions= ['0.5% Mal',
        ...        '1% Mal'], hue= 'strain', style= 'condition',
        ...         nonull= True, strainincludes= 'mCherry')
        >>> p.plot(y= 'c-GFPperOD', col= 'experiment')
        >>> p.plot(y= 'max gr')
        """
        # choose the correct dataframe
        basedf, dfname = self._plotfinddf(x, y)
        if not np.any(basedf):
            return
        # get experiments, conditions and strains
        exps, cons, strs = self._getall(
            experiments,
            experimentincludes,
            experimentexcludes,
            conditions,
            conditionincludes,
            conditionexcludes,
            strains,
            strainincludes,
            strainexcludes,
            nonull,
        )
        # choose the right type of plot
        if plate:
            # plot each well following the plate's layout
            for e in exps:
                if x == "time":
                    self._plotplate(e, y)
                else:
                    self._plotplate(e, x)
            if not noshow:
                plt.show()
            return None
        elif wells:
            # multiple figures grouping data by wells with the same strain and condition
            for e in exps:
                for c in cons:
                    for s in strs:
                        df = basedf.query(
                            "experiment == @e and condition == @c and strain == @s"
                        )
                        if df.empty:
                            if messages:
                                print(e + ":", "No data found for", s, "in", c)
                        else:
                            sfig = sns.relplot(
                                x=x,
                                y=y,
                                data=df,
                                hue="well",
                                kind=kind,
                                style=style,
                                size=size,
                                **kwargs,
                            )
                            if title:
                                sfig.fig.suptitle(title)
                            else:
                                sfig.fig.suptitle(e + ": " + s + " in " + c)
                            if ymin is not False:
                                plt.ylim(ymin, None)
            if not noshow:
                plt.show()
            return None
        else:
            # plot summary stats
            if dfname == "sc":
                df = basedf.query(
                    "experiment == @exps and condition == @cons and strain == @strs"
                )
                xcols = df.columns[df.columns.str.startswith(x)]
                ycols = df.columns[df.columns.str.startswith(y)]
                df = df[
                    np.unique(
                        ["experiment", "condition", "strain"]
                        + list(xcols)
                        + list(ycols)
                    )
                ].dropna()
                if df.empty:
                    raise _PlotError("No data found")
                else:
                    if sortby:
                        df = df.sort_values(by=gu.makelist(sortby))
                    sfig = sns.relplot(
                        x=x,
                        y=y,
                        data=df,
                        hue=hue,
                        kind="scatter",
                        style=style,
                        size=size,
                        col=col,
                        row=row,
                        aspect=aspect,
                        height=height,
                        **kwargs,
                    )
                    if row == None and col == None:
                        # add error bars
                        # find coordinates of points in relplot
                        xc, yc = [], []
                        for point_pair in sfig.ax.collections:
                            for xp, yp in point_pair.get_offsets():
                                xc.append(xp)
                                yc.append(yp)
                        # add error bars
                        xerr = df[x + " err"] if x + \
                            " err" in df.columns else None
                        yerr = df[y + " err"] if y + \
                            " err" in df.columns else None
                        sfig.ax.errorbar(
                            xc,
                            yc,
                            xerr=xerr,
                            yerr=yerr,
                            fmt=" ",
                            ecolor="dimgray",
                            alpha=0.5,
                        )
            else:
                # plot time series
                df = basedf.query(
                    "experiment == @exps and condition == @cons and strain == @strs"
                )
                if df.empty:
                    raise _PlotError("No data found")
                else:
                    if sortby:
                        df = df.sort_values(by=gu.makelist(sortby))
                    # add warnings for poor choice of seaborn's parameters - may cause inadvertent averaging
                    if hue == style:
                        print(
                            'Warning: "hue" and "style" have both been set to "'
                            + hue
                            + '" and there may be unintended averaging'
                        )
                    if (
                        x != "commontime"
                        and len(df["experiment"].unique()) > 1
                        and hue != "experiment"
                        and size != "experiment"
                        and style != "experiment"
                        and col != "experiment"
                    ):
                        print(
                            'Warning: there are multiple experiments, but neither "hue", "style", nor "size" is set to "experiment" and there may be averaging over experiments'
                        )
                    # augment df to allow seaborn to estimate errors
                    df = self._augmentdf(df, y)
                    # plot
                    sfig = sns.relplot(
                        x=x,
                        y=y,
                        data=df,
                        hue=hue,
                        kind=kind,
                        style=style,
                        ci="sd",
                        size=size,
                        col=col,
                        row=row,
                        aspect=aspect,
                        height=height,
                        **kwargs,
                    )
                    if title:
                        sfig.fig.suptitle(title)
                    if ymin is not False:
                        plt.ylim(ymin, None)
            if figsize and len(figsize) == 2:
                sfig.fig.set_figwidth(figsize[0])
                sfig.fig.set_figheight(figsize[1])
            if not noshow:
                plt.show()
            return sfig if returnfacetgrid else None

    def _plotfinddf(self, x, y):
        """
        Internal function: finds the correct dataframe for plotting y versus x

        Parameters
        ----------
        x: string
            Name of x-variable.
        y: string
            Name of y-variable.

        Returns
        -------
        basedf: dataframe
            The dataframe that contains the x and y variables.
        dfname: string
            The name of the dataframe.
        """
        # choose the correct dataframe
        if hasattr(self, "r") and x in self.r.columns and y in self.r.columns:
            # raw data (with wells)
            basedf = self.r
            dfname = "r"
        elif x in self.s.columns and y in self.s.columns:
            # processed data (no wells)
            basedf = self.s
            dfname = "s"
        elif x in self.sc.columns and y in self.sc.columns:
            # summary stats
            basedf = self.sc
            dfname = "sc"
        else:
            raise _PlotError(
                "The variables x= "
                + x
                + " and y= "
                + y
                + " cannot be plotted against each other because they are not in the same dataframe"
            )
        return basedf, dfname

    def _plotplate(self, exp, dtype):
        """
        Internal function: plots the data for each well following the layout of a 96-well plate.

        Parameters
        --
        exp: float
            The name of the experiment.
        dtype: float
            The data type to be plotted: 'OD', 'GFP', etc.
        """
        plt.figure()
        # first create an empty plate - in case of missing wells
        ax = []
        for rowl in range(8):
            for coll in np.arange(1, 13):
                sindex = coll + 12 * rowl
                axi = plt.subplot(8, 12, sindex)
                ax.append(axi)
                plt.tick_params(labelbottom=False, labelleft=False)
                # label well locations
                for j in range(12):
                    if sindex == j + 1:
                        plt.title(j + 1)
                for j, k in enumerate(np.arange(1, 96, 12)):
                    if sindex == k:
                        plt.ylabel("ABCDEFGH"[j] + " ", rotation=0)
        # fill in the wells that have been measured
        for pl in self.r.query("experiment == @exp")["well"].unique():
            rowl = "ABCDEFGH".index(pl[0])
            coll = int(pl[1:])
            sindex = coll + 12 * rowl
            wd = self.r.query("experiment == @exp and well == @pl")
            ax[sindex - 1].plot(wd["time"].to_numpy(),
                                wd[dtype].to_numpy(), "-")
        plt.suptitle(exp + ": " + dtype)
        plt.show()

    def getdataframe(
        self,
        dfname="s",
        experiments="all",
        conditions="all",
        strains="all",
        experimentincludes=False,
        experimentexcludes=False,
        conditionincludes=False,
        conditionexcludes=False,
        strainincludes=False,
        strainexcludes=False,
        nonull=True,
    ):
        """
        Obtain a subset of the data in a dataframe, which can be used plotting directly.

        Parameters
        ---------
        dfname: string
            The dataframe of interest either 'r' (raw data), 's' (default; processed data),
            or 'sc' (summary statistics).
        experiments: string or list of strings
            The experiments to include.
        conditions: string or list of strings
            The conditions to include.
        strains: string or list of strings
            The strains to include.
        experimentincludes: string, optional
            Selects only experiments that include the specified string in their name.
        experimentexcludes: string, optional
            Ignores experiments that include the specified string in their name.
        conditionincludes: string, optional
            Selects only conditions that include the specified string in their name.
        conditionexcludes: string, optional
            Ignores conditions that include the specified string in their name.
        strainincludes: string, optional
            Selects only strains that include the specified string in their name.
        strainexcludes: string, optional
            Ignores strains that include the specified string in their name.
        nonull: boolean, optional
            If True, ignore 'Null' strains

        Returns
        -------
        ndf: dataframe

        Example
        -------
        >>> ndf= p.getdataframe('s', conditions= ['2% Glu'],
        ...                     nonull= True)
        """
        exps, cons, strs = self._getall(
            experiments,
            experimentincludes,
            experimentexcludes,
            conditions,
            conditionincludes,
            conditionexcludes,
            strains,
            strainincludes,
            strainexcludes,
            nonull,
        )
        if hasattr(self, dfname):
            df = getattr(self, dfname)
            ndf = df.query(
                "experiment == @exps and condition == @cons and strain == @strs"
            )
            if ndf.empty:
                print("No data found")
            else:
                return ndf.copy()
        else:
            raise _UnknownDataFrame(
                "Dataframe " + dfname + " is not recognised")

    #####
    def savefigs(self, fname=None, onefile=True):
        """
        Saves all current figures to PDF, either to one file or each to a separate file.

        Parameters
        ----------
        fname: string, optional
            Name of file. If unspecified, the name of the experiment is used.
        onefile: boolean, optional
            If False, each figures is save to its own PDF file.

        Example
        -------
        >>> p.savefigs()
        >>> p.savefigs('figures.pdf')
        """
        if fname:
            if ".pdf" not in fname:
                fname += ".pdf"
            fname = self.wdir + fname
        else:
            fname = self.wdir + "".join(self.allexperiments) + ".pdf"
        if onefile:
            gu.figs2pdf(fname)
        else:
            for i in plt.get_fignums():
                plt.figure(i)
                savename = str(plt.getp(plt.gcf(), "axes")
                               [0].title).split("'")[1]
                savename = savename.replace(" ", "_")
                if savename == "":
                    savename = "Whole_plate_Figure_" + str(i)
                print("Saving", savename)
                plt.savefig(self.wdir + savename + ".pdf")

    #####
    def close(self):
        """
        Close all figures.

        Example
        -------
        >>> p.close()
        """
        plt.close("all")

    #####
    # Internal functions
    #####
    def _getsubset(
        self,
        type,
        set="all",
        includes=False,
        excludes=False,
        nonull=False,
        nomedia=False,
    ):
        """
        Internal function: returns a subset of either the conditions or strains.

        Parameters
        --
        type: string
            Either 'c' (conditions) or 's' (strains).
        set: list of strings
            List of items to include (default is 'all').
        includes: string
            Select only items with this string in their name.
        excludes: string
            Ignore any items with this string in their name.
        nonull: boolean
            If True, ignore Null strain.
        nomedia: boolean
            If True, ignores 'media' condition.

        Returns
        -------
        sset: list of strings
        """
        if set == "all" or includes or excludes:
            if type == "c":
                sset = list(
                    np.unique(
                        [
                            con
                            for e in self.allconditions
                            for con in self.allconditions[e]
                        ]
                    )
                )
                if nomedia and "media" in sset:
                    sset.pop(sset.index("media"))
            elif type == "s":
                sset = list(
                    np.unique(
                        [str for e in self.allstrains for str in self.allstrains[e]]
                    )
                )
                if nonull and "Null" in sset:
                    sset.pop(sset.index("Null"))
            else:
                sset = self.allexperiments
            # find those items containing keywords given in 'includes'
            if includes:
                includes = gu.makelist(includes)
                newset = []
                for s in sset:
                    gotone = 0
                    for item in includes:
                        if item in s:
                            gotone += 1
                    if gotone == len(includes):
                        newset.append(s)
                sset = newset
            # remove any items containing keywords given in 'excludes'
            if excludes:
                excludes = gu.makelist(excludes)
                exs = []
                for s in sset:
                    for item in excludes:
                        if item in s:
                            exs.append(s)
                            break
                for ex in exs:
                    sset.pop(sset.index(ex))
        else:
            sset = gu.makelist(set)
        if sset:
            # sort by numeric values in list entries
            return sorted(sset, key=gu.natural_keys)
        else:
            if includes:
                raise __getsubset("Nothing found for "
                                  + " and ".join(includes))
            else:
                raise __getsubset("Nothing found")

    def _getexps(self, experiments, experimentincludes, experimentexcludes):
        """
        Internal function: returns list of experiments
        """
        if experimentincludes or experimentexcludes:
            exps = self._getsubset(
                "e", includes=experimentincludes, excludes=experimentexcludes
            )
        elif experiments == "all":
            exps = self.allexperiments
        else:
            exps = gu.makelist(experiments)
        return exps

    def _getcons(self, conditions, conditionincludes, conditionexcludes, nomedia):
        """
        Internal function: returns list of conditions
        """
        if conditionincludes or conditionexcludes:
            cons = self._getsubset(
                "c",
                includes=conditionincludes,
                excludes=conditionexcludes,
                nomedia=nomedia,
            )
        elif conditions == "all":
            cons = list(
                np.unique(
                    [con for e in self.allconditions for con in self.allconditions[e]]
                )
            )
            if nomedia and "media" in cons:
                cons.pop(cons.index("media"))
        else:
            cons = gu.makelist(conditions)
        return sorted(cons, key=gu.natural_keys)

    def _getstrs(self, strains, strainincludes, strainexcludes, nonull):
        """
        Internal function: returns list of strains
        """
        if strainincludes or strainexcludes:
            strs = self._getsubset(
                "s", includes=strainincludes, excludes=strainexcludes, nonull=nonull
            )
        elif strains == "all":
            strs = list(
                np.unique(
                    [str for e in self.allstrains for str in self.allstrains[e]])
            )
            if nonull and "Null" in strs:
                strs.pop(strs.index("Null"))
        else:
            strs = gu.makelist(strains)
        if nonull and "Null" in strs:
            strs.pop(strs.index("Null"))
        return sorted(strs, key=gu.natural_keys)

    def _getall(
        self,
        experiments,
        experimentincludes,
        experimentexcludes,
        conditions,
        conditionincludes,
        conditionexcludes,
        strains,
        strainincludes,
        strainexcludes,
        nonull=True,
        nomedia=True,
    ):
        """
        Internal function: returns experiments, conditions, and strains
        """
        exps = self._getexps(
            experiments, experimentincludes, experimentexcludes)
        cons = self._getcons(conditions, conditionincludes,
                             conditionexcludes, nomedia)
        strs = self._getstrs(strains, strainincludes, strainexcludes, nonull)
        return exps, cons, strs

    def _extractwells(self, experiment, condition, strain, datatypes):
        """
        Internal function: extracts a list of matrices for each dtype in datatypes for the given
        experiment, condition, and strain with each column in each matrix having the data for one well
        """
        datatypes = gu.makelist(datatypes)
        # restrict time if necessary
        rdf = self.r[
            (self.r.time >= self.s.time.min()) & (
                self.r.time <= self.s.time.max())
        ]
        # extract data
        df = rdf.query(
            "experiment == @experiment and condition == @condition and strain == @strain"
        )
        matrices = []
        for dtype in datatypes:
            df2 = df[[dtype, "well"]]
            df2well = df2.groupby("well")[dtype].apply(list)
            matrices.append(np.transpose([df2well[w] for w in df2well.index]))
        if len(datatypes) == 1:
            # return array
            return matrices[0]
        else:
            # return list of arrays
            return matrices

    def _augmentdf(self, df, datatype):
        """
        Internal function: artifically augments dataframe using 'err' (if present in the
        dataframe) to allow Seaborn to generate errors.

        Note the sqrt(3) is necessary because seaborn calculates the standard deviation
        from the augmented data (the mean, the mean + std, and the mean - std) and so
        would get std/sqrt(3) because there are three data points.
        """
        if datatype + " err" in df:
            derr = datatype + " err"
        elif "mean" in datatype and datatype.split(" mean")[0] + " err" in df:
            derr = datatype.split(" mean")[0] + " err"
        else:
            derr = False
        if derr:
            df.insert(0, "augtype", "mean")
            mn = df[datatype].to_numpy()
            err = df[derr].to_numpy()
            # add std
            dfp = df.copy()
            dfp[datatype] = mn + np.sqrt(3) * err
            dfp["augtype"] = "+err"
            # minus std
            dfm = df.copy()
            dfm[datatype] = mn - np.sqrt(3) * err
            dfm["augtype"] = "-err"
            # append
            df = df.append([dfp, dfm], ignore_index=True)
        return df

    #####
    # OD correction
    #####
    def correctOD(
        self,
        figs=True,
        odmatch=0.3,
        experiments="all",
        experimentincludes=False,
        experimentexcludes=False,
        conditions="all",
        conditionincludes=False,
        conditionexcludes=False,
    ):
        """
        Corrects OD data for the non-linear relationship between OD and cell number.
        Requires a set of dilution data set, with the default being haploid yeast
        growing in glucose (collected by L Bandiera).
        An alternative can be loaded from a file - a txt file of two columns with OD
        specified in the first column and the dilution factor specified in descending
        order in the second.

        Parameters
        ---------
        figs: boolean, optional
            If True, a plot of the fit to the dilution data is produced.
        odmatch: float, optional
            If non-zero, then the corrected OD is rescaled to equal the measured OD
            at this value. Only large ODs typically need to be corrected.
        experiments: string or list of strings
            The experiments to include.
        conditions: string or list of strings
            The conditions to include.
        experimentincludes: string, optional
            Selects only experiments that include the specified string in their name.
        experimentexcludes: string, optional
            Ignores experiments that include the specified string in their name.
        conditionincludes: string, optional
            Selects only conditions that include the specified string in their name.
        conditionexcludes: string, optional
            Ignores conditions that include the specified string in their name.

        Examples
        -------
        >>> p.correctOD()
        >>> p.correctOD(figs= False)
        """
        self._logmethod(self.logger)
        exps = self._getexps(
            experiments, experimentincludes, experimentexcludes)
        cons = self._getcons(
            conditions, conditionincludes, conditionexcludes, nomedia=False
        )
        for exp in exps:
            for c in cons:
                if self.sc[(self.sc.experiment == exp) & (self.sc.condition == c)][
                    "OD corrected"
                ].any():
                    print(exp, ": OD is already corrected for", c)
                else:
                    # fit dilution data
                    if not self.progress["gc"][exp]:
                        ODfname = (
                            self.wdir + self.progress["ODfname"][exp]
                            if self.progress["ODfname"][exp]
                            else None
                        )
                        self._findODcorrection(
                            ODfname,
                            exp,
                            figs,
                            odmatch,
                        )
                    # correct all wells
                    gc = self.progress["gc"][exp]
                    gc.batchpredict(
                        self.r.query("experiment == @exp and condition == @c")[
                            "OD"
                        ].to_numpy()
                    )
                    # update r dataframe
                    self.r.loc[
                        (self.r.experiment == exp) & (
                            self.r.condition == c), "OD"
                    ] = gc.f
                    # flag corrections in summary stats dataframe
                    self.sc.loc[
                        (self.sc.experiment == exp) & (self.sc.condition == c),
                        "OD corrected",
                    ] = True
        # update s dataframe
        self._update_s()

    #####
    def _findODcorrection(self, ODfname, exp, figs, odmatch):
        """
        Internal function: Uses a Gaussian process to fit serial dilution data to
        correct for non-linearities in the relationship between OD and cell density.
        The data are either loaded from file ODfname or the default data for haploid
        yeast growing in glucose are used (collected by L Bandiera).
        """
        print("Fitting dilution data for OD correction for non-linearities")
        if ODfname:
            try:
                od, dilfac = np.loadtxt(ODfname, unpack=True)
                print("Using", ODfname)
            except (FileNotFoundError, OSError) as err:
                raise _FileNotFound(self.wdir + ODfname)
        else:
            print("Using default data for haploid yeast in glucose")
            # Lucia's data
            od = np.array(
                [
                    1.38192778,
                    1.15388333,
                    0.96450556,
                    0.78569444,
                    0.61685,
                    0.45291666,
                    0.33923888,
                    0.24501666,
                    0.18033889,
                    0.12463889,
                    0.08463889,
                    0.05783889,
                    0.04019444,
                    0.01776111,
                    0.01790556,
                    0.66888333,
                    0.47343889,
                    0.35310556,
                    0.25619444,
                    0.18245,
                    0.19291667,
                    0.12428333,
                    0.08719444,
                    0.05910555,
                    0.04203889,
                    0.02910556,
                    0.02035,
                    0.01392778,
                    0.00946111,
                    0.00651666,
                    1.06491665,
                    0.85690557,
                    0.71552777,
                    0.52646112,
                    0.39376111,
                    0.28846111,
                    0.20293889,
                    0.14296111,
                    0.10538333,
                    0.07017222,
                    0.04939444,
                    0.03397222,
                    0.02639445,
                    0.01780556,
                    0.01463889,
                    0.34130555,
                    0.21385,
                    0.15140556,
                    0.10612778,
                    0.07330556,
                    0.05147222,
                    0.03702778,
                    0.02599445,
                    0.01739444,
                    0.01188333,
                    0.00956111,
                    0.00572778,
                    0.00491667,
                    0.00275,
                    0.00316111,
                ]
            )
            dilfac = np.array(
                [
                    1.0000000e00,
                    7.1968567e-01,
                    5.1794747e-01,
                    3.7275937e-01,
                    2.6826958e-01,
                    1.9306977e-01,
                    1.3894955e-01,
                    1.0000000e-01,
                    7.1968570e-02,
                    5.1794750e-02,
                    3.7275940e-02,
                    2.6826960e-02,
                    1.9306980e-02,
                    1.3894950e-02,
                    1.0000000e-02,
                    3.0484230e-01,
                    2.1939064e-01,
                    1.5789230e-01,
                    1.1363283e-01,
                    8.1779920e-02,
                    5.8855830e-02,
                    4.2357700e-02,
                    3.0484230e-02,
                    2.1939060e-02,
                    1.5789230e-02,
                    1.1363280e-02,
                    8.1779900e-03,
                    5.8855800e-03,
                    4.2357700e-03,
                    3.0484200e-03,
                    4.4830728e-01,
                    3.2264033e-01,
                    2.3219962e-01,
                    1.6711074e-01,
                    1.2026721e-01,
                    8.6554590e-02,
                    6.2292100e-02,
                    4.4830730e-02,
                    3.2264030e-02,
                    2.3219960e-02,
                    1.6711070e-02,
                    1.2026720e-02,
                    8.6554600e-03,
                    6.2292100e-03,
                    4.4830700e-03,
                    7.7885310e-02,
                    5.6052940e-02,
                    4.0340500e-02,
                    2.9032480e-02,
                    2.0894260e-02,
                    1.5037300e-02,
                    1.0822130e-02,
                    7.7885300e-03,
                    5.6052900e-03,
                    4.0340500e-03,
                    2.9032500e-03,
                    2.0894300e-03,
                    1.5037300e-03,
                    1.0822100e-03,
                    7.7885000e-04,
                ]
            )
        # process data
        dilfac = dilfac[np.argsort(od)]
        od = np.sort(od)
        if odmatch:
            # rescale so that OD and dilfac match as a particular OD
            # compares better with Warringer & Blomberg, Yeast 2003, and rescaled OD is larger
            dilfacmatch = interp1d(od, dilfac)(odmatch)
            y = dilfac / dilfacmatch * odmatch
        else:
            y = dilfac
        # run Gaussian process
        gc = gp.sqexplinGP(
            {0: (-4, 2), 1: (-3, 1), 2: (-6, 1), 3: (-6, 1)}, od, y)
        gc.findhyperparameters(noruns=5, exitearly=True, quiet=True)
        gc.predict(od)
        if figs:
            plt.figure()
            gc.sketch(".")
            # plt.xlim([0, 1.05 * np.max(np.concatenate((od, y)))])
            # plt.ylim([0, 1.05 * np.max(np.concatenate((od, y)))])
            # plt.gca().set_aspect("equal", adjustable="box")
            # plt.draw()
            plt.grid(True)
            plt.xlabel("OD")
            plt.ylabel("corrected OD (relative cell numbers)")
            if ODfname:
                plt.title("Fitting " + ODfname)
            else:
                plt.title("for haploid budding yeast in glucose")
            plt.show()
        self.progress["gc"][exp] = gc
        # copy gc to experiments with the same ODfname
        for e in self.allexperiments:
            if self.progress["ODfname"][e] == self.progress["ODfname"][exp]:
                self.progress["gc"][e] = gc

    #####
    # Media correction
    #####
    def correctmedia(
        self,
        datatypes="all",
        commonmedia=False,
        experiments="all",
        experimentincludes=False,
        experimentexcludes=False,
        conditions="all",
        conditionincludes=False,
        conditionexcludes=False,
        figs=False,
        log=True,
        frac=0.33,
    ):
        """
        Corrects OD or fluorescence for the OD or fluorescence of the media
        using data from wells marked Null.
        Uses lowess to smooth measurements of from all Null wells and subtracts
        this smoothed time series from the raw data.

        Parameters
        ----------
        datatypes: string or list of strings
            Data types to be corrected.
        commonmedia: string
            A condition containing Null wells that should be used to correct
            media for other conditions.
        experiments: string or list of strings
            The experiments to include.
        conditions: string or list of strings
            The conditions to include.
        experimentincludes: string, optional
            Selects only experiments that include the specified string in their name.
        experimentexcludes: string, optional
            Ignores experiments that include the specified string in their name.
        conditionincludes: string, optional
            Selects only conditions that include the specified string in their name.
        conditionexcludes: string, optional
            Ignores conditions that include the specified string in their name.
        figs: boolean, optional
            If True, display fits to data for the Null wells.
        log: boolean, optional
            If False, call will not be added to the log.
        frac: float
            The fraction of the data used for smoothing via lowess.
            https://www.statsmodels.org/devel/generated/statsmodels.nonparametric.smoothers_lowess.lowess.html

        Examples
        --------
        >>> p.correctmedia()
        >>> p.correctmedia('OD')
        >>> p.correctmedia(commonmedia= '1% Glu')
        """
        if log:
            self._logmethod(self.logger)
        exps = self._getexps(
            experiments, experimentincludes, experimentexcludes)
        cons = self._getcons(
            conditions, conditionincludes, conditionexcludes, nomedia=False
        )
        for exp in exps:
            # data types
            expdatatypes = (
                self.datatypes[exp] if datatypes == "all" else gu.makelist(
                    datatypes)
            )
            # correct for media
            for dtype in expdatatypes:
                for c in cons:
                    if self.sc[(self.sc.experiment == exp) & (self.sc.condition == c)][
                        dtype + " corrected for media"
                    ].any():
                        print(exp + ":", dtype,
                              "is already corrected for media in", c)
                    else:
                        print(exp + ": Correcting", dtype, "for media in", c)
                        cm = commonmedia if commonmedia else c
                        # update r dataframe
                        success = self._performmediacorrection(
                            dtype, exp, c, figs, cm, frac
                        )
                        if success:
                            self.sc.loc[
                                (self.sc.experiment == exp) & (
                                    self.sc.condition == c),
                                dtype + " corrected for media",
                            ] = True
            if self.progress["negativevalues"][exp]:
                print(
                    "\nWarning: correcting media has created negative values in",
                    exp,
                    "for",
                )
                print(self.progress["negativevalues"][exp])
        # update s dataframe
        self._update_s()

    #####
    def _performmediacorrection(self, dtype, exp, condition, figs, commonmedia, frac):
        """
        Internal function: Uses lowess to smooth the media data from Null wells over time
        and subtracts the smoothed values from the data.
        """
        # find data for correction with condition equal to commonmedia
        df = self.r.query(
            "experiment == @exp and condition == @commonmedia and strain == 'Null'"
        )
        if df.empty:
            # no data
            print(
                ' No well annotated "Null" was found for',
                commonmedia,
                "in experiment",
                exp,
            )
            print(" Correcting for media for", dtype,
                  "in", commonmedia, "abandoned!")
            return False
        else:
            # there is data - change r dataframe
            r = self.r
            rtest = (r.experiment == exp) & (r.condition == condition)
            t, data = df["time"].to_numpy(), df[dtype].to_numpy()
            # find correction
            res = lowess(data, t, frac=frac)
            correctionfn = interp1d(
                res[:, 0],
                res[:, 1],
                fill_value=(res[0, 1], res[-1, 1]),
                bounds_error=False,
            )
            if figs:
                plt.figure()
                plt.plot(t, data, "ro", res[:, 0], res[:, 1], "b-")
                plt.xlabel("time (hours)")
                plt.title(exp + ": media correction for "
                          + dtype + " in " + condition)
                plt.show()
            # perform correction
            r.loc[rtest, dtype] = r[rtest][dtype] - \
                correctionfn(r[rtest]["time"])
            # check for any negative values
            for s in np.unique(r[rtest]["strain"][r[rtest][dtype] < 0]):
                if s != "Null":
                    wstr = "\t" + dtype + ": " + s + " in " + condition + " for wells "
                    for well in np.unique(
                        r[rtest][r[rtest].strain == s]["well"][r[rtest][dtype] < 0]
                    ):
                        wstr += well + " "
                    wstr += "\n"
                    if not self.progress["negativevalues"][exp]:
                        self.progress["negativevalues"][exp] = wstr
                    else:
                        self.progress["negativevalues"][exp] += wstr

    #####
    # Statistical analysis
    #####
    def getstats(
        self,
        dtype="OD",
        bd=False,
        cvfn="matern",
        esterrs=False,
        noruns=10,
        exitearly=True,
        noinits=100,
        nosamples=100,
        logs=True,
        iskip=False,
        stats=True,
        figs=True,
        findareas=False,
        plotlocalmax=True,
        showpeakproperties=False,
        experiments="all",
        experimentincludes=False,
        experimentexcludes=False,
        conditions="all",
        conditionincludes=False,
        conditionexcludes=False,
        strains="all",
        strainincludes=False,
        strainexcludes=False,
        **kwargs,
    ):
        """
        Calls fitderiv.py to estimate the first and second time-derivatives of, typically,
        OD using a Gaussian process (Swain et al., 2016) and find corresponding summary
        statistics.

        The derivatives are stored in the .s dataframe; summary statistics are stored
        in the .sc dataframe.

        Parameters
        ----------
        dtype: string, optional
            The type of data - 'OD', 'GFP', 'c-GFPperOD', or 'c-GFP' - for which the
            derivatives are to be found. The data must exist in the .r or .s dataframes.
        bd: dictionary, optional
            The bounds on the hyperparameters for the Gaussian process.
            For example, bd= {1: [-2,0])} fixes the bounds on the hyperparameter controlling
            flexibility to be 1e-2 and 1e0.
            The default for a Matern covariance function is
                {0: (-5,5), 1: (-4,4), 2: (-5,2)},
            where the first element controls amplitude, the second controls flexibility, and
            the third determines the magnitude of the measurement error.
        cvfn: string, optional
            The covariance function used in the Gaussian process, either 'matern' or 'sqexp'
            or 'nn'.
        esterrs: boolean, optional
            If True, measurement errors are empirically estimated from the variance across
            replicates at each time point and so vary with time.
            If False, the magnitude of the measurement error is fit from the data assuming
            that this magnitude is the same at all time points.
        noruns: integer, optional
            The number of attempts made for each fit. Each attempt is made with random
            initial estimates of the hyperparameters within their bounds.
        exitearly: boolean, optional
            If True, stop at the first successful fit.
            If False, use the best fit from all successful fits.
        noinits: integer, optional
            The number of random attempts to find a good initial condition before running the
            optimization.
        nosamples: integer, optional
            The number of samples used to calculate errors in statistics by bootstrapping.
        logs: boolean, optional
            If True, find the derivative of the log of the data and should be True to
            determine the specific growth rate when dtype= 'OD'.
        iskip: integer, optional
            Use only every iskip'th data point to increase speed.
        stats: boolean, optional
            If False, do not calculate statistics.
        figs: boolean, optional
            If True, plot both the fits and inferred derivative.
        findareas: boolean, optional
            If True, find the area under the plot of gr vs OD and the area under the plot
            of OD vs time. Setting to True can make getstats slow.
        plotlocalmax: boolean, optional
            If True, mark the highest local maxima found, which is used to calculate
            statistics, on any plots.
        showpeakproperties: boolean, optional
            If True, show properties of any local peaks that have found by scipy's
            find_peaks. Additional properties can be specified as kwargs and are
            passed to find_peaks.
        experiments: string or list of strings
            The experiments to include.
        conditions: string or list of strings
            The conditions to include.
        strains: string or list of strings
            The strains to include.
        experimentincludes: string, optional
            Selects only experiments that include the specified string in their name.
        experimentexcludes: string, optional
            Ignores experiments that include the specified string in their name.
        conditionincludes: string, optional
            Selects only conditions that include the specified string in their name.
        conditionexcludes: string, optional
            Ignores conditions that include the specified string in their name.
        strainincludes: string, optional
            Selects only strains that include the specified string in their name.
        strainexcludes: string, optional
            Ignores strains that include the specified string in their name.
        kwargs: for scipy's find_peaks
            To set the minimum property of a peak. e.g. prominence= 0.1 and width= 15
            (specified in numbers of x-points or y-points and not real units).
            https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.find_peaks.html

        Examples
        --------
        >>> p.getstats()
        >>> p.getstats(conditionincludes= 'Gal')
        >>> p.getstats(noruns= 10, exitearly= False)

        If the fits are poor, often changing the bounds on the hyperparameter for the
        measurement error helps:

        >>> p.getstats(bd= {2: (-3,0)})

        References
        ----------
        PS Swain, K Stevenson, A Leary, LF Montano-Gutierrez, IB Clark, J Vogel, T Pilizota.
        (2016). Inferring time derivatives including cell growth rates using Gaussian
        processes. Nat Commun, 7, 1-8.
        """
        self._logmethod(self.logger)
        linalgmax = 5
        warnings = ""
        if dtype == "OD":
            snames = ["max gr", "time of max gr",
                      "doubling time", "max OD", "lag time"]
            ylabels = ["log(OD)", "gr"]
        else:
            snames = [
                "max d/dt of " + dtype,
                "time of max d/dt of " + dtype,
                "inverse of max d/dt of " + dtype,
                "max " + dtype,
                "lag time of " + dtype,
            ]
            ylabels = [dtype, "d/dt " + dtype]
        # extract data
        exps, cons, strs = self._getall(
            experiments,
            experimentincludes,
            experimentexcludes,
            conditions,
            conditionincludes,
            conditionexcludes,
            strains,
            strainincludes,
            strainexcludes,
        )
        # find growth rate and stats
        for e in exps:
            for c in cons:
                for s in strs:
                    figtitle = e + ": " + s + " in " + c
                    if dtype in self.r.columns:
                        # raw data
                        d = self._extractwells(e, c, s, dtype)
                    elif dtype in self.s.columns:
                        # processed data
                        df = self.s.query(
                            "experiment == @e and condition == @c and strain == @s"
                        )
                        d = df[dtype].to_numpy()
                    else:
                        print(dtype, "not recognized for", figtitle)
                        return
                    # checks
                    if d.size == 0:
                        # no data
                        break
                    if dtype != "OD":
                        # should be a variance
                        esterrs = (df[dtype + " err"].to_numpy()) ** 2
                    print("\nFitting", dtype, "for", figtitle)
                    t = self.s.query(
                        "experiment == @e and condition == @c and strain == @s"
                    )["time"].to_numpy()
                    # call fitderiv
                    f = fitderiv(
                        t,
                        d,
                        figs=False,
                        cvfn=cvfn,
                        logs=logs,
                        bd=bd,
                        esterrs=esterrs,
                        statnames=snames,
                        noruns=noruns,
                        noinits=noinits,
                        exitearly=exitearly,
                        linalgmax=linalgmax,
                        nosamples=nosamples,
                        iskip=iskip,
                    )
                    if figs:
                        plt.figure()
                        plt.subplot(2, 1, 1)
                        f.plotfit("f", ylabel=ylabels[0], figtitle=figtitle)
                        axgr = plt.subplot(2, 1, 2)
                        f.plotfit("df", ylabel=ylabels[1])
                        plt.tight_layout()
                    # find summary statistics
                    outdf, statsdict, warning = self._findsummarystats(
                        dtype,
                        nosamples,
                        f,
                        t,
                        e,
                        c,
                        s,
                        findareas,
                        figs,
                        plotlocalmax,
                        axgr,
                        showpeakproperties,
                        **kwargs,
                    )
                    if warning:
                        warnings += warning
                    # store results in global dataframes
                    statsdict[dtype + " logmaxlike"] = f.logmaxlike
                    statsdict[dtype + " gp"] = cvfn
                    if stats:
                        for sname in f.ds.keys():
                            statsdict[sname] = f.ds[sname]
                    # add growth rates, etc., to dataframe of summary data
                    if (dtype == "OD" and "gr" not in self.s.columns) or (
                        dtype != "OD" and "f" + dtype not in self.s.columns
                    ):
                        # add new columns to dataframe
                        self.s = pd.merge(self.s, outdf, how="outer")
                    else:
                        # update dataframe
                        self.s = gu.absorbdf(
                            self.s, outdf, ["experiment",
                                            "condition", "strain", "time"]
                        )
                    # create or add summary stats to stats dataframe
                    statsdf = pd.DataFrame(
                        statsdict, index=pd.RangeIndex(0, 1, 1))
                    if dtype + " logmaxlike" not in self.sc.columns:
                        # add new columns to dataframe
                        self.sc = pd.merge(self.sc, statsdf, how="outer")
                    else:
                        # update dataframe
                        self.sc = gu.absorbdf(
                            self.sc, statsdf, [
                                "experiment", "condition", "strain"]
                        )
                    if figs:
                        plt.show()
        self._cleansc()
        if warnings:
            print(warnings)

    def _statserr(self, d):
        """
        Internal function: errors in statistics calculated from samples from a Gaussian
        process are half the interquartile range (consist with fitderiv).
        """
        return gu.findiqr(d) / 2

    def _cleansc(self):
        """
        Internal function: ensure that NaNs do not change numeric variables from being floats.
        """
        floatvars = [
            "log2 OD ratio",
            "log2 OD ratio err",
            "local max gr",
            "local max gr err",
            "time of local max gr",
            "time of local max gr err",
            "area under gr vs OD",
            "area under gr vs OD err",
            "normalized area under gr vs OD",
            "normalized area under gr vs OD err",
            "area under OD",
            "area under OD err",
            "normalized area under OD",
            "normalized area under OD err",
            "OD logmaxlike",
            "max gr",
            "max gr err",
            "time of max gr",
            "time of max gr err",
            "doubling time",
            "doubling time err",
            "max OD",
            "max OD err",
            "lag time",
            "lag time err",
        ]
        for var in floatvars:
            if var in self.sc.columns:
                self.sc[var] = self.sc[var].astype(float)

    def _findsummarystats(
        self,
        dtype,
        nosamples,
        f,
        t,
        e,
        c,
        s,
        findareas,
        figs,
        plotlocalmax,
        axgr,
        showpeakproperties,
        **kwargs,
    ):
        """
        Internal function: finds summary statistics from GP fit to time series of dtype
        """
        warning = None
        if dtype != "OD":
            # not OD
            outdf = pd.DataFrame(
                {
                    "experiment": e,
                    "condition": c,
                    "strain": s,
                    "time": t,
                    "f" + dtype: f.f,
                    "f" + dtype + " err": np.sqrt(f.fvar),
                    "d/dt " + dtype: f.df,
                    "d/dt " + dtype + " err": np.sqrt(f.dfvar),
                    "d2/dt2 " + dtype: f.ddf,
                    "d2/dt2 " + dtype + " err": np.sqrt(f.ddfvar),
                }
            )
            statsdict = {"experiment": e, "condition": c, "strain": s}
        else:
            # OD
            outdf = pd.DataFrame(
                {
                    "experiment": e,
                    "condition": c,
                    "strain": s,
                    "time": t,
                    "flogOD": f.f,
                    "flogOD err": np.sqrt(f.fvar),
                    "gr": f.df,
                    "gr err": np.sqrt(f.dfvar),
                    "d/dt gr": f.ddf,
                    "d/dt gr err": np.sqrt(f.ddfvar),
                }
            )
            # check growth rate has been sensibly defined
            if (
                np.max(np.abs(f.df)) < 1.0e-20
                and np.max(np.abs(np.diff(f.dfvar))) < 1.0e-20
            ):
                warning = (
                    "\nWarning: finding gr may have failed for "
                    + e
                    + ": "
                    + s
                    + " in "
                    + c
                )
            # store GP to use in correcting autofluorescence
            self.progress["getstatsGP"][e][c][s] = f
            # find summary statistics
            fs, gs, hs = f.fitderivsample(nosamples)
            # log2 OD ratio
            dr = np.log2(np.exp(fs[-1, :] - fs[0, :]))
            # find local maximum growth rate
            da, dt = self._findlocalmaxgr(
                f, gs, axgr, figs, plotlocalmax, showpeakproperties, **kwargs
            )
            # find area under gr vs OD and area under OD
            if findareas:
                agod, angod, atod, antod = self._findareasunderOD(t, fs, gs)
            else:
                agod, angod, atod, antod = np.nan, np.nan, np.nan, np.nan
            # store results
            statsdict = {
                "experiment": e,
                "condition": c,
                "strain": s,
                "log2 OD ratio": np.median(dr),
                "log2 OD ratio err": self._statserr(dr),
                "local max gr": np.median(da),
                "local max gr err": self._statserr(da),
                "time of local max gr": np.median(dt),
                "time of local max gr err": self._statserr(dt),
                "area under gr vs OD": np.median(agod),
                "area under gr vs OD err": self._statserr(agod),
                "normalized area under gr vs OD": np.median(angod),
                "normalized area under gr vs OD err": self._statserr(angod),
                "area under OD": np.median(atod),
                "area under OD err": self._statserr(atod),
                "normalized area under OD": np.median(antod),
                "normalized area under OD err": self._statserr(antod),
            }
        return outdf, statsdict, warning

    def _findlocalmaxgr(
        self, f, gs, axgr, figs, plotlocalmax, showpeakproperties, **kwargs
    ):
        """
        Internal function: Check if growth rate has a local maxima.
        If so, find the local maximum with the highest growth rate using samples
        of gs of growth rates.
        The keyword variables kwargs are passed to scipy's find_peaks.
        """
        from scipy.signal import find_peaks

        # find peaks in mean gr
        lpksmn, lpksmndict = find_peaks(f.df, **kwargs)
        if np.any(lpksmn):
            if showpeakproperties:
                # display properties of peaks
                print("Peak properties\n---")
                for prop in lpksmndict:
                    print("{:15s}".format(prop), lpksmndict[prop])
            # da: samples of local max growth rate
            # dt: samples of time of local max growth rate
            da, dt = [], []
            # find peaks of sampled growth rates
            for gsample in np.transpose(gs):
                tpks = find_peaks(gsample, **kwargs)[0]
                if np.any(tpks):
                    da.append(np.max(gsample[tpks]))
                    dt.append(f.pt[tpks[np.argmax(gsample[tpks])]])
            if figs and plotlocalmax:
                # plot local max gr as a point
                axgr.plot(
                    np.median(dt),
                    np.median(da),
                    "o",
                    color="yellow",
                    markeredgecolor="k",
                )
            return da, dt
        else:
            # mean gr has no peaks
            return np.nan, np.nan

    def _findareasunderOD(self, t, fs, gs):
        """
        Internal function: Given samples of log OD and of growth rate, find the area
        under gr vs OD and the area under OD vs time.
        """
        from scipy import integrate

        # agod: samples of area under gr vs OD
        # angod: samples of normalised area under gr vs OD
        # atod: samples of area under OD vs time
        # antod: samples of normalised area under OD vs time
        agod, angod, atod, antod = [], [], [], []
        for fsample, gsample in zip(np.transpose(fs), np.transpose(gs)):
            sod = np.exp(fsample)
            # area under gr vs OD: integrand has OD as x and gr as y
            def integrand(x): return interp1d(sod, gsample)(x)
            iresult = integrate.quad(
                integrand, np.min(sod), np.max(sod), limit=100, full_output=1
            )[0]
            agod.append(iresult)
            angod.append(iresult / (np.max(sod) - np.min(sod)))
            # area under OD vs t: integrand has t as x and OD as y
            def integrand(x): return interp1d(t, sod)(x)
            iresult = integrate.quad(
                integrand, np.min(t), np.max(t), limit=100, full_output=1
            )[0]
            atod.append(iresult)
            antod.append(iresult / (np.max(t) - np.min(t)))
        return agod, angod, atod, antod

    #####
    def getfitnesspenalty(
        self, ref, com, y="gr", abs=False, figs=True, nosamples=100, norm=False
    ):
        """
        Calculates - as a measure of fitness - the area between typically two growth rate
        versus OD curves, normalized by the length along the OD-axis where they overlap.

        Parameters
        -----------
        ref: list of strings
            For only a single experiment, a list of two strings. The first string specifies
            the condition and the second specifies the strain to be used for the reference
            to which fitness is to be calculated.
            With multiple experiments, a list of three strings. The first string specifies
            the experiment, the second specifies the condition, and the third specifies the
            strain.
        com: list of strings
            For only a single experiment, a list of two strings. The first string specifies
            the condition and the second specifies the strain to be compared with the
            reference.
            With multiple experiments, a list of three strings. The first string specifies
            the experiment, the second specifies the condition, and the third specifies the
            strain.
        y: string, optional
            The variable to be compared.
        figs: boolean, optional
            If True, a plot of the area between the two growth rate versus OD curves is shown.
        nosamples: integer
            The number bootstraps used to estimate the error.
        norm: boolean
            If True, returns the mean and variance of the area under the reference strain
            for normalisation.

        Returns
        -------
        fp: float
            The area between the two curves.
        err: float
            An estimate of the error in the calculated error, found by bootstrapping.
        reffp: float, optional
            The area beneath the reference strain.
        referr: float, optional
            An estimate of the erroe in the calculated area for the reference strain.

        Example
        -------
        >>> p.getfitnesspenalty(['1% raf 0.0µg/ml cyclohex', 'WT'],
        ...                     ['1% raf 0.5µg/ml cyclohex', 'WT'])
        """
        self._logmethod(self.logger)
        if len(self.allexperiments) == 1:
            ref.insert(0, self.allexperiments[0])
            com.insert(0, self.allexperiments[0])
        # get and sample from Gaussian processes
        if nosamples and y == "gr":
            # estimate errors
            try:
                # sample from Gaussian process
                f0s, g0s, h0s = self.progress["getstatsGP"][ref[0]][ref[1]][
                    ref[2]
                ].fitderivsample(nosamples)
                f1s, g1s, h1s = self.progress["getstatsGP"][com[0]][com[1]][
                    com[2]
                ].fitderivsample(nosamples)
                xsref, ysref = np.exp(f0s), g0s
                xscom, yscom = np.exp(f1s), g1s
            except KeyError:
                raise _GetFitnessPenalty(
                    "getstats('OD') needs to be run for these strains to estimate errors or else set nosamples= 0"
                )
        else:
            # no estimates of errors
            if nosamples:
                print(
                    "Cannot estimate errors - require y= 'gr' and a recently run getstats"
                )
            xsref = self.s.query(
                "experiment == @ref[0] and condition == @ref[1] and strain == @ref[2]"
            )["OD mean"][:, None]
            ysref = self.s.query(
                "experiment == @ref[0] and condition == @ref[1] and strain == @ref[2]"
            )[y].to_numpy()[:, None]
            xscom = self.s.query(
                "experiment == @com[0] and condition == @com[1] and strain == @com[2]"
            )["OD mean"].to_numpy()[:, None]
            yscom = self.s.query(
                "experiment == @com[0] and condition == @com[1] and strain == @com[2]"
            )[y].to_numpy()[:, None]
            if xsref.size == 0 or ysref.size == 0:
                print(ref[0] + ": Data missing for", ref[2], "in", ref[1])
                return np.nan, np.nan
            elif xscom.size == 0 or yscom.size == 0:
                print(com[0] + ": Data missing for", com[2], "in", com[1])
                return np.nan, np.nan
        fps = np.zeros(xsref.shape[1])
        nrm = np.zeros(xsref.shape[1])
        samples = zip(
            np.transpose(xsref),
            np.transpose(ysref),
            np.transpose(xscom),
            np.transpose(yscom),
        )
        # process samples
        for j, (xref, yref, xcom, ycom) in enumerate(samples):
            # remove any double values in OD because of OD plateau'ing
            uxref, uiref = np.unique(xref, return_inverse=True)
            uyref = np.array(
                [np.median(yref[np.nonzero(uiref == i)[0]])
                 for i in range(len(uxref))]
            )
            uxcom, uicom = np.unique(xcom, return_inverse=True)
            uycom = np.array(
                [np.median(ycom[np.nonzero(uicom == i)[0]])
                 for i in range(len(uxcom))]
            )
            # interpolate data
            iref = interp1d(
                uxref, uyref, fill_value="extrapolate", kind="slinear")
            icom = interp1d(
                uxcom, uycom, fill_value="extrapolate", kind="slinear")
            # find common range of x
            uxi = np.max([uxref[0], uxcom[0]])
            uxf = np.min([uxref[-1], uxcom[-1]])
            # perform integration to find normalized area between curves
            from scipy import integrate

            if abs:
                def igrand(x): return np.abs(iref(x) - icom(x))
            else:
                def igrand(x): return iref(x) - icom(x)
            fps[j] = integrate.quad(igrand, uxi, uxf, limit=100, full_output=1)[0] / (
                uxf - uxi
            )
            if norm:
                # calculate area under curve of reference strain as a normalisation
                def igrand(x): return iref(x)
                nrm[j] = integrate.quad(igrand, uxi, uxf, limit=100, full_output=1)[
                    0
                ] / (uxf - uxi)
            # an example figure
            if figs and j == 0:
                plt.figure()
                plt.plot(uxref, uyref, "k-", uxcom, uycom, "b-")
                x = np.linspace(uxi, uxf, np.max([len(uxref), len(uxcom)]))
                plt.fill_between(x, iref(x), icom(
                    x), facecolor="red", alpha=0.5)
                plt.xlabel("OD")
                plt.ylabel(y)
                plt.legend(
                    [
                        ref[0] + ": " + ref[2] + " in " + ref[1],
                        com[0] + ": " + com[2] + " in " + com[1],
                    ],
                    loc="upper left",
                    bbox_to_anchor=(-0.05, 1.15),
                )
                plt.show()
        if norm:
            return (
                np.median(fps),
                self._statserr(fps),
                np.median(nrm),
                self._statserr(nrm),
            )
        else:
            return np.median(fps), self._statserr(fps)

    #####
    def averageoverexpts(
        self, condition, strain, tvr="OD mean", bd=False, addnoise=True, plot=False
    ):
        """
        Uses a Matern Gaussian process to average a time-dependent variable over all
        experiments.

        An alternative and best first choice is to use addcommonvar.

        Parameters
        ----------
        condition: string
            The condition of interest.
        strain: string
            The strain of interest.
        tvr: float
            The time-dependent variable to be averaged.
            For example, 'c-GFPperOD' or 'OD mean'.
        bd: dictionary, optional
            The limits on the hyperparameters for the Matern Gaussian process.
            For example,
                {0: (-5,5), 1: (-4,4), 2: (-5,2)}
            where the first element controls amplitude, setting the bounds to 1e-5
            and 1e5, the second controls flexibility, and the third determines the
            magnitude of the measurement error.
        addnoise: boolean
            If True, add the fitted magnitude of the measurement noise to the predicted
            standard deviation for better comparison with the spread of the data.

        Returns
        -------
        res: dictionary
            {'t' : time, tvr : time-dependent data, 'mn' : mean, 'sd' : standard deviation}
            where 'mn' is the average found and 'sd' is its standard deviation. 'tvr' is the
            data used to find the average.

        Examples
        --------
        >>> p.averageoverexpts('1% Gal', 'GAL2', bd= {1: [-1,-1])})
        """
        self._logmethod(self.logger)
        # boundaries on hyperparameters
        if "OD" in tvr:
            bds = {0: (-4, 4), 1: (-1, 4), 2: (-6, 2)}
        else:
            bds = {0: (2, 12), 1: (-1, 4), 2: (4, 10)}
        if bd:
            bds = gu.mergedicts(original=bds, update=bd)
        # extract data
        df = self.s[["experiment", "condition", "strain", "time", tvr]]
        ndf = df.query("condition == @condition and strain == @strain")
        # use GP to average over experiments
        x = ndf["time"].to_numpy()
        y = ndf[tvr].to_numpy()
        ys = y[np.argsort(x)]
        xs = np.sort(x)
        g = gp.maternGP(bds, xs, ys)
        print("averaging over", tvr, "experiments for", strain, "in", condition)
        g.findhyperparameters(noruns=2, noinits=1000)
        g.results()
        g.predict(xs, addnoise=addnoise)
        if plot:
            plt.figure()
            g.sketch(".")
            plt.title("averaging " + strain + " in " + condition)
            plt.xlabel("time")
            plt.ylabel(tvr)
            plt.show()
        # return results as a dictionary
        res = {"t": xs, tvr: ys, "mn": g.f, "sd": np.sqrt(g.fvar)}
        return res

    #####
    # Fluorescence corrections
    #####
    def correctauto(
        self,
        f=["GFP", "AutoFL"],
        refstrain="WT",
        figs=True,
        experiments="all",
        experimentincludes=False,
        experimentexcludes=False,
        conditions="all",
        conditionincludes=False,
        conditionexcludes=False,
        strains="all",
        strainincludes=False,
        strainexcludes=False,
    ):
        """
        Corrects fluorescence data for autofluorescence by comparing with the
        fluorescence of an untagged reference strain.

        The reference strain is used to estimate the autofluoresence via either
        the method of Licthen et al., 2014, where measurements of fluoescence
        at two wavelengths is required, or by using the fluorescence of the reference
        strain interpolated to the OD of the strain of interest (Berthoumieux et al.,
        2013).

        Using two measurements of fluorescence is thought to be more accurate,
        particularly for low fluorescence measurements (Mihalcescu et al., 2015).

        Arguments
        --
        f: string or list of strings
            The fluorescence measurements, typically either ['mCherry'] or
            ['GFP', 'AutoFL'].
        refstrain: string
            The reference strain.
        figs: boolean
            If True, display plots showing the fits to the reference strain's
            fluorescnce.
        experiments: string or list of strings
            The experiments to include.
        conditions: string or list of strings
            The conditions to include.
        strains: string or list of strings
            The strains to include.
        experimentincludes: string, optional
            Selects only experiments that include the specified string in their name.
        experimentexcludes: string, optional
            Ignores experiments that include the specified string in their name.
        conditionincludes: string, optional
            Selects only conditions that include the specified string in their name.
        conditionexcludes: string, optional
            Ignores conditions that include the specified string in their name.
        strainincludes: string, optional
            Selects only strains that include the specified string in their name.
        strainexcludes: string, optional
            Ignores strains that include the specified string in their name.

        Notes
        -----
        In principle

        >>> p.correctmedia()

        should be run before running correctauto when processing data with two fluorescence
        measurements.

        It is unnecessary with only one fluorescence measurement because the normalisation
        is then done directly with the reference strain's fluorescence and this fluorescence
        can include the fluorescence from the media.

        In practice, running correctmedia may generate negative values of the fluorescence
        at some time points. These negative values will create NaNs in the corrected
        fluorescence, which are normally harmless.

        With sufficiently many negative values of the fluorescence, however, correcting
        data with two fluorescence measurements can become corrupted.

        If correctmedia generates negative fluorescence values, we therefore recommend
        comparing the corrected fluorescence between

        >>> p.correctmedia()
        >>> p.correctauto(['GFP', 'AutoFL')

        and

        >>> p.correctauto('GFP')

        to determine if these negative values are deleterious.

        Examples
        --------
        To correct data with one type of fluorescence measurement, use:

        >>> p.correctauto('GFP')
        >>> p.correctauto('mCherry', refstrain= 'BY4741')

        To correct data with two types of fluorescence measurement, use:

        >>> p.correctauto(['GFP', 'AutoFL'])
        >>> p.correctauto(['GFP', 'AutoFL'], refstrain= 'wild-type')

        References
        ----------
        S Berthoumieux, H De Jong, G Baptist, C Pinel, C Ranquet, D Ropers, J Geiselmann (2013).
        Shared control of gene expression in bacteria by transcription factors and global
        physiology of the cell.
        Mol Syst Biol, 9, 634.

        CA Lichten, R White, IB Clark, PS Swain (2014). Unmixing of fluorescence spectra
        to resolve quantitative time-series measurements of gene expression in plate readers.
        BMC Biotech, 14, 1-11.

        I Mihalcescu, MVM Gateau, B Chelli, C Pinel, JL Ravanat (2015). Green autofluorescence,
        a double edged monitoring tool for bacterial growth and activity in micro-plates.
        Phys Biol, 12, 066016.

        """
        self._logmethod(self.logger)
        f = gu.makelist(f)
        exps, cons, strs = self._getall(
            experiments,
            experimentincludes,
            experimentexcludes,
            conditions,
            conditionincludes,
            conditionexcludes,
            strains,
            strainincludes,
            strainexcludes,
        )
        # check for negative fluorescence values
        for e in exps:
            for c in cons:
                if self.progress["negativevalues"][e]:
                    for datatype in f:
                        if (
                            datatype in self.progress["negativevalues"][e]
                            and c in self.progress["negativevalues"][e]
                        ):
                            print(
                                e + ": The negative values for",
                                datatype,
                                "in",
                                c,
                                "will generate NaNs",
                            )
        # going ahead
        print("Using", refstrain, "as the reference")
        # correct for autofluorescence
        if len(f) == 2:
            self._correctauto2(
                f,
                refstrain,
                figs,
                experiments,
                experimentincludes,
                experimentexcludes,
                conditions,
                conditionincludes,
                conditionexcludes,
                strains,
                strainincludes,
                strainexcludes,
            )
        elif len(f) == 1:
            self._correctauto1(
                f,
                refstrain,
                figs,
                experiments,
                experimentincludes,
                experimentexcludes,
                conditions,
                conditionincludes,
                conditionexcludes,
                strains,
                strainincludes,
                strainexcludes,
            )
        else:
            print("f must be a list of length 1 or 2")

    #####
    def _correctauto1(
        self,
        f,
        refstrain,
        figs,
        experiments,
        experimentincludes,
        experimentexcludes,
        conditions,
        conditionincludes,
        conditionexcludes,
        strains,
        strainincludes,
        strainexcludes,
    ):
        """
        Internal function: Corrects for autofluorescence for experiments with measured
        emissions at one wavelength using the fluorescence of the reference strain
        interpolated to the OD of the tagged strain. This in principle corrects too
        for the fluorescence of the medium, although running correctmedia is still
        preferred.
        """
        print("Correcting autofluorescence using", f[0])
        for e in self._getexps(experiments, experimentincludes, experimentexcludes):
            for c in self._getcons(
                conditions, conditionincludes, conditionexcludes, nomedia=True
            ):
                # process reference strain
                refstrfn = self._processref1(f, refstrain, figs, e, c)
                # correct strains
                for s in self._getstrs(
                    strains, strainincludes, strainexcludes, nonull=True
                ):
                    if not self.sc[
                        (self.sc.experiment == e)
                        & (self.sc.condition == c)
                        & (self.sc.strain == s)
                    ][f[0] + " corrected for autofluorescence"].any():
                        od, rawfl = self._extractwells(e, c, s, ["OD", f[0]])
                        # no data
                        if od.size == 0 or rawfl.size == 0:
                            continue
                        # correct autofluorescence for each replicate
                        fl = np.transpose(
                            [
                                rawfl[:, i] - refstrfn(od[:, i])
                                for i in range(od.shape[1])
                            ]
                        )
                        flperod = np.transpose(
                            [
                                (rawfl[:, i] - refstrfn(od[:, i])) / od[:, i]
                                for i in range(od.shape[1])
                            ]
                        )
                        # replace negative values with NaNs
                        fl[fl < 0] = np.nan
                        flperod[flperod < 0] = np.nan
                        # store results
                        bname = "c-" + f[0]
                        autofdict = {
                            "experiment": e,
                            "condition": c,
                            "strain": s,
                            "time": self.s.query(
                                "experiment == @e and condition == @c and strain == @s"
                            )["time"].to_numpy(),
                            bname: np.nanmean(fl, 1),
                            bname + " err": self._nanstdzeros2nan(fl, 1),
                            bname + "perOD": np.nanmean(flperod, 1),
                            bname + "perOD err": self._nanstdzeros2nan(flperod, 1),
                        }
                        autofdf = pd.DataFrame(autofdict)
                        if bname not in self.s.columns:
                            # extend dataframe
                            self.s = pd.merge(self.s, autofdf, how="outer")
                        else:
                            # update dataframe
                            self.s = gu.absorbdf(
                                self.s,
                                autofdf,
                                ["experiment", "condition", "strain", "time"],
                            )
                        # record that correction has occurred
                        self.sc.loc[
                            (self.sc.experiment == e)
                            & (self.sc.condition == c)
                            & (self.sc.strain == s),
                            f[0] + " corrected for autofluorescence",
                        ] = True

    #####
    def _processref1(self, f, refstrain, figs, experiment, condition):
        """
        Internal function: Processes reference strain for data with one fluorescence
        measurement. Uses lowess to smooth the fluorescence of the reference strain
        as a function of OD.

        Parameters
        ----------
        f: string
            The fluorescence to be corrected. For example, ['mCherry'].
        refstrain: string
            The reference strain. For example, 'WT'.
        figs: boolean
            If True, display fits of the reference strain's fluorescence.
        experiment: string
            The experiment to be corrected.
        condition: string
            The condition to be corrected.

        Returns
        -------
        refstrfn: function
            The reference strain's fluorescence as a function of OD.
        """
        e, c = experiment, condition
        print(e + ": Processing reference strain",
              refstrain, "for", f[0], "in", c)
        od, fl = self._extractwells(e, c, refstrain, ["OD", f[0]])
        if od.size == 0 or fl.size == 0:
            raise _CorrectAuto(e + ": " + refstrain + " not found in " + c)
        else:
            odf = od.flatten("F")
            flf = fl.flatten("F")
            # smooth fluorescence as a function of OD using lowess to minimize refstrain's autofluorescence

            def choosefrac(frac):
                res = lowess(flf, odf, frac=frac)
                refstrfn = interp1d(
                    res[:, 0],
                    res[:, 1],
                    fill_value=(res[0, 1], res[-1, 1]),
                    bounds_error=False,
                )
                # max gives smoother fits than mean
                return np.max(np.abs(flf - refstrfn(odf)))

            res = minimize_scalar(choosefrac, bounds=(
                0.1, 0.99), method="bounded")
            # choose the optimum frac
            frac = res.x if res.success else 0.33
            res = lowess(flf, odf, frac=frac)
            refstrfn = interp1d(
                res[:, 0],
                res[:, 1],
                fill_value=(res[0, 1], res[-1, 1]),
                bounds_error=False,
            )
            if figs:
                # plot fit
                plt.figure()
                plt.plot(odf, flf, ".", alpha=0.5)
                plt.plot(res[:, 0], res[:, 1])
                plt.xlabel("OD")
                plt.ylabel(f[0])
                plt.title(e + ": " + refstrain + " for " + c)
                plt.show()
            return refstrfn

    #####
    def _correctauto2(
        self,
        f,
        refstrain,
        figs,
        experiments,
        experimentincludes,
        experimentexcludes,
        conditions,
        conditionincludes,
        conditionexcludes,
        strains,
        strainincludes,
        strainexcludes,
    ):
        """
        Internal function: Corrects for autofluorescence using spectral unmixing
        for experiments with measured emissions at two wavelengths.

        References
        ----------
        CA Lichten, R White, IB Clark, PS Swain (2014). Unmixing of fluorescence spectra
        to resolve quantitative time-series measurements of gene expression in plate readers.
        BMC Biotech, 14, 1-11.
        """
        # correct for autofluorescence
        print("Correcting autofluorescence using", f[0], "and", f[1])
        for e in self._getexps(experiments, experimentincludes, experimentexcludes):
            for c in self._getcons(
                conditions, conditionincludes, conditionexcludes, nomedia=True
            ):
                # process reference strain
                refqrfn = self._processref2(f, refstrain, figs, e, c)
                # process other strains
                for s in self._getstrs(
                    strains, strainincludes, strainexcludes, nonull=True
                ):
                    if s != refstrain and not (
                        self.sc[
                            (self.sc.experiment == e)
                            & (self.sc.condition == c)
                            & (self.sc.strain == s)
                        ][f[0] + " corrected for autofluorescence"].any()
                    ):
                        f0, f1 = self._extractwells(e, c, s, f)
                        if f0.size == 0 or f1.size == 0:
                            continue
                        nodata, nr = f0.shape
                        # set negative values to NaNs
                        f0[f0 < 0] = np.nan
                        f1[f1 < 0] = np.nan
                        # use mean OD for correction
                        odmean = self.s.query(
                            "experiment == @e and condition == @c and strain == @s"
                        )["OD mean"].to_numpy()
                        # remove autofluorescence
                        ra = refqrfn(odmean)
                        fl = self._applyautoflcorrection(ra, f0, f1)
                        od = self._extractwells(e, c, s, "OD")
                        flperod = fl / od
                        # set negative values to NaNs
                        fl[fl < 0] = np.nan
                        flperod[flperod < 0] = np.nan
                        # store corrected fluorescence
                        bname = "c-" + f[0]
                        autofdict = {
                            "experiment": e,
                            "condition": c,
                            "strain": s,
                            "time": self.s.query(
                                "experiment == @e and condition == @c and strain == @s"
                            )["time"].to_numpy(),
                            bname: np.nanmean(fl, 1),
                            bname + " err": self._nanstdzeros2nan(fl, 1),
                            bname + "perOD": np.nanmean(flperod, 1),
                            bname + "perOD err": self._nanstdzeros2nan(flperod, 1),
                        }
                        # add to dataframe
                        self.s = gu.absorbdf(
                            self.s,
                            pd.DataFrame(autofdict),
                            ["experiment", "condition", "strain", "time"],
                        )
                        self.sc.loc[
                            (self.sc.experiment == e)
                            & (self.sc.condition == c)
                            & (self.sc.strain == s),
                            f[0] + " corrected for autofluorescence",
                        ] = True

    #####
    def _processref2(self, f, refstrain, figs, experiment, condition):
        """
        Internal function: Processes reference strain data for spectral unmixing
        (for experiments with two fluorescence measurements). Uses lowess to smooth
        the ratio of emitted fluorescence measurements so that the reference strain's
        data is corrected to zero as best as possible.

        Parameters
        ----------
        f: list of strings
            The fluorescence measurements. For example, ['GFP', 'AutoFL'].
        refstrain: string
            The reference strain. For example, 'WT'.
        figs: boolean
            If True, display fits of the fluorescence ratios.
        experiment: string
            The experiment to be corrected.
        condition: string
            The condition to be corrected.

        Returns
        -------
        qrfn: function
            The ratio of the two fluorescences for the reference strain as a function of OD.
        """
        e, c = experiment, condition
        print(e + ": Processing reference strain",
              refstrain, "for", f[0], "in", c)
        # refstrain data
        f0, f1, od = self._extractwells(e, c, refstrain, f + ["OD"])
        if f0.size == 0 or f1.size == 0 or od.size == 0:
            raise _CorrectAuto(e + ": " + refstrain + " not found in " + c)
        else:
            f0[f0 < 0] = np.nan
            f1[f1 < 0] = np.nan
            odf = od.flatten("F")
            odrefmean = np.mean(od, 1)
            qrf = (f1 / f0).flatten("F")
            if np.all(np.isnan(qrf)):
                raise _CorrectAuto(
                    e + ": " + refstrain + " in " + c + " has too many NaNs"
                )
            # smooth to minimize autofluorescence in refstrain

            def choosefrac(frac):
                res = lowess(qrf, odf, frac)
                qrfn = interp1d(
                    res[:, 0],
                    res[:, 1],
                    fill_value=(res[0, 1], res[-1, 1]),
                    bounds_error=False,
                )
                flref = self._applyautoflcorrection(qrfn(odrefmean), f0, f1)
                return np.max(np.abs(flref))

            res = minimize_scalar(choosefrac, bounds=(
                0.1, 0.99), method="bounded")
            # calculate the relationship between qr and OD
            frac = res.x if res.success else 0.95
            res = lowess(qrf, odf, frac)
            qrfn = interp1d(
                res[:, 0],
                res[:, 1],
                fill_value=(res[0, 1], res[-1, 1]),
                bounds_error=False,
            )
            if figs:
                plt.figure()
                plt.plot(odf, qrf, ".", alpha=0.5)
                plt.plot(res[:, 0], res[:, 1])
                plt.xlabel("OD")
                plt.ylabel(f[1] + "/" + f[0])
                plt.title(e + ": " + refstrain + " in " + c)
                plt.show()
            # check autofluorescence correction for reference strain
            flref = self._applyautoflcorrection(qrfn(odrefmean), f0, f1)
            flrefperod = flref / od
            # set negative values to NaNs
            flref[flref < 0] = np.nan
            flrefperod[flrefperod < 0] = np.nan
            # store results
            bname = "c-" + f[0]
            autofdict = {
                "experiment": e,
                "condition": c,
                "strain": refstrain,
                "time": self.s.query(
                    "experiment == @e and condition == @c and strain == @refstrain"
                )["time"].to_numpy(),
                bname: np.nanmean(flref, 1),
                bname + "perOD": np.nanmean(flrefperod, 1),
                bname + " err": self._nanstdzeros2nan(flref, 1),
                bname + "perOD err": self._nanstdzeros2nan(flrefperod, 1),
            }
            if bname not in self.s.columns:
                self.s = pd.merge(self.s, pd.DataFrame(autofdict), how="outer")
            else:
                self.s = gu.absorbdf(
                    self.s,
                    pd.DataFrame(autofdict),
                    ["experiment", "condition", "strain", "time"],
                )
            return qrfn

    #####
    def _applyautoflcorrection(self, ra, f0data, f1data):
        """
        Internal function: Corrects for autofluorescence returning an array of replicates.
        """
        nr = f0data.shape[1]
        raa = np.reshape(np.tile(ra, nr), (np.size(ra), nr), order="F")
        return (raa * f0data - f1data) / (raa - self.gamma * np.ones(np.shape(raa)))

    def _nanstdzeros2nan(self, a, axis=None):
        """
        Internal function: nanstd but setting zeros to nan
        """
        err = np.nanstd(a, axis)
        err[err == 0] = np.nan
        return err

    #####
    # Logging
    #####
    def _initialiselogging(self):
        """
        Internal function: initialise a log, which is exported to a txt file
        when exportdf is called.
        """
        import datetime
        import logging
        from io import StringIO

        # enable logging
        starttime = "{:%Y-%b-%d %H:%M:%S}".format(datetime.datetime.now())
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.logstream = StringIO()
        loghandler = logging.StreamHandler(self.logstream)
        loghandler.setLevel(logging.INFO)
        self.logger.addHandler(loghandler)
        self.logger.propagate = False
        # start log
        self.logger.info("om.platereader version " + f"{self.__version__}")
        self.logger.info(f"{starttime}\n")

    def log(self):
        """
        Prints a log of all methods called and their arguments.

        Example
        -------
        >>> p.log()
        """
        print(self.logstream.getvalue())

    def savelog(self, fname=False):
        """
        Save log to file.

        Parameters
        --
        fname: string, optional
            The name of the file. If unspecified, the name of the experiment.

        Example
        -------
        >>> p.savelog()
        """
        # export log
        if fname:
            if self.wdir and self.wdir not in fname:
                fname = self.wdir + fname
        else:
            fname = self.wdir + "".join(self.allexperiments)
        f = open(fname + ".log", "w")
        f.write(self.logstream.getvalue())
        f.close()
        if self.wdir:
            print("Exported to", self.wdir)

    def _logmethod(self, logger):
        """
        Internal function: logs a method and its arguments.
        """
        currframe = inspect.currentframe()
        # find frame of calling routine
        frame = inspect.getouterframes(currframe)[1].frame
        # name of calling routine
        methodname = inspect.getframeinfo(frame)[2]
        # arguments of calling routine
        args, _, _, locals = inspect.getargvalues(frame)
        # add to log
        if methodname == "__init__":
            logstring = "p= platereader("
        else:
            logstring = "p." + methodname + "("
        for arg in args:
            if "self" not in arg:
                if type(locals[arg]) is str:
                    argstr = "'" + locals[arg] + "'"
                else:
                    argstr = str(locals[arg])
                logstring += arg + "= " + argstr + ", "
        logstring = logstring[:-2] + ")\n"
        logger.info(logstring)

    #####
    # Exporting and importing
    #####
    def exportdf(self, commonname=False, type="tsv"):
        """
        Exports the dataframes as either tab-delimited or csv or json files.
        Dataframes for the (processed) raw data, for summary data, and for summary
        statistics and corrections, as well as a log file, are exported.

        Parameters
        ----------
        commonname: string, optional
            The name used for the output files.
            If unspecified, the experiment or experiments is used.
        type: string
            The type of file for export, either 'json' or 'csv' or 'tsv'.

        Examples
        --------
        >>> p.exportdf()
        >>> p.exportdf('processed', type= 'json')
        """
        self._logmethod(self.logger)
        if commonname:
            commonname = self.wdir + commonname
        else:
            commonname = self.wdir + "".join(self.allexperiments)
        # export data
        if type == "json":
            self.r.to_json(commonname + "_r.json", orient="split")
            self.s.to_json(commonname + "_s.json", orient="split")
            self.sc.to_json(commonname + "_sc.json", orient="split")
        else:
            sep = "\t" if type == "tsv" else ","
            self.r.to_csv(commonname + "_r." + type, sep=sep, index=False)
            self.s.to_csv(commonname + "_s." + type, sep=sep, index=False)
            self.sc.to_csv(commonname + "_sc." + type, sep=sep, index=False)
        # export log to file
        self.savelog(commonname)

    def importdf(self, commonnames, info=True, sep="\t"):
        """
        Import dataframes saved as either json or csv or tsv files.

        Parameters
        ----------
        commonnames: list of strings
            A list of names for the files to be imported with one string for each experiment.

        Examples
        --------
        >>> p.importdf('Gal')
        >>> p.importdf(['Gal', 'Glu', 'Raf'])
        """
        self._logmethod(self.logger)
        commonnames = gu.makelist(commonnames)
        # import data
        for commonname in commonnames:
            commonname = self.wdir + commonname
            for df in ["r", "s", "sc"]:
                try:
                    # json files
                    exec(
                        "impdf= pd.read_json(commonname + '_' + df + '.json', orient= 'split')"
                    )
                    print("Imported", commonname + "_" + df + ".json")
                except ValueError:
                    try:
                        # csv files
                        exec(
                            "impdf= pd.read_csv(commonname + '_' + df + '.csv', sep= ',')"
                        )
                        print("Imported", commonname + "_" + df + ".csv")
                    except FileNotFoundError:
                        try:
                            # tsv files
                            exec(
                                "impdf= pd.read_csv(commonname + '_' + df + '.tsv', sep= '\t')"
                            )
                            print("Imported", commonname + "_" + df + ".tsv")
                        except FileNotFoundError:
                            print(
                                "No file called",
                                commonname + "_" + df + ".json or .csv or .tsv found",
                            )
                            return
                # ensure all are imported as strings
                for var in ["experiment", "condition", "strain"]:
                    exec("impdf[var]= impdf[var].astype(str)")
                # merge dataframes
                if hasattr(self, df):
                    exec(
                        "self."
                        + df
                        + "= pd.merge(self."
                        + df
                        + ", impdf, how= 'outer')"
                    )
                else:
                    exec("self." + df + "= impdf")
            print()

        # update attributes
        self.allexperiments = list(self.s.experiment.unique())
        self.allconditions.update(
            {
                e: list(self.s[self.s.experiment == e].condition.unique())
                for e in self.allexperiments
            }
        )
        self.allstrains.update(
            {
                e: list(self.s[self.s.experiment == e].strain.unique())
                for e in self.allexperiments
            }
        )

        # find datatypes with mean in self.s
        dtypdict = {}
        for e in self.allexperiments:
            # drop columns of NaNs - these are created by merge if a datatype is in one experiment but not in another
            tdf = self.s[self.s.experiment == e].dropna(axis=1, how="all")
            dtypdict[e] = list(tdf.columns[tdf.columns.str.contains("mean")])
        self.datatypes.update(
            {e: [dt.split(" mean")[0] for dt in dtypdict[e]] for e in dtypdict}
        )
        # initialise progress
        for e in self.allexperiments:
            self._initialiseprogress(e)
        # display info on import
        if info:
            self.info()

        # display warning if duplicates created
        # if (np.any(np.nonzero(self.r.set_index(['experiment', 'condition', 'strain', 'time', 'well']).index.duplicated())[0]) or np.any(np.nonzero(self.s.set_index(['experiment', 'condition', 'strain', 'time']).index.duplicated())[0])):
        if len(self.allexperiments) != np.unique(self.allexperiments).size:
            print(
                "\nLikely ERROR: data with the same experiment, condition, strain, and time now appears twice!!"
            )


# errors
class _omniplateError(ValueError):
    pass


class _FileNotFound(_omniplateError):
    pass


class _UnknownPlateReader(_omniplateError):
    pass


class _IgnoreWells(_omniplateError):
    pass


class _PlotError(_omniplateError):
    pass


class _UnknownDataFrame(_omniplateError):
    pass


class __getsubset(_omniplateError):
    pass


class _GetFitnessPenalty(_omniplateError):
    pass


class _CorrectAuto(_omniplateError):
    pass


#####

if __name__ == "__main__":
    print(platereader.__doc__)
