"""
Module that contains the command line app.

Why does this file exist, and why not put this in __main__?

  You might be tempted to import things from __main__ later, but that will cause
  problems: the code will get executed twice:

  - When you run `python -mTime_Frequency_Analysis` python will execute
    ``__main__.py`` as a script. That means there won't be any
    ``Time_Frequency_Analysis.__main__`` in ``sys.modules``.
  - When you import __main__ it will get executed again (as a module) because
    there's no ``Time_Frequency_Analysis.__main__`` in ``sys.modules``.

  Also see (1) from http://click.pocoo.org/5/setuptools/#setuptools-integration
"""

import argparse
import yaml

from Audio_proc_lib.audio_proc_functions import * 
from Plotting_funcs.Plotting_util_and_other import *
import NSGT_custom,STFT_custom
import os


parser = argparse.ArgumentParser(description='Command description.')
# parser.add_argument('names', metavar='NAME', nargs=argparse.ZERO_OR_MORE,
#                     help="A name of something.")

parser.add_argument('--front_end', type=str, default="STFT",
                        help='provide Transform name')

parser.add_argument('-p', '--params', type=yaml.load,
                        help='provide Transform parameters as a quoted json sting')

parser.add_argument('--plot_spectrograms', type=str, default="True",
                        help='flag for ploting the spectrograms')

args, _ = parser.parse_known_args()



def main():    

    #load music
    x,s = load_music()


    def cputime():
        utime, stime, cutime, cstime, elapsed_time = os.times()
        return utime


    def timeis(func):
        '''Decorator that reports the execution time.'''
  
        def wrap(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            
            print(func.__name__, end-start)
            return result
        return wrap


    if args.front_end=="NSGT":
        #NSGT cqt
        # ksi_min = 32.7
        # ksi_max = 5000
        # real=1
        # #ksi_max = 21049
        # B=12
        ksi_s = s
        #ksi_max =ksi_s//2-1
        matrix_form = True
        reduced_form = False

        #f = x[:len(x)-1]
        f=x
        L = len(f)

        t1 = cputime()
        nsgt = NSGT_custom.NSGT_CUSTOM(ksi_s,args.params["ksi_min"],args.params["ksi_max"],args.params["B"],L,matrix_form)
        
        c = nsgt.forward(f)
        f_rec = nsgt.backward(c)
        t2 = cputime()

        norm = lambda x: np.sqrt(np.sum(np.abs(np.square(x))))
        rec_err = norm(f_rec - f)/norm(f)
        print("Reconstruction error : %.16e \t  \n  " %(rec_err) )
        print("Calculation time (forward and backward): %.3fs"%(t2-t1))
        #----------------------------------------------------------------------------------------

        #compare with library:
        t1 = cputime()
        nsgt = instantiate_NSGT( f , ksi_s , 'log',args.params["ksi_min"],args.params["ksi_max"],args.params["B"]*7,matrix_form,reduced_form,multithreading=False)
        c1 = NSGT_forword(f,nsgt,pyramid_lvl=0,wavelet_type='db2')
        f_rec1 = NSGT_backward(c1,nsgt,pyramid_lvl=0,wavelet_type='db2')
        rec_err = norm(f_rec1 - f)/norm(f)
        t2 = cputime()

        print("Reconstruction error : %.16e \t  \n  " %(rec_err) )
        print("Calculation time (forward and backward): %.3fs"%(t2-t1))      
        #_--------------------------------------------------------------------------------------------



        if args.plot_spectrograms=="True":
          plot_spectrogram(c,ksi_s,"linear")
          plt.title("NSGT_custom")
          plt.figure()
          plot_spectrogram(c1,ksi_s,"linear")
          plt.title("NSGT_library")  
          plt.show()

        #_--------------------------------------------------------------------------------------------

    elif args.front_end=="STFT":
        #TESTING STFT_custom----------------------------------------------
        # a = 512
        # M = 4096
        # support = 4096
        g = np.hanning(args.params["support"]) 
        L = len(x)      


        t1 = cputime()
        stft = STFT_custom.STFT_CUSTOM(g,args.params["a"],args.params["M"],args.params["support"],L)
        X = stft.forward(x)
        x_rec = stft.backward(X)
        t2 = cputime()
        norm = lambda x: np.sqrt(np.sum(np.abs(np.square(x))))
        rec_err = norm(x_rec - x)/norm(x)
        print("Calculation time (forward and backward): %.3fs"%(t2-t1))
        print("Reconstruction error : %.16e \t  \n  " %(rec_err) )  
        #-----------------------------------------------------------------------------------------------

        #compare with library:
        t1 = cputime()
        X1 = librosa.stft(x,  n_fft =args.params["M"] , hop_length=args.params["a"], win_length=args.params["support"], window=g )
        x_rec1 = librosa.istft(X1,  hop_length=args.params["a"], win_length=args.params["support"], window=g )
        t2 = cputime()
        rec_err = norm(x_rec1 - x[:len(x_rec1)] )/norm(x[:len(x_rec1)])
        print("Calculation time (forward and backward): %.3fs"%(t2-t1))
        print("Reconstruction error : %.16e \t  \n  " %(rec_err) )  
        #-----------------------------------------------------------------------------------------------------------------------------------


        if args.plot_spectrograms=="True":
          plot_spectrogram(X,s)
          plt.title("STFT_custom")

          plt.figure()
          plot_spectrogram(X1,s)
          plt.title("STFT_librsoa")
          plt.show()

        #------------------------------------------------------------------
