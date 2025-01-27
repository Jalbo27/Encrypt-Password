using encryptimages.Properties;
using System;
using System.Drawing;
using System.Windows.Forms;

namespace encryptimages
{
    public partial class Form1 : Form
    {
        private string fileName = "";
        private Form newDialog;
        public Form1() => LoadForm();

        private void LoadForm()
        {
            InitializeComponent();
        }

        private void scuroToolStripMenuItem_Click(object sender, EventArgs e)
        {
            if (!scuroToolStripMenuItem.Checked)
            {
                if (chiaroToolStripMenuItem.Checked)
                    chiaroToolStripMenuItem.Checked = false;
                scuroToolStripMenuItem.Checked = true;
            }
            else
            {
                scuroToolStripMenuItem.Checked = false;
                chiaroToolStripMenuItem_Click(sender, e);
            }
        }

        private void chiaroToolStripMenuItem_Click(object sender, EventArgs e)
        {
            if (!chiaroToolStripMenuItem.Checked)
            {
                if (scuroToolStripMenuItem.Checked)
                    scuroToolStripMenuItem.Checked = false;
                chiaroToolStripMenuItem.Checked = true;
            }
            else
            {
                chiaroToolStripMenuItem.Checked = false;
                scuroToolStripMenuItem_Click(sender, e);
            }
        }

        private void caricaDaUnBackupToolStripMenuItem_Click(object sender, EventArgs e)
        {
            fileName = FileDialog("Select a backup", "Backup Password file (*.ppdb)|*.ppdb", "Open Passwords' backup file");
            if(fileName != null)
            {

            }
        }

        private string FileDialog(string fileName, string filter, string title)
        {
            OpenFileDialog fileDialog = new OpenFileDialog()
            {
                FileName = fileName,
                Filter = filter,
                Title = title
            };

            DialogResult result = fileDialog.ShowDialog();
            if (fileDialog.FileName != "" && (result == DialogResult.OK || result == DialogResult.Yes))
                return fileDialog.FileName;
            else
                return "";
        }

        private void nuovaPasswordToolStripMenuItem_Click(object sender, EventArgs e)
        {
            TextBox newpassText = new TextBox()
            {
                Text = "Inserisci la nuova password...",
                Size = new Size(200, Height)
            };
            Button butPass = new Button()
            {
                Text = "Conferma",
                Location = new Point(205, 0),
                Capture = true,
            };
            butPass.Click += new EventHandler(SubmitNewPassword_Click);

            newDialog = new Form() 
            {
                Icon = new Icon("D:\\school\\Progetto\\encryptimages\\password_icon.ico"),
                Text = "Inserisci una nuova password",
                Size = new Size(300, 100),
                MinimizeBox = false,
                MaximizeBox = false,
                AutoSize = false,
                AutoScaleMode = AutoScaleMode.None,
                AutoSizeMode = AutoSizeMode.GrowAndShrink,
                FormBorderStyle = FormBorderStyle.Fixed3D
            };
            newDialog.Controls.AddRange(
                new Control[]
                {
                    newpassText,
                    butPass
                }
            );

            newDialog.ShowDialog();
        }

        private void SubmitNewPassword_Click(object sender, EventArgs e)
        {
            string newPass = newDialog.Controls[0].Text;
            newDialog.Dispose();
            newDialog.Close();
        }

        private void apriPasswordToolStripMenuItem_Click(object sender, EventArgs e)
        {
            fileName = FileDialog("Select a backup", "Backup Password file (*.ppdb)|*.ppdb", "Open Passwords' backup file");
        }

        private void tabella_password_CellContentClick(object sender, DataGridViewCellEventArgs e)
        {

        }

        private void confirm_button_Click(object sender, EventArgs e)
        {
            if(name_text.Text != "" || username_text.Text != "" || password_text.Text != "" || uri_text.Text != "")
            {
                int last_row = tabella_password.Rows.Count - 1;

                this.tabella_password.Rows.Add();
                tabella_password.Rows[last_row].Cells["Nome"].Value = name_text.Text;
                tabella_password.Rows[last_row].Cells["Username"].Value = username_text.Text;
                tabella_password.Rows[last_row].Cells["Password"].Value = password_text.Text;
                tabella_password.Rows[last_row].Cells["URI"].Value = uri_text.Text;
            }
            else
            {
                //if (name_text.Text == "")


            }
        }
    }
}
