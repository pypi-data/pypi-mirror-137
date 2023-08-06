
from numpy.fft import rfft,irfft
import numpy as np
import math

#THIS MODULE TAKES ARGUMENTS  (the obvious input signal x)
# 1)hopsize : a  
# 2)freq bins : M
# 3)support of the window : support
# 4)window type : g 

#REQUIERMENTS: 
# 1)the arguments (a,M,support) have to be power of 2
# 2)M>=support (painless case condition) preferably =
# 3)M must be divisible by a ( i.e. M=4096 a=256,512,1024,2048 )



class STFT_CUSTOM:

    #PADD TO NEAREST POWER OF TWO (auxiliary functiuons)---------------------------------------------------
    def NextPowerOfTwo(self,number):
        # Returns next power of two following 'number'
        return math.ceil(math.log(number,2))    
    
    def PadRight(self,arr):
        nextPower = self.NextPowerOfTwo(len(arr))
        deficit = int(math.pow(2, nextPower) - len(arr))

        arr = np.concatenate(( arr,np.zeros(deficit, dtype=arr.dtype)))
        return arr
    #---------------------------------------------------------------------------


    def __init__(self,g,a,M,support,signal_len):

        self.g = g
        self.a = a
        self.M = M
        self.support = support
        self.L = signal_len
        #writing in the correct order the function calls in order for the FORWARD AND BACKWARD methods to work
        self.initialize_TF_parameters()
        self.get_transition_window()
        self.get_frame_operator()


    
    def initialize_TF_parameters(self):
        #In this function we zero pad the signal to the nearest power of 2
        #and further initialize some basic TF parameters

        self.padded_sig_len = 2**self.NextPowerOfTwo( self.L )

        self.N = self.padded_sig_len//self.a
        self.b = self.padded_sig_len//self.M

        #blocks to not compute:
        self.N_avoid = self.M//self.a 

        #padd the g in case M > support (we are still in painless case)
        self.g = np.concatenate((self.g,np.zeros(self.M-len(self.g))))
        self.frame_operator = np.zeros(self.padded_sig_len)




    def get_transition_window(self):
        #transition WINDOW-------------------------------------------------
        self.g_transition = np.roll(self.g,len(self.g)//2)
        all_inds = np.arange(self.padded_sig_len)
        self.initial_inds =  list(all_inds[:len(self.g)//2])  + list(all_inds[:-len(self.g)//2-1:-1][::-1])


    def get_frame_operator(self,): 
        
        self.frame_operator[self.initial_inds]+=self.g_transition**2   
        for n in range(self.N-self.N_avoid):
            self.frame_operator[ n*self.a : n*self.a + self.M] += self.g**2    


    def get_inds(self,X_padded):
        X_padded = np.array(X_padded).T

        self.nnz_inds = np.abs(X_padded[1])!=0

        #DETECTING THE LATEST SHARP TRANSITION (in order to calculate the start indice where the zero padded columns added)
        h = [1,-1]
        #ind = np.argmax(np.flip(LTI_filtering(h,np.flip(self.nnz_inds))))
        ind = np.argmax(np.flip(np.convolve(h,np.flip(self.nnz_inds))))
        #ind = np.argmax(np.flip(nnz_inds))
        self.nb_zeroes = len(self.nnz_inds)-1 - (ind)
        X_orig = X_padded[:,:ind+1] 

        return X_orig         

    def forward(self,signal):


        signal_padded = self.PadRight(signal)
        X = []

        periodized_sig = signal_padded[self.initial_inds]*self.g_transition     
        initial_fourier_len_M = rfft(periodized_sig,norm="ortho")   
        X.append(initial_fourier_len_M) 

        for n in range(self.N-self.N_avoid):
        
            periodized_sig = signal_padded[n*self.a:n*self.a+self.M]*self.g    

            fourier_len_M = rfft(periodized_sig,norm="ortho")
            X.append(fourier_len_M)

        #DELETING the zero padding 
        # (droping the zero columns that came from the signal padding)
        X = self.get_inds(X)

        return X  


    def backward(self,X):
        #adding the requiered zeros in order to reconstruct
        X = np.concatenate( (X,np.zeros((X.shape[0],self.nb_zeroes)) ) , axis=1 )


        self.N = X.shape[1]


        f_rec = np.zeros(len(self.frame_operator)) 
        #Transition window
        f_rec[self.initial_inds] = f_rec[self.initial_inds] + (np.real(irfft(X[:,0],norm="ortho")))*(self.g_transition/self.frame_operator[self.initial_inds])

        for n in range(self.N-self.N_avoid):

            g_dual_tmp = self.g/self.frame_operator[n*self.a:n*self.a+self.M]
            fn = (np.real(irfft(X[:,n+1],norm="ortho")))*g_dual_tmp  
            f_rec[n*self.a:n*self.a+self.M] = f_rec[n*self.a:n*self.a+self.M] + fn  

        #Equivalent in one line
        #f_rec = list(map( lambda n : f_rec[n*a:n*a+M] +  ( np.real( irfft( X[:,n+1],norm="ortho") ) )* ( g/frame_operator[n*a:n*a+M] )    , np.arange(N-N_avoid) ))

        return f_rec[:self.L]
              
          




# if __name__ =='__main__':
#     #load music
#     x,s = load_music()

#     def cputime():
#         utime, stime, cutime, cstime, elapsed_time = os.times()
#         return utime

#     a = 512
#     M = 4096
#     support = 4096
#     g = np.hanning(support) 
#     L = len(x)      


#     t1 = cputime()
#     stft = STFT_CUSTOM(g,a,M,support,L)
#     X = stft.forward(x)
#     x_rec = stft.backward(X)
#     t2 = cputime()


#     norm = lambda x: np.sqrt(np.sum(np.abs(np.square(x))))
#     rec_err = norm(x_rec - x)/norm(x)
#     print("Calculation time: %.3fs"%(t2-t1))
#     print("Reconstruction error : %.16e \t  \n  " %(rec_err) )    


a = 0