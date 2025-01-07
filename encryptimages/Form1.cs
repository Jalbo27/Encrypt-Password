using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Net.Mail;
using System.Reflection;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace encryptimages
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
            /*var outPutDirectory = Path.GetDirectoryName(Assembly.GetExecutingAssembly().CodeBase);
            var logoimage = Path.Combine(outPutDirectory, "Images\\logo.png");
            string relLogo = new Uri(logoimage).LocalPath;
            var logoImage = new LinkedResource(relLogo);*/
        }

        private void browser_button_Click(object sender, EventArgs e)
        {            
            if(fileDialog.ShowDialog() != DialogResult.OK)
            {
                return;
            }

            string filename = fileDialog.FileName;
            path.Text = filename;
            pictureBox1.Load(filename);
            next_button.Enabled = true;
        }

        private void next_button_Click(object sender, EventArgs e)
        {
            panel1.Visible = false;

            loadNextPage();
        }

        private void loadNextPage() 
        {
            panel1.Visible=true;
            foreach (Control p in panel1.Controls)
                if(!p.Equals(pictureBox1))
                    p.Visible = false;
            pictureBox1.Location = new System.Drawing.Point(100, 50);
        }
    }
}
