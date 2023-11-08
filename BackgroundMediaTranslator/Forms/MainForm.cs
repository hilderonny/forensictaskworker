
using System.Diagnostics;
using System.Reflection;

namespace BackgroundMediaTranslator.Forms
{
    public partial class MainForm : Form
    {

        private AppSettings settings = AppSettings.Default;
        private readonly SynchronizationContext? synchronizationContext;

        public MainForm()
        {
            synchronizationContext = SynchronizationContext.Current;
            InitializeComponent();
            LoadSettings();

            Version? version = Assembly.GetExecutingAssembly().GetName().Version;
            Text += " " + version?.Major + "." + version?.Minor + "." + version?.Build;
        }

        private void LoadSettings()
        {
            labelHomePythonPath.Text = settings.PythonPath;
            labelSettingsPythonPath.Text = settings.PythonPath;
            labelHomeWhisperPath.Text = settings.WhisperPath;
            labelSettingsWhisperPath.Text = settings.WhisperPath;
            labelHomeArgosPath.Text = settings.ArgosTranslatePath;
            labelSettingsArgosPath.Text = settings.ArgosTranslatePath;
            labelHomeInputPath.Text = settings.InputPath;
            labelSettingsInputPath.Text = settings.InputPath;
            labelHomeProcessingPath.Text = settings.ProcessingPath;
            labelSettingsProcessingPath.Text = settings.ProcessingPath;
            labelHomeOutputPath.Text = settings.OutputPath;
            labelSettingsOutputPath.Text = settings.OutputPath;
            labelHomeWhisperModel.Text = settings.WhisperModel;
            comboBoxSettingsWhisperModel.SelectedItem = settings.WhisperModel;
        }

        private void comboBoxSettingsWhisperModel_SelectedIndexChanged(object sender, EventArgs e)
        {
            settings.WhisperModel = comboBoxSettingsWhisperModel.SelectedItem.ToString();
            settings.Save();
            LoadSettings();
        }

        private void buttonHomeChangeSettings_Click(object sender, EventArgs e)
        {
            tabControl.SelectTab(tabPageSettings);
        }

        private void buttonSettingsChooseInputPath_Click(object sender, EventArgs e)
        {
            FolderBrowserDialog folderBrowserDialog = new()
            {
                InitialDirectory = settings.InputPath
            };
            if (folderBrowserDialog.ShowDialog() == DialogResult.OK)
            {
                settings.InputPath = folderBrowserDialog.SelectedPath;
                settings.Save();
                LoadSettings();
            }
        }

        private void buttonSettingsChooseProcessingPath_Click(object sender, EventArgs e)
        {
            FolderBrowserDialog folderBrowserDialog = new()
            {
                InitialDirectory = settings.ProcessingPath
            };
            if (folderBrowserDialog.ShowDialog() == DialogResult.OK)
            {
                settings.ProcessingPath = folderBrowserDialog.SelectedPath;
                settings.Save();
                LoadSettings();
            }
        }

        private void buttonSettingsChooseOutputPath_Click(object sender, EventArgs e)
        {
            FolderBrowserDialog folderBrowserDialog = new()
            {
                InitialDirectory = settings.OutputPath
            };
            if (folderBrowserDialog.ShowDialog() == DialogResult.OK)
            {
                settings.OutputPath = folderBrowserDialog.SelectedPath;
                settings.Save();
                LoadSettings();
            }
        }

        private void buttonSettingsChoosePythonPath_Click(object sender, EventArgs e)
        {
            FolderBrowserDialog folderBrowserDialog = new()
            {
                InitialDirectory = settings.PythonPath
            };
            if (folderBrowserDialog.ShowDialog() == DialogResult.OK)
            {
                settings.PythonPath = folderBrowserDialog.SelectedPath;
                settings.Save();
                LoadSettings();
            }
        }

        private void buttonSettingsChooseWhisperPath_Click(object sender, EventArgs e)
        {
            FolderBrowserDialog folderBrowserDialog = new()
            {
                InitialDirectory = settings.WhisperPath
            };
            if (folderBrowserDialog.ShowDialog() == DialogResult.OK)
            {
                settings.WhisperPath = folderBrowserDialog.SelectedPath;
                settings.Save();
                LoadSettings();
            }
        }

        private void buttonHomeStart_Click(object sender, EventArgs e)
        {
            Process? process = null;
            if (buttonHomeStart.Text == "Starten")
            {
                string command = settings.PythonPath + "\\python.exe";
                string modelKey = new Dictionary<string, string> {
                    { "Tiny", "tiny" },
                    { "Base", "base" },
                    { "Small", "small" },
                    { "Medium", "medium" },
                    { "Large V2", "large-v2" },
                }[settings.WhisperModel];
                string arguments = ".\\Scripts\\BackgroundMediaTranslatorCLI.py -i " + settings.InputPath + " -p " + settings.ProcessingPath + " -o " + settings.OutputPath + " -w " + settings.WhisperPath + " -a " + settings.ArgosTranslatePath + " -m " + modelKey;
                richTextBoxConsoleOutput.Text = "";
                WriteToConsole(command + " " + arguments);
                process = new Process
                {
                    StartInfo = new ProcessStartInfo
                    {
                        FileName = command,
                        UseShellExecute = false,
                        RedirectStandardOutput = true,
                        RedirectStandardError = true,
                        Arguments = arguments,
                        CreateNoWindow = true
                    }
                };
                process.OutputDataReceived += (sender, args) => synchronizationContext?.Post(_ => WriteToConsole(args.Data), null);
                process.ErrorDataReceived += (sender, args) => synchronizationContext?.Post(_ => WriteToConsole(args.Data), null);
                process.Start();
                process.BeginOutputReadLine();
                process.BeginErrorReadLine();
                buttonHomeStart.Text = "Stoppen";
            }
            else
            {
                process?.Kill();
                process?.WaitForExit();
                buttonHomeStart.Text = "Starten";
            }
        }

        private void WriteToConsole(string? line)
        {
            richTextBoxConsoleOutput.AppendText(line);
            richTextBoxConsoleOutput.AppendText(Environment.NewLine);
            richTextBoxConsoleOutput.ScrollToCaret();
        }

        private void buttonSettingsChoosArgosPath_Click(object sender, EventArgs e)
        {
            FolderBrowserDialog folderBrowserDialog = new()
            {
                InitialDirectory = settings.ArgosTranslatePath
            };
            if (folderBrowserDialog.ShowDialog() == DialogResult.OK)
            {
                settings.ArgosTranslatePath = folderBrowserDialog.SelectedPath;
                settings.Save();
                LoadSettings();
            }
        }
    }
}
