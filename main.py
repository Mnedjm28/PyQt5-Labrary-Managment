import datetime
import glob
import smtplib, ssl
from email.message import EmailMessage

from PyQt5 import uic, QtWidgets, QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.Qt import Qt
import sys
import MySQLdb
from xlsxwriter import *
from xlrd import *
from Labrery.labrery import Ui_MainWindow



class Send_Email():
    def __init__(self, username, to, password_user):
        smtp_server = "smtp.gmail.com"
        port = 587  # For starttls
        sender_email = 'eddinenedjm815@gmail.com'
        password = '0035547305nadjmo'

        # Create a secure SSL context
        context = ssl.create_default_context()

        # Try to log in to server and send email
        try:
            server = smtplib.SMTP(smtp_server, port)
            server.ehlo()  # Can be omitted
            server.starttls(context=context)  # Secure the connection
            server.ehlo()  # Can be omitted
            server.login(sender_email, password)

            msg = EmailMessage()
            msg['Subject'] = "Rest Password"
            msg['From'] = sender_email
            msg['To'] = username
            msg.set_content(f'hey {username}\n your password its :{password_user}')

            server.sendmail(sender_email, to, msg.as_string())

        except Exception as e:
            # Print any error messages to stdout
            print(e)
        finally:
            server.quit()


class Main(QMainWindow,Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        super(Main, self).__init__()
        # uic.loadUi('labrery.ui',self)
        # self.showMaximized()
        self.setupUi(self)
        self.db_connection()
        self.handel_button()
        self.ui_changes()
        # self.ui_visible_edit()
        self.show_all_categories()
        self.show_all_publisher()
        self.show_all_author()
        self.show_all_branch()
        self.show_all_books()
        self.show_all_clients()
        self.show_all_day_work()
        self.show_all_employee()
        self.show_history()
        self.change_dash()

        # book = open_workbook('all_books.xlsx')
        # sheet = book.sheet_by_index(0)
        # print(book.name_obj_list)
        # print(sheet.nrows)
        # print(sheet.ncols)
        #
        # print(sheet.cell(0,1).value)
        #
        #
        # for row in range(sheet.nrows):
        #     if row !=0:
        #         for col in range(sheet.ncols):
        #             print(sheet.cell(row,col).value,",",end='')
        #         print("\n")
        #
        # self.cur.execute('''select * from employee''')
        # data = self.cur.fetchall()
        # for row in data:
        #     print(row)

    def db_connection(self):
        self.db = MySQLdb.connect(db ='library', user='root', password='1509',
                         host='127.0.0.1', port=3306, charset='utf8')
        self.cur = self.db.cursor()
        print('connection')

    def handel_button(self):
        #handel all button in our project
        self.today_btn.clicked.connect(self.open_daily_movment_today)
        self.client_btn.clicked.connect(self.open_client_tab)
        self.books_btn.clicked.connect(self.open_book_tab)
        self.history_btn.clicked.connect(self.open_history_tab)
        self.dash_btn.clicked.connect(self.open_dashboard_tab)
        self.settings_btn.clicked.connect(self.open_settings_tab)
        self.reports_btn.clicked.connect(self.open_report_tab)
        self.out_btn.clicked.connect(self.handel_logout)
        self.booksearchframe_btn.clicked.connect(self.open_search_book_stacked)
        self.bookaddframe_btn.clicked.connect(self.open_add_book_stacked)
        self.bookeditframe_btn.clicked.connect(self.open_edite_book_stacked)
        self.clientsearchframe_btn.clicked.connect(self.open_search_client_stacked)
        self.clientaddfram_btn.clicked.connect(self.open_add_client_stacked)
        self.clienteditefram_btn.clicked.connect(self.open_edite_client_stacked)
        self.reportbooksfram_btn.clicked.connect(self.open_report_book_stacked)
        self.reportclientsfram_btn.clicked.connect(self.open_report_client_stacked)
        self.reportmonthlyfram_btn_2.clicked.connect(self.open_report_monthly_stacked)
        self.settingsadddataframe_btn.clicked.connect(self.open_settings_data_stacked)
        self.settingspermisframe_btn.clicked.connect(self.open_settings_permissions_stacked)
        self.settingsaddemplframe_btn.clicked.connect(self.open_settings_employee_stacked)
        self.settingsemailframe_btn.clicked.connect(self.open_settings_email_stacked)
        self.settingsaddbranch_btn.clicked.connect(self.add_branch)
        self.settingsaddauthor_btn.clicked.connect(self.add_author)
        self.settingsaddpublish_btn.clicked.connect(self.add_publisher)
        self.settingsaddcatg_btn.clicked.connect(self.add_category)
        self.settingsaddemp_btn.clicked.connect(self.add_employe)
        self.bookadd_btn.clicked.connect(self.add_new_book)
        self.clientadd_btn.clicked.connect(self.add_new_client)
        self.bookeditesearch_btn.clicked.connect(self.edite_book)
        self.bookeditesave_btn.clicked.connect(self.save_edite_book)
        self.clienteditesearch_btn.clicked.connect(self.edite_client)
        self.clienteditesave_btn.clicked.connect(self.save_edite_client)
        self.bookeditedelete_btn.clicked.connect(self.delete_book)
        self.clienteditedelete_btn.clicked.connect(self.delete_client)
        self.todayadd_btn.clicked.connect(self.handel_today_work)
        self.pushButton_15.clicked.connect(self.all_books_filter)
        self.settingseditecheck_btn.clicked.connect(self.check_employe)
        self.settingsediteempsave_btn.clicked.connect(self.edite_employe)
        self.settingsparmsapply_btn.clicked.connect(self.add_employe_permissions)
        self.settingsparmscheck_btn.clicked.connect(self.ui_Tenabled_permiss_emp)
        self.booksearchexport_btn.clicked.connect(self.export_books)
        self.clientsearchexport_btn.clicked.connect(self.export_clients)
        self.login_btn.clicked.connect(self.handel_login)
        self.clientsearch_btn.clicked.connect(self.all_clients_filter)
        self.clientsearchimport_btn.clicked.connect(self.get_all_client)
        self.loginrestpass_btn.clicked.connect(self.open_restp_tab)
        self.emaillogin_btn.clicked.connect(self.open_login_tab)
        self.emailsend_btn.clicked.connect(self.handel_restp)
        self.emailresend_btn.clicked.connect(self.handel_restp)
        self.settingsediteempforgtpass_btn.clicked.connect(self.open_restp_tab)
        self.booksearchimport_btn.clicked.connect(self.show_all_books)



    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return and self.Main_tab.currentIndex() == 0:
            self.handel_login()

    def ui_changes(self):
        #Ui_changes in login
        self.Main_tab.tabBar().setVisible(False)
        self.Main_tab.setCurrentIndex(0)
        self.settingsediteempsave_btn.setEnabled(False)
        self.ui_visible_edit()
        self.ui_fenabled_permiss_emp()

    def change_dash(self):

        self.cur.execute('''select id from employee''')
        employee = self.cur.fetchall()
        len_emp = 0
        for emp in employee:
            len_emp +=1

        self.label_59.setText(str(len_emp))
        self.cur.execute('''select id from client''')
        employee = self.cur.fetchall()
        len_cli = 0
        for emp in employee:
            len_cli +=1
        self.label_58.setText(str(len_cli))

        self.cur.execute('''select id from book''')
        employee = self.cur.fetchall()
        len_boo = 0
        for emp in employee:
            len_boo +=1
        self.label_57.setText(str(len_boo))


        self.cur.execute('''select id from daily_movment''')
        employee = self.cur.fetchall()
        len_dail = 0
        for emp in employee:
            len_dail +=1
        self.label_60.setText(str(len_dail))

    def ui_visible_edit(self):
        self.clienteditesave_btn.setDisabled(True)
        self.clienteditedelete_btn.setDisabled(True)
        self.bookeditesave_btn.setDisabled(True)
        self.groupBox_6.setEnabled(True)

    def ui_fenabled_permiss_emp(self):
        self.groupBox_3.setEnabled(False)
        self.groupBox.setEnabled(False)
        self.groupBox_2.setEnabled(False)
        self.groupBox_4.setEnabled(False)
        self.settingsparmsdclient_check_9.setEnabled(False)
        self.settingsparmsapply_btn.setEnabled(False)

    def ui_Tenabled_permiss_emp(self):
        if self.settingspermsemp_combo.currentIndex() != 0:
            employe_name = self.settingspermsemp_combo.currentText()

            query = '''select id from employee where name = %s'''
            self.cur.execute(query, (employe_name,))
            data = self.cur.fetchone()
            id_employee = int(data[0])

            query = '''select idemployee from employee_permissions where idemployee = %s'''
            self.cur.execute(query, (id_employee,))
            data = self.cur.fetchone()
            if data is not None:
                QMessageBox.warning(self, "Field",
                                    "THis employee have Permissions Please Try it out with another employee")
            else:
                self.groupBox_3.setEnabled(True)
                self.groupBox.setEnabled(True)
                self.groupBox_2.setEnabled(True)
                self.groupBox_4.setEnabled(True)
                self.settingsparmsdclient_check_9.setEnabled(True)
                self.settingsparmsapply_btn.setEnabled(True)
        else:
            QMessageBox.warning(self, "Permission message", "Please select Employee")

    def ui_clear_permissions(self):
        self.settingsparmsaclient_check.setChecked(False)
        self.settingsparmseclient_check.setChecked(False)
        self.settingsparmsdclient_check.setChecked(False)
        self.settingsparmsdclient_check_2.setChecked(False)
        self.settingsparmsdclient_check_3.setChecked(False)
        self.settingsparmsabook_check.setChecked(False)
        self.settingsparmsebook_check.setChecked(False)
        self.settingsparmsdbook_check.setChecked(False)
        self.settingsparmsdclient_check_5.setChecked(False)
        self.settingsparmsdclient_check_4.setChecked(False)
        self.settingsparmsabook_check_2.setChecked(False)
        self.settingsparmsebook_check_2.setChecked(False)
        self.settingsparmsdbook_check_2.setChecked(False)
        self.settingsparmsdclient_check_7.setChecked(False)
        self.settingsparmsdclient_check_6.setChecked(False)
        self.settingsparmsdclient_check_8.setChecked(False)
        self.settingsparmsbook_check.setChecked(False)
        self.settingsparmsclient_check.setChecked(False)
        self.settingsparmsdashboard_check.setChecked(False)
        self.settingsparmshistory_check.setChecked(False)
        self.settingsparmsreports_check.setChecked(False)
        self.settingsparmssettings_check.setChecked(False)
        self.settingspermsemp_combo.setCurrentIndex(0)

    global emp_id
    global branch_id

    def handel_login(self):
        self.ereur_nom.clear()
        self.ereur_pass.clear()
        self.ereur_general.clear()
        username = self.loginuser_line.text()
        password = self.loginpass_line.text()
        self.cur.execute('''select id ,name , password, branch_id from employee where name =%s and password = %s''',(username, password,))
        data = self.cur.fetchone()
        if username != '' and password != '':
            if data is not None:  # data for get value cursor

                self.emp_id = data[0]
                self.branch_id = data[3]
                try:
                    self.cur.execute('''insert into history(employeid,action,branchid,datee)
                                values (%s,%s,%s,%s);
                                ''', (self.emp_id, 'Login', self.branch_id, datetime.datetime.now()))
                except (self.db.Error, self.db.Warning) as e:
                    print(e)
                self.db.commit()
                self.show_history()
                self.cur.execute('''select * from employee_permissions where idemployee = %s''', (int(data[0]),))
                data = self.cur.fetchone()
                self.groupBox_5.setEnabled(True)
                #today tab
                self.today_btn.setEnabled(True)
                #book tab
                ###Admmmin###
                if data[24] == 1:
                    self.books_btn.setEnabled(True)
                    self.bookaddframe_btn.setEnabled(True)
                    self.bookeditframe_btn.setEnabled(True)
                    self.groupBox_6.setEnabled(True)
                    self.booksearchimport_btn.setEnabled(True)
                    self.booksearchexport_btn.setEnabled(True)
                    self.client_btn.setEnabled(True)
                    self.clientaddfram_btn.setEnabled(True)
                    self.clienteditefram_btn.setEnabled(True)
                    self.clienteditedelete_btn.setEnabled(True)
                    self.clientsearchimport_btn.setEnabled(True)
                    self.clientsearchexport_btn.setEnabled(True)
                    self.dash_btn.setEnabled(True)
                    self.history_btn.setEnabled(True)
                    self.reports_btn.setEnabled(True)
                    self.settings_btn.setEnabled(True)
                    self.settingsaddbranch_btn.setEnabled(True)
                    self.settingsaddpublish_btn.setEnabled(True)
                    self.settingsaddauthor_btn.setEnabled(True)
                    self.settingsaddcatg_btn.setEnabled(True)
                    self.settingsaddemp_btn.setEnabled(True)
                    self.settingsediteemp_box.setEnabled(True)
                    self.settingspermisframe_btn.setEnabled(True)
                    self.settingsemailframe_btn.setEnabled(True)
                    self.Main_tab.setCurrentIndex(2)
                    self.today_btn.setStyleSheet(
                        'background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);'
                        '\n border:none;\nborder-right:10px solid black;\n color:black;\n border-radius:0;outline: none;')
                else:
                    if data[2] == 1:
                        self.books_btn.setEnabled(True)
                    else:
                        self.books_btn.setEnabled(False)

                    if data[8] == 1:
                        self.bookaddframe_btn.setEnabled(True)
                    else:
                        self.bookaddframe_btn.setEnabled(False)

                    if data[9] == 1:
                        self.bookeditframe_btn.setEnabled(True)
                    else:
                        self.bookeditframe_btn.setEnabled(False)

                    if data[10] == 1:
                        self.groupBox_6.setEnabled(True)
                    else:
                        self.groupBox_6.setEnabled(False)

                    if data[11] == 1:
                        self.booksearchimport_btn.setEnabled(True)
                    else:
                        self.booksearchimport_btn.setEnabled(False)

                    if data[12] == 1:
                        self.booksearchexport_btn.setEnabled(True)
                    else:
                        self.booksearchexport_btn.setEnabled(False)


                    #client tab
                    if data[3] == 1:
                        self.client_btn.setEnabled(True)
                    else:
                        self.client_btn.setEnabled(False)

                    if data[13] == 1:
                        self.clientaddfram_btn.setEnabled(True)
                    else:
                        self.clientaddfram_btn.setEnabled(False)

                    if data[14] == 1:
                        self.clienteditefram_btn.setEnabled(True)
                    else:
                        self.clienteditefram_btn.setEnabled(False)

                    if data[15] == 1:
                        self.clienteditedelete_btn.setEnabled(True)
                    else:
                        self.clienteditedelete_btn.setEnabled(False)

                    if data[16] == 1:
                        self.clientsearchimport_btn.setEnabled(True)
                    else:
                        self.clientsearchimport_btn.setEnabled(False)

                    if data[17] == 1:
                        self.clientsearchexport_btn.setEnabled(True)
                    else:
                        self.clientsearchexport_btn.setEnabled(False)


                #dashboard tab
                if data[4] == 1:
                    self.dash_btn.setEnabled(True)
                else:
                    self.dash_btn.setEnabled(False)

                #history tab
                if data[5] == 1:
                    self.history_btn.setEnabled(True)
                else:
                    self.history_btn.setEnabled(False)
                #reports tab
                if data[6] == 1:
                    self.reports_btn.setEnabled(True)
                else:
                    self.reports_btn.setEnabled(False)
                #settings tab
                if data[7] == 1:
                    self.settings_btn.setEnabled(True)
                else:
                    self.settings_btn.setEnabled(False)

                if data[18] == 1:
                    self.settingsaddbranch_btn.setEnabled(True)
                else:
                    self.settingsaddbranch_btn.setEnabled(False)

                if data[19] == 1:
                    self.settingsaddpublish_btn.setEnabled(True)
                else:
                    self.settingsaddpublish_btn.setEnabled(False)

                if data[20] == 1:
                    self.settingsaddauthor_btn.setEnabled(True)
                else:
                    self.settingsaddauthor_btn.setEnabled(False)

                if data[22] == 1:
                    self.settingsaddcatg_btn.setEnabled(True)
                else:
                    self.settingsaddcatg_btn.setEnabled(False)

                if data[21] == 1:
                    self.settingsaddemp_btn.setEnabled(True)
                else:
                    self.settingsaddemp_btn.setEnabled(False)

                if data[23] == 1:
                    self.settingsediteemp_box.setEnabled(True)


                else:
                    self.settingsediteemp_box.setEnabled(False)
                self.Main_tab.setCurrentIndex(2)
                self.today_btn.setStyleSheet(
                    'background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);'
                    '\n border:none;\nborder-right:10px solid black;\n color:black;\n border-radius:0;outline: none;')

                self.cur.execute('''select name,phone,mail from employee where id =%s''', (self.emp_id,))
                dash = self.cur.fetchone()
                self.label_62.setText(str(dash[0]))
                self.label_66.setText(str(dash[0]))
                self.label_68.setText(str(dash[1]))
                self.label_67.setText(str(dash[2]))

                self.cur.execute('''select admin from employee_permissions where idemployee =%s''', (self.emp_id,))
                perm = self.cur.fetchone()
                if perm[0] == 1:
                    self.label_70.setText("Admin")
                else:
                    self.label_70.setText("Employe")
                self.loginuser_line.clear()
                self.loginuser_line.clear()
            else:
                self.ereur_general.setText('Please confirm your username or password')
        else:
            if username == '':
                self.ereur_nom.setText('Please enter your username')
                if password== '':
                    self.ereur_pass.setText('Please enter password ')
            else:
                self.ereur_pass.setText('Please enter password')


    def handel_logout(self):
        try:
            self.cur.execute('''insert into history(employeid,action,branchid,datee)
                        values (%s,%s,%s,%s);
                        ''', (self.emp_id, 'Logout', self.branch_id, datetime.datetime.now()))
        except (self.db.Error, self.db.Warning) as e:
            print(e)
        self.db.commit()
        self.show_history()
        self.close()

    def handel_restp(self):
        mail_user = self.emailrest_line.text()
        self.cur.execute('''select name, mail, password from employee where mail = %s''',(mail_user,))
        data = self.cur.fetchone()
        if data is not None:
            username = data[0]
            email = data[1]
            password = data[2]
            t = Send_Email(username=username, to=email, password_user=password )
            QMessageBox.information(self, "succes", "the password send to your email cheking him")

        else:
            self.ereur_nom_2.setText('This email does not exist')

    def handel_today_work(self):
        barcode_book = self.todaybooktitle_line.text()
        client_nat_id = self.lineEdit_2.text()
        type_opert = self.todaybooktype_combo.currentText()
        type_index = self.todaybooktype_combo.currentIndex()
        if barcode_book == '' or client_nat_id == '' or type_index == 0:
            QMessageBox.warning(self, "errer", "Please complete all Field")
        else:
            book_to1 = self.dateEdit.date()
            book_to2 = book_to1.toPyDate()
            book_from = datetime.datetime.today().strftime('%Y-%m-%d')
            date = datetime.datetime.now()
            branch = 1
            employe = 1

            query = 'select code,title from book where barcode = %s'
            self.cur.execute(query,(barcode_book,))
            data_book = self.cur.fetchone()
            if data_book is None:
                QMessageBox.warning(self, "errer", "This barcode does not exist for book please scan the right book")
            else :
                query = 'select national_id, name  from client where national_id = %s'
                self.cur.execute(query,(client_nat_id,))
                data_client = self.cur.fetchone()
                if data_client is None:
                    QMessageBox.warning(self, "errer","This national id does not exist for client please comfirm the corect id national")
                else:
                    query = '''insert into daily_movment(book_code, book_title, client_nat_id, type, date, employe_id, branch_id, book_to, book_from,Client_name)
                                    values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                        '''
                    self.cur.execute(query,(int(data_book[0]), str(data_book[1]), data_client[0], type_opert, date, employe, branch, book_to2,book_from,data_client[1]))
                    self.db.commit()
                    self.show_all_day_work()
                    self.todaybooktitle_line.clear()
                    self.lineEdit_2.clear()
                    self.todaybooktype_combo.setCurrentIndex(0)
                    v = datetime.datetime.now()
                    self.dateEdit.setDate(v)
                    try:
                        self.cur.execute('''insert into history(employeid,action,tablee,branchid,datee)
                                    values (%s,%s,%s,%s,%s);
                                    ''', (self.emp_id, 'Add', 'Daily movment', self.branch_id, datetime.datetime.now()))
                    except (self.db.Error, self.db.Warning) as e:
                        print(e)
                    self.db.commit()
                    self.show_history()
                    self.change_dash()

    def retrieve_day_work(self):
        pass

    def show_all_day_work(self):
        self.tableWidget.setRowCount(0)
        query = '''select book_code,book_title, type, client_name, book_from, book_to from daily_movment'''
        self.cur.execute(query)
        data = self.cur.fetchall()

        for row , form in enumerate(data):
            self.tableWidget.insertRow(row)
            for col , item in enumerate(form):
                self.tableWidget.setItem(row,col,QTableWidgetItem(str(item)))


    #############--Books Operations --##################

    def show_all_books(self):
        self.booksearchtabel.setRowCount(0)
        self.cur.execute('''select code, title, category_id, author_id, price from book''')
        data = self.cur.fetchall()

        for row , form in enumerate(data):
            self.booksearchtabel.insertRow(row)
            for col , item in enumerate(form):
                if col == 2:
                    self.cur.execute('''select category_name from category where id = %s''',(item,))
                    catg = self.cur.fetchone()
                    self.booksearchtabel.setItem(row, col, QTableWidgetItem(str(catg[0])))
                elif col == 3:
                    self.cur.execute('''select name from author where id = %s''',(item,))
                    catg = self.cur.fetchone()
                    self.booksearchtabel.setItem(row, col, QTableWidgetItem(str(catg[0])))
                else:
                    self.booksearchtabel.setItem(row, col, QTableWidgetItem(str(item)))

    def add_new_book(self):
        #add book
        title = self.bookaddtitle_line.text()
        description = self.bookadddescrp_line.toPlainText()
        category = self.bookaddcatg_combo.currentText()
        code = self.bookaddcode_line.text()
        barcode = self.bookaddbarcode_line.text()
        price = self.bookaddprice_line.text()
        publisher = self.bookaddpublisher_combo.currentText()
        author = self.bookaddauthor_combo.currentText()
        status = self.bookaddstatus_combo.currentText()
        status_index = self.bookaddstatus_combo.currentIndex()
        part_order = self.bookaddpart_line.text()
        date = datetime.datetime.now()
        if title == '' or code == '' or barcode =='' or status_index == 0:
            QMessageBox.warning(self, "field", "Please checking for title code docebar and status because theme field reqiured")
        else:
            self.cur.execute(''' select id from category where category_name= %s  ''',(category,))
            query_catg = self.cur.fetchall()
            for i in query_catg:
                catg_id = i[0]

            self.cur.execute(''' select id from publisher where name= %s  ''',(publisher,))
            query_publ = self.cur.fetchall()
            for i in query_publ:
                publ_id = i[0]

            self.cur.execute(''' select id from author where name= %s  ''',(author,))
            query_auth = self.cur.fetchall()
            for i in query_auth:
                auth_id = i[0]

            self.cur.execute(''' insert into book(title, description, category_id, code, barcode, part_order, price, publisher_id, author_id, status, date)
            values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            ''',(title, description, catg_id, code, barcode, part_order, price, publ_id, auth_id, status, date))
            self.db.commit()

            QMessageBox.information(self, "success", "Add book successflly")
            self.bookaddtitle_line.clear()
            self.bookadddescrp_line.clear()
            self.bookaddcatg_combo.setCurrentIndex(0)
            self.bookaddpublisher_combo.setCurrentIndex(0)
            self.bookaddauthor_combo.setCurrentIndex(0)
            self.bookaddstatus_combo.setCurrentIndex(0)
            self.bookaddcode_line.clear()
            self.bookaddbarcode_line.clear()
            self.bookaddprice_line.clear()
            self.bookaddpart_line.clear()
            self.show_all_books()
            self.change_dash()
            try:
                self.cur.execute('''insert into history(employeid,action,tablee,branchid,datee)
                            values (%s,%s,%s,%s,%s);
                            ''', (self.emp_id, 'Add', 'Book', self.branch_id, datetime.datetime.now()))
            except (self.db.Error, self.db.Warning) as e:
                print(e)
            self.db.commit()
            self.show_history()

    def edite_book(self):
        self.bookeditecode_line_2.setDisabled(True)
        self.bookeditedescrp_line.clear()
        self.bookeditetitle_line.clear()
        self.bookeditecatg_combo.setCurrentIndex(0)
        self.bookeditecode_line_2.clear()
        self.bookediteprice_line.clear()
        self.bookeditepublish_compbo.setCurrentIndex(0)
        self.bookediteauthor_line.setCurrentIndex(0)
        self.bookeditestatus_combo.setCurrentIndex(0)
        self.bookeditepart_line.clear()
        code = self.bookeditecode_line.text()
        query = "select * from book where code = %s"
        self.cur.execute(query,(code,))
        data = self.cur.fetchone()
        if data != None and code != '':
            self.bookeditesave_btn.setDisabled(False)
            self.bookeditedelete_btn.setDisabled(False)
            title = data[1]
            description = str(data[2])
            code = data[4]
            barcode = data[5]
            part_order = data[6]
            price = data[7]
            status = data[11]
            publ_id = data[8]
            auth_id = data[9]
            catg_id = data[3]
            query_catg= "select category_name from category where id = %s"
            query_auth= "select name from author where id = %s"
            query_publ= "select name from publisher where id = %s"
            self.cur.execute(query_catg,(catg_id,))
            data_catg = self.cur.fetchone()
            self.cur.execute(query_auth, (auth_id,))
            data_auth = self.cur.fetchone()
            self.cur.execute(query_publ, (publ_id,))
            data_publ = self.cur.fetchone()
            self.bookeditedescrp_line.setPlainText(description)
            self.bookeditetitle_line.setText(title)
            self.bookeditecatg_combo.setCurrentText(data_catg[0])
            self.bookeditecode_line_2.setText(str(code))
            self.bookediteprice_line.setText(str(price))
            self.bookeditepublish_compbo.setCurrentText(data_publ[0])
            self.bookediteauthor_line.setCurrentText(data_auth[0])
            self.bookeditestatus_combo.setCurrentText(status)
            self.bookeditepart_line.setText(str(part_order))

        elif code == '':
            QMessageBox.warning(self, "field", "Please enter Your code book")
            self.ui_visible_edit()
        else:
            QMessageBox.warning(self, "field", "This code haven't a book")
            self.clear_data_book()
            self.ui_visible_edit()

    def save_edite_book(self):

        self.bookeditecode_line_2.setDisabled(True)
        new_descrp = self.bookeditedescrp_line.toPlainText()
        new_title = self.bookeditetitle_line.text()
        code = self.bookeditecode_line.text()
        new_price = self.bookediteprice_line.text()
        new_part = self.bookeditepart_line.text()

        new_status_index = self.bookeditestatus_combo.currentIndex()
        new_status = self.bookeditestatus_combo.setCurrentIndex(new_status_index)

        new_status = self.bookeditestatus_combo.currentText()
        new_catg = self.bookeditecatg_combo.currentText()
        new_publ = self.bookeditepublish_compbo.currentText()
        new_auth = self.bookediteauthor_line.currentText()

        query_catg = "select id from category where category_name = %s"
        query_auth = "select id from author where name = %s"
        query_publ = "select id from publisher where name = %s"
        self.cur.execute(query_catg,(new_catg,))
        new_id__catg = self.cur.fetchone()
        self.cur.execute(query_auth,(new_auth,))
        new_id__auth = self.cur.fetchone()
        self.cur.execute(query_publ,(new_publ,))
        new_id__publ = self.cur.fetchone()
        self.cur.execute(''' update book set title =%s , description = %s, category_id = %s, part_order = %s,
         price = %s, publisher_id = %s, author_id = %s, status = %s where code = %s;
        ''',(new_title, new_descrp, new_id__catg[0], new_part, new_price, new_id__publ[0], new_id__auth[0], new_status, code,))

        self.db.commit()
        self.show_all_books()
        QMessageBox.information(self, "success", "Edite book succes ")
        self.clear_data_book()
        self.ui_visible_edit()
        try:
            self.cur.execute('''insert into history(employeid,action,tablee,branchid,datee)
                        values (%s,%s,%s,%s,%s);
                        ''',(self.emp_id,'Edite','Book',self.branch_id,datetime.datetime.now()))
        except (self.db.Error, self.db.Warning) as e:
            print(e)
        self.db.commit()
        self.show_history()

    def clear_data_book(self):
        self.bookeditecode_line_2.clear()
        self.bookeditedescrp_line.clear()
        self.bookeditetitle_line.clear()
        self.bookeditecode_line.clear()
        self.bookediteprice_line.clear()
        self.bookeditepart_line.clear()
        self.bookeditestatus_combo.setCurrentIndex(0)
        self.bookeditestatus_combo.setCurrentIndex(0)
        self.bookeditecatg_combo.setCurrentIndex(0)
        self.bookeditepublish_compbo.setCurrentIndex(0)
        self.bookediteauthor_line.setCurrentIndex(0)

    def delete_book(self):
        btn_reply = QMessageBox.warning(self, "softwar message", "Are you sur you want to delete this book", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if btn_reply == QMessageBox.Yes:
            code = self.bookeditecode_line.text()
            self.cur.execute('''delete from book where code = %s''', (code,))
            self.db.commit()
            QMessageBox.information(self,"success", "The book has been successfully deleted")
            self.clear_data_book()
            self.show_all_books()
            try:
                self.cur.execute('''insert into history(employeid,action,tablee,branchid,datee)
                            values (%s,%s,%s,%s,%s);
                            ''', (self.emp_id, 'Delete', 'Book', self.branch_id, datetime.datetime.now()))
            except (self.db.Error, self.db.Warning) as e:
                print(e)
            self.db.commit()
            self.show_history()
            self.change_dash()

    def all_books_filter(self):
        title = self.booksearchtitle_btn.text()
        catg = self.booksearchcatg_btn.currentText()
        if self.booksearchcatg_btn.currentIndex() !=0 and title!='':
            query_catg = '''select id from category where category_name=%s'''
            self.cur.execute(query_catg,(catg,))
            data_catg = self.cur.fetchone()

            query = '''select code, title,category_id,author_id, price from book where title=%s '''
            self.cur.execute(query,(title,))
            book_title =self.cur.fetchone()

            # if book_title is not None:
            query = '''select code, title,category_id,author_id, price from book where title=%s and category_id=%s '''
            self.cur.execute(query,(title,data_catg[0],))
            data =self.cur.fetchone()



            if data is not None:
                try:
                    self.cur.execute('''insert into history(employeid,action,tablee,branchid,datee)
                                values (%s,%s,%s,%s,%s);
                                ''', (self.emp_id, 'search', 'Book', self.branch_id, datetime.datetime.now()))
                except (self.db.Error, self.db.Warning) as e:
                    print(e)
                self.db.commit()
                self.show_history()
                self.cur.execute('''select category_name from category where id = %s''',(data_catg[0],))
                data_catg = self.cur.fetchone()

                self.cur.execute('''select name from author where id = %s''',(str(data[3]),))
                data_auth = self.cur.fetchone()
                self.booksearchtabel.setRowCount(0)
                self.booksearchtabel.insertRow(0)
                for col, item in enumerate(data):
                    if col ==2:
                        self.booksearchtabel.setItem(0, col, QTableWidgetItem(str(data_catg[0])))
                    elif col == 3:
                        self.booksearchtabel.setItem(0, col, QTableWidgetItem(str(data_auth[0])))
                    else :
                        self.booksearchtabel.setItem(0, col, QTableWidgetItem(str(item)))
            else:
                QMessageBox.warning(self, "book search", "Nothing to show with your search")
        elif self.booksearchcatg_btn.currentIndex() == 0:
            QMessageBox.warning(self, "book search", "Please choice category field")
        else:
            QMessageBox.warning(self, "book search", "Please Enter book title field")

    def export_books(self):
        path = 'C:/Users/Nadjmo m/PycharmProjects/PyQt5/Labrery'
        for f in glob.iglob(path + '/all_books.xlsx', recursive=True):
            os.remove(f)
        query = '''select * from book'''
        self.cur.execute(query)
        data = self.cur.fetchall()
        excel_file = Workbook('all_books.xlsx')
        sheet1 = excel_file.add_worksheet()
        sheet1.write(0, 0, 'id')
        sheet1.write(0, 1, 'title')
        sheet1.write(0, 2, 'description')
        sheet1.write(0, 3, 'category_id')
        sheet1.write(0, 4, 'code')
        sheet1.write(0, 5, 'barcode')
        sheet1.write(0, 6, 'part_order')
        sheet1.write(0, 7, 'price')
        sheet1.write(0, 8, 'publisher_id')
        sheet1.write(0, 9, 'author_id')
        sheet1.write(0, 10, 'image')
        sheet1.write(0, 11, 'status')
        sheet1.write(0, 12,'date')


        row_number = 1
        for row in data:
            col_number = 0
            for item in row:
                sheet1.write(row_number,col_number,str(item))
                col_number += 1
            row_number += 1
        excel_file.close()
        QMessageBox.information(self, "success", "export books successflly")

        #############--Client Operations --###################


    #############--clients Operations --##################

    def show_all_clients(self):
        self.clientsearchall_table.setRowCount(0)
        self.cur.execute(''' select name, mail, phone, national_id, date from client''')
        data = self.cur.fetchall()
        for row, form in enumerate(data):
            self.clientsearchall_table.insertRow(row)
            for col, item in enumerate(form):
               self.clientsearchall_table.setItem(row, col, QTableWidgetItem(str(item)))

    def add_new_client(self):
        name = self.clientaddname_line.text()
        email = self.clientaddmail_line.text()
        phone = self.clientaddphone_line.text()
        national_id = self.clientaddnatid_line.text()
        date = datetime.datetime.now()
        if name == '' or national_id =='':
            QMessageBox.warning(self, "field", "Please checking for name and national id because theme field reqiured")
        else:
            self.cur.execute(''' insert into client(name, mail, phone, date, national_id)
                        values (%s, %s, %s, %s, %s);
            ''',(name, email, phone, date, national_id))
            self.db.commit()
            self.clientaddname_line.clear()
            self.clientaddmail_line.clear()
            self.clientaddphone_line.clear()
            self.clientaddnatid_line.clear()
            self.show_all_clients()
            QMessageBox.information(self, "success", "Add client successflly")
            try:
                self.cur.execute('''insert into history(employeid,action,tablee,branchid,datee)
                            values (%s,%s,%s,%s,%s);
                            ''', (self.emp_id, 'Add', 'client', self.branch_id, datetime.datetime.now()))
            except (self.db.Error, self.db.Warning) as e:
                print(e)
            self.db.commit()
            self.show_history()
            self.change_dash()

    def edite_client(self):
        client_data = self.clienteditedata_line.text()
        if client_data != '':
            if self.clienteditetype_combo.currentIndex() == 0:
                query = 'select * from client where name = %s'
                self.cur.execute(query, (client_data,))
                data = self.cur.fetchone()
                if data is not None:
                    self.set_data_cleint(data=data)
                    self.clienteditesave_btn.setDisabled(False)
                    self.clienteditedelete_btn.setDisabled(False)
                else:
                    self.clear_data_client()
                    self.ui_visible_edit()
                    QMessageBox.warning(self, "field", "This name client does not exist")
            if self.clienteditetype_combo.currentIndex() == 1:
                query = 'select * from client where mail = %s'
                self.cur.execute(query, (client_data,))
                data = self.cur.fetchone()
                if data is not None:
                    self.set_data_cleint(data=data)
                    self.clienteditesave_btn.setDisabled(False)
                    self.clienteditedelete_btn.setDisabled(False)
                else:
                    self.clear_data_client()
                    self.ui_visible_edit()
                    QMessageBox.warning(self, "field", "This mail client does not exist")
            if self.clienteditetype_combo.currentIndex() == 2:
                query = 'select * from client where phone = %s'
                self.cur.execute(query, (client_data,))
                data = self.cur.fetchone()
                if data is not None:
                    self.set_data_cleint(data=data)
                    self.clienteditesave_btn.setDisabled(False)
                    self.clienteditedelete_btn.setDisabled(False)
                else:
                    self.clear_data_client()
                    self.ui_visible_edit()
                    QMessageBox.warning(self, "field", "This phone client does not exist")
            if self.clienteditetype_combo.currentIndex() == 3:
                query = 'select * from client where national_id = %s'
                self.cur.execute(query, (client_data,))
                data = self.cur.fetchone()
                if data is not None:
                    self.set_data_cleint(data=data)
                    self.clienteditesave_btn.setDisabled(False)
                    self.clienteditedelete_btn.setDisabled(False)
                else:
                    self.ui_visible_edit()
                    self.clear_data_client()
                    QMessageBox.warning(self, "field", "This national id client does not exist")
        else:
            QMessageBox.warning(self, "field", "Please Enter Client data")

    global client_id
    def set_data_cleint(self,data):
        self.client_id = data[0]
        self.clienteditename_line.setText(str(data[1]))
        self.clienteditemail_line.setText(str(data[2]))
        self.clienteditephone_line.setText(str(data[3]))
        self.clienteditenatid_line.setText(str(data[5]))

    def clear_data_client(self):
        self.clienteditedata_line.clear()
        self.clienteditename_line.clear()
        self.clienteditemail_line.clear()
        self.clienteditephone_line.clear()
        self.clienteditenatid_line.clear()

    def save_edite_client(self):

        name = self.clienteditename_line.text()
        mail = self.clienteditemail_line.text()
        phone = self.clienteditephone_line.text()
        nat_id = self.clienteditenatid_line.text()

        self.cur.execute('''
            update client set name = %s , mail = %s, phone= %s, national_id=%s where id=%s
        ''', (name, mail, phone, nat_id,self.client_id))
        self.db.commit()
        QMessageBox.information(self, "success", "Edite Client success ")
        self.clear_data_client()
        self.ui_visible_edit()
        self.show_all_clients()
        try:
            self.cur.execute('''insert into history(employeid,action,tablee,branchid,datee)
                        values (%s,%s,%s,%s,%s);
                        ''', (self.emp_id, 'Edite', 'Client', self.branch_id, datetime.datetime.now()))
        except (self.db.Error, self.db.Warning) as e:
            print(e)
        self.db.commit()
        self.show_history()

    def delete_client(self):
        btn_reply = QMessageBox.warning(self, "softwar message", "Are you sur do you want delete This client ?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if btn_reply == QMessageBox.Yes:
            self.cur.execute('''delete from client where id=%s''',(self.client_id,))
            self.db.commit()
            QMessageBox.warning(self,"success", "The client has been successfully deleted")
            self.clear_data_client()
            self.show_all_clients()
            try:
                self.cur.execute('''insert into history(employeid,action,tablee,branchid,datee)
                            values (%s,%s,%s,%s,%s);
                            ''', (self.emp_id, 'Delete', 'client', self.branch_id, datetime.datetime.now()))
            except (self.db.Error, self.db.Warning) as e:
                print(e)
            self.db.commit()
            self.show_history()
            self.change_dash()

    def all_clients_filter(self):
        data_client = self.clientsearchdata_line.text()
        catg = self.clientsearchtypedata_combo.currentText()
        if self.clientsearchtypedata_combo.currentIndex() !=0 and data_client!='':

            if self.clientsearchtypedata_combo.currentIndex() == 1:
                query = '''select name,mail,phone,national_id,date from client where name=%s'''
                self.cur.execute(query, (data_client,))
                data = self.cur.fetchone()

            elif self.clientsearchtypedata_combo.currentIndex() == 2:
                query = '''select name,mail,phone,national_id,date from client where mail=%s'''
                self.cur.execute(query, (data_client,))
                data = self.cur.fetchone()

            elif self.clientsearchtypedata_combo.currentIndex() == 3:
                query = '''select name,mail,phone,national_id,date from client where phone=%s'''
                self.cur.execute(query, (data_client,))
                data = self.cur.fetchone()

            elif self.clientsearchtypedata_combo.currentIndex() == 4:
                query = '''select name,mail,phone,national_id,date from client where national_id=%s'''
                self.cur.execute(query ,(data_client,))
                data = self.cur.fetchone()

            if data is not None:
                try:
                    self.cur.execute('''insert into history(employeid,action,tablee,branchid,datee)
                                values (%s,%s,%s,%s,%s);
                                ''', (self.emp_id, 'Search', 'Client', self.branch_id, datetime.datetime.now()))
                except (self.db.Error, self.db.Warning) as e:
                    print(e)
                self.db.commit()
                self.show_history()
                self.clientsearchall_table.setRowCount(0)
                self.clientsearchall_table.insertRow(0)
                for col, item in enumerate(data):
                    self.clientsearchall_table.setItem(0, col, QTableWidgetItem(str(data[col])))
            else:
                QMessageBox.warning(self, "Client search", "Nothing to show with your search")
        elif data_client == '' :
            QMessageBox.warning(self, "Client search", "Please enter data field")

        elif self.clientsearchtypedata_combo.currentIndex() == 0:
            QMessageBox.warning(self, "Client search", "Please choice type data field")

        else:
            QMessageBox.warning(self, "Client search", "Please cemplete all field")

    def get_all_client(self):
        self.show_all_clients()
        self.clientsearchdata_line.clear()
        self.clientsearchtypedata_combo.setCurrentIndex(0)

    def export_clients(self):
        path = 'C:/Users/Nadjmo m/PycharmProjects/PyQt5/Labrery'
        for f in glob.iglob('/all_client.xlsx',recursive=True):
            os.remove(f)
        query = '''select * from client'''
        self.cur.execute(query)
        data = self.cur.fetchall()
        excel_file = Workbook('all_client.xlsx')
        sheet1 = excel_file.add_worksheet()
        sheet1.write(0, 0, 'id')
        sheet1.write(0, 1, 'name')
        sheet1.write(0, 2, 'mail')
        sheet1.write(0, 3, 'phone')
        sheet1.write(0, 4, 'date')
        sheet1.write(0, 5, 'national_id')

        row_number = 1
        for row in data:
            col_number = 0
            for item in row:
                sheet1.write(row_number,col_number,str(item))
                col_number += 1
            row_number += 1
        excel_file.close()
        QMessageBox.information(self, "success", "export clients successflly")

        #############--Client Operations --###################

      
    ######################################################

    ##########--history--####################

    def show_history(self):
        self.cur.execute('''select employeid,action,tablee,branchid,datee from history''')
        data = self.cur.fetchall()
        self.historyall_table.setRowCount(0)
        for row ,form in enumerate(data):
            self.historyall_table.insertRow(row)
            for col , item in enumerate(form):
                if col == 0:
                    self.cur.execute('''select name from employee where id = %s''',(int(item),))
                    emp_name = self.cur.fetchone()
                    self.historyall_table.setItem(row, col, QTableWidgetItem(emp_name[0]))

                elif col == 3:
                    self.cur.execute('''select name from branch where id = %s''',(int(item),))
                    brn_name = self.cur.fetchone()
                    self.historyall_table.setItem(row, col, QTableWidgetItem(brn_name[0]))
                else:
                    self.historyall_table.setItem(row, col, QTableWidgetItem(str(item)))

    ###########--reports--#####################
    #####books resport

    def all_books_report(self):
        #show all report of books
        pass

    def books_filter_report(self):
        #show report for filtred report books
        pass

    def book_export_report(self):
        #export books data to excel file
        pass

    #####client resport

    def all_clinets_report(self):
        #show all report of clinets
        pass

    def clinets_filter_report(self):
        #show report for filtred report clinets
        pass

    def clinet_export_report(self):
        #export clinets data to excel file
        pass

    #####Monthly resport

    def monthly_report(self):
        #show one month report
        pass

    def monthly_report_export(self):
        #export monthly data to excel file
        pass

    ###########--settings--#####################
    ####### add data
    def add_branch(self):
        branch_name = self.settingsaddbranchname_line.text()
        branch_code = self.settingsaddbranchcode_line.text()
        branch_location = self.settingsaddbranchloc_line.text()
        if branch_name =='':
            QMessageBox.warning(self, "field", "Please checking branch name because him field reqiured")
        else:
            self.cur.execute('''
                insert into branch(name, code, location)
                values (%s, %s, %s)
            ''',(branch_name,branch_code,branch_location))
            self.db.commit()
            QMessageBox.about(self, "succese", "your are now add branch")
            self.settingsaddbranchname_line.setText('')
            self.settingsaddbranchcode_line.setText('')
            self.settingsaddbranchloc_line.setText('')
            QMessageBox.information(self, "success", "Add branch successflly")
            self.show_all_branch()
            try:
                self.cur.execute('''insert into history(employeid,action,tablee,branchid,datee)
                            values (%s,%s,%s,%s,%s);
                            ''', (self.emp_id, 'Add', 'Branch', self.branch_id, datetime.datetime.now()))
            except (self.db.Error, self.db.Warning) as e:
                print(e)
            self.db.commit()
            self.show_history()

    def add_category(self):
        name_catg = self.settingsaddcatgname_line.text()
        if self.settingsaddparntcatg_combo.currentIndex() == 0 :
            parent_category = 'Null'
        else:
            parent_category = self.settingsaddparntcatg_combo.currentText()
        if name_catg == '':
            QMessageBox.warning(self, "field", "Please checking category name because him field reqiured")

        else:
            self.cur.execute('''
                        insert into category(category_name, parent_category)
                        values (%s, %s)
                    ''', (name_catg, parent_category))
            self.db.commit()
            QMessageBox.information(self, "succese", "Add Category successflly")
            self.settingsaddcatgname_line.setText('')
            self.show_all_categories()
            try:
                self.cur.execute('''insert into history(employeid,action,tablee,branchid,datee)
                            values (%s,%s,%s,%s,%s);
                            ''', (self.emp_id, 'Add', 'Category', self.branch_id, datetime.datetime.now()))
            except (self.db.Error, self.db.Warning) as e:
                print(e)
            self.db.commit()
            self.show_history()

    def add_publisher(self):
        name = self.settingsaddpublishname_line.text()
        lacation = self.settingsaddpublishloc_line.text()
        if name == '':
            QMessageBox.warning(self, "field", "Please checking publisher name because him field reqiured")
        else:
            self.cur.execute('''
                insert into publisher(name, location)
                values (%s, %s)
            ''',(name,lacation,))
            self.db.commit()
            QMessageBox.information(self, "succese", "Add Publisher successfly")
            self.settingsaddpublishname_line.setText('')
            self.settingsaddpublishloc_line.setText('')
            self.show_all_publisher()
            try:
                self.cur.execute('''insert into history(employeid,action,tablee,branchid,datee)
                            values (%s,%s,%s,%s,%s);
                            ''', (self.emp_id, 'Add', 'Publisher', self.branch_id, datetime.datetime.now()))
            except (self.db.Error, self.db.Warning) as e:
                print(e)
            self.db.commit()
            self.show_history()

    def add_author(self):
        name = self.settingsaddauthorname_line.text()
        lacation = self.settingsaddauthorloc_line.text()
        if name == '':
            QMessageBox.warning(self, "field", "Please checking author name because him field reqiured")
        else:
            self.cur.execute('''
                insert into author(name, location)
                values (%s, %s)
            ''',(name,lacation))
            self.db.commit()
            QMessageBox.about(self, "succese", "Add Author successfly")
            self.settingsaddauthorname_line.setStyleSheet('')
            self.settingsaddauthorname_line.setText('')
            self.settingsaddauthorloc_line.setText('')
            self.show_all_author()
            try:
                self.cur.execute('''insert into history(employeid,action,tablee,branchid,datee)
                            values (%s,%s,%s,%s,%s);
                            ''', (self.emp_id, 'Add', 'Author', self.branch_id, datetime.datetime.now()))
            except (self.db.Error, self.db.Warning) as e:
                print(e)
            self.db.commit()
            self.show_history()

    ######################---show all ---#########################################"
    #############################################################################"

    def show_all_categories(self):
        self.settingsaddparntcatg_combo.clear()
        self.settingsaddparntcatg_combo.addItem('-----------------')
        self.booksearchcatg_btn.clear()
        self.booksearchcatg_btn.addItem('-----------------')
        self.bookaddcatg_combo.clear()
        self.bookaddcatg_combo.addItem('-----------------')
        self.bookeditecatg_combo.clear()
        self.bookeditecatg_combo.addItem('-----------------')
        self.cur.execute('''
         select * from category
        ''')
        categories = self.cur.fetchall()
        for catg in categories:
            self.settingsaddparntcatg_combo.addItem(catg[1])
            self.booksearchcatg_btn.addItem(catg[1])
            self.bookaddcatg_combo.addItem(catg[1])
            self.bookeditecatg_combo.addItem(catg[1])

    def show_all_publisher(self):
        self.bookaddpublisher_combo.clear()
        self.bookaddpublisher_combo.addItem('-----------------')
        self.bookeditepublish_compbo.clear()
        self.bookeditepublish_compbo.addItem('-----------------')
        self.cur.execute('''
         select name from publisher
        ''')
        publisher = self.cur.fetchall()
        for publisher in publisher:
            self.bookaddpublisher_combo.addItem(publisher[0])
            self.bookeditepublish_compbo.addItem(publisher[0])

    def show_all_author(self):
        self.bookaddauthor_combo.clear()
        self.bookaddauthor_combo.addItem('-----------------')
        self.bookediteauthor_line.clear()
        self.bookediteauthor_line.addItem('-----------------')
        self.cur.execute('''
         select name from author
        ''')
        author = self.cur.fetchall()
        for author in author:
            self.bookaddauthor_combo.addItem(author[0])
            self.bookediteauthor_line.addItem(author[0])

    def show_all_branch(self):
        self.historybranch_cpmbo.clear()
        self.historybranch_cpmbo.addItem('-----------------')
        self.settingsaddempbranch_combo.clear()
        self.settingsaddempbranch_combo.addItem('-----------------')
        self.settingsediteempbranch_combo.clear()
        self.settingsediteempbranch_combo.addItem('-----------------')

        self.cur.execute('''
         select name from branch
        ''')
        branch = self.cur.fetchall()
        for branch in branch:
            self.historybranch_cpmbo.addItem(branch[0])
            self.settingsaddempbranch_combo.addItem(branch[0])
            self.settingsediteempbranch_combo.addItem(branch[0])

    #############################################################################"
    #############################################################################"


    ####### employe
    def add_employe(self):
        password_emp = self.settingsaddemppass_line.text()
        password2 = self.settingsaddemppasagain_line.text()
        name_emp = self.settingsaddempname_line.text()
        mail_emp = self.settingsaddempmail_line.text()
        phone_emp =  self.settingsaddempphone_line.text()
        nationId_emp = self.settingsaddempnatid_line.text()
        date_emp = datetime.datetime.now()
        perio_emp = self.settingsaddempperiority_line.text()
        branch_emp = self.settingsaddempbranch_combo.currentText()
        branch_index = self.settingsaddempbranch_combo.currentIndex()
        if (name_emp == '') or (nationId_emp == '') or (password_emp == '') or (branch_index == 0) :
            QMessageBox.warning(self, "faild", "name employee and national id and password and branch is required ")
        else:
            self.cur.execute(''' select id from branch where name= %s  ''',(branch_emp,))
            query_branch  = self.cur.fetchall()
            for i in query_branch:
                branch_id = i[0]
            if password_emp == password2:
                self.cur.execute('''insert into employee(name, mail, phone, date, national_id, periority, password, branch_id)
                                                values (%s, %s, %s, %s, %s, %s, %s, %s);
                ''',(name_emp, mail_emp, phone_emp, date_emp, nationId_emp, perio_emp, password_emp, branch_id))
                self.db.commit()
                self.settingsaddempname_line.clear()
                self.settingsaddempmail_line.clear()
                self.settingsaddempphone_line.clear()
                self.settingsaddempnatid_line.clear()
                self.settingsaddempperiority_line.clear()
                self.settingsaddemppass_line.clear()
                self.settingsaddempbranch_combo.setCurrentIndex(0)
                self.settingsaddemppasagain_line.clear()
                self.show_all_employee()
                QMessageBox.information(self, "succese", "your are now add employee")
                self.change_dash()
            else:
                QMessageBox.warning(self, "faild", "password fields not some much")

    def edite_employe(self):
        name = self.settingsediteempname_line.text()
        mail =self.settingsediteempmail_line.text()
        phone = self.settingsediteempphone_line.text()
        branch = self.settingsediteempbranch_combo.currentText()
        nat_id = self.settingsediteempnatid_line.text()
        periority = self.settingsediteempperiority_line.text()
        password2 = self.settingsediteemppass_line_2.text()
        password = self.settingsediteemppass_line.text()
        if password2 == password:
            query = '''select id from branch where name=%s'''
            self.cur.execute(query, (branch,))
            data_branch = self.cur.fetchone()
            query = '''update employee set mail = %s, phone = %s, national_id = %s, periority=%s, branch_id = %s, password=%s where name=%s'''
            self.cur.execute(query,(mail, phone, nat_id, periority, data_branch[0], password2, name))
            self.db.commit()
            self.settingsediteempname_line.clear()
            self.settingsediteempmail_line.clear()
            self.settingsediteempphone_line.clear()
            self.settingsediteempbranch_combo.setCurrentIndex(0)
            self.settingsediteempnatid_line.clear()
            self.settingsediteempperiority_line.clear()
            self.settingsediteemppass_line_2.clear()
            self.settingsediteemppass_line.clear()
            self.groupBox2.setEnabled(False)
            QMessageBox.about(self, "succese", "edite employee successfully")


        else:
            QMessageBox.warning(self, "faild", "Please confirm your password in inforamtion edite ")

    def check_employe(self):
        emp_name = self.settingsediteempname_line.text()
        password = self.settingsediteemppass_line.text()
        query = '''select * from employee where name = %s and password = %s;'''
        self.cur.execute(query,(emp_name.lower(), password))
        data = self.cur.fetchone()
        if data != None:
            query = '''select name from branch where id=%s'''
            self.cur.execute(query, (data[8],))
            data_branch = self.cur.fetchone()
            if emp_name.lower() == data[1].lower() and password == data[7]:
                self.settingsediteempsave_btn.setEnabled(True)
                self.groupBox2.setEnabled(True)
                self.settingsediteempmail_line.setText(str(data[2]))
                self.settingsediteempphone_line.setText(str(data[3]))
                self.settingsediteempbranch_combo.setCurrentText(data_branch[0])
                self.settingsediteempnatid_line.setText(str(data[5]))
                self.settingsediteempperiority_line.setText(str(data[6]))
                self.settingsediteemppass_line_2.setText(str(data[7]))
        else:
            QMessageBox.warning(self, "faild", "Please confirm your name or password")

    def show_all_employee(self):
        self.settingspermsemp_combo.clear()
        self.settingspermsemp_combo.addItem('--------------------------------')
        self.historybranch_cpmbo.clear()
        self.historybranch_cpmbo.addItem('--------------------------------')
        query = '''select name from employee'''
        self.cur.execute(query)
        data = self.cur.fetchall()
        for form in data:
            self.settingspermsemp_combo.addItem(form[0])
            self.historybranch_cpmbo.addItem(form[0])
    ###### permissions
    def add_employe_permissions(self):

        book_tab = 0
        client_tab = 0
        dashboard_tab = 0
        history_tab = 0
        reports_tab = 0
        settings_tab = 0
        employe_name = self.settingspermsemp_combo.currentText()
        add_book = 0
        edite_book = 0
        delete_book = 0
        import_book = 0
        export_book = 0

        add_client = 0
        edite_client = 0
        delete_client = 0
        import_client = 0
        export_client = 0

        add_branch = 0
        add_publisher = 0
        add_author = 0
        add_employe = 0
        add_category = 0
        edite_employe = 0
        admin = 0


        query ='''select id from employee where name = %s'''
        self.cur.execute(query,(employe_name,))
        data = self.cur.fetchone()
        id_employee = int(data[0])

        query ='''select idemployee from employee_permissions where idemployee = %s'''
        self.cur.execute(query,(id_employee,))
        data = self.cur.fetchone()

        # if data is None:
        if self.settingsparmsdclient_check_9.isChecked() == True:
                admin = 1
                self.cur.execute('''
                            insert into employee_permissions(idemployee,employe_name,book_tab, client_tab, dashboard_tab, history_tab, reports_tab, settings_tab,
                            add_book ,edite_book ,delete_book,import_book,export_book,add_client, edite_client ,delete_client,import_client,export_client,
                            add_branch,add_publisher,add_author,add_employe,add_category ,edite_employe,admin)
                            values (%s,%s, 1, 1, 1, 1, 1, 1,
                            1, 1, 1, 1, 1, 1, 1,1,1,1,
                            1, 1, 1, 1, 1, 1, 1)
                    ''',(id_employee,employe_name,))
                QMessageBox.about(self, "succese", "Add Permissions employe successfully")
                self.db.commit()
                self.ui_clear_permissions()
                self.ui_fenabled_permiss_emp()
        else:
                admin = 0
                if self.settingsparmsaclient_check.isChecked() == True:
                    add_client = 1
                if self.settingsparmseclient_check.isChecked() == True:
                    edite_client = 1
                if self.settingsparmsdclient_check.isChecked() == True:
                    delete_client = 1
                if self.settingsparmsdclient_check_2.isChecked() == True:
                    import_client = 1
                if self.settingsparmsdclient_check_3.isChecked() == True:
                    export_client = 1
                if self.settingsparmsabook_check.isChecked() == True:
                    add_book = 1
                if self.settingsparmsebook_check.isChecked() == True:
                    edite_book = 1
                if self.settingsparmsdbook_check.isChecked() == True:
                    delete_book = 1
                if self.settingsparmsdclient_check_5.isChecked() == True:
                    import_book = 1
                if self.settingsparmsdclient_check_4.isChecked() == True:
                    export_book = 1

                if self.settingsparmsabook_check_2.isChecked() == True:
                    add_branch = 1
                if self.settingsparmsebook_check_2.isChecked() == True:
                    add_publisher = 1
                if self.settingsparmsdbook_check_2.isChecked() == True:
                    add_author = 1
                if self.settingsparmsdclient_check_7.isChecked() == True:
                    add_category = 1
                if self.settingsparmsdclient_check_6.isChecked() == True:
                    add_employe = 1
                if self.settingsparmsdclient_check_8.isChecked() == True:
                    edite_employe = 1
                if self.settingsparmsbook_check.isChecked() == True:
                    book_tab = 1
                if self.settingsparmsclient_check.isChecked() == True:
                    client_tab = 1
                if self.settingsparmsdashboard_check.isChecked() == True:
                    dashboard_tab = 1
                if self.settingsparmshistory_check.isChecked() == True:
                    history_tab = 1
                if self.settingsparmsreports_check.isChecked() == True:
                    reports_tab = 1
                if self.settingsparmssettings_check.isChecked() == True:
                    settings_tab = 1

                self.cur.execute('''
                        insert into employee_permissions(idemployee,employe_name,book_tab, client_tab, dashboard_tab, history_tab, reports_tab, settings_tab,
                            add_book ,edite_book ,delete_book,import_book,export_book,add_client, edite_client ,delete_client,import_client,export_client,
                            add_branch,add_publisher,add_author,add_employe,add_category ,edite_employe,admin)
                        values (%s,%s, %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s, %s,%s,%s,%s,
                        %s, %s, %s, %s, %s, %s, %s)
                ''',(id_employee,employe_name,book_tab, client_tab, dashboard_tab, history_tab, reports_tab, settings_tab,
                     add_book, edite_book, delete_book, import_book, export_book, add_client,
                     edite_client, delete_client, import_client, export_client,
                     add_branch, add_publisher, add_author, add_employe, add_category, edite_employe,admin,))

                self.db.commit()
                QMessageBox.about(self, "succese", "Add Permissions employe successfully")
                self.ui_clear_permissions()
                self.ui_fenabled_permiss_emp()
        # else:
        #     QMessageBox.warning(self, "Field", "THis employee have Permissions Please Try it out with another employee")

    ###### email report

    def admin_report_email(self):
        pass


    ################################################################################
    ################################################################################

##########################--move in the project--#######################################"
#############################################################################"
    def open_daily_movment_today(self):
        self.today_btn.setStyleSheet('background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);'
                                     '\n border:none;\nborder-right:10px solid black;\n color:black;\n border-radius:0;outline: none;')
        self.books_btn.setStyleSheet('')
        self.client_btn.setStyleSheet('')
        self.dash_btn.setStyleSheet('')
        self.history_btn.setStyleSheet('')
        self.reports_btn.setStyleSheet('')
        self.settings_btn.setStyleSheet('')
        self.Main_tab.setCurrentIndex(2)

    def open_client_tab(self):
        self.client_btn.setStyleSheet('background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);'
                                     '\n border:none;\nborder-right:10px solid black;\n color:black;\n border-radius:0;outline: none;')
        self.today_btn.setStyleSheet('')
        self.books_btn.setStyleSheet('')
        self.dash_btn.setStyleSheet('')
        self.history_btn.setStyleSheet('')
        self.reports_btn.setStyleSheet('')
        self.settings_btn.setStyleSheet('')
        self.Main_tab.setCurrentIndex(4)
        self.client_stacked.setCurrentIndex(0)
        self.clientsearchframe_btn.setStyleSheet('border-bottom: 2px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);outline: none;')
        self.clientaddfram_btn.setStyleSheet('')
        self.clienteditefram_btn.setStyleSheet('')

    def open_book_tab(self):
        self.books_btn.setStyleSheet('background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);'
                                     '\n border:none;\nborder-right:10px solid black;\n color:black;\n border-radius:0;outline: none;')
        self.today_btn.setStyleSheet('')
        self.client_btn.setStyleSheet('')
        self.dash_btn.setStyleSheet('')
        self.history_btn.setStyleSheet('')
        self.reports_btn.setStyleSheet('')
        self.settings_btn.setStyleSheet('')
        self.Main_tab.setCurrentIndex(3)
        self.books_stacked.setCurrentIndex(0)
        self.booksearchframe_btn.setStyleSheet('border-bottom: 2px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);outline: none;')
        self.bookeditframe_btn.setStyleSheet('')
        self.bookaddframe_btn.setStyleSheet('')

    def open_dashboard_tab(self):
        self.dash_btn.setStyleSheet('background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);'
                                     '\n border:none;\nborder-right:10px solid black;\n color:black;\n border-radius:0;outline: none;')
        self.books_btn.setStyleSheet('')
        self.client_btn.setStyleSheet('')
        self.today_btn.setStyleSheet('')
        self.history_btn.setStyleSheet('')
        self.reports_btn.setStyleSheet('')
        self.settings_btn.setStyleSheet('')
        self.Main_tab.setCurrentIndex(5)

    def open_history_tab(self):
        self.history_btn.setStyleSheet('background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);'
                                     '\n border:none;\nborder-right:10px solid black;\n color:black;\n border-radius:0;outline: none;')
        self.books_btn.setStyleSheet('')
        self.client_btn.setStyleSheet('')
        self.dash_btn.setStyleSheet('')
        self.today_btn.setStyleSheet('')
        self.reports_btn.setStyleSheet('')
        self.settings_btn.setStyleSheet('')
        self.Main_tab.setCurrentIndex(6)

    def open_report_tab(self):
        self.reports_btn.setStyleSheet('background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);'
                                     '\n border:none;\nborder-right:10px solid black;\n color:black;\n border-radius:0;outline: none;')
        self.books_btn.setStyleSheet('')
        self.client_btn.setStyleSheet('')
        self.dash_btn.setStyleSheet('')
        self.history_btn.setStyleSheet('')
        self.today_btn.setStyleSheet('')
        self.settings_btn.setStyleSheet('')
        self.Main_tab.setCurrentIndex(7)
        self.reports_stacked.setCurrentIndex(0)
        self.reportbooksfram_btn.setStyleSheet('border-bottom: 2px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);outline: none;')
        self.reportclientsfram_btn.setStyleSheet('')
        self.reportmonthlyfram_btn_2.setStyleSheet('')

    def open_settings_tab(self):
        self.settings_btn.setStyleSheet('background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);'
                                     '\n border:none;\nborder-right:10px solid black;\n color:black;\n border-radius:0;outline: none;')
        self.books_btn.setStyleSheet('')
        self.client_btn.setStyleSheet('')
        self.dash_btn.setStyleSheet('')
        self.history_btn.setStyleSheet('')
        self.reports_btn.setStyleSheet('')
        self.today_btn.setStyleSheet('')
        self.Main_tab.setCurrentIndex(8)
        self.settings_stacked.setCurrentIndex(0)
        self.settingsadddataframe_btn.setStyleSheet('border-bottom: 2px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);outline: none;')
        self.settingspermisframe_btn.setStyleSheet('')
        self.settingsaddemplframe_btn.setStyleSheet('')
        self.settingsemailframe_btn.setStyleSheet('')

    #############stacked ############################

    def open_search_book_stacked(self):
        self.books_stacked.setCurrentIndex(0)
        self.booksearchframe_btn.setStyleSheet('border-bottom: 2px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);outline: none;')
        self.bookeditframe_btn.setStyleSheet('')
        self.bookaddframe_btn.setStyleSheet('')

    def open_add_book_stacked(self):
        self.books_stacked.setCurrentIndex(1)
        self.bookaddframe_btn.setStyleSheet('border-bottom: 2px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);outline: none;')
        self.bookeditframe_btn.setStyleSheet('')
        self.booksearchframe_btn.setStyleSheet('')

    def open_edite_book_stacked(self):
        self.books_stacked.setCurrentIndex(2)
        self.bookeditframe_btn.setStyleSheet('border-bottom: 2px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);outline: none;')
        self.bookaddframe_btn.setStyleSheet('')
        self.booksearchframe_btn.setStyleSheet('')

    def open_search_client_stacked(self):
        self.client_stacked.setCurrentIndex(0)
        self.clientsearchframe_btn.setStyleSheet('border-bottom: 2px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);outline: none;')
        self.clientaddfram_btn.setStyleSheet('')
        self.clienteditefram_btn.setStyleSheet('')

    def open_add_client_stacked(self):
        self.client_stacked.setCurrentIndex(1)
        self.clientaddfram_btn.setStyleSheet('border-bottom: 2px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);outline: none;')
        self.clientsearchframe_btn.setStyleSheet('')
        self.clienteditefram_btn.setStyleSheet('')

    def open_edite_client_stacked(self):
        self.client_stacked.setCurrentIndex(2)
        self.clienteditefram_btn.setStyleSheet('border-bottom: 2px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);outline: none;')
        self.clientsearchframe_btn.setStyleSheet('')
        self.clientaddfram_btn.setStyleSheet('')

    def open_report_book_stacked(self):
        self.reports_stacked.setCurrentIndex(0)
        self.reportbooksfram_btn.setStyleSheet('border-bottom: 2px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);outline: none;')
        self.reportclientsfram_btn.setStyleSheet('')
        self.reportmonthlyfram_btn_2.setStyleSheet('')

    def open_report_client_stacked(self):
        self.reports_stacked.setCurrentIndex(1)
        self.reportclientsfram_btn.setStyleSheet('border-bottom: 2px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);outline: none;')
        self.reportbooksfram_btn.setStyleSheet('')
        self.reportmonthlyfram_btn_2.setStyleSheet('')

    def open_report_monthly_stacked(self):
        self.reports_stacked.setCurrentIndex(2)
        self.reportmonthlyfram_btn_2.setStyleSheet('border-bottom: 2px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);outline: none;')
        self.reportbooksfram_btn.setStyleSheet('')
        self.reportclientsfram_btn.setStyleSheet('')

    def open_settings_data_stacked(self):
        self.settings_stacked.setCurrentIndex(0)
        self.settingsadddataframe_btn.setStyleSheet('border-bottom: 2px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);outline: none;')
        self.settingspermisframe_btn.setStyleSheet('')
        self.settingsaddemplframe_btn.setStyleSheet('')
        self.settingsemailframe_btn.setStyleSheet('')

    def open_settings_employee_stacked(self):
        self.settings_stacked.setCurrentIndex(1)
        self.settingsaddemplframe_btn.setStyleSheet('border-bottom: 2px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);outline: none;')
        self.settingspermisframe_btn.setStyleSheet('')
        self.settingsadddataframe_btn.setStyleSheet('')
        self.settingsemailframe_btn.setStyleSheet('')

    def open_settings_permissions_stacked(self):
        self.settings_stacked.setCurrentIndex(2)
        self.settingspermisframe_btn.setStyleSheet('border-bottom: 2px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);outline: none;')
        self.settingsaddemplframe_btn.setStyleSheet('')
        self.settingsadddataframe_btn.setStyleSheet('')
        self.settingsemailframe_btn.setStyleSheet('')

    def open_settings_email_stacked(self):
        self.settings_stacked.setCurrentIndex(3)
        self.settingsemailframe_btn.setStyleSheet('border-bottom: 2px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);outline: none;')
        self.settingsaddemplframe_btn.setStyleSheet('')
        self.settingsadddataframe_btn.setStyleSheet('')
        self.settingspermisframe_btn.setStyleSheet('')

    def open_restp_tab(self):
        self.Main_tab.setCurrentIndex(1)

    def open_login_tab(self):
        self.Main_tab.setCurrentIndex(0)
#############################################################################"
#############################################################################"
def main():
    app = QApplication(sys.argv)
    window = Main()
    window.showMaximized()
    app.exec()

if __name__ == '__main__':
    main()