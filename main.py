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
        self.headerLabel.setGeometry(QtCore.QRect(20, 10, 201, 31))
        self.headerLabel.setObjectName("headerLabel")

        self.lblSelectTable = QtWidgets.QLabel(self.centralwidget)
        self.lblSelectTable.setGeometry(QtCore.QRect(20, 70, 91, 25))
        self.lblSelectTable.setObjectName("lblSelectTable")

        self.lblCurrentOption = QtWidgets.QLabel(self.centralwidget)
        self.lblCurrentOption.setGeometry(QtCore.QRect(20, 105, 91, 25))
        self.lblCurrentOption.setObjectName("lblCurrentOption")

        self.lblNewOption = QtWidgets.QLabel(self.centralwidget)
        self.lblNewOption.setGeometry(QtCore.QRect(20, 140, 91, 25))
        self.lblNewOption.setObjectName("lblNewOption")

        self.cmbSelectTable = QtWidgets.QComboBox(self.centralwidget)
        self.cmbSelectTable.setGeometry(QtCore.QRect(140, 70, 110, 25))
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

        self.btnSubmit = QtWidgets.QPushButton(self.centralwidget)
        self.btnSubmit.setGeometry(QtCore.QRect(50, 175, 130, 35))
        self.btnSubmit.setObjectName("btnSubmit")

        self.btnClear = QtWidgets.QPushButton(self.centralwidget)
        self.btnClear.setGeometry(QtCore.QRect(190, 175, 130, 35))
        self.btnClear.setObjectName("btnClear")

        self.txtCurrentOption = QtWidgets.QLineEdit(self.centralwidget)
        self.txtCurrentOption.setGeometry(QtCore.QRect(140, 105, 220, 25))
        self.txtCurrentOption.setReadOnly(True)
        self.txtCurrentOption.setObjectName("txtCurrentOption")

        self.txtSetOption = QtWidgets.QLineEdit(self.centralwidget)
        self.txtSetOption.setGeometry(QtCore.QRect(140, 140, 220, 25))
        self.txtSetOption.setObjectName("txtSetOption")

        self.txtTableList = QtWidgets.QTextBrowser(self.centralwidget)
        self.txtTableList.setGeometry(QtCore.QRect(20, 220, 350, 300))
        self.txtTableList.setObjectName("txtTableList")

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

        # actions
        self.cmbSelectTable.activated.connect(self.getTableInfo)
        self.btnSubmit.clicked.connect(self.setTableInfo)
        self.btnClear.clicked.connect(self.clearTableInfo)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("Prov Option Updater 3000", "Prov Option Updater 3000"))
        self.headerLabel.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:18pt;\">Prov Table Updater</span></p></body></html>"))
        self.headerLabel.adjustSize()
        self.lblSelectTable.setText(_translate("MainWindow", "Select Table"))
        self.lblCurrentOption.setText(_translate("MainWindow", "Current Option"))
        self.lblNewOption.setText(_translate("MainWindow", "New Option"))
        self.cmbSelectTable.setItemText(0, _translate("MainWindow", "Select a table"))
        self.cmbSelectTable.setItemText(1, _translate("MainWindow", "Table 1"))
        self.cmbSelectTable.setItemText(2, _translate("MainWindow", "Table 2"))
        self.cmbSelectTable.setItemText(3, _translate("MainWindow", "Table 3"))
        self.cmbSelectTable.setItemText(4, _translate("MainWindow", "Table 4"))
        self.cmbSelectTable.setItemText(5, _translate("MainWindow", "Table 5"))
        self.cmbSelectTable.setItemText(6, _translate("MainWindow", "Table 6"))
        self.cmbSelectTable.setItemText(7, _translate("MainWindow", "Table 7"))
        self.cmbSelectTable.setItemText(8, _translate("MainWindow", "Table 8"))
        self.cmbSelectTable.adjustSize()
        self.txtSetOption.setPlaceholderText("Set new option...")
        self.txtTableList.setPlaceholderText("Waiting for API call...")
        self.btnSubmit.setText(_translate("MainWindow", "Send it!"))
        self.btnClear.setText(_translate("MainWindow", "Clear that shit"))
        self.txtCurrentOption.setPlaceholderText(_translate("MainWindow", "Select a table..."))

    
    def getTableInfo(self):
        self.txtCurrentOption.setText("Getting table info...")
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
            tables_string = ''
            for vlan in vlans:
                vlan_id = vlan['id']
                option_value = 'UNSET'
                if 'dhcpOptions' in vlan:
                    for option in vlan['dhcpOptions']:
                        option_value = option['value']
                        if vlan['id'] == table_id:
                            dhcp_option = option['value']

                if vlan_id in range(101,109):
                    tables_string += f'Table {vlan_id}: {option_value}\n\n'

        self.txtTableList.setText(tables_string)
        
        print(f'Current option: {dhcp_option}')
        if dhcp_option != 'Select a table...':
            self.txtCurrentOption.setText(dhcp_option)

    def setTableInfo(self):
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
        tables_string = ''

        optionToSet = self.txtSetOption.text()
        print(f'Setting table {table_id} with option {optionToSet}')

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
            list_of_vlans = []
            for vlan in vlans:
                # vlan_id = vlan['id']
                option_value = 'UNSET'
                if 'dhcpOptions' in vlan:
                    for option in vlan['dhcpOptions']:
                        option_value = option['value']
                    vlan_dict = {
                        "table_id": vlan['id'],
                        "table_option": option_value
                    }
                    list_of_vlans.append(vlan_dict)
                if vlan['id'] == table_id:
                    dhcp_option = []
                    set_vlan = {
                        "code": "66",
                        "type": "text",
                        "value": optionToSet
                    }
                    option_value = set_vlan['value']
                    dhcp_option.append(set_vlan)
                    print(dhcp_option)

                    dashboard.appliance.updateNetworkApplianceVlan(network, table_id, dhcpOptions=dhcp_option)

            for vlan in list_of_vlans:
                if vlan['table_id'] in range(101,109):
                    table_option = vlan['table_option']
                    vlan_id = vlan['table_id']
                    if vlan_id == table_id:
                        table_option = optionToSet
                    tables_string += f'Table {vlan_id}: {table_option}\n\n'
        
        self.txtCurrentOption.setText(optionToSet)
        self.txtTableList.setText(tables_string)
        self.txtSetOption.setText('')

    
    def clearTableInfo(self):
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
        tables_string = ''

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
            list_of_vlans = []
            for vlan in vlans:
                # vlan_id = vlan['id']
                option_value = 'UNSET'
                if 'dhcpOptions' in vlan:
                    for option in vlan['dhcpOptions']:
                        option_value = option['value']
                    vlan_dict = {
                        "table_id": vlan['id'],
                        "table_option": option_value
                    }
                    list_of_vlans.append(vlan_dict)

            for vlan in list_of_vlans:
                if vlan['table_id'] in range(101,109):
                    table_option = vlan['table_option']
                    vlan_id = vlan['table_id']
                    if vlan_id == table_id:
                        table_option = 'UNSET'
                    tables_string += f'Table {vlan_id}: {table_option}\n\n'

        dashboard.appliance.updateNetworkApplianceVlan(network, table_id, dhcpOptions=[])

        self.txtCurrentOption.setText('UNSET')
        self.txtTableList.setText(tables_string)
        self.txtSetOption.setText('')
        

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
