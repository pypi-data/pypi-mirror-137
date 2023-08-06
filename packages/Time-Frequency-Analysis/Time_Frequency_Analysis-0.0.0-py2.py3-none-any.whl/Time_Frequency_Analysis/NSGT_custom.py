
import numpy as np
import scipy
from numpy.fft import fft,ifft,rfft,irfft
import os




#1)This implementation of NSGT CQ is not working only for ksi_max =ksi_s//2-1 
# (both for irregular array and matrix_form)

#2)And it is intended only for real signals (we exploit the conjugate symmetry of the real signals)

#TODO
#1)NA TO FTIAKSW NA PAIZEI KAI GIA ksi_max =ksi_s//2-1 (DEN EINAI PROVLHMA MONO TOY MATRIX FORM)
#2)SLice CQT


class NSGT_CUSTOM:


    g = []
    g_dual = []
    odd_flag_len = 0


    def __init__(self,ksi_s,ksi_min,ksi_max,B,L,matrix_form):
        self.ksi_s=ksi_s
        self.ksi_min=ksi_min
        self.ksi_max=ksi_max
        self.B=B
        self.L=L
        self.matrix_form=matrix_form
        #writing in the correct order the function calls in order for the FORWARD AND BACKWARD methods to work
        self.set_Q_factor() 
        self.check_for_len()  
        self.create_filter_indices()         
        self.create_filters()
        self.get_frame_operator()
        self.get_dual_frame()        

    
    def check_for_len(self):
        if self.L%2:
            #Then it is of odd length and we need to padd a 0 
            # to make it even in order for the rfft to work properly 
            self.odd_flag_len=1
            self.L += 1 

    


    def set_Q_factor(self):
        #calculating the Q factor (as described in the paper) 
        #FOR THE GIVEN TRANSFORM PARAMETERS
        self.K = int(np.ceil(self.B*np.log2(self.ksi_max/self.ksi_min)+1))    
        m = np.arange(self.K-1)+1
        self.fr_range = self.ksi_min*(2**((m-1)/self.B))
        self.Q = 1/(2**(1/self.B)-2**(-1/self.B))  




    def create_filter_indices(self): 
        #bandwidth_inds IS THE SAME FOR BOTH IRREGULAR AND MATRIX FORM :) 

        # self.set_Q_factor() 
        # self.check_for_len()          

        #calculating the argument of the (in theory) continious hann function 
        j = np.arange(self.L)
        arg = j*self.ksi_s/self.L

        
        #the filters  for k = 1 : K
        nnz_bandwidth_inds = []

        k = 0
        for ksi_k in self.fr_range:

            tmp_arg = (arg-ksi_k)/(ksi_k/self.Q)

            #FAST WAY using an indicator function of the bandwidth for each filter in frequency
            tmp_inds = np.abs(tmp_arg)<=1/2
            #M = len(tmp_arg[tmp_inds])
            #converting the true false indices to sequence of integer indecies...
            nnz_bandwidth_inds.append( [index for index, element in enumerate(tmp_inds, start=0) if element] )
            k+=1


        #finding the integer start and end indices for the Tukey window filters (using the allready computed filter's indices)
        #small filter
        a_s = nnz_bandwidth_inds[1][0]
        small_filter_inds = list(np.arange(0,a_s))


        #big filter
        a_b = nnz_bandwidth_inds[len(nnz_bandwidth_inds)-2][-1]
        big_filter_inds = list(np.arange(a_b,self.L//2+1))        

        self.bandwidth_inds = [small_filter_inds] + nnz_bandwidth_inds + [big_filter_inds]



    def create_filters(self):

        #in order to create the filters we have to create the indices for the filters first :)
        #self.create_filter_indices()
        

        #MATRIX FORM CASE:
        if self.matrix_form:
            Nmax = max(list(map( lambda x : len(x) , self.bandwidth_inds))) 
            fft_len = Nmax

            new_inds = []

            
            #creating the extended indices and filter for the small filter (zero padding)---------------------
            fft_len_old = len(self.bandwidth_inds[0]) 
            g_tmp = np.roll( scipy.signal.tukey(fft_len_old*2) , fft_len_old )[:fft_len_old]
            g_tmp = np.concatenate( ( g_tmp , np.zeros(fft_len-fft_len_old) ) )
            self.g.append(g_tmp)
            
            #extend the small_filter_inds
            small_filter_inds = self.bandwidth_inds[0]
            small_filter_end_ind = len(small_filter_inds) 
            extended_inds = list(np.arange(small_filter_end_ind,fft_len))
            small_filter_inds = small_filter_inds + extended_inds            
            new_inds.append(small_filter_inds)
            #----------------------------------------------------------------------------------------------------


            #creating the extended indices for CQ-filters---------------------------------------------------------

            #K = len(self.bandwidth_inds)
            for k in range(1,self.K):

                Lk = len(self.bandwidth_inds[k])
                end = self.bandwidth_inds[k][Lk-1]
                new_inds.append( np.concatenate(( self.bandwidth_inds[k] , np.arange( end+1,end+1 + fft_len-Lk ) )) )
                
                #creating the windows.........
                tmp = np.zeros(fft_len)
                tmp[np.arange(Lk)] = np.hanning(Lk)
                self.g.append(tmp)

            

            #creating the extended indices and filter for the small filter (zero padding)------------------------------------------
            big_filter_inds = self.bandwidth_inds[-1]
            if Nmax!=len(big_filter_inds):
                #creating the filter:
                fft_len_old = len(big_filter_inds)
                padding_len = fft_len-fft_len_old
                g_tmp = scipy.signal.tukey(fft_len_old*2)[:fft_len_old]
                g_tmp = np.concatenate( ( np.zeros(padding_len) , g_tmp ) )
                self.g.append(g_tmp)
            
                #extend the big_filter_inds:
                start = big_filter_inds[0]
                new_start = start - padding_len
                extended_inds = list(np.arange(new_start,start))
                big_filter_inds = extended_inds  + big_filter_inds           
                new_inds.append(big_filter_inds)                

            else:
                #creating the filter:
                new_inds.append(big_filter_inds)
                g_tmp = scipy.signal.tukey(fft_len*2)[:fft_len]
                self.g.append(g_tmp)

                #IN THIS CASE for this filter the new_inds remains the same..


            #The BW inds are changed
            self.bandwidth_inds = new_inds

            

        #IRREGULAR MATRIX CASE:
        else:

            #Creating the small filter:
            fft_len = len(self.bandwidth_inds[0])
            g_small = np.roll( scipy.signal.tukey(fft_len*2) , fft_len )[:fft_len]
            self.g_additional.append(g_small)

            #Creating the big filter:
            fft_len = len(self.bandwidth_inds[-1])
            g_big = scipy.signal.tukey(fft_len*2)[:fft_len]

            self.g_additional.append(g_big)


        # #NOW WE ARE READY TO CREATE THE DUAL FRAME (because we have the frame calculated)
        # self.get_frame_operator()
        # self.get_dual_frame()



    def get_frame_operator(self):
        
        #CONSTRUCTING THE FRAME OPERATOR-----------------------------------------------
        self.frame_operator = np.zeros(self.L//2+1)

        #MATRIX FORM CASE:
        if self.matrix_form:
            for k in range(len(self.g)):
                self.frame_operator[self.bandwidth_inds[k]]+= len(self.bandwidth_inds[k])*self.g[k]**2 

        #IRREGULAR MATRIX CASE:
        else:
            #Small filter
            fft_len = len(self.bandwidth_inds[0])
            self.frame_operator[self.bandwidth_inds[0]]+= fft_len*self.g_additional[0]**2

            #1:K filter
            for k in range(1,self.K):
                fft_len = len(self.bandwidth_inds[k])
                g_tmp = np.hanning(fft_len)
                self.frame_operator[self.bandwidth_inds[k]]+= fft_len*g_tmp**2

            #Big filter
            fft_len = len(self.bandwidth_inds[-1])
            self.frame_operator[self.bandwidth_inds[-1]]+= fft_len*self.g_additional[-1]**2 


    def get_dual_frame(self):
        
        #CONSTRUCTING THE DUAL FRAME------------------------------------------------------

        if self.matrix_form:
            for k in range(len(self.g)):
                self.g_dual.append(self.g[k]/self.frame_operator[self.bandwidth_inds[k]])
        
        else:
            #Small filter
            self.g_dual.append(self.g_additional[0]/self.frame_operator[self.bandwidth_inds[0]])

            #1:K filter
            for k in range(1,self.K):
                fft_len = len(self.bandwidth_inds[k])
                g_tmp = np.hanning(fft_len)           
                self.g_dual.append(g_tmp/self.frame_operator[self.bandwidth_inds[k]])

            #Big filter
            self.g_dual.append(self.g_additional[1]/self.frame_operator[self.bandwidth_inds[-1]])
              


    
    def forward(self,signal):

        # self.create_filters()

        if  self.odd_flag_len:           
            #append is not efficient because it allocates a copy (doesnt change in-place) 
            signal = np.append(signal,0)

        
        ff = rfft(signal) 
        c = []

        #MATRIX FORM CASE:
        if self.matrix_form:
            Nmax = len(self.bandwidth_inds[0])
            # for k in range(len(self.g)):
            #     c.append( np.sqrt(Nmax)*ifft(self.g[k]*ff[self.bandwidth_inds[k]] ) )

            # c = np.array(c)

            c = np.array( list( map( lambda tmp : np.sqrt(Nmax)*ifft(tmp[0]*ff[tmp[1]] ) , zip(self.g,self.bandwidth_inds)) ) )

        #IRREGULAR MATRIX CASE:
        else:
            
            #Small filter
            fft_len = len(self.bandwidth_inds[0])
            c.append( np.sqrt(fft_len)*ifft(self.g_additional[0]*ff[self.bandwidth_inds[0]] ) )
            

            #1:K filter
            # for k in range(1,self.K):
            #     fft_len = len(self.bandwidth_inds[k])
            #     g_tmp = np.hanning(fft_len)
            #     c.append( np.sqrt(fft_len)*ifft(g_tmp*ff[self.bandwidth_inds[k]] ) )

            c = c + list( map( lambda tmp : np.sqrt(len(tmp))*ifft(np.hanning(len(tmp))*ff[tmp] ) , self.bandwidth_inds[1:self.K] ) )


            #Big filter
            fft_len = len(self.bandwidth_inds[-1])
            c.append( np.sqrt(fft_len)*ifft(self.g_additional[1]*ff[self.bandwidth_inds[-1]] ) )            

        
        return c


    
    def backward(self,c):
        
        #L//2+1 because of the rfft....
        f_rec = np.zeros(self.L//2+1).astype('complex128')

        if self.matrix_form:

            for k in range(len(c)):
                #fk.append(np.sqrt(len(new_bandwidth_inds[k]))*fft(c[k]))
                Nmax = len(self.bandwidth_inds[-1])
                fk = np.sqrt(Nmax)*fft(c[k])
                f_rec[self.bandwidth_inds[k]] += fk*self.g_dual[k]

            
        else:
            for k in range(len(self.bandwidth_inds)):
                fft_len = len(self.bandwidth_inds[k])
                fk = np.sqrt(fft_len)*fft(c[k])
                f_rec[self.bandwidth_inds[k]] += fk*self.g_dual[k]

            

        
        #RECONSTRUCTION
        f_rec = np.real(irfft(f_rec))

        if self.odd_flag_len:
            #remove the added zero
            f_rec = f_rec[:len(f_rec)-1]

        

        return f_rec






# if __name__ =='__main__':

#     x,s = load_music()

#     def cputime():
#         utime, stime, cutime, cstime, elapsed_time = os.times()
#         return utime

#     def timeis(func):
#         '''Decorator that reports the execution time.'''
  
#         def wrap(*args, **kwargs):
#             start = time.time()
#             result = func(*args, **kwargs)
#             end = time.time()
            
#             print(func.__name__, end-start)
#             return result
#         return wrap


#     #NSGT cqt
#     ksi_min = 32.7
#     ksi_max = 5000
#     real=1
#     #ksi_max = 21049
#     B=12
#     ksi_s = s
#     #ksi_max =ksi_s//2-1
#     matrix_form = True
#     reduced_form = False

#     #f = x[:len(x)-1]
#     f=x
#     L = len(f)

#     t1 = cputime()
#     nsgt = NSGT_CUSTOM(ksi_s,ksi_min,ksi_max,B,L,matrix_form)
    
#     c = nsgt.forward(f)
#     f_rec = nsgt.backward(c)
#     t2 = cputime()

#     norm = lambda x: np.sqrt(np.sum(np.abs(np.square(x))))
#     rec_err = norm(f_rec - f)/norm(f)
#     print("Reconstruction error : %.16e \t  \n  " %(rec_err) )
#     print("Calculation time: %.3fs"%(t2-t1))
#     #----------------------------------------------------------------------------------------

#     #compare withe library:
#     t1 = cputime()
#     nsgt = instantiate_NSGT( f , s , 'log',ksi_min,ksi_max,B*7,matrix_form,reduced_form,multithreading=False)
#     c1 = NSGT_forword(f,nsgt,pyramid_lvl=0,wavelet_type='db2')
#     f_rec1 = NSGT_backward(c1,nsgt,pyramid_lvl=0,wavelet_type='db2')
#     rec_err = norm(f_rec1 - f)/norm(f)
#     t2 = cputime()

#     print("Reconstruction error : %.16e \t  \n  " %(rec_err) )
#     print("Calculation time: %.3fs"%(t2-t1))

a=0


