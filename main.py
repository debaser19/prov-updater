from PyQt5 import QtCore, QtGui, QtWidgets
import meraki
import creds
import json


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(398, 524)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.headerLabel = QtWidgets.QLabel(self.centralwidget)
        self.headerLabel.setGeometry(QtCore.QRect(30, 10, 201, 31))
        self.headerLabel.setObjectName("headerLabel")
        self.lblGetTable = QtWidgets.QLabel(self.centralwidget)
        self.lblGetTable.setGeometry(QtCore.QRect(20, 70, 91, 16))
        self.lblGetTable.setObjectName("lblGetTable")
        self.cmbSelectTable = QtWidgets.QComboBox(self.centralwidget)
        self.cmbSelectTable.setGeometry(QtCore.QRect(230, 70, 131, 26))
        self.cmbSelectTable.setObjectName("cmbSelectTable")
        self.cmbSelectTable.addItem("")
        self.cmbSelectTable.addItem("")
        self.cmbSelectTable.addItem("")
        self.cmbSelectTable.addItem("")
        self.cmbSelectTable.addItem("")
        self.cmbSelectTable.addItem("")
        self.cmbSelectTable.addItem("")
        self.cmbSelectTable.addItem("")
        self.cmbSelectTable.addItem("")
        self.cmbSetTable = QtWidgets.QComboBox(self.centralwidget)
        self.cmbSetTable.setGeometry(QtCore.QRect(240, 300, 131, 26))
        self.cmbSetTable.setObjectName("cmbSetTable")
        self.cmbSetTable.addItem("")
        self.cmbSetTable.addItem("")
        self.cmbSetTable.addItem("")
        self.cmbSetTable.addItem("")
        self.cmbSetTable.addItem("")
        self.cmbSetTable.addItem("")
        self.cmbSetTable.addItem("")
        self.cmbSetTable.addItem("")
        self.cmbSetTable.addItem("")
        self.lblUpdateTable = QtWidgets.QLabel(self.centralwidget)
        self.lblUpdateTable.setGeometry(QtCore.QRect(30, 300, 171, 16))
        self.lblUpdateTable.setObjectName("lblUpdateTable")
        self.lblSetOption = QtWidgets.QLineEdit(self.centralwidget)
        self.lblSetOption.setGeometry(QtCore.QRect(30, 330, 341, 21))
        self.lblSetOption.setObjectName("lblSetOption")
        self.btnSubmit = QtWidgets.QPushButton(self.centralwidget)
        self.btnSubmit.setGeometry(QtCore.QRect(140, 360, 113, 32))
        self.btnSubmit.setObjectName("btnSubmit")
        self.txtCurrentOption = QtWidgets.QLineEdit(self.centralwidget)
        self.txtCurrentOption.setGeometry(QtCore.QRect(20, 100, 341, 21))
        self.txtCurrentOption.setReadOnly(True)
        self.txtCurrentOption.setObjectName("txtCurrentOption")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 398, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.cmbSelectTable.activated.connect(self.getTableInfo)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.headerLabel.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:24pt;\">Prov Table Updater</span></p></body></html>"))
        self.lblGetTable.setText(_translate("MainWindow", "Get Table Info"))
        self.cmbSelectTable.setItemText(0, _translate("MainWindow", "Select a table"))
        self.cmbSelectTable.setItemText(1, _translate("MainWindow", "Table 1"))
        self.cmbSelectTable.setItemText(2, _translate("MainWindow", "Table 2"))
        self.cmbSelectTable.setItemText(3, _translate("MainWindow", "Table 3"))
        self.cmbSelectTable.setItemText(4, _translate("MainWindow", "Table 4"))
        self.cmbSelectTable.setItemText(5, _translate("MainWindow", "Table 5"))
        self.cmbSelectTable.setItemText(6, _translate("MainWindow", "Table 6"))
        self.cmbSelectTable.setItemText(7, _translate("MainWindow", "Table 7"))
        self.cmbSelectTable.setItemText(8, _translate("MainWindow", "Table 8"))
        self.cmbSetTable.setItemText(0, _translate("MainWindow", "Select a table"))
        self.cmbSetTable.setItemText(1, _translate("MainWindow", "Table 1"))
        self.cmbSetTable.setItemText(2, _translate("MainWindow", "Table 2"))
        self.cmbSetTable.setItemText(3, _translate("MainWindow", "Table 3"))
        self.cmbSetTable.setItemText(4, _translate("MainWindow", "Table 4"))
        self.cmbSetTable.setItemText(5, _translate("MainWindow", "Table 5"))
        self.cmbSetTable.setItemText(6, _translate("MainWindow", "Table 6"))
        self.cmbSetTable.setItemText(7, _translate("MainWindow", "Table 7"))
        self.cmbSetTable.setItemText(8, _translate("MainWindow", "Table 8"))
        self.lblUpdateTable.setText(_translate("MainWindow", "Update Table DHCP Option"))
        self.lblSetOption.setText(_translate("MainWindow", "Add an option"))
        self.btnSubmit.setText(_translate("MainWindow", "Send it!"))
        self.txtCurrentOption.setText(_translate("MainWindow", "Select a table..."))

    def getTableInfo(self):
        print("Getting table info...")
        API_KEY = creds.creds['api_key']
        dashboard = meraki.DashboardAPI(
            api_key = API_KEY,
            base_url = 'https://api-mp.meraki.com/api/v1/',
            print_console = False,
            output_log = False
        )

        network = 'L_613052499275810377'
        selected_table = self.cmbSelectTable.currentText()
        selected_table = '10' + selected_table[-1:]

        table_id = int(selected_table)
        dhcp_option = 'UNSET'
        try:
            # Get list of clients on network, filtering on timespan of last 14 days
            vlans = dashboard.appliance.getNetworkApplianceVlans(network)
        except meraki.APIError as e:
            print(f'Meraki API error: {e}')
            print(f'status code = {e.status}')
            print(f'reason = {e.reason}')
            print(f'error = {e.message}')
        except Exception as e:
            print(f'some other error: {e}')
        else:
            for vlan in vlans:
                if vlan['id'] == table_id and 'dhcpOptions' in vlan:
                    print(f'VLAN: {vlan}')
                    for option in vlan['dhcpOptions']:
                        dhcp_option = option['value']
        
        print(f'Current option: {dhcp_option}')
        self.txtCurrentOption.setText(dhcp_option)
        

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
