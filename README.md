# background-media-translator

Background worker for transcribing and translating media files dropped in a folder. 

## Installation and running

1. Download and install the Visual C++ Redistributables from https://aka.ms/vs/17/release/vc_redist.x64.exe
1. Download and extract the latest release of this software from https://github.com/hilderonny/background-media-translator/releases
1. Install Python 3.11 from https://www.python.org/downloads/windows/
1. Open Terminal in the folder **./BackgroundMediaTranslator/Scripts** of the repository and run `pip install -r .\requirements.txt`
1. Run the program itself and start with setting up required paths

## Development setup

1. Install Visual Studio Community 2022 from https://learn.microsoft.com/en-us/visualstudio/releases/2022/release-notes
1. Select
	1. Workload **.NET Desktop** with *Windows App SDK C# Templates*
	1. Workload **Python**
	1. Component **Windows 10 SDK (10.0.190412.0)**
1. Install Python 3.11 from https://www.python.org/downloads/windows/
1. Open the solution **BackgroundMediaTranslator/BackgroundMediaTranslator.sln**
1. Right click on the solution in the solution explorer and run **Restore NuGet Packages**
1. Open Terminal in the folder **./BackgroundMediaTranslator** of the repository and run `pip install -r .\requirements.txt`
