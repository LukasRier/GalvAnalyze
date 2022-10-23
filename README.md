# GalvAnalyze
GalvAnalyze is a tool created to simplify the analysis of galvanostatic charge-discharge cycling for battery research scientists. A compiled executable is available for download from the Nottingham Applied Materials and Interfaces group website (https://www.thenamilab.com/about-4) in a plug-and-play format.

### Dependencies
* Python >= 3.7.9
* NumPy >= 1.18.1
* Matplotlib >= 3.3.1
* Pandas >= 1.1.3
* Tkinter

### Downloading GalvAnalzye

The source code for GalvAnalyze can be accessed by cloning this repository

To download the GalvAnalyze executable for MS Windows (recommended for those without experience of using the python programming language), go to https://www.thenamilab.com/about-4, scroll to the bottom of the page and click the “Download GalvAnalyze” button. This will begin the download of a zipped file containing the executable. NOTE: this file is ~321 MB, ensure that you have sufficient space on your hard drive.

Once downloaded, the executable can be run from within the zipped folder. Upon opening of the executable, Windows Defender SmartScreen may declare that this is an “unrecognized app”. To bypass this, press “More Info” and then “Run anyway”.

Should you deem this unsuitable, clone this repository, install the [dependencies](https://github.com/LukasRier/GalvAnalyze/blob/main/dependencies.yml "dependencies") (see below) and run [GalvAnalyze.py](https://github.com/LukasRier/GalvAnalyze/blob/main/GalvAnalyze.py "GalvAnalyze.py")  or generate your own executable by following the below step-by-step guide.

### Compiling GalvAnalyze

Clone the repository and generate a virtual environment from the [dependencies](https://github.com/LukasRier/GalvAnalyze/blob/main/dependencies.yml "dependencies") i.e. using conda:

```
conda env create --file=/path/to/dependencies.yml -n GAInstaller
```

(`GAInstaller` can be substituted with an environment name of choice of course)

Next, install [pyinstaller](https://pyinstaller.org/en/stable/# "pyinstaller") using
```
pip install -U pyinstaller
```
and finally run
```
pyinstaller -F --specpath \path\to\GalvAnalyze -n \path\to\GalvAnalyze -w GalvAnalyze.py
```
where `\path\to` is the location of your cloned repository.

The command above will generate two folders \'dist\' and \'build\'.
\'dist\' will contain your executable.

## DISCLAIMER
GalvAnalyze is provided by the authors “as is” and “with all faults”. The authors makes no representations or warranties of any kind concerning the safety, suitability, lack of viruses, inaccuracries, typrographical errors, or other harmful components of GalvAnalyze. There are inherent dangers in the use of any software, and you are solely responsible for determining whether GalvAnalyze is compatible with your equipment and other software installed on your equipment. You are also solely responsible for the protection of your equipment and backup of your data, and GalvAnalyze will not be liable for any damages you may sugar in conncetin with using, modifying, or distributing GalvAnalyze.
