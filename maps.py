import folium, io, json, sys, math, random, os
import psycopg2
from folium.plugins import Draw, MousePosition, MeasureControl
from jinja2 import Template
from branca.element import Element
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import (QtGui, QtCore, QtWidgets)


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.resize(600, 600)
        
        main = QWidget()
        self.setCentralWidget(main)
        main.setLayout(QVBoxLayout())
        main.setFocusPolicy(Qt.StrongFocus)

        # Create a QSplitter to divide the space evenly
        splitter = QSplitter(Qt.Vertical)

        # Add the webView to the splitter (switched positions)
        self.webView = myWebView()
        splitter.addWidget(self.webView)

        # Add the tableWidget to the splitter (switched positions)
        self.tableWidget = QTableWidget()
        self.tableWidget.doubleClicked.connect(self.table_Click)

        # Set the size policy for the QWebEngineView and QTableWidget
        self.webView.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.tableWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        splitter.addWidget(self.tableWidget)

        main.layout().addWidget(splitter)

        controls_layout = QHBoxLayout()
        # Add the webView to the top section
        top_section_layout = QVBoxLayout()  # Create top_section_layout here
        top_section_layout.addWidget(self.webView)

        # Create a layout for the controls section
        controls_layout = QHBoxLayout()

        # Create and add the FROM box to the controls section
        from_label = QLabel('From: ', self)
        from_label.setFixedSize(50, 50)
        self.from_box = QComboBox()
        self.from_box.setEditable(True)
        self.from_box.completer().setCompletionMode(QCompleter.PopupCompletion)
        self.from_box.setInsertPolicy(QComboBox.NoInsert)
        controls_layout.addWidget(from_label)
        controls_layout.addWidget(self.from_box)

        # Create and add the TO box to the controls section
        to_label = QLabel('  To: ', self)
        to_label.setFixedSize(30, 30)
        self.to_box = QComboBox()
        self.to_box.setEditable(True)
        self.to_box.completer().setCompletionMode(QCompleter.PopupCompletion)
        self.to_box.setInsertPolicy(QComboBox.NoInsert)
        controls_layout.addWidget(to_label)
        controls_layout.addWidget(self.to_box)

        # Create and add the HOPS box to the controls section
        hops_label = QLabel('Hops: ', self)
        hops_label.setFixedSize(40, 40)
        self.hop_box = QComboBox()
        self.hop_box.addItems(['1', '2', '3'])
        self.hop_box.setCurrentIndex(2)
        controls_layout.addWidget(hops_label)
        controls_layout.addWidget(self.hop_box)

        # Create and add the GO button to the controls section
        self.go_button = QPushButton("Go!")
        self.go_button.clicked.connect(self.button_Go)
        controls_layout.addWidget(self.go_button)

        # Create and add the CLEAR button to the controls section
        self.clear_button = QPushButton("Clear")
        self.clear_button.clicked.connect(self.button_Clear)
        controls_layout.addWidget(self.clear_button)

        # Create and add the MAP TYPE box to the controls section
        self.maptype_box = QComboBox()
        self.maptype_box.addItems(self.webView.maptypes)
        self.maptype_box.currentIndexChanged.connect(self.webView.setMap)
        controls_layout.addWidget(self.maptype_box)

        # Add the controls section to the main layout
        main.layout().addLayout(top_section_layout)
        main.layout().addLayout(controls_layout)

        # Create and add the USER controls section
        user_controls_layout = QVBoxLayout()

        # Create and add the USER box to the USER controls section
        user_label = QLabel('User: ', self)
        user_label.setFixedSize(40, 20)
        self.user_box = QComboBox()
        self.user_box.setEditable(True)
        self.user_box.completer().setCompletionMode(QCompleter.PopupCompletion)
        self.user_box.setInsertPolicy(QComboBox.NoInsert)
        user_controls_layout.addWidget(user_label)
        user_controls_layout.addWidget(self.user_box)

        # Create and add the VEHICLE TYPE box to the controls section
        vehicle_type_label = QLabel('Transport: ', self)
        vehicle_type_label.setFixedSize(70, 60)
        self.vehicle_type_box = QComboBox()
        self.vehicle_type_box.addItems(['Bus', 'Walk'])
        controls_layout.addWidget(vehicle_type_label)
        controls_layout.addWidget(self.vehicle_type_box)

        # Create and add the ADD USER button to the USER controls section
        self.add_user_button = QPushButton("Add user")
        self.add_user_button.clicked.connect(self.add_user)
        user_controls_layout.addWidget(self.add_user_button)

        # Create and add the DELETE HISTORY button to the USER controls section
        self.delete_history_button = QPushButton("Delete history")
        self.delete_history_button.clicked.connect(self.delete_history)
        user_controls_layout.addWidget(self.delete_history_button)

        # Create and add the SHOW HISTORY button to the USER controls section
        self.show_history_button = QPushButton("Show history")
        self.show_history_button.clicked.connect(self.show_history)
        user_controls_layout.addWidget(self.show_history_button)

        # Add the USER controls section to the main layout
        main.layout().addLayout(user_controls_layout)

        self.connect_DB()

        self.startingpoint = True
        self.show()

    def show_users(self):
        self.cursor.execute(
            """SELECT username FROM p_users""")
        self.conn.commit()
        rows_name = self.cursor.fetchall()

        for row in rows_name:
            self.user_box.addItem(str(row[0]))

    def add_user(self):
        name, done1 = QtWidgets.QInputDialog.getText(self, 'Input Dialog', 'Enter your name:')

        if done1:
            self.cursor.execute(
                f"""INSERT INTO p_users(username) VALUES ('{name}')""")
            self.conn.commit()
            self.user_box.addItem(f"""{name}""")


    def connect_DB(self):
        self.conn = psycopg2.connect(database="projet", user="", host="", password="", port = "")
        self.cursor = self.conn.cursor()

        self.cursor.execute("""SELECT distinct name FROM nodes ORDER BY name""")
        self.conn.commit()
        rows = self.cursor.fetchall()

        for row in rows : 
            self.from_box.addItem(str(row[0]))
            self.to_box.addItem(str(row[0]))


    def table_Click(self):
        k = 0
        prev_lat = 0
        for col in self.rows[self.tableWidget.currentRow()] :
            if (k % 3) == 0:
                lst = col.split(',')
                lat = float(lst[0])
                lon = float(lst[1]) 

                if prev_lat != 0:
                    self.webView.addSegment( prev_lat, prev_lon, lat, lon )
                prev_lat = lat
                prev_lon = lon

                self.webView.addMarker( lat, lon )
            k = k + 1
        

    def button_Go(self):
        self.tableWidget.clearContents()

        _fromstation = str(self.from_box.currentText())
        _tostation = str(self.to_box.currentText())
        _hops = int(self.hop_box.currentText())

        self.rows = []

        selected_vehicle = self.vehicle_type_box.currentText()

        if selected_vehicle == "Bus":
            print("Le véhicule sélectionné est un bus.")
            if _hops >= 1: 
                self.cursor.execute(f"""
                SELECT
                    CONCAT(A.latitude, ',', A.longitude), A.name ,C.n_vehicles,CONCAT(B.latitude, ',', B.longitude),B.name
                FROM
                    nodes AS A
                JOIN
                    combined AS C ON A.stop_I = C.from_stop_I
                JOIN
                    nodes AS B ON B.stop_I = C.to_stop_I
                WHERE
                    A.name = $${_fromstation}$$ AND B.name = $${_tostation}$$;
                """)
                self.conn.commit()
                self.rows += self.cursor.fetchall()


            if _hops >= 2 : 
                self.cursor.execute(""f" SELECT distinct CONCAT(A.latitude, ',', A.longitude), A.name, C.n_vehicles,CONCAT(B.latitude, ',', B.longitude), B.name, D.n_vehicles,CONCAT(E.latitude, ',', E.longitude), E.name FROM nodes as A, nodes as B, nodes as E, combined as D, combined as C WHERE A.name = $${_fromstation}$$ AND E.name = $${_tostation}$$ AND A.stop_I = C.from_stop_I AND B.stop_I = C.to_stop_I AND B.stop_I = D.from_stop_I AND  E.stop_I = D.to_stop_I AND C.n_vehicles <> D.n_vehicles AND A.name <> B.name AND B.name <> E.name""")
                self.conn.commit()
                self.rows += self.cursor.fetchall()

            if _hops >= 3 : 
                self.cursor.execute(""f" SELECT distinct CONCAT(A.latitude, ',', A.longitude), A.name, E.n_vehicles,CONCAT(B.latitude, ',', B.longitude), B.name, F.n_vehicles,CONCAT(C.latitude, ',', C.longitude), C.name, G.n_vehicles,CONCAT(D.latitude, ',', D.longitude), D.name FROM nodes as A, nodes as B, nodes as C, nodes as D, combined as E, combined as F, combined as G  WHERE A.name = $${_fromstation}$$ AND D.name = $${_tostation}$$ AND A.stop_I = E.from_stop_I AND B.stop_I = E.to_stop_I AND B.stop_I = F.from_stop_I AND C.stop_I = F.to_stop_I AND C.stop_I = G.from_stop_I AND D.stop_I = G.to_stop_I AND E.n_vehicles <> F.n_vehicles AND F.n_vehicles = G.n_vehicles AND A.name <> B.name AND B.name <> C.name AND C.name <> D.name AND B.name <> D.name AND A.name <> D.name AND C.name <> A.name """)
                self.conn.commit()
                self.rows += self.cursor.fetchall()


        elif selected_vehicle == "Walk":
            if _hops >= 1: 
                self.cursor.execute(f"""
                SELECT
                    CONCAT(A.latitude, ',', A.longitude), A.name ,
                    C.n_vehicles,
                    CONCAT(B.latitude, ',', B.longitude), B.name
                    
                FROM
                    nodes AS A
                JOIN
                    walk AS C ON A.stop_I = C.from_stop_I
                JOIN
                    nodes AS B ON B.stop_I = C.to_stop_I
                WHERE
                    A.name = $${_fromstation}$$ AND B.name = $${_tostation}$$;
                """)
                self.conn.commit()
                self.rows += self.cursor.fetchall()


            if _hops >= 2 : 
                self.cursor.execute(""f" SELECT distinct CONCAT(A.latitude, ',', A.longitude), A.name, C.n_vehicles, CONCAT(B.latitude, ',', B.longitude), B.name, D.n_vehicles, CONCAT(E.latitude, ',', E.longitude), E.name FROM nodes as A, nodes as B, nodes as E, walk as D, walk as C WHERE A.name = $${_fromstation}$$ AND E.name = $${_tostation}$$ AND A.stop_I = C.from_stop_I AND B.stop_I = C.to_stop_I AND B.stop_I = D.from_stop_I AND  E.stop_I = D.to_stop_I AND C.n_vehicles <> D.n_vehicles AND A.name <> B.name AND B.name <> E.name""")
                self.conn.commit()
                self.rows += self.cursor.fetchall()

            if _hops >= 3 : 
                self.cursor.execute(""f" SELECT distinct CONCAT(A.latitude, ',', A.longitude), A.name, E.n_vehicles, CONCAT(B.latitude, ',', B.longitude), B.name, F.n_vehicles,CONCAT(C.latitude, ',', C.longitude),  C.name, G.n_vehicles,CONCAT(D.latitude, ',', D.longitude),  D.name FROM nodes as A, nodes as B, nodes as C, nodes as D, walk as E, combined as F, walk as G  WHERE A.name = $${_fromstation}$$ AND D.name = $${_tostation}$$ AND A.stop_I = E.from_stop_I AND B.stop_I = E.to_stop_I AND B.stop_I = F.from_stop_I AND C.stop_I = F.to_stop_I AND C.stop_I = G.from_stop_I AND D.stop_I = G.to_stop_I AND E.n_vehicles <> F.n_vehicles AND F.n_vehicles = G.n_vehicles AND A.name <> B.name AND B.name <> C.name AND C.name <> D.name AND B.name <> D.name AND A.name <> D.name AND C.name <> A.name """)
                self.conn.commit()
                self.rows += self.cursor.fetchall()
                print("Le véhicule sélectionné est la marche.")
            

        if len(self.rows) == 0 : 
            self.tableWidget.setRowCount(0)
            self.tableWidget.setColumnCount(0)
            return

        numrows = len(self.rows)
        numcols = len(self.rows[-1]) - math.floor(len(self.rows[-1]) / 3.0) - 1 
        self.tableWidget.setRowCount(numrows)
        self.tableWidget.setColumnCount(numcols)

        i = 0
        for row in self.rows : 
            j = 0
            k = 0 
            for col in row :
                if j % 3 == 0 : 
                    k = k + 1
                else : 
                    self.tableWidget.setItem(i, j-k, QTableWidgetItem(str(col)))
                j = j + 1
            i = i + 1

        header = self.tableWidget.horizontalHeader()
        j = 0
        while j < numcols : 
            header.setSectionResizeMode(j, QHeaderView.ResizeToContents)
            j = j+1
        
        self.update()	
       


    def button_Clear(self):
        # Clear the map
        self.webView.clearMap(self.maptype_box.currentIndex())
        self.startingpoint = True
        self.update()
        self.rows = []

        # Clear the table
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(0)


    def show_history(self):
        # clear map
        self.webView.clearMap(self.maptype_box.currentIndex())
        self.startingpoint = True
        self.update()


        _current_user = str(self.user_box.currentText())


        if _current_user != "anonymous" :

            self.cursor.execute(
            f"""SELECT id FROM p_users WHERE username = '{_current_user}'""")
            self.conn.commit()
            _current_user_id = self.cursor.fetchall()


            self.cursor.execute(
            f"""SELECT id, from_station, to_station FROM p_history WHERE id = {_current_user_id[0][0]}""")
            self.conn.commit()
            elements = self.cursor.fetchall()


            numrows = len(elements)
            self.tableWidget.setRowCount(numrows)
            self.tableWidget.setColumnCount(3)
            i = 0
            for row in elements : 
                print(row)
                j = 0
                for col in row :
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(col)))
                    j = j + 1
                i = i + 1

            self.update()	


    
    
    
    
    def delete_history(self):

        _current_user = str(self.user_box.currentText())
        self.cursor.execute(
        f"""SELECT id FROM p_users WHERE username = '{_current_user}'""")
        self.conn.commit()
        _current_user_id = self.cursor.fetchall()

        self.cursor.execute(
        f"""delete from p_history where id = '{_current_user_id[0][0]}'""")
        self.conn.commit()
        return



    def mouseClick(self, lat, lng):
        self.webView.addPointMarker(lat, lng)

        print(f"Clicked on: latitude {lat}, longitude {lng}")
        self.cursor.execute(""f" WITH mytable (distance, name) AS (SELECT ( ABS(latitude-{lat}) + ABS(longitude-{lng}) ), name FROM nodes) SELECT A.name FROM mytable as A WHERE A.distance <=  (SELECT min(B.distance) FROM mytable as B)  """)
        self.conn.commit()
        rows = self.cursor.fetchall()
        #print('Closest STATION is: ', rows[0][0])
        if self.startingpoint :
            self.from_box.setCurrentIndex(self.from_box.findText(rows[0][0], Qt.MatchFixedString))
        else :
            self.to_box.setCurrentIndex(self.to_box.findText(rows[0][0], Qt.MatchFixedString))
        self.startingpoint = not self.startingpoint



class myWebView (QWebEngineView):
    def __init__(self):
        super().__init__()

        self.maptypes = ["OpenStreetMap", "Stamen Terrain", "stamentoner", "cartodbpositron"]
        self.setMap(0)


    def add_customjs(self, map_object):
        my_js = f"""{map_object.get_name()}.on("click",
                 function (e) {{
                    var data = `{{"coordinates": ${{JSON.stringify(e.latlng)}}}}`;
                    console.log(data)}}); """
        e = Element(my_js)
        html = map_object.get_root()
        html.script.get_root().render()
        html.script._children[e.get_name()] = e

        return map_object


    def handleClick(self, msg):
        data = json.loads(msg)
        lat = data['coordinates']['lat']
        lng = data['coordinates']['lng']


        window.mouseClick(lat, lng)


    def addSegment(self, lat1, lng1, lat2, lng2):
        js = Template(
        """
        L.polyline(
            [ [{{latitude1}}, {{longitude1}}], [{{latitude2}}, {{longitude2}}] ], {
                "color": "red",
                "opacity": 1.0,
                "weight": 4,
                "line_cap": "butt"
            }
        ).addTo({{map}});
        """
        ).render(map=self.mymap.get_name(), latitude1=lat1, longitude1=lng1, latitude2=lat2, longitude2=lng2 )

        self.page().runJavaScript(js)


    def addMarker(self, lat, lng):
        js = Template(
        """
        L.marker([{{latitude}}, {{longitude}}] ).addTo({{map}});
        L.circleMarker(
            [{{latitude}}, {{longitude}}], {
                "bubblingMouseEvents": true,
                "color": "#3388ff",
                "popup": "hello",
                "dashArray": null,
                "dashOffset": null,
                "fill": false,
                "fillColor": "#3388ff",
                "fillOpacity": 0.2,
                "fillRule": "evenodd",
                "lineCap": "round",
                "lineJoin": "round",
                "opacity": 1.0,
                "radius": 2,
                "stroke": true,
                "weight": 5
            }
        ).addTo({{map}});
        """
        ).render(map=self.mymap.get_name(), latitude=lat, longitude=lng)
        self.page().runJavaScript(js)


    def addPointMarker(self, lat, lng):
        js = Template(
        """
        L.circleMarker(
            [{{latitude}}, {{longitude}}], {
                "bubblingMouseEvents": true,
                "color": 'green',
                "popup": "hello",
                "dashArray": null,
                "dashOffset": null,
                "fill": false,
                "fillColor": 'green',
                "fillOpacity": 0.2,
                "fillRule": "evenodd",
                "lineCap": "round",
                "lineJoin": "round",
                "opacity": 1.0,
                "radius": 2,
                "stroke": true,
                "weight": 5
            }
        ).addTo({{map}});
        """
        ).render(map=self.mymap.get_name(), latitude=lat, longitude=lng)
        self.page().runJavaScript(js)


    def setMap (self, i):
        self.mymap = folium.Map(location=[62.89238, 27.67703], tiles=self.maptypes[i], zoom_start=12, prefer_canvas=True, width='100%', height='100%')

        self.mymap = self.add_customjs(self.mymap)

        page = WebEnginePage(self)
        self.setPage(page)

        data = io.BytesIO()
        self.mymap.save(data, close_file=False)

        self.setHtml(data.getvalue().decode())

    def clearMap(self, index):
        self.setMap(index)



class WebEnginePage(QWebEnginePage):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

    def javaScriptConsoleMessage(self, level, msg, line, sourceID):
        #print(msg)
        if 'coordinates' in msg:
            self.parent.handleClick(msg)


       
			
if __name__ == '__main__':
    sys.argv.append('--no-sandbox')
    app = QApplication(sys.argv) 
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
