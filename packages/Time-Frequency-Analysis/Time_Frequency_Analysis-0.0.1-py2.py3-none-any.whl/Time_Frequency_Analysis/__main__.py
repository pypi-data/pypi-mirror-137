"""
Entrypoint module, in case you use `python -mTime_Frequency_Analysis`.


Why does this file exist, and why __main__? For more info, read:

- https://www.python.org/dev/peps/pep-0338/
- https://docs.python.org/2/using/cmdline.html#cmdoption-m
- https://docs.python.org/3/using/cmdline.html#cmdoption-m
"""
#from Time_Frequency_Analysis.cli import main
from cli import main


#execute the __main__.py module in order to test (and compare with the library) the transforms  
# 1)execution time 2)perfect reconstruction property 3)visualization   
#For NSGT_CQT : python __main__.py --front_end NSGT -p "{ ksi_min : 32.07 , ksi_max : 3907.07 , B : 12 }" --plot_spectrograms True
#For STFT : python __main__.py --front_end STFT -p "{ a : 1024 , M : 4096 , support : 4096 }" --plot_spectrograms True

if __name__ == "__main__":

    main()



