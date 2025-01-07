namespace encryptimages
{
    partial class Form1
    {
        /// <summary>
        /// Variabile di progettazione necessaria.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Pulire le risorse in uso.
        /// </summary>
        /// <param name="disposing">ha valore true se le risorse gestite devono essere eliminate, false in caso contrario.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Codice generato da Progettazione Windows Form

        /// <summary>
        /// Metodo necessario per il supporto della finestra di progettazione. Non modificare
        /// il contenuto del metodo con l'editor di codice.
        /// </summary>
        private void InitializeComponent()
        {
            this.browser_button = new System.Windows.Forms.Button();
            this.path = new System.Windows.Forms.TextBox();
            this.panel1 = new System.Windows.Forms.Panel();
            this.next_button = new System.Windows.Forms.Button();
            this.pictureBox1 = new System.Windows.Forms.PictureBox();
            this.fileDialog = new System.Windows.Forms.OpenFileDialog();
            this.panel1.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.pictureBox1)).BeginInit();
            this.SuspendLayout();
            // 
            // browser_button
            // 
            this.browser_button.Location = new System.Drawing.Point(247, 19);
            this.browser_button.Name = "browser_button";
            this.browser_button.Size = new System.Drawing.Size(71, 27);
            this.browser_button.TabIndex = 0;
            this.browser_button.Text = "Browser...";
            this.browser_button.UseVisualStyleBackColor = true;
            this.browser_button.Click += new System.EventHandler(this.browser_button_Click);
            // 
            // path
            // 
            this.path.Location = new System.Drawing.Point(15, 19);
            this.path.Name = "path";
            this.path.Size = new System.Drawing.Size(226, 22);
            this.path.TabIndex = 1;
            this.path.Text = "Insert path....";
            // 
            // panel1
            // 
            this.panel1.AutoSize = true;
            this.panel1.AutoSizeMode = System.Windows.Forms.AutoSizeMode.GrowAndShrink;
            this.panel1.Controls.Add(this.next_button);
            this.panel1.Controls.Add(this.browser_button);
            this.panel1.Controls.Add(this.path);
            this.panel1.Controls.Add(this.pictureBox1);
            this.panel1.Dock = System.Windows.Forms.DockStyle.Fill;
            this.panel1.Location = new System.Drawing.Point(0, 0);
            this.panel1.Name = "panel1";
            this.panel1.Size = new System.Drawing.Size(984, 684);
            this.panel1.TabIndex = 2;
            // 
            // next_button
            // 
            this.next_button.Anchor = ((System.Windows.Forms.AnchorStyles)((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom) 
            | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.next_button.Enabled = false;
            this.next_button.Location = new System.Drawing.Point(863, 572);
            this.next_button.Name = "next_button";
            this.next_button.Size = new System.Drawing.Size(92, 96);
            this.next_button.TabIndex = 1;
            this.next_button.Text = "Next";
            this.next_button.UseVisualStyleBackColor = true;
            this.next_button.Click += new System.EventHandler(this.next_button_Click);
            // 
            // pictureBox1
            // 
            this.pictureBox1.Location = new System.Drawing.Point(391, 63);
            this.pictureBox1.Name = "pictureBox1";
            this.pictureBox1.Size = new System.Drawing.Size(183, 144);
            this.pictureBox1.SizeMode = System.Windows.Forms.PictureBoxSizeMode.AutoSize;
            this.pictureBox1.TabIndex = 0;
            this.pictureBox1.TabStop = false;
            // 
            // fileDialog
            // 
            this.fileDialog.Filter = "Images (*.jpg, *.jpeg, *.png)|*.jpg;*.jpeg;*.png";
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(8F, 16F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.AutoSize = true;
            this.ClientSize = new System.Drawing.Size(984, 684);
            this.Controls.Add(this.panel1);
            this.Name = "Form1";
            this.Text = "Encrypt Images - Alberto Lorenzini";
            this.panel1.ResumeLayout(false);
            this.panel1.PerformLayout();
            ((System.ComponentModel.ISupportInitialize)(this.pictureBox1)).EndInit();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Button browser_button;
        private System.Windows.Forms.TextBox path;
        private System.Windows.Forms.Panel panel1;
        private System.Windows.Forms.PictureBox pictureBox1;
        private System.Windows.Forms.OpenFileDialog fileDialog;
        private System.Windows.Forms.Button next_button;
    }
}

