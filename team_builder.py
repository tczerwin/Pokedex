# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PokemonDatabase import TYPE_COLORS, DEFAULT_TYPE_COLOR

class Ui_TeamBuilder(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("TeamBuilder")
        MainWindow.resize(641, 611)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Background
        self.background = QtWidgets.QLabel(self.centralwidget)
        self.background.setGeometry(QtCore.QRect(0, 0, 641, 611))
        self.background.setText("")
        self.background.setObjectName("background")

        # Title
        self.title = QtWidgets.QLabel(self.centralwidget)
        self.title.setGeometry(QtCore.QRect(20, 10, 600, 40))
        self.title.setObjectName("title")
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.title.setStyleSheet("color: black; font-weight: bold; font-size: 20pt;")
        self.title.setText("Team Builder")

        # Team name input
        self.team_name_label = QtWidgets.QLabel(self.centralwidget)
        self.team_name_label.setGeometry(QtCore.QRect(20, 55, 100, 24))
        self.team_name_label.setText("Team Name:")
        self.team_name_label.setStyleSheet("color: black; font-weight: bold; font-size: 11pt;")

        self.team_name_input = QtWidgets.QLineEdit(self.centralwidget)
        self.team_name_input.setGeometry(QtCore.QRect(130, 55, 300, 28))
        self.team_name_input.setStyleSheet(
            "QLineEdit { background-color: white; color: black; border-radius: 6px; "
            "padding: 2px 8px; font-size: 11pt; } "
            "QLineEdit::placeholder { color: gray; }"
        )
        self.team_name_input.setPlaceholderText("Enter team name")

        # Export button
        self.export_btn = QtWidgets.QPushButton(self.centralwidget)
        self.export_btn.setGeometry(QtCore.QRect(445, 55, 80, 28))
        self.export_btn.setText("Export PDF")
        self.export_btn.setObjectName("export_btn")
        self.export_btn.setStyleSheet(
            "QPushButton { color: black; font-size: 10pt; background-color: rgba(255, 255, 255, 220); "
            "border: 1px solid #999999; border-radius: 4px; box-shadow: 0 12px 24px rgba(0, 0, 0, 0.6); } "
            "QPushButton:hover { background-color: rgba(255, 255, 255, 240); box-shadow: 0 16px 32px rgba(0, 0, 0, 0.7); } "
            "QPushButton:pressed { background-color: rgba(230, 230, 230, 220); box-shadow: inset 0 4px 8px rgba(0, 0, 0, 0.4), 0 2px 4px rgba(0, 0, 0, 0.3); }"
        )

        # Pokemon slots (6 slots)
        self.pokemon_slots = []
        slot_positions = [100, 170, 240, 310, 380, 450]

        for i in range(6):
            # Slot frame
            slot_frame = QtWidgets.QFrame(self.centralwidget)
            slot_frame.setGeometry(QtCore.QRect(20, slot_positions[i], 600, 60))
            slot_frame.setStyleSheet(
                "QFrame { background-color: rgba(255, 255, 255, 200); "
                "border-radius: 8px; border: 2px solid #999999; }"
            )
            slot_frame.setObjectName(f"slot_frame_{i}")

            # Slot number
            slot_num = QtWidgets.QLabel(slot_frame)
            slot_num.setGeometry(QtCore.QRect(10, 10, 30, 40))
            slot_num.setText(f"{i+1}.")
            slot_num.setStyleSheet("color: black; font-weight: bold; font-size: 14pt;")
            slot_num.setAlignment(QtCore.Qt.AlignCenter)

            # Pokemon sprite button
            sprite_btn = QtWidgets.QPushButton(slot_frame)
            sprite_btn.setGeometry(QtCore.QRect(50, 8, 44, 44))
            sprite_btn.setObjectName(f"sprite_{i}")
            sprite_btn.setStyleSheet("border: none; background-color: transparent;")
            sprite_btn.setFlat(True)
            setattr(self, f"sprite_{i}", sprite_btn)

            # Pokemon name button (search)
            name_btn = QtWidgets.QPushButton(slot_frame)
            name_btn.setGeometry(QtCore.QRect(100, 8, 150, 44))
            name_btn.setObjectName(f"pokemon_name_{i}")
            name_btn.setText("Click to add")
            name_btn.setStyleSheet(
                "QPushButton { color: black; font-weight: bold; font-size: 11pt; "
                "background-color: white; border: 1px solid #999999; border-radius: 4px; box-shadow: 0 12px 24px rgba(0, 0, 0, 0.6); } "
                "QPushButton:hover { background-color: #f0f0f0; box-shadow: 0 16px 32px rgba(0, 0, 0, 0.7); } "
                "QPushButton:pressed { color: black; background-color: rgba(230, 230, 230, 220); box-shadow: inset 0 4px 8px rgba(0, 0, 0, 0.4), 0 2px 4px rgba(0, 0, 0, 0.3); }"
            )
            name_btn.setFlat(False)
            setattr(self, f"pokemon_name_{i}", name_btn)

            # Level slider
            level_label = QtWidgets.QLabel(slot_frame)
            level_label.setGeometry(QtCore.QRect(260, 10, 50, 20))
            level_label.setText("Lvl:")
            level_label.setStyleSheet("color: black; font-weight: bold;")

            level_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal, slot_frame)
            level_slider.setGeometry(QtCore.QRect(300, 12, 80, 20))
            level_slider.setMinimum(1)
            level_slider.setMaximum(100)
            level_slider.setValue(50)
            level_slider.setObjectName(f"level_slider_{i}")
            setattr(self, f"level_slider_{i}", level_slider)

            level_value = QtWidgets.QLabel(slot_frame)
            level_value.setGeometry(QtCore.QRect(385, 10, 30, 20))
            level_value.setText("50")
            level_value.setStyleSheet("color: black; font-weight: bold;")
            level_value.setAlignment(QtCore.Qt.AlignCenter)
            setattr(self, f"level_value_{i}", level_value)

            level_slider.valueChanged.connect(
                lambda val, idx=i: self._update_level_display(idx, val)
            )

            # Remove button
            remove_btn = QtWidgets.QPushButton(slot_frame)
            remove_btn.setGeometry(QtCore.QRect(555, 18, 30, 28))
            remove_btn.setText("✕")
            remove_btn.setObjectName(f"remove_{i}")
            remove_btn.setStyleSheet(
                "QPushButton { color: red; font-weight: bold; font-size: 12pt; "
                "background-color: white; border: 1px solid #999999; border-radius: 4px; box-shadow: 0 12px 24px rgba(0, 0, 0, 0.6); } "
                "QPushButton:hover { background-color: #ffcccc; box-shadow: 0 16px 32px rgba(0, 0, 0, 0.7); } "
                "QPushButton:pressed { background-color: rgba(230, 230, 230, 220); box-shadow: inset 0 4px 8px rgba(0, 0, 0, 0.4), 0 2px 4px rgba(0, 0, 0, 0.3); }"
            )
            setattr(self, f"remove_{i}", remove_btn)

            self.pokemon_slots.append({
                'frame': slot_frame,
                'sprite': sprite_btn,
                'name_btn': name_btn,
                'level_slider': level_slider,
                'level_value': level_value,
                'remove_btn': remove_btn
            })

        # Save/Load/Delete buttons
        button_style_team = "QPushButton { color: black; font-size: 10pt; background-color: rgba(255, 255, 255, 220); border: 2px solid #333333; border-radius: 6px; box-shadow: 0 12px 24px rgba(0, 0, 0, 0.6); } QPushButton:hover { background-color: rgba(255, 255, 255, 240); box-shadow: 0 16px 32px rgba(0, 0, 0, 0.7); } QPushButton:pressed { background-color: rgba(230, 230, 230, 220); box-shadow: inset 0 4px 8px rgba(0, 0, 0, 0.4), 0 2px 4px rgba(0, 0, 0, 0.3); }"

        self.save_btn = QtWidgets.QPushButton(self.centralwidget)
        self.save_btn.setGeometry(QtCore.QRect(20, 520, 100, 30))
        self.save_btn.setText("Save Team")
        self.save_btn.setObjectName("save_btn")
        self.save_btn.setStyleSheet(button_style_team)

        self.load_btn = QtWidgets.QPushButton(self.centralwidget)
        self.load_btn.setGeometry(QtCore.QRect(130, 520, 100, 30))
        self.load_btn.setText("Load Team")
        self.load_btn.setObjectName("load_btn")
        self.load_btn.setStyleSheet(button_style_team)

        self.coverage_btn = QtWidgets.QPushButton(self.centralwidget)
        self.coverage_btn.setGeometry(QtCore.QRect(240, 520, 120, 30))
        self.coverage_btn.setText("Type Coverage")
        self.coverage_btn.setObjectName("coverage_btn")
        self.coverage_btn.setStyleSheet(button_style_team)

        # Navigation buttons
        button_style = "QPushButton { color: black; font-size: 10pt; background-color: rgba(255, 255, 255, 220); border: 2px solid #333333; border-radius: 6px; box-shadow: 0 12px 24px rgba(0, 0, 0, 0.6); } QPushButton:hover { background-color: rgba(255, 255, 255, 240); box-shadow: 0 16px 32px rgba(0, 0, 0, 0.7); } QPushButton:pressed { background-color: rgba(230, 230, 230, 220); box-shadow: inset 0 4px 8px rgba(0, 0, 0, 0.4), 0 2px 4px rgba(0, 0, 0, 0.3); }"

        self.lookup_b1 = QtWidgets.QPushButton(self.centralwidget)
        self.lookup_b1.setGeometry(QtCore.QRect(20, 560, 100, 30))
        self.lookup_b1.setText("Look Up")
        self.lookup_b1.setObjectName("lookup_b1")
        self.lookup_b1.setStyleSheet(button_style)

        self.battle_b1 = QtWidgets.QPushButton(self.centralwidget)
        self.battle_b1.setGeometry(QtCore.QRect(130, 560, 100, 30))
        self.battle_b1.setText("Battle!")
        self.battle_b1.setObjectName("battle_b1")
        self.battle_b1.setStyleSheet(button_style)

        self.raid_b1 = QtWidgets.QPushButton(self.centralwidget)
        self.raid_b1.setGeometry(QtCore.QRect(240, 560, 120, 30))
        self.raid_b1.setText("Raid Counters")
        self.raid_b1.setObjectName("raid_b1")
        self.raid_b1.setStyleSheet(button_style)

        self.top_b1 = QtWidgets.QPushButton(self.centralwidget)
        self.top_b1.setGeometry(QtCore.QRect(370, 560, 100, 30))
        self.top_b1.setText("Top 10")
        self.top_b1.setObjectName("top_b1")
        self.top_b1.setStyleSheet(button_style)

        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def _update_level_display(self, slot_idx, value):
        """Update the level display label."""
        getattr(self, f"level_value_{slot_idx}").setText(str(value))

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Team Builder"))
