import numpy as np
import scipy.stats as scistat
import scipy.integrate as integrate
from scipy.optimize import minimize
from scipy import interpolate
from functools import partial
import mpmath as mp
mp.dps = 25; mp.pretty = True


class OnOffMeasurement:
    """Perform the computation of the signal PDF
       from an ON/OFF measurement with the inclusion 
       of the single event likelihoods of being a signal 
       or background event.
       
       It is also possible to compute statistical parameter
       like the upper limit, the credible interval, the incerse
       of the cdf, etc... 


    Parameters
    ----------
    Non   : init
        Total count in the ON region
    Noff  : init
        Total count in the OFF region
    alpha : init
        Normalization factor ON exposure / OFF exposure
    signal_likelihoods : `array`
        Array of lenght Non with single events likelihood
        of being a signal event
    bkg_likelihoods    : `array`
        Array of lenght Non with single events likelihood
        of being a background event
    
    """
    def __init__(self,
                 Non                = None , 
                 Noff               = None , 
                 alpha              = None , 
                 signal_likelihoods = None ,
                 bkg_likelihoods    = None ,
                 
                ):
        
        self.Non                = Non
        self.Noff               = Noff
        self.alpha              = alpha
        self.signal_likelihoods = signal_likelihoods
        self.bkg_likelihoods    = bkg_likelihoods
        
        self.excess             = Non - alpha*Noff
        self.excess_error       = np.sqrt( Non + alpha**2*Noff)
        self.LiMa_significance  = LiMaSignificance(Non,Noff,alpha)*np.sign(self.excess)
        self.Ns                 = None
        self.pmf                = None
        self.mean               = None
        self.variance           = None
        self.mode_pmf           = None
        self.run_ok             = False
    
    
    def run(self,**par):
        """
        From Non, Noff, alpha and the events likelihoods
        it computes the signal events PMF and signal PDF
        """
        self.Ns ,self.pmf = signal_events_PMF( 
            self.Non, 
            self.Noff, 
            self.alpha)
        if self.signal_likelihoods is not None or self.bkg_likelihoods is not None:
            if self.signal_likelihoods is None:
                self.signal_likelihoods = np.ones_like(self.bkg_likelihoods)
            if self.bkg_likelihoods is None:
                self.bkg_likelihoods = np.ones_like(self.signal_likelihoods)
                
            self.comb = combinatorial_term( self.bkg_likelihoods,
                                            self.signal_likelihoods,
                                            )
            
            self.pmf  *= self.comb
            
            self.pmf  /= np.sum(self.pmf)
        
        self.pmf = np.array(self.pmf.tolist(),dtype=np.float32) 
        # we ignore those Ns with negligble pmf 
        self.Ns  = self.Ns[  self.pmf > 1e-6]
        self.pmf = self.pmf[ self.pmf > 1e-6]
        self.mode_pmf = self.Ns[ np.argmax(self.pmf) ]
        
        self.get_mean_and_variance(**par)
        minusPDF     = lambda x: -1* self.pdf(x)
        self.mode_pdf =minimize(minusPDF,self.mode_pmf,bounds=((0,None),)).x[0]
        
        self.run_ok = True
    
    
    def pdf(self,s):
        if self.Ns is None or self.pmf is None:
            self.run()
        PDF_values = np.sum( 
            [iPMF*scistat.poisson.pmf(iNs,s) for iNs , iPMF in zip(self.Ns,self.pmf)] 
            ,axis=0)
        return PDF_values
    
    def cdf(self,s):
        if self.Ns is None or self.pmf is None:
            self.run()
        
        CDF_values = np.sum( [iPMF*PoissonCDF(s,iNs)  for iNs , iPMF in zip(self.Ns,self.pmf)] ,
                            axis=0) 
        return CDF_values
    
    def cdfsquared(self,u,x):
        return (u -self.cdf(x))**2
    
    def invcdf(self,u):
        
        if hasattr(u,'__len__'):
            cost_func    = [partial(self.cdfsquared,ui) for ui in u]
            invcdf_val   = np.array( 
                            [minimize(icost_func,
                                      self.mode_pdf,
                                      bounds=((0,None),)).x[0] for icost_func in cost_func] 
                    )
        else:
            cost_func    = partial(self.cdfsquared,u)
            invcdf_val   = minimize(cost_func,self.mode_pdf,bounds=((0,None),)).x[0]
        
        return invcdf_val
    
    def get_mean_and_variance(self,signal_range=None):
        if signal_range is None:
            signal_range = [0, self.mode_pmf +10*self.excess_error] 
    
        self.mean      = integrate.quad(lambda x: \
                  x*self.pdf(x), signal_range[0], signal_range[1])[0]
        self.variance  = integrate.quad(lambda x: \
                  (x-self.mean)**2*self.pdf(x), signal_range[0], signal_range[1])[0]
        
        
    def upper_limit(self,alpha=0.95, start=0):
        if alpha<0 or alpha >1:
            raise ValueError("Alpha level must be a real number between 0 and 1!")
        if start < 0:
            raise ValueError("Start point must be equal or greater than zero!")
        if start == 0:
            cdf_start = 0
        else:
            cdf_start = self.cdf(start)
        
        if cdf_start > (1-alpha):
            raise ValueError("Start point too big, cannot find an upper limit!")
        
        upper_limit = self.invcdf( alpha + cdf_start)
        
        return upper_limit
    
    
    def sum_pdfpoints(self, alpha, start):
        end    = self.upper_limit(alpha, start)
        points = np.linspace(start, end, 100)
        return - np.sum( self.pdf( points) )

    def credible_interval(self, alpha=0.6827 ):
        max_start   = self.invcdf( 1- alpha)
        x           = np.linspace( 0, max_start,100, endpoint=False) 
        y           = np.array( [self.sum_pdfpoints( alpha, ix) for ix in x] )
        first_guess = x[ np.argmin(y) ]
        cost_func   = partial(self.sum_pdfpoints,alpha)
        start       = minimize(cost_func,first_guess,bounds=((0,max_start*0.9999),)).x[0]
        end         = self.upper_limit(alpha, start)
        return start, end
    
    
    def __str__(self):
        str_ = f"{self.__class__.__name__}\n"
        str_ += "-" * len(self.__class__.__name__) + "\n"
        str_ += "\n"
        str_ += f"\t{{:32}}:  {self.Non} \n".format("Non")
        str_ += f"\t{{:32}}:  {self.Noff} \n".format("Noff")
        str_ += f"\t{{:32}}:  {self.alpha} \n\n".format("Alpha")
        
        str_ += f"\t{{:32}}:  {self.excess} \n".format("Excess")
        str_ += f"\t{{:32}}:  {self.excess_error} \n".format("SD Excess")
        str_ += f"\t{{:32}}:  {self.LiMa_significance} \n\n".format("Li&Ma Significance")
        
        if self.run_ok:
            str_ += f"\t{{:32}}:  {self.mode_pdf} \n".format("Most probable signal")
            str_ += f"\t{{:32}}:  {self.mean} \n".format("Expected signal")
            str_ += f"\t{{:32}}:  {np.sqrt(self.mean)} \n".format("Signal SD")

        return str_.expandtabs(tabsize=2)
    
    def __repr__(self):
        str_ = f"{self.__class__.__name__}"+"("
        str_ += f"\t {{:1}}: {self.Non}".format("Non")+","
        str_ += f"\t {{:1}}: {self.Noff}".format("Noff")+","
        str_ += f"\t {{:1}}: {self.alpha}".format("Alpha")+","
        
        if self.signal_likelihoods is None and self.bkg_likelihoods is None:
            str_ += f"\t Likelihoods: False"+" )"
        else:
            str_ += f"\t Likelihoods: True"+" )"
            
        return repr(str_.expandtabs(tabsize=1))
    
    
    
def fake_measurement( s, b, alpha, bkg_pdf=None, signal_pdf=None, efficiency=1, seed=None ):
    rng  = np.random.default_rng(seed)
    Ns   = rng.poisson(s)
    Nb   = rng.poisson(alpha*b)
    Non  = Ns + Nb
    
    Noff = rng.poisson(b)
    
    bkg_likelihoods    = None
    signal_likelihoods = None
    
    if signal_pdf is not None and bkg_pdf is not None:
        x_signal = signal_pdf.fake(Ns,seed)
        x_bkg    = bkg_pdf.fake(Nb,seed)
        xON  = np.concatenate( (x_signal,x_bkg))
        
        if efficiency <1:
            cut  = signal_pdf.invcdf(efficiency)
            xON  = xON[xON<=cut]
            Non  = len(xON)
            xOFF = bkg_pdf.fake(Noff,seed)
            xOFF = xOFF[xOFF<=cut]
            Noff = len(xOFF)
            
        
        bkg_likelihoods    = bkg_pdf(xON)
        signal_likelihoods = signal_pdf(xON)
        
    return OnOffMeasurement(Non,Noff,alpha, 
                               bkg_likelihoods    = bkg_likelihoods,
                               signal_likelihoods = signal_likelihoods)




class PDF:
    
    def __init__(self, func=None, pdf_range=(0,1),integration_steps=None):
        
        self.func      = func
        self.pdf_range = pdf_range
        a              = self.pdf_range[0]
        b              = self.pdf_range[1]
        if integration_steps is None:
            self.norm      = 1/integrate.quad(func, a,b )[0]
        else:
            ints = [integrate.quad(func, a,b )[0] 
                    for a, b in zip(integration_steps[:-1],integration_steps[1:])]
            self.norm = 1/np.sum(ints)
            
        self.get_cdf_and_invcdf(integration_steps=integration_steps)
    
    def __call__(self,x):
        return self.norm*self.func(x)
        
    @classmethod   
    def from_data(cls,data,bins,data_range=(0,1)):
        hist      = np.histogram( data, bins=bins, range=data_range)
        x         = hist[1]
        y         = np.insert( hist[0], -1, hist[0][-1])
        hist_func = interpolate.interp1d( x, y , kind='previous' )
        return cls(hist_func, pdf_range=data_range, integration_steps=x)
        
        
    def get_cdf_and_invcdf(self,integration_steps=None):
        a                = self.pdf_range[0]
        b                = self.pdf_range[1]
        if integration_steps is None:
            x            = np.linspace(a,b,1000,endpoint=True)
            cdf_vals     = np.array([integrate.quad(self, a,X )[0] for X in x ])
        else:
            ints         = [integrate.quad(self, a,b )[0] 
                            for a, b in zip(integration_steps[:-1],integration_steps[1:])]
            cdf_vals     = np.cumsum(ints)
            cdf_vals     = np.insert(cdf_vals,0,0)
            cdf_vals[-1] = round(cdf_vals[-1])
            x            = integration_steps
            
        if np.sum( cdf_vals ==  np.sort(cdf_vals) ) == len(cdf_vals):
            self.cdf    =  interpolate.interp1d(x, cdf_vals)
            self.invcdf =  interpolate.interp1d(cdf_vals, x)
        else:
            raise ValueError("PDF is not defined positive in the given range!")
    
    def fake(self,n=None,seed=None):
        if n is None:
            raise ValueError("Please provide how many variables to simulate!")
        rng  = np.random.default_rng(seed)
        u = rng.uniform(0,1,n)
        return self.invcdf(u)
        

        


###################################################
## Log of (Non + Noff - Ns)!/(Non - Ns)! * (1 + 1/alpha)**Ns
def log_single_term(Ns, Non, Noff,a):
    integer_vals  = np.arange(Non-Ns+1, Non + Noff-Ns+1)
    logfactorial  = np.sum( np.log(integer_vals) )
    logsecondterm = Ns*np.log(1 + 1/a)
    return logfactorial + logsecondterm


###################################################
## PMF of the number of signal events NS
def signal_events_PMF( Non, Noff, a):
    Ns         = np.arange(0,Non+1)
    vectfunc   = np.vectorize(log_single_term)
    log_Ns_PMF = vectfunc(Ns, Non, Noff, a)
    vectexp    = np.vectorize( mp.exp)
    Ns_PMF     = vectexp(log_Ns_PMF)
    Ns_PMF    /= np.sum(Ns_PMF)
    return Ns, Ns_PMF 

###################################################
## Combinatorial term C divided by the binomial term
def combinatorial_term(a1,a2):
    if len(a1) != len(a2):
        raise ValueError("Likelihoods values must have same lenght!")
    n     = len(a1)
    
    # First we make one array = 1
    a1 /= a2 
    a2 /= a2
    # We convert the arrays in mpmath quantities
    a1  = a1 * mp.ones(1,n)
    a2  = a2 * mp.ones(1,n)
    
    C     = np.concatenate( ( [1.],np.zeros_like(a1) ))
    for i in range(n):
        D = np.concatenate( ( [0.],C[:-1] ))
        C = a1[i]*C + a2[i]*D
        
    binomial = np.array([mp.binomial(n,i) for i in range(n+1)])
    C       /= binomial
    C       /= np.max(C)
    C       /= np.sum(C) 
    return C  


###################################################
## CDF of Poisson Function
def PoissonCDF(s,n):
    vectfuncCDF   = np.vectorize(mp.gammainc)
    cdf = (1- vectfuncCDF(n+1, s)/mp.gamma(n+1))
    return np.float128(cdf)
    
###################################################
## LI&MA SIGNIFICANCE
def LiMaSignificance(Non,Noff,alfa):
    """Return Li&Ma significance
    """
    return np.sqrt( 2*Non* np.log( (1+alfa)/alfa * ( (Non+0.) / (Non+Noff) ) ) + \
                          2*Noff*np.log( (1+alfa)      * ( (Noff+0.)/ (Non+Noff) ) )   )
