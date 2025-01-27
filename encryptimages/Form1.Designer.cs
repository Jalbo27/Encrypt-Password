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
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(Form1));
            this.panel1 = new System.Windows.Forms.Panel();
            this.confirm_button = new System.Windows.Forms.Button();
            this.uri_text = new System.Windows.Forms.TextBox();
            this.password_text = new System.Windows.Forms.TextBox();
            this.username_text = new System.Windows.Forms.TextBox();
            this.name_text = new System.Windows.Forms.TextBox();
            this.label4 = new System.Windows.Forms.Label();
            this.label3 = new System.Windows.Forms.Label();
            this.label2 = new System.Windows.Forms.Label();
            this.label1 = new System.Windows.Forms.Label();
            this.tabella_password = new System.Windows.Forms.DataGridView();
            this.menuStrip1 = new System.Windows.Forms.MenuStrip();
            this.toolStripMenuItem1 = new System.Windows.Forms.ToolStripMenuItem();
            this.nuovaPasswordToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.apriPasswordToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.caricaDaUnBackupToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.salvaPasswordToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.salvaTutteLePasswordToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.modificaToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.generaPasswordToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.visualizzaToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.themeToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.chiaroToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.scuroToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.Nome = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.Password = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.Username = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.URI = new System.Windows.Forms.DataGridViewLinkColumn();
            this.Edita = new System.Windows.Forms.DataGridViewButtonColumn();
            this.DeleteButton = new System.Windows.Forms.DataGridViewButtonColumn();
            this.panel1.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.tabella_password)).BeginInit();
            this.menuStrip1.SuspendLayout();
            this.SuspendLayout();
            // 
            // panel1
            // 
            this.panel1.AutoSize = true;
            this.panel1.Controls.Add(this.confirm_button);
            this.panel1.Controls.Add(this.uri_text);
            this.panel1.Controls.Add(this.password_text);
            this.panel1.Controls.Add(this.username_text);
            this.panel1.Controls.Add(this.name_text);
            this.panel1.Controls.Add(this.label4);
            this.panel1.Controls.Add(this.label3);
            this.panel1.Controls.Add(this.label2);
            this.panel1.Controls.Add(this.label1);
            this.panel1.Controls.Add(this.tabella_password);
            this.panel1.Controls.Add(this.menuStrip1);
            this.panel1.Dock = System.Windows.Forms.DockStyle.Fill;
            this.panel1.Location = new System.Drawing.Point(0, 0);
            this.panel1.Margin = new System.Windows.Forms.Padding(3, 2, 3, 2);
            this.panel1.Name = "panel1";
            this.panel1.Size = new System.Drawing.Size(984, 684);
            this.panel1.TabIndex = 2;
            // 
            // confirm_button
            // 
            this.confirm_button.Location = new System.Drawing.Point(888, 91);
            this.confirm_button.Name = "confirm_button";
            this.confirm_button.Size = new System.Drawing.Size(75, 23);
            this.confirm_button.TabIndex = 10;
            this.confirm_button.Text = "Conferma";
            this.confirm_button.UseVisualStyleBackColor = true;
            this.confirm_button.Click += new System.EventHandler(this.confirm_button_Click);
            // 
            // uri_text
            // 
            this.uri_text.Location = new System.Drawing.Point(739, 93);
            this.uri_text.Name = "uri_text";
            this.uri_text.Size = new System.Drawing.Size(108, 22);
            this.uri_text.TabIndex = 9;
            // 
            // password_text
            // 
            this.password_text.Location = new System.Drawing.Point(509, 92);
            this.password_text.Name = "password_text";
            this.password_text.Size = new System.Drawing.Size(108, 22);
            this.password_text.TabIndex = 8;
            // 
            // username_text
            // 
            this.username_text.Location = new System.Drawing.Point(279, 92);
            this.username_text.Name = "username_text";
            this.username_text.Size = new System.Drawing.Size(108, 22);
            this.username_text.TabIndex = 7;
            // 
            // name_text
            // 
            this.name_text.Location = new System.Drawing.Point(56, 93);
            this.name_text.Name = "name_text";
            this.name_text.Size = new System.Drawing.Size(108, 22);
            this.name_text.TabIndex = 6;
            // 
            // label4
            // 
            this.label4.AutoSize = true;
            this.label4.Location = new System.Drawing.Point(53, 52);
            this.label4.Name = "label4";
            this.label4.Size = new System.Drawing.Size(44, 16);
            this.label4.TabIndex = 5;
            this.label4.Text = "Nome";
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Location = new System.Drawing.Point(736, 52);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(41, 16);
            this.label3.TabIndex = 4;
            this.label3.Text = "URI://";
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(276, 52);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(70, 16);
            this.label2.TabIndex = 3;
            this.label2.Text = "Username";
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(506, 52);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(67, 16);
            this.label1.TabIndex = 2;
            this.label1.Text = "Password";
            // 
            // tabella_password
            // 
            this.tabella_password.ColumnHeadersHeightSizeMode = System.Windows.Forms.DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            this.tabella_password.Columns.AddRange(new System.Windows.Forms.DataGridViewColumn[] {
            this.Nome,
            this.Password,
            this.Username,
            this.URI,
            this.Edita,
            this.DeleteButton});
            this.tabella_password.Location = new System.Drawing.Point(56, 169);
            this.tabella_password.Name = "tabella_password";
            this.tabella_password.RowTemplate.Height = 24;
            this.tabella_password.Size = new System.Drawing.Size(907, 319);
            this.tabella_password.TabIndex = 1;
            this.tabella_password.CellContentClick += new System.Windows.Forms.DataGridViewCellEventHandler(this.tabella_password_CellContentClick);
            // 
            // menuStrip1
            // 
            this.menuStrip1.AutoSize = false;
            this.menuStrip1.BackColor = System.Drawing.Color.IndianRed;
            this.menuStrip1.ImageScalingSize = new System.Drawing.Size(20, 20);
            this.menuStrip1.Items.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.toolStripMenuItem1,
            this.modificaToolStripMenuItem,
            this.visualizzaToolStripMenuItem,
            this.themeToolStripMenuItem});
            this.menuStrip1.Location = new System.Drawing.Point(0, 0);
            this.menuStrip1.Name = "menuStrip1";
            this.menuStrip1.Size = new System.Drawing.Size(984, 30);
            this.menuStrip1.TabIndex = 0;
            this.menuStrip1.Text = "menuStrip1";
            // 
            // toolStripMenuItem1
            // 
            this.toolStripMenuItem1.DropDownItems.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.nuovaPasswordToolStripMenuItem,
            this.apriPasswordToolStripMenuItem,
            this.caricaDaUnBackupToolStripMenuItem,
            this.salvaPasswordToolStripMenuItem,
            this.salvaTutteLePasswordToolStripMenuItem});
            this.toolStripMenuItem1.Name = "toolStripMenuItem1";
            this.toolStripMenuItem1.Size = new System.Drawing.Size(37, 26);
            this.toolStripMenuItem1.Text = "File";
            // 
            // nuovaPasswordToolStripMenuItem
            // 
            this.nuovaPasswordToolStripMenuItem.Name = "nuovaPasswordToolStripMenuItem";
            this.nuovaPasswordToolStripMenuItem.Size = new System.Drawing.Size(194, 22);
            this.nuovaPasswordToolStripMenuItem.Text = "Nuova password";
            this.nuovaPasswordToolStripMenuItem.Click += new System.EventHandler(this.nuovaPasswordToolStripMenuItem_Click);
            // 
            // apriPasswordToolStripMenuItem
            // 
            this.apriPasswordToolStripMenuItem.Name = "apriPasswordToolStripMenuItem";
            this.apriPasswordToolStripMenuItem.Size = new System.Drawing.Size(194, 22);
            this.apriPasswordToolStripMenuItem.Text = "Apri password";
            this.apriPasswordToolStripMenuItem.Click += new System.EventHandler(this.apriPasswordToolStripMenuItem_Click);
            // 
            // caricaDaUnBackupToolStripMenuItem
            // 
            this.caricaDaUnBackupToolStripMenuItem.Name = "caricaDaUnBackupToolStripMenuItem";
            this.caricaDaUnBackupToolStripMenuItem.Size = new System.Drawing.Size(194, 22);
            this.caricaDaUnBackupToolStripMenuItem.Text = "Carica da un backup";
            this.caricaDaUnBackupToolStripMenuItem.Click += new System.EventHandler(this.caricaDaUnBackupToolStripMenuItem_Click);
            // 
            // salvaPasswordToolStripMenuItem
            // 
            this.salvaPasswordToolStripMenuItem.Name = "salvaPasswordToolStripMenuItem";
            this.salvaPasswordToolStripMenuItem.Size = new System.Drawing.Size(194, 22);
            this.salvaPasswordToolStripMenuItem.Text = "Salva password";
            // 
            // salvaTutteLePasswordToolStripMenuItem
            // 
            this.salvaTutteLePasswordToolStripMenuItem.Name = "salvaTutteLePasswordToolStripMenuItem";
            this.salvaTutteLePasswordToolStripMenuItem.Size = new System.Drawing.Size(194, 22);
            this.salvaTutteLePasswordToolStripMenuItem.Text = "Salva tutte le password";
            // 
            // modificaToolStripMenuItem
            // 
            this.modificaToolStripMenuItem.DropDownItems.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.generaPasswordToolStripMenuItem});
            this.modificaToolStripMenuItem.Name = "modificaToolStripMenuItem";
            this.modificaToolStripMenuItem.Size = new System.Drawing.Size(66, 26);
            this.modificaToolStripMenuItem.Text = "Modifica";
            // 
            // generaPasswordToolStripMenuItem
            // 
            this.generaPasswordToolStripMenuItem.Name = "generaPasswordToolStripMenuItem";
            this.generaPasswordToolStripMenuItem.Size = new System.Drawing.Size(164, 22);
            this.generaPasswordToolStripMenuItem.Text = "Genera password";
            // 
            // visualizzaToolStripMenuItem
            // 
            this.visualizzaToolStripMenuItem.Name = "visualizzaToolStripMenuItem";
            this.visualizzaToolStripMenuItem.Size = new System.Drawing.Size(69, 26);
            this.visualizzaToolStripMenuItem.Text = "Visualizza";
            // 
            // themeToolStripMenuItem
            // 
            this.themeToolStripMenuItem.DropDownItems.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.chiaroToolStripMenuItem,
            this.scuroToolStripMenuItem});
            this.themeToolStripMenuItem.Name = "themeToolStripMenuItem";
            this.themeToolStripMenuItem.Size = new System.Drawing.Size(55, 26);
            this.themeToolStripMenuItem.Text = "Theme";
            // 
            // chiaroToolStripMenuItem
            // 
            this.chiaroToolStripMenuItem.Name = "chiaroToolStripMenuItem";
            this.chiaroToolStripMenuItem.Size = new System.Drawing.Size(109, 22);
            this.chiaroToolStripMenuItem.Text = "Chiaro";
            this.chiaroToolStripMenuItem.Click += new System.EventHandler(this.chiaroToolStripMenuItem_Click);
            // 
            // scuroToolStripMenuItem
            // 
            this.scuroToolStripMenuItem.Name = "scuroToolStripMenuItem";
            this.scuroToolStripMenuItem.Size = new System.Drawing.Size(109, 22);
            this.scuroToolStripMenuItem.Text = "Scuro";
            this.scuroToolStripMenuItem.Click += new System.EventHandler(this.scuroToolStripMenuItem_Click);
            // 
            // Nome
            // 
            this.Nome.HeaderText = "Nome";
            this.Nome.Name = "Nome";
            this.Nome.ReadOnly = true;
            // 
            // Password
            // 
            this.Password.HeaderText = "Username";
            this.Password.Name = "Password";
            this.Password.ReadOnly = true;
            // 
            // Username
            // 
            this.Username.HeaderText = "Password";
            this.Username.Name = "Username";
            this.Username.ReadOnly = true;
            // 
            // URI
            // 
            this.URI.HeaderText = "URI";
            this.URI.Name = "URI";
            this.URI.ReadOnly = true;
            this.URI.Resizable = System.Windows.Forms.DataGridViewTriState.True;
            this.URI.SortMode = System.Windows.Forms.DataGridViewColumnSortMode.Automatic;
            // 
            // Edita
            // 
            this.Edita.HeaderText = "Modifica";
            this.Edita.Name = "Edita";
            this.Edita.Text = "Modifica";
            this.Edita.UseColumnTextForButtonValue = true;
            // 
            // DeleteButton
            // 
            this.DeleteButton.HeaderText = "Elimina";
            this.DeleteButton.Name = "DeleteButton";
            this.DeleteButton.Text = "Elimina";
            this.DeleteButton.UseColumnTextForButtonValue = true;
            // 
            // Form1
            // 
            this.AllowDrop = true;
            this.AutoScaleDimensions = new System.Drawing.SizeF(8F, 16F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.AutoSizeMode = System.Windows.Forms.AutoSizeMode.GrowAndShrink;
            this.ClientSize = new System.Drawing.Size(984, 684);
            this.Controls.Add(this.panel1);
            this.HelpButton = true;
            this.Icon = ((System.Drawing.Icon)(resources.GetObject("$this.Icon")));
            this.ImeMode = System.Windows.Forms.ImeMode.On;
            this.MainMenuStrip = this.menuStrip1;
            this.Margin = new System.Windows.Forms.Padding(3, 2, 3, 2);
            this.Name = "Form1";
            this.Text = "Encrypt Images - Alberto Lorenzini";
            this.panel1.ResumeLayout(false);
            this.panel1.PerformLayout();
            ((System.ComponentModel.ISupportInitialize)(this.tabella_password)).EndInit();
            this.menuStrip1.ResumeLayout(false);
            this.menuStrip1.PerformLayout();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion
        private System.Windows.Forms.Panel panel1;
        private System.Windows.Forms.MenuStrip menuStrip1;
        private System.Windows.Forms.ToolStripMenuItem toolStripMenuItem1;
        private System.Windows.Forms.ToolStripMenuItem nuovaPasswordToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem apriPasswordToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem caricaDaUnBackupToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem salvaPasswordToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem salvaTutteLePasswordToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem modificaToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem visualizzaToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem themeToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem chiaroToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem scuroToolStripMenuItem;
        private System.Windows.Forms.DataGridView tabella_password;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.ToolStripMenuItem generaPasswordToolStripMenuItem;
        private System.Windows.Forms.Label label4;
        private System.Windows.Forms.Button confirm_button;
        private System.Windows.Forms.TextBox uri_text;
        private System.Windows.Forms.TextBox password_text;
        private System.Windows.Forms.TextBox username_text;
        private System.Windows.Forms.TextBox name_text;
        private System.Windows.Forms.DataGridViewTextBoxColumn Nome;
        private System.Windows.Forms.DataGridViewTextBoxColumn Password;
        private System.Windows.Forms.DataGridViewTextBoxColumn Username;
        private System.Windows.Forms.DataGridViewLinkColumn URI;
        private System.Windows.Forms.DataGridViewButtonColumn Edita;
        private System.Windows.Forms.DataGridViewButtonColumn DeleteButton;
    }
}

