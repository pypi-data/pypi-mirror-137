import numpy as np
import scipy.stats as scistat
import scipy.integrate as integrate
from scipy.optimize import minimize
from functools import partial
import mpmath as mp
mp.dps = 25; mp.pretty = True


class basilpy:
    def __init__(self,
                 Non, 
                 Noff, 
                 alpha, 
                 Ns                 = None ,
                 pmf                = None ,
                 signal_likelihoods = None ,
                 bkg_likelihoods    = None ,
                ):
        
        self.Non                = Non
        self.Noff               = Noff
        self.alpha              = alpha
        self.excess             = Non - alpha*Noff
        self.excess_error       = np.sqrt( Non + alpha**2*Noff)
        self.LiMa_significance  = LiMaSignificance(Non,Noff,alpha)*np.sign(self.excess)
        self.Ns                 = Ns
        self.pmf                = pmf
        self.signal_likelihoods = signal_likelihoods
        self.bkg_likelihoods    = bkg_likelihoods
        
        self.mean               = None
        self.variance           = None
        self.mode_pmf           = None
    
    
    def run(self,**par):
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

    def credible_interval(self, alpha ):
        max_start   = self.invcdf( 1- alpha)
        x           = np.linspace( 0, max_start,100, endpoint=False) 
        y           = np.array( [self.sum_pdfpoints( alpha, ix) for ix in x] )
        first_guess = x[ np.argmin(y) ]
        cost_func   = partial(self.sum_pdfpoints,alpha)
        start       = minimize(cost_func,first_guess,bounds=((0,max_start*0.9999),)).x[0]
        end         = bs.upper_limit(alpha, start)
        return start, end
    
    
    def __str__(self):
        str_ = f"{self.__class__.__name__}\n"
        str_ += "-" * len(self.__class__.__name__) + "\n"
        str_ += "\n"
        str_ += f"\t{{:32}}:  {self.Non} \n".format("Non")
        str_ += f"\t{{:32}}:  {self.Noff} \n".format("Noff")
        str_ += f"\t{{:32}}:  {self.alpha} \n\n".format("Alpha")
        
        str_ += f"\t{{:32}}:  {self.excess} \n".format("Excess")
        str_ += f"\t{{:32}}:  {self.excess_error} \n".format("Error Excess")
        str_ += f"\t{{:32}}:  {self.LiMa_significance} \n\n".format("Li&Ma Significance")
        
        str_ += f"\t{{:32}}:  {self.mode_pdf} \n".format("Most probable signal")
        str_ += f"\t{{:32}}:  {self.mean} \n".format("Expected signal")
        str_ += f"\t{{:32}}:  {np.sqrt(self.mean)} \n".format("Root mean squared")
        
        


        return str_.expandtabs(tabsize=2)

        





    





def log_single_term(Ns, Non, Noff,a):
    integer_vals  = np.arange(Non-Ns+1, Non + Noff-Ns+1)
    logfactorial  = np.sum( np.log(integer_vals) )
    logsecondterm = Ns*np.log(1 + 1/a)
    return logfactorial + logsecondterm


def signal_events_PMF( Non, Noff, a):
    Ns         = np.arange(0,Non+1)
    vectfunc   = np.vectorize(log_single_term)
    log_Ns_PMF = vectfunc(Ns, Non, Noff, a)
    vectexp    = np.vectorize( mp.exp)
    Ns_PMF     = vectexp(log_Ns_PMF)
    Ns_PMF    /= np.sum(Ns_PMF)
    return Ns, Ns_PMF #np.array(Ns_PMF.tolist(),dtype=np.float32)  


def signal_PDF( s, Non, Noff, a):
    Ns, PMF = signal_events_PMF(Non, Noff, a)
    return s, np.sum( [iPMF*scistat.poisson.pmf(iNs,s) for iNs , iPMF in zip(Ns,PMF)] ,axis=0)


def combinatorial_term(a1,a2):
    if len(a1) != len(a2):
        raise ValueError("Likelihoods values must have same lenght!")
    n     = len(a1)
    
    a1 /= a2 
    a1  = a1 * mp.ones(1,n)
    a2 /= a2
    a2  = a2 * mp.ones(1,n)
    
  
    C     = np.concatenate( ( [1.],np.zeros_like(a1) ))
    for i in range(n):
        D = np.concatenate( ( [0.],C[:-1] ))
        C = a1[i]*C + a2[i]*D
        
    binomial = np.array([mp.binomial(n,i) for i in range(n+1)])
    C       /= binomial
    C       /= np.max(C)
    C       /= np.sum(C) 
    return C #np.array(C.tolist(),dtype=np.float32)  



    


def PoissonCDF(s,n):
    vectfuncCDF   = np.vectorize(mp.gammainc)
    cdf = (1- vectfuncCDF(n+1, s)/mp.gamma(n+1))
    return np.float128(cdf)
    
###################################################
###################################################
## LI&MA SIGNIFICANCE
def LiMaSignificance(Non,Noff,alfa):
    """Return Li&Ma significance
    """
    return np.sqrt( 2*Non* np.log( (1+alfa)/alfa * ( (Non+0.) / (Non+Noff) ) ) + \
                          2*Noff*np.log( (1+alfa)      * ( (Noff+0.)/ (Non+Noff) ) )   )



