import numpy as np

__version__= '0.1.0'

###
class dotdict(dict):
    '''
    A class of dictionaries that allows the items to be accessed using the dot notation.

    Example
    -------
    >>> dict= dotdict({'B' : 100, 'q' : 1e-3})
    >>> dict.B
    '''
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError as k:
            raise AttributeError(k)

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError as k:
            raise AttributeError(k)

###
def tableau20():
    '''
    Returns a list of the tableau20 colours for plotting.
    '''
    import numpy as np
    return np.array([(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),
     (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),
     (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),
     (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),
     (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)])/255



###
def samplemode(d):
    '''
    Estimates mode of a unimodal distribution using the half-range mode from
    Bickel DR. Robust estimators of the mode and skewness of continuous data.
    Computational Statistics and Data Analysis. 2002;39:153–163

    Arguments
    ---
    d: a one-dimensional array of data
    '''
    ds= np.sort(np.concatenate(d, axis= None))
    while ds.size > 2:
        dmin, dmax= ds[0], ds[-1]
        # find data in the upper half of the data's range
        dsbigger= np.nonzero(ds > (dmin + dmax)/2)[0]
        if np.any(dsbigger):
            # dmin < dmax
            imid= dsbigger[0]
            # pick the half-interval with the most data
            ds= ds[:imid] if imid > ds.size - imid else ds[imid:]
        else:
            # dmin == dmax
            ds= np.array([dmin])
    # estimate mode
    return np.mean(ds)



###
def findiqr(d):
    '''
    Finds the interquartile range of data in an array

    Arguments
    --
    d: a one-dimensional array of data
    '''
    return np.subtract(*np.percentile(d, [75, 25]))



###
def oldbindata(x, y, bnsz= 2):
    '''
    Bin multivalued y over values of x so that there is a one-to-one relationship between x and y.

    Arguments
    x: data fron which bins are formed
    y: data to be binned
    bnsz: size of bins defined as the number of x-values comprising each bin
    '''
    # bin data so that there is a one-to-one relationship between x and y
    xs= np.sort(x)
    xbins= np.array([np.mean(xs[i:i + bnsz]) for i in np.arange(0, len(xs), bnsz)])
    nx= np.zeros(xbins.size - 1)
    ny= np.zeros(xbins.size - 1)
    for i in range(xbins.size - 1):
        inds= np.where(np.logical_and(x >= xbins[i], x < xbins[i+1]))[0]
        if np.any(inds):
            nx[i]= (xbins[i] + xbins[i+1])/2
            ny[i]= np.median(y[inds])
        else:
            nx[i]= np.nan
            ny[i]= np.nan
    return rmnans(nx), rmnans(ny)


def bindata(x, y, nobins, statistic= 'median', smooth= False, **kwargs):
    '''
    Bin y into bins of variable x using a statistic using scipy.stats.binned_statistic.
    Returns x values at the centre of the bins and the binned y values.

    Arguments
    x: data fron which bins are formed
    y: data to be binned
    nobins: number of bins
    statistic: statistic to be used - default is 'median'
    smooth: if True, smooth binned data use lowess from statsmodels
            (all lowess parameters are passed on via keyword arguments)
    '''
    from scipy.stats import binned_statistic
    x= np.asarray(x)
    y= np.asarray(y)
    # loop through nobins to make sure there are no empty bins - given a nan value
    newy= np.nan
    while np.any(np.isnan(newy)):
        res= binned_statistic(x.flatten('F'), y.flatten('F'), statistic, bins= nobins)
        newy= res.statistic
        nobins -= 1
    newx= np.array([(res.bin_edges[i] + res.bin_edges[i+1])/2 for i in range(res.bin_edges.size - 1)])
    if smooth:
        from statsmodels.nonparametric.smoothers_lowess import lowess
        res= lowess(newy, newx, **kwargs)
        return res[:,0], res[:,1]
    else:
        return newx, newy




###
def natural_keys(text):
    '''
    Used to sort a list of strings by the numeric values in the list entries.

    Eg sorted(list, key= natural_keys)

    Arguments
    --
    text: a string (but see above example)
    '''
    import re
    def atof(text):
        try:
            retval = float(text)
        except ValueError:
            retval = text
        return retval
    return [atof(c) for c in re.split(r'[+-]?([0-9]+(?:[.][0-9]*)?|[.][0-9]+)', text)]



####
def absorbdf(blob, victim, cols):
    '''
    Absorb one dataframe into another using a list of columns as an index to align the dataframes.
    Any NaNs in the victim will replace those in blob (not the default behaviour of pd.update).

    Arguments
    --
    blob: the absorbing dataframe
    victim: the dataframe to be absorbed
    cols: a list of columns to align the dataframes
    '''
    df= blob.set_index(cols)
    victim.update(victim.fillna(np.inf))
    df.update(victim.set_index(cols))
    df.replace(np.inf, np.nan)
    return df.reset_index()


####
def mygamma(a, x= False):
    '''
    Defines gamma and standard definition of incomplete gamma (Scipy's definition is normalised)

    Arguments
    --
    a: argument of gamma function
    x: additional argument for incomplete gamma
    '''
    from scipy.special import gammaincc, gamma
    if x:
        return gammaincc(a, x)*gamma(a)
    else:
        return gamma(a)


####
def flattenlist(ell):
    '''
    Flatten list of lists

    Arguments:
    --
    ell: list of lists
    '''
    if any(isinstance(sublist, list) for sublist in ell):
        return [item for sublist in ell for item in sublist]
    else:
        return ell

####
def islistempty(ell):
    '''
    Check if a list of lists is empty, e.g. [[]]

    Arguments
    --
    ell: list
    '''
    if isinstance(ell, list): # Is a list
        return all( map(islistempty, ell) )
    return False # Not a list


####
def brutemin(minfunc, xy, *args):
    '''
    Minimization by systematic evaluation of all points on a grid or line segment ignorning any NaNs returned by minfunc.

    Arguments:
    ---
    minfunc: function to be minimized
    xy: a list of arrays of the values of the parameters to be checked
    args: additional arguments for minfunc
    '''
    xy= makelist(xy)
    if len(xy) == 1:
        xs= xy[0]
        e= np.array([minfunc(x, *args) for x in xs])
        fe= np.copy(e)
        fe[np.isnan(e)]= np.nanmax(e)
        return xs[np.argmin(fe)]
    elif len(xy) == 2:
        xs, ys= xy
        e= np.zeros((len(xs), len(ys)))
        for i, x in enumerate(xs):
            for j, y in enumerate(ys):
                e[i,j]= minfunc(np.array([x, y]), *args)
        fe= np.copy(e)
        fe[np.isnan(e)]= np.nanmax(e)
        mini= np.unravel_index(np.argmin(fe, axis= None), fe.shape)
        return np.array([xs[mini[0]], ys[mini[1]]])
    else:
        print('brutemin failed. xy must be an array with dimension at most 2')

####
def addtodict(dict, a, aname):
    '''
    Adds an array to a dictionary

    dict: the dictionary
    a: the array
    aname: the new key to be added to the dictionary
    '''
    if np.isscalar(a):
        dict[aname]= np.append(dict['aname'], a) if 'aname' in dict else np.array([a])
    else:
        dict[aname]= np.vstack((dict['aname'], a)) if 'aname' in dict else np.array([a])
    return dict



####
def invposdef(m):
    '''
    Finds inverse of a positive definite matrix

    Arguments:
    m: a positive definite matrix
    '''
    from scipy import linalg
    cho= linalg.cholesky(m)
    choI= linalg.pinv(cho)
    return choI.dot(choI.T)


####
def makecmap(n, type= 'soft'):
    '''
    Using seaborn to make a colormap with n distinct colors

    For example,
        cmap= makecmap(n)
        for i in range(n):
            plt.plot(x, y, color= cmap[i])

    Arguments
    --
    n: number of colours
    type: nature of colormap ('soft', 'hard')
    '''
    import seaborn as sns
    if type == 'soft':
        cmap= sns.color_palette('hls', n)
    elif type == 'hard':
        cmap= sns.hls_palette(n, l= 0.3, s= 0.8)
    return cmap

#####
def isfloat(s):
    '''
    Tests if variable is a float

    Arguments
    --
    s: variable to be tested
    '''
    try:
        float(s)
    except ValueError:
        return False
    return True


#####
def rmwhitespace(s):
    '''
    Removes white space from a string.

    Arguments
    --
    s:
    '''
    return ''.join(s.split())


#####
def getdatestring():
    '''
    Finds the current data and time as a string
    '''
    import time
    localtime = time.localtime(time.time())
    return ( str(localtime.tm_mday).zfill(2) + str(localtime.tm_mon).zfill(2) + str(localtime.tm_year)
            + '_' + str(localtime.tm_hour).zfill(2) + str(localtime.tm_min).zfill(2) )


#####
def crosscorrelate(t, s, r, mode= 'full', title= '', ylim= False):
    '''
    Find and plot normalized cross-correlation. Returns cross-correlation and lags.

    Arguments
    --
    t : 1D array of equally spaced time points
    s : signal (1D array)
    r : response (1D array)
    title: title of plot
    '''
    from scipy.signal import correlate
    import matplotlib.pyplot as plt

    nodata= t.size
    dt= np.median(np.diff(t))
    ns= (s - np.mean(s))/np.std(s)
    nr= (r - np.mean(r))/np.std(r)
    corr= correlate(nr, ns, mode= mode)/nodata
    if mode == 'full':
        lags= -(np.arange(np.size(corr)) - (nodata-1))*dt
    elif mode == 'same':
        lags= -(np.arange(np.size(corr)) - (int(nodata/2)-1))*dt
    else:
        lags= np.arange(np.size(corr))*dt

    plt.figure()
    plt.subplot(2,1,1)
    plt.suptitle(title, fontsize= 20)
    plt.plot(t, ns, t, nr)
    plt.ylabel('normalized signals')
    plt.xlabel('t')
    plt.legend(['signal', 'response'], loc= 'upper center', bbox_to_anchor=(0.5, 1.05),
          ncol=3, fancybox=True, shadow=True)
    plt.subplot(2,1,2)
    plt.stem(lags, corr)
    plt.ylabel('normalized correlation')
    plt.xlabel('lags')
    if np.any(ylim): plt.ylim(ylim)
    plt.show()

    return corr, lags


#####
def estimateerrorbar(y, nopts= False):
    """
    Estimates measurement error for each data point of y by calculating the standard deviation of the nopts data points closest to that data point

    Arguments
    --
    y: data - one column for each replicate
    nopts: number of points used to estimate error bars
    """
    y= np.asarray(y)
    if y.ndim == 1:
        ebar= np.empty(len(y))
        if not nopts: nopts= np.round(0.1*len(y))
        for i in range(len(y)):
            ebar[i]= np.std(np.sort(np.abs(y[i] - y))[:nopts])
        return ebar
    else:
        print('estimateerrorbar: works for 1-d arrays only.')



#####
def findsmoothvariance(y, filtsig= 0.1, nopts= False):
    '''
    Estimates and then smooths the variance over replicates of data

    Arguments
    --
    y: data - one column for each replicate
    filtsig: sets the size of the Gaussian filter used to smooth the variance
    nopts: if set, uses estimateerrorbar to estimate the variance
    '''
    from scipy.ndimage import filters
    if y.ndim == 1:
        # one dimensional data
        v= estimateerrorbar(y, nopts)**2
    else:
        # multi-dimensional data
        v= np.var(y, 1)
    # apply Gaussian filter
    vs= filters.gaussian_filter1d(v, int(len(y)*filtsig))
    return vs


######
def rejectionsample1D(x, y, nosamples):
    """
    Uses unadulterated rejection sampling to sample values of x from the probability distribution given by y

    Arguments
    --
    x: support of distribution
    y: histgram of distribution
    nosamples: number of samples to generate
    """
    s= np.empty(nosamples)
    ymax= max(y)
    for i in range(nosamples):
        gotone= False
        while not gotone:
            trialsample= np.random.randint(0, len(x))
            if np.random.uniform(0, ymax) <= y[trialsample]:
                gotone= True
                s[i]= x[trialsample]
    return s


######
def makelist(c):
    '''
    Ensures that a variable is a list

    Arguments
    --
    c: variable to be made into a list
    '''
    import numpy as np
    if type(c) == np.ndarray:
        return list(c)
    elif type(c) is not list:
        return [c]
    else:
        return c

######
def tilec(c, n):
    '''
    Creates an array of repeated columns

    Arguments
    --
    c: array to be repeated
    n: number of repeats
    '''
    return np.tile(np.array([c]).transpose(), (1, n))


######
def unique_rows(a):
    '''
    Finds the unique rows in an array

    Arguments
    --
    a: array of interest
    '''
    a = np.ascontiguousarray(a)
    unique_a = np.unique(a.view([('', a.dtype)]*a.shape[1]))
    return unique_a.view(a.dtype).reshape((unique_a.shape[0], a.shape[1]))


######
def mergedicts(original, update):
    '''
    Given two dicts, merge them into a new dict

    Arguments
    --
    x: first dict
    y: second dict
    '''
    z= original.copy()
    z.update(update)
    return z

######
def dict2list(d):
    '''
    Put the values of a dictionary into a list.

    Arguments
    --
    d: dictionary
    '''
    return [d[a] for a in d.keys()]

######
def nans(shape):
    '''
    Creates an array of NaNs

    Arguments
    --
    shape: shape of array to be created
    '''
    a= np.empty(shape)
    a[:]= np.nan
    return a

######
def rmcolsofnans(a):
    '''
    Removes any columns of an array that start with a NaN

    Arguments
    --
    a: array of interest
    '''
    a= np.asarray(a)
    try:
        return a[:, ~np.isnan(a[0,:])]
    except:
        # 1D array
        return a[:, ~np.isnan(a)]


######
def rmnans(a):
    '''
    Removes NaN from a 1-D array

    Arguments
    --
    a: array of interest
    '''
    a= np.asarray(a)
    return a[~np.isnan(a)]

######
def plotxyerr(x, y, xerr, yerr, xlabel= 'x', ylabel= 'y', title= '', color= 'b', figref= False):
    '''
    Plots a noisy x versus a noisy y with errorbars shown as ellipses.

    Arguments
    --
    x: x variable (a 1D array)
    y: y variable (a 1D array)
    xerr: (symmetric) error in x (a 1D array)
    yerr: (symmetric) error in y (a 1D array)
    xlabel: label for x-axis
    ylabel: label for y-axis
    title: title of figure
    color: default 'b'
    figref: if specified, allows data to be added to an existing figure
    '''
    import matplotlib.pyplot as plt
    from matplotlib.patches import Ellipse
    if figref:
        fig= figref
    else:
        fig= plt.figure()
    ax= fig.add_subplot(111)
    ax.plot(x, y, '.-', color= color)
    for i in range(len(x)):
        e= Ellipse(xy= (x[i], y[i]), width= 2*xerr[i], height= 2*yerr[i], alpha= 0.2)
        ax.add_artist(e)
        e.set_facecolor(color)
        e.set_linewidth(0)
    if not figref:
        plt.xlim([np.min(x-2*xerr), np.max(x+2*xerr)])
        plt.ylim([np.min(y-2*yerr), np.max(y+2*yerr)])
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)
        plt.show(block= False)


######
def smoothGP(x, y, xp= False, bd= False, noruns= 3, exitearly= False,
             merrors= False, results= True):
    '''
    Uses a squared exponential Gaussian process to smooth data.

    Arguments
    --
    x: data on x-axis
    y: data on y-axis
    xp: x values for which smoothed values of y are required (default: x)
    bd: to change the limits on the hyperparameters for the Gaussian process
    noruns: number of fit attempts used
    exitearly: if True, fitting will stop at the first successful attempt
    merrors: if specified, a 1-d array of the measurement errors (as variances)
    results: if True, display results of the fitting
    '''
    import gaussianprocess as gp
    # sort data
    y= y[np.argsort(x)]
    x= np.sort(x)
    if not np.any(xp): xp= x
    # use Gaussian process to fit
    b= {0: (-6,4), 1: (-6,1), 2: (-5,1)}
    if bd: b= mergedicts(original= b, update= bd)
    g= gp.sqexpGP(b, x, y, merrors= merrors)
    g.findhyperparameters(noruns, exitearly= exitearly)
    if results: g.results()
    g.predict(xp)
    return g.f, g.fvar, g



#######
def putpkl(path, item):
    '''
    Stores object, including dictionaries, in a pickle file

    Arguments
    --
    path: file name
    item: object to be stored
    '''
    import pickle
    with open(path, 'wb') as file:
        pickle.dump(item, file, pickle.HIGHEST_PROTOCOL)


def getpkl(path):
    '''
    Reads an object from a pickle file

    Arguments
    --
    path: file name
    '''
    import pickle
    with open(path, 'rb') as file:
        try:
            while True:
                b= pickle.load(file)
        except EOFError:
            return b

####
def multireplace(string, replacements):
    '''
    Given a string and a replacement map, it returns the replaced string

    Arguments
    ---
    string : string to execute replacements on
    replacements: dictionary of replacements {value to find: value to replace}
    '''
    import re
    # Place longer ones first to keep shorter substrings from matching
    # where the longer ones should take place
    # For instance given the replacements {'ab': 'AB', 'abc': 'ABC'} against
    # the string 'hey abc', it should produce 'hey ABC' and not 'hey ABc'
    substrs= sorted(replacements, key=len, reverse=True)
    # Create a big OR regex that matches any of the substrings to replace
    regexp= re.compile('|'.join(map(re.escape, substrs)))
    # For each match, look up the new string in the replacements
    return regexp.sub(lambda match: replacements[match.group(0)], string)


####
def replacevariables(listvar, reprules, twice= True):
    '''
    Uses the dictionary of replacement rules to convert a list of variables into numerical values

    Arguments
    --
    listvar: a list of variables containing algebraic expression
    reprules: a dictionary mapping the algebraic expressions onto numbers as strings
    twice: if True, run replacementrules twice to catch algebraic expressions that are also defined as algebraic expressions
    '''
    import numexpr as ne
    if twice:
        return np.array([float(ne.evaluate(multireplace(multireplace(il, reprules), reprules)))
                        for il in listvar])
    else:
        return np.array([float(ne.evaluate(multireplace(il, reprules))) for il in listvar])


####
def figs2pdf(savename):
    '''
    Save all open figures to a pdf file
    '''
    from matplotlib.backends.backend_pdf import PdfPages
    import matplotlib.pyplot as plt
    if '.' not in savename: savename += '.pdf'
    pp= PdfPages(savename)
    for i in plt.get_fignums():
        plt.figure(i)
        pp.savefig()
    pp.close()
