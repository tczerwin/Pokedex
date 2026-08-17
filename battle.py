# -*- coding: utf-8 -*-

"""
Battle page for the Pokedex app.

Allows users to select two Pokemon and see who would win in a battle.
Battle logic: type advantage + stats comparison.
"""

from PyQt5 import QtCore, QtGui, QtWidgets

from PokemonDatabase import TYPE_COLORS, DEFAULT_TYPE_COLOR


class Ui_Battle(object):
    def setupUi(self, Battle):
        Battle.setObjectName("Battle")
        Battle.resize(651, 720)
        self.centralwidget = QtWidgets.QWidget(Battle)
        self.centralwidget.setObjectName("centralwidget")

        # Background
        self.background = QtWidgets.QLabel(self.centralwidget)
        self.background.setGeometry(QtCore.QRect(0, 0, 651, 720))
        self.background.setText("")
        self.background.setObjectName("background")

        # Header
        self.header = QtWidgets.QLabel(self.centralwidget)
        self.header.setGeometry(QtCore.QRect(50, 10, 550, 40))
        self.header.setObjectName("header")
        self.header.setAlignment(QtCore.Qt.AlignCenter)
        self.header.setStyleSheet("color: black; font-weight: bold; font-size: 24pt;")

        # Left Pokemon Section
        self.left_label = QtWidgets.QLabel(self.centralwidget)
        self.left_label.setGeometry(QtCore.QRect(50, 60, 250, 24))
        self.left_label.setObjectName("left_label")
        self.left_label.setStyleSheet("color: black; font-weight: bold; font-size: 12pt;")
        self.left_label.setText("Pokémon 1:")

        self.left_input = QtWidgets.QLineEdit(self.centralwidget)
        self.left_input.setGeometry(QtCore.QRect(50, 88, 250, 32))
        self.left_input.setObjectName("left_input")
        self.left_input.setStyleSheet(
            "background-color: white;"
            "color: black;"
            "border-radius: 6px;"
            "padding: 2px 8px;"
            "font-size: 11pt;"
        )
        self.left_input.setPlaceholderText("Enter Pokémon name")

        # Right Pokemon Section
        self.right_label = QtWidgets.QLabel(self.centralwidget)
        self.right_label.setGeometry(QtCore.QRect(420, 60, 250, 24))
        self.right_label.setObjectName("right_label")
        self.right_label.setStyleSheet("color: black; font-weight: bold; font-size: 12pt;")
        self.right_label.setText("Pokémon 2:")

        self.right_input = QtWidgets.QLineEdit(self.centralwidget)
        self.right_input.setGeometry(QtCore.QRect(420, 88, 250, 32))
        self.right_input.setObjectName("right_input")
        self.right_input.setStyleSheet(
            "background-color: white;"
            "color: black;"
            "border-radius: 6px;"
            "padding: 2px 8px;"
            "font-size: 11pt;"
        )
        self.right_input.setPlaceholderText("Enter Pokémon name")

        # Randomize button
        self.clear_button = QtWidgets.QPushButton(self.centralwidget)
        self.clear_button.setGeometry(QtCore.QRect(250, 95, 150, 35))
        self.clear_button.setObjectName("clear_button")
        self.clear_button.setText("Randomize")
        self.clear_button.setStyleSheet("QPushButton { color: black; font-size: 12pt; font-weight: bold; border: 2px solid #333333; border-radius: 6px; background-color: rgba(255, 255, 255, 220); box-shadow: 0 12px 24px rgba(0, 0, 0, 0.6); } QPushButton:hover { background-color: rgba(255, 255, 255, 240); box-shadow: 0 16px 32px rgba(0, 0, 0, 0.7); } QPushButton:pressed { background-color: rgba(230, 230, 230, 220); box-shadow: inset 0 4px 8px rgba(0, 0, 0, 0.4), 0 2px 4px rgba(0, 0, 0, 0.3); }")

        # Battle button
        self.battle_button = QtWidgets.QPushButton(self.centralwidget)
        self.battle_button.setGeometry(QtCore.QRect(250, 135, 150, 35))
        self.battle_button.setObjectName("battle_button")
        self.battle_button.setText("BATTLE!")
        self.battle_button.setStyleSheet("color: black; font-size: 12pt; font-weight: bold; border: 2px solid #333333; border-radius: 6px; background-color: rgba(255, 255, 255, 220);")

        # Left pokemon card
        self.left_card = QtWidgets.QFrame(self.centralwidget)
        self.left_card.setGeometry(QtCore.QRect(40, 190, 280, 380))
        self.left_card.setObjectName("left_card")
        self.left_card.setStyleSheet(
            "QFrame#left_card {"
            "background-color: rgba(255, 255, 255, 235);"
            "border: 5px solid #777777;"
            "border-radius: 24px;"
            "}"
        )

        # Left pokemon name
        self.left_name = QtWidgets.QLabel(self.centralwidget)
        self.left_name.setGeometry(QtCore.QRect(60, 210, 240, 35))
        self.left_name.setObjectName("left_name")
        self.left_name.setStyleSheet("color: #222222; font-weight: bold; font-size: 18pt;")
        self.left_name.setText("Pokemon 1")

        # Left pokemon sprite
        self.left_sprite_frame = QtWidgets.QFrame(self.centralwidget)
        self.left_sprite_frame.setGeometry(QtCore.QRect(95, 260, 150, 120))
        self.left_sprite_frame.setObjectName("left_sprite_frame")
        self.left_sprite_frame.setStyleSheet(
            "QFrame#left_sprite_frame {"
            "background-color: white;"
            "border: 2px solid #dddddd;"
            "border-radius: 16px;"
            "}"
        )

        self.left_sprite = QtWidgets.QPushButton(self.centralwidget)
        self.left_sprite.setGeometry(QtCore.QRect(102, 267, 136, 106))
        self.left_sprite.setObjectName("left_sprite")
        self.left_sprite.setStyleSheet("border: none; background-color: transparent;")
        self.left_sprite.setFlat(True)

        # Left microphone button for cry
        self.left_cry_btn = QtWidgets.QPushButton(self.centralwidget)
        self.left_cry_btn.setGeometry(QtCore.QRect(295, 200, 24, 24))
        self.left_cry_btn.setObjectName("left_cry_btn")
        self.left_cry_btn.setText("🔊")
        self.left_cry_btn.setStyleSheet("border: none; background-color: transparent; font-size: 14pt;")
        self.left_cry_btn.setFlat(True)

        # Left type badges
        self.left_type = QtWidgets.QLabel(self.centralwidget)
        self.left_type.setGeometry(QtCore.QRect(60, 390, 110, 30))
        self.left_type.setObjectName("left_type")
        self.left_type.setAlignment(QtCore.Qt.AlignCenter)
        self.left_type.setStyleSheet("font-size: 10pt; font-weight: bold; border-radius: 4px; padding: 2px;")

        self.left_type_2 = QtWidgets.QLabel(self.centralwidget)
        self.left_type_2.setGeometry(QtCore.QRect(175, 390, 110, 30))
        self.left_type_2.setObjectName("left_type_2")
        self.left_type_2.setAlignment(QtCore.Qt.AlignCenter)
        self.left_type_2.setStyleSheet("font-size: 10pt; font-weight: bold; border-radius: 4px; padding: 2px;")

        # Left individual stats
        self.left_hp = QtWidgets.QLabel(self.centralwidget)
        self.left_hp.setGeometry(QtCore.QRect(60, 428, 240, 20))
        self.left_hp.setObjectName("left_hp")
        self.left_hp.setStyleSheet("color: #333333; font-size: 10pt;")
        self.left_hp.setText("HP: --")

        self.left_atk = QtWidgets.QLabel(self.centralwidget)
        self.left_atk.setGeometry(QtCore.QRect(60, 448, 240, 20))
        self.left_atk.setObjectName("left_atk")
        self.left_atk.setStyleSheet("color: #333333; font-size: 10pt;")
        self.left_atk.setText("Attack: --")

        self.left_def = QtWidgets.QLabel(self.centralwidget)
        self.left_def.setGeometry(QtCore.QRect(60, 468, 240, 20))
        self.left_def.setObjectName("left_def")
        self.left_def.setStyleSheet("color: #333333; font-size: 10pt;")
        self.left_def.setText("Defense: --")

        self.left_spa = QtWidgets.QLabel(self.centralwidget)
        self.left_spa.setGeometry(QtCore.QRect(60, 488, 240, 20))
        self.left_spa.setObjectName("left_spa")
        self.left_spa.setStyleSheet("color: #333333; font-size: 10pt;")
        self.left_spa.setText("Sp. Attack: --")

        self.left_spd = QtWidgets.QLabel(self.centralwidget)
        self.left_spd.setGeometry(QtCore.QRect(60, 508, 240, 20))
        self.left_spd.setObjectName("left_spd")
        self.left_spd.setStyleSheet("color: #333333; font-size: 10pt;")
        self.left_spd.setText("Sp. Defense: --")

        self.left_stats = QtWidgets.QLabel(self.centralwidget)
        self.left_stats.setGeometry(QtCore.QRect(60, 528, 240, 20))
        self.left_stats.setObjectName("left_stats")
        self.left_stats.setAlignment(QtCore.Qt.AlignCenter)
        self.left_stats.setStyleSheet("color: #333333; font-size: 11pt; font-weight: bold;")
        self.left_stats.setText("Total: --")

        # Right pokemon card
        self.right_card = QtWidgets.QFrame(self.centralwidget)
        self.right_card.setGeometry(QtCore.QRect(330, 190, 280, 380))
        self.right_card.setObjectName("right_card")
        self.right_card.setStyleSheet(
            "QFrame#right_card {"
            "background-color: rgba(255, 255, 255, 235);"
            "border: 5px solid #777777;"
            "border-radius: 24px;"
            "}"
        )

        # Right pokemon name
        self.right_name = QtWidgets.QLabel(self.centralwidget)
        self.right_name.setGeometry(QtCore.QRect(350, 210, 240, 35))
        self.right_name.setObjectName("right_name")
        self.right_name.setStyleSheet("color: #222222; font-weight: bold; font-size: 18pt;")
        self.right_name.setText("Pokemon 2")

        # Right pokemon sprite
        self.right_sprite_frame = QtWidgets.QFrame(self.centralwidget)
        self.right_sprite_frame.setGeometry(QtCore.QRect(385, 260, 150, 120))
        self.right_sprite_frame.setObjectName("right_sprite_frame")
        self.right_sprite_frame.setStyleSheet(
            "QFrame#right_sprite_frame {"
            "background-color: white;"
            "border: 2px solid #dddddd;"
            "border-radius: 16px;"
            "}"
        )

        self.right_sprite = QtWidgets.QPushButton(self.centralwidget)
        self.right_sprite.setGeometry(QtCore.QRect(392, 267, 136, 106))
        self.right_sprite.setObjectName("right_sprite")
        self.right_sprite.setStyleSheet("border: none; background-color: transparent;")
        self.right_sprite.setFlat(True)

        # Right microphone button for cry
        self.right_cry_btn = QtWidgets.QPushButton(self.centralwidget)
        self.right_cry_btn.setGeometry(QtCore.QRect(585, 200, 24, 24))
        self.right_cry_btn.setObjectName("right_cry_btn")
        self.right_cry_btn.setText("🔊")
        self.right_cry_btn.setStyleSheet("border: none; background-color: transparent; font-size: 14pt;")
        self.right_cry_btn.setFlat(True)

        # Right type badges
        self.right_type = QtWidgets.QLabel(self.centralwidget)
        self.right_type.setGeometry(QtCore.QRect(350, 390, 110, 30))
        self.right_type.setObjectName("right_type")
        self.right_type.setAlignment(QtCore.Qt.AlignCenter)
        self.right_type.setStyleSheet("font-size: 10pt; font-weight: bold; border-radius: 4px; padding: 2px;")

        self.right_type_2 = QtWidgets.QLabel(self.centralwidget)
        self.right_type_2.setGeometry(QtCore.QRect(465, 390, 110, 30))
        self.right_type_2.setObjectName("right_type_2")
        self.right_type_2.setAlignment(QtCore.Qt.AlignCenter)
        self.right_type_2.setStyleSheet("font-size: 10pt; font-weight: bold; border-radius: 4px; padding: 2px;")

        # Right individual stats
        self.right_hp = QtWidgets.QLabel(self.centralwidget)
        self.right_hp.setGeometry(QtCore.QRect(350, 428, 240, 20))
        self.right_hp.setObjectName("right_hp")
        self.right_hp.setStyleSheet("color: #333333; font-size: 10pt;")
        self.right_hp.setText("HP: --")

        self.right_atk = QtWidgets.QLabel(self.centralwidget)
        self.right_atk.setGeometry(QtCore.QRect(350, 448, 240, 20))
        self.right_atk.setObjectName("right_atk")
        self.right_atk.setStyleSheet("color: #333333; font-size: 10pt;")
        self.right_atk.setText("Attack: --")

        self.right_def = QtWidgets.QLabel(self.centralwidget)
        self.right_def.setGeometry(QtCore.QRect(350, 468, 240, 20))
        self.right_def.setObjectName("right_def")
        self.right_def.setStyleSheet("color: #333333; font-size: 10pt;")
        self.right_def.setText("Defense: --")

        self.right_spa = QtWidgets.QLabel(self.centralwidget)
        self.right_spa.setGeometry(QtCore.QRect(350, 488, 240, 20))
        self.right_spa.setObjectName("right_spa")
        self.right_spa.setStyleSheet("color: #333333; font-size: 10pt;")
        self.right_spa.setText("Sp. Attack: --")

        self.right_spd = QtWidgets.QLabel(self.centralwidget)
        self.right_spd.setGeometry(QtCore.QRect(350, 508, 240, 20))
        self.right_spd.setObjectName("right_spd")
        self.right_spd.setStyleSheet("color: #333333; font-size: 10pt;")
        self.right_spd.setText("Sp. Defense: --")

        self.right_stats = QtWidgets.QLabel(self.centralwidget)
        self.right_stats.setGeometry(QtCore.QRect(350, 528, 240, 20))
        self.right_stats.setObjectName("right_stats")
        self.right_stats.setAlignment(QtCore.Qt.AlignCenter)
        self.right_stats.setStyleSheet("color: #333333; font-size: 11pt; font-weight: bold;")
        self.right_stats.setText("Total: --")

        # Winner announcement
        self.winner_label = QtWidgets.QLabel(self.centralwidget)
        self.winner_label.setGeometry(QtCore.QRect(50, 565, 550, 50))
        self.winner_label.setObjectName("winner_label")
        self.winner_label.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        self.winner_label.setStyleSheet("color: #333333; font-weight: bold; font-size: 20pt;")
        self.winner_label.setText("")

        # Navigation buttons
        self.lookup_b1 = QtWidgets.QPushButton(self.centralwidget)
        self.lookup_b1.setGeometry(QtCore.QRect(20, 620, 140, 30))
        self.lookup_b1.setObjectName("lookup_b1")
        self.lookup_b1.setText("Look Up")

        self.team_b1 = QtWidgets.QPushButton(self.centralwidget)
        self.team_b1.setGeometry(QtCore.QRect(172, 620, 140, 30))
        self.team_b1.setObjectName("team_b1")
        self.team_b1.setText("My Team")

        self.raid_b1 = QtWidgets.QPushButton(self.centralwidget)
        self.raid_b1.setGeometry(QtCore.QRect(324, 620, 140, 30))
        self.raid_b1.setObjectName("raid_b1")
        self.raid_b1.setText("Raid Counters")

        self.top_b1 = QtWidgets.QPushButton(self.centralwidget)
        self.top_b1.setGeometry(QtCore.QRect(476, 620, 140, 30))
        self.top_b1.setObjectName("top_b1")
        self.top_b1.setText("Top 10")

        self.type_chart_b1 = QtWidgets.QPushButton(self.centralwidget)
        self.type_chart_b1.setGeometry(QtCore.QRect(620, 10, 30, 30))
        self.type_chart_b1.setObjectName("type_chart_b1")
        self.type_chart_b1.setText("📊")

        Battle.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Battle)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 651, 21))
        self.menubar.setObjectName("menubar")
        Battle.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Battle)
        self.statusbar.setObjectName("statusbar")
        Battle.setStatusBar(self.statusbar)

        self.retranslateUi(Battle)
        QtCore.QMetaObject.connectSlotsByName(Battle)

    def retranslateUi(self, Battle):
        _translate = QtCore.QCoreApplication.translate
        Battle.setWindowTitle(_translate("Battle", "Battle"))
        self.header.setText(_translate("Battle", "Pokémon Battle Arena"))

        set_background(self, "poke_background.jpg")


def scale_pixmap_cover(pixmap, target_width, target_height):
    """Scale a pixmap to completely fill a target box with no distortion."""
    if pixmap.isNull() or target_width <= 0 or target_height <= 0:
        return pixmap

    scaled = pixmap.scaled(
        target_width,
        target_height,
        QtCore.Qt.KeepAspectRatioByExpanding,
        QtCore.Qt.SmoothTransformation
    )

    x = max(0, (scaled.width() - target_width) // 2)
    y = max(0, (scaled.height() - target_height) // 2)

    return scaled.copy(x, y, target_width, target_height)


def set_background(ui, name_of_background):
    widget_width = 651
    widget_height = 720

    pixmap = QtGui.QPixmap("img/" + name_of_background)
    pixmap = scale_pixmap_cover(pixmap, widget_width, widget_height)

    ui.background.setGeometry(0, 0, widget_width, widget_height)
    ui.background.setPixmap(pixmap)
    ui.background.lower()

    ui.background_overlay = QtWidgets.QLabel(ui.centralwidget)
    ui.background_overlay.setGeometry(0, 0, widget_width, widget_height)
    ui.background_overlay.setStyleSheet("background-color: rgba(255, 255, 255, 150);")
    ui.background_overlay.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
    ui.background_overlay.raise_()

    # Raise all elements above background
    ui.header.raise_()
    ui.left_label.raise_()
    ui.left_input.raise_()
    ui.right_label.raise_()
    ui.right_input.raise_()
    ui.battle_button.raise_()
    ui.left_card.raise_()
    ui.left_name.raise_()
    ui.left_sprite_frame.raise_()
    ui.left_sprite.raise_()
    ui.left_cry_btn.raise_()
    ui.left_type.raise_()
    ui.left_type_2.raise_()
    ui.left_hp.raise_()
    ui.left_atk.raise_()
    ui.left_def.raise_()
    ui.left_spa.raise_()
    ui.left_spd.raise_()
    ui.left_stats.raise_()
    ui.right_card.raise_()
    ui.right_name.raise_()
    ui.right_sprite_frame.raise_()
    ui.right_sprite.raise_()
    ui.right_cry_btn.raise_()
    ui.right_type.raise_()
    ui.right_type_2.raise_()
    ui.right_hp.raise_()
    ui.right_atk.raise_()
    ui.right_def.raise_()
    ui.right_spa.raise_()
    ui.right_spd.raise_()
    ui.right_stats.raise_()
    ui.winner_label.raise_()
    ui.lookup_b1.raise_()
    ui.raid_b1.raise_()
    ui.top_b1.raise_()
    ui.team_b1.raise_()
    ui.type_chart_b1.raise_()
    ui.clear_button.raise_()
    ui.battle_button.raise_()

    # Style buttons
    button_style = "QPushButton { color: black; font-size: 10pt; background-color: rgba(255, 255, 255, 220); border: 2px solid #333333; border-radius: 6px; box-shadow: 0 12px 24px rgba(0, 0, 0, 0.6); } QPushButton:hover { background-color: rgba(255, 255, 255, 240); box-shadow: 0 16px 32px rgba(0, 0, 0, 0.7); } QPushButton:pressed { background-color: rgba(230, 230, 230, 220); box-shadow: inset 0 4px 8px rgba(0, 0, 0, 0.4), 0 2px 4px rgba(0, 0, 0, 0.3); }"
    ui.lookup_b1.setStyleSheet(button_style)
    ui.raid_b1.setStyleSheet(button_style)
    ui.top_b1.setStyleSheet(button_style)
    ui.team_b1.setStyleSheet(button_style)
    ui.type_chart_b1.setStyleSheet("QPushButton { color: black; font-size: 14pt; background-color: rgba(255, 255, 255, 220); border: 2px solid #333333; border-radius: 6px; box-shadow: 0 12px 24px rgba(0, 0, 0, 0.6); } QPushButton:hover { background-color: rgba(255, 255, 255, 240); box-shadow: 0 16px 32px rgba(0, 0, 0, 0.7); } QPushButton:pressed { background-color: rgba(230, 230, 230, 220); box-shadow: inset 0 4px 8px rgba(0, 0, 0, 0.4), 0 2px 4px rgba(0, 0, 0, 0.3); }")
    ui.battle_button.setStyleSheet("QPushButton { color: black; font-size: 12pt; font-weight: bold; border: 2px solid #333333; border-radius: 10px; background-color: rgba(255, 255, 255, 220); box-shadow: 0 12px 24px rgba(0, 0, 0, 0.6); } QPushButton:hover { background-color: rgba(255, 255, 255, 240); box-shadow: 0 16px 32px rgba(0, 0, 0, 0.7); } QPushButton:pressed { background-color: rgba(230, 230, 230, 220); box-shadow: inset 0 4px 8px rgba(0, 0, 0, 0.4), 0 2px 4px rgba(0, 0, 0, 0.3); }")


def calculate_type_advantage(attacking_type, defending_type):
    """
    Calculate type advantage. Returns a multiplier.
    Super effective: 1.5
    Not very effective: 0.67
    Neutral: 1.0
    """
    # Simplified type effectiveness chart
    advantages = {
        'fire': ['grass', 'ice', 'bug', 'steel'],
        'water': ['fire', 'ground', 'rock'],
        'grass': ['water', 'ground', 'rock'],
        'electric': ['water', 'flying'],
        'ice': ['grass', 'ground', 'flying', 'dragon'],
        'fighting': ['normal', 'ice', 'rock', 'dark', 'steel'],
        'poison': ['grass', 'fairy'],
        'ground': ['fire', 'electric', 'poison', 'rock', 'steel'],
        'flying': ['grass', 'fighting', 'bug'],
        'psychic': ['fighting', 'poison'],
        'bug': ['grass', 'psychic', 'dark'],
        'rock': ['fire', 'ice', 'flying', 'bug'],
        'ghost': ['psychic', 'ghost'],
        'dragon': ['dragon'],
        'dark': ['psychic', 'ghost'],
        'steel': ['ice', 'rock', 'fairy'],
        'fairy': ['fighting', 'dragon', 'dark'],
    }

    attacking_type = attacking_type.lower()
    defending_type = defending_type.lower()

    if attacking_type in advantages and defending_type in advantages[attacking_type]:
        return 1.5
    return 1.0


def load_pokemon_card(ui, pokedex, pokemon_input, side):
    """
    Load a single pokemon into the specified side (left or right).
    Can accept either a pokemon name or pokedex number.
    """
    pokemon = None

    # Try to parse as a number first
    try:
        pokemon_num = int(pokemon_input)
        pokemon = pokedex.get_pokemon_by_number(pokemon_num)
        if pokemon is not None and not pokemon.empty:
            pokemon = pokemon.iloc[0].to_dict()
    except (ValueError, AttributeError):
        # If not a number or lookup failed, try by name
        pokemon = pokedex.get_pokemon_by_name(pokemon_input)

    if not pokemon:
        if side == "left":
            ui.left_name.setText("Not Found")
            ui.left_stats.setText("Total: --")
            ui.left_type.setText("?")
        else:
            ui.right_name.setText("Not Found")
            ui.right_stats.setText("Total: --")
            ui.right_type.setText("?")
        return

    _display_pokemon_card(ui, pokedex, pokemon, side)
    ui.winner_label.setText("")  # Clear winner when loading new pokemon


def _flash_winner_announcement(ui, winner_text):
    """Flash the winner announcement at the bottom of the screen."""
    ui.winner_label.setText(winner_text)
    ui.winner_label.setStyleSheet("color: #FFD700; font-weight: bold; font-size: 30pt;")

    # Create a timer to flash the text
    flash_count = [0]  # Use list to allow modification in nested function

    def toggle_flash():
        try:
            if flash_count[0] < 8:  # Flash 8 times (4 seconds at 0.25s intervals)
                if ui.winner_label.isVisible():
                    ui.winner_label.setVisible(False)
                else:
                    ui.winner_label.setVisible(True)
                flash_count[0] += 1
            else:
                timer.stop()
                ui.winner_label.setVisible(True)  # Keep it visible at the end
        except RuntimeError:
            # UI object was deleted, stop the timer
            timer.stop()

    timer = QtCore.QTimer()
    timer.timeout.connect(toggle_flash)
    timer.start(250)  # Flash every 250ms


def handle_battle(ui, pokedex, window=None):
    """
    Calculate and display battle results for the two loaded pokemon.
    """
    # Get the loaded pokemon names
    left_name_text = ui.left_name.text()
    right_name_text = ui.right_name.text()

    if left_name_text == "Unknown" or left_name_text == "Not Found" or left_name_text == "Pokemon 1":
        ui.winner_label.setText("Load Pokémon 1 first!")
        ui.winner_label.setStyleSheet("color: red; font-weight: bold; font-size: 14pt;")
        return

    if right_name_text == "Unknown" or right_name_text == "Not Found" or right_name_text == "Pokemon 2":
        ui.winner_label.setText("Load Pokémon 2 first!")
        ui.winner_label.setStyleSheet("color: red; font-weight: bold; font-size: 14pt;")
        return

    # Fetch pokemon data again to get stats
    left_pokemon = pokedex.get_pokemon_by_name(left_name_text)
    right_pokemon = pokedex.get_pokemon_by_name(right_name_text)

    if not left_pokemon or not right_pokemon:
        ui.winner_label.setText("Error loading Pokémon data!")
        ui.winner_label.setStyleSheet("color: red; font-weight: bold; font-size: 14pt;")
        return

    # Calculate battle result
    left_total = sum([
        left_pokemon.get('hp', 0) or 0,
        left_pokemon.get('attack', 0) or 0,
        left_pokemon.get('defense', 0) or 0,
        left_pokemon.get('special_attack', 0) or 0,
        left_pokemon.get('special_defense', 0) or 0,
        left_pokemon.get('speed', 0) or 0,
    ])

    right_total = sum([
        right_pokemon.get('hp', 0) or 0,
        right_pokemon.get('attack', 0) or 0,
        right_pokemon.get('defense', 0) or 0,
        right_pokemon.get('special_attack', 0) or 0,
        right_pokemon.get('special_defense', 0) or 0,
        right_pokemon.get('speed', 0) or 0,
    ])

    # Apply type advantage (considering both types)
    left_type1 = str(left_pokemon.get('type_1', 'normal')).lower()
    left_type2 = str(left_pokemon.get('type_2', '')).lower() if left_pokemon.get('type_2') else None
    right_type1 = str(right_pokemon.get('type_1', 'normal')).lower()
    right_type2 = str(right_pokemon.get('type_2', '')).lower() if right_pokemon.get('type_2') else None

    # Calculate best type advantage for left Pokemon (attacking)
    left_advantages = [calculate_type_advantage(left_type1, right_type1)]
    if right_type2:
        left_advantages.append(calculate_type_advantage(left_type1, right_type2))
    if left_type2:
        left_advantages.append(calculate_type_advantage(left_type2, right_type1))
        if right_type2:
            left_advantages.append(calculate_type_advantage(left_type2, right_type2))
    left_advantage = max(left_advantages)

    # Calculate best type advantage for right Pokemon (attacking)
    right_advantages = [calculate_type_advantage(right_type1, left_type1)]
    if left_type2:
        right_advantages.append(calculate_type_advantage(right_type1, left_type2))
    if right_type2:
        right_advantages.append(calculate_type_advantage(right_type2, left_type1))
        if left_type2:
            right_advantages.append(calculate_type_advantage(right_type2, left_type2))
    right_advantage = max(right_advantages)

    left_score = left_total * left_advantage
    right_score = right_total * right_advantage

    # Determine winner
    if left_score > right_score:
        winner = left_pokemon.get('pokemon', 'Pokemon 1')
        ui.winner_label.setText(f"🏆 {winner.capitalize()} wins! 🏆")
        ui.winner_label.setStyleSheet("color: #FFD700; font-weight: bold; font-size: 20pt;")
        _flash_winner_announcement(ui, f"🏆 {winner.capitalize()} WINS! 🏆")
    elif right_score > left_score:
        winner = right_pokemon.get('pokemon', 'Pokemon 2')
        ui.winner_label.setText(f"🏆 {winner.capitalize()} wins! 🏆")
        ui.winner_label.setStyleSheet("color: #FFD700; font-weight: bold; font-size: 20pt;")
        _flash_winner_announcement(ui, f"🏆 {winner.capitalize()} WINS! 🏆")
    else:
        ui.winner_label.setText("It's a tie!")
        ui.winner_label.setStyleSheet("color: #333333; font-weight: bold; font-size: 20pt;")
        _flash_winner_announcement(ui, "It's a TIE!")

    # Show damage calculator
    _show_damage_calculator(ui, left_pokemon, right_pokemon, window)


def _show_damage_calculator(ui, left_pokemon, right_pokemon, window=None):
    """Calculate and display damage for both Pokemon attacking each other."""
    # Get stats
    left_name = left_pokemon.get('pokemon', 'Pokemon 1').title()
    right_name = right_pokemon.get('pokemon', 'Pokemon 2').title()

    left_attack = int(left_pokemon.get('attack', 0) or 0)
    left_sp_attack = int(left_pokemon.get('special_attack', 0) or 0)
    left_type1 = str(left_pokemon.get('type_1', 'normal')).lower()
    left_type2 = str(left_pokemon.get('type_2', '')).lower() if left_pokemon.get('type_2') else None

    right_attack = int(right_pokemon.get('attack', 0) or 0)
    right_sp_attack = int(right_pokemon.get('special_attack', 0) or 0)
    right_defense = int(right_pokemon.get('defense', 0) or 0)
    right_sp_defense = int(right_pokemon.get('special_defense', 0) or 0)
    right_type1 = str(right_pokemon.get('type_1', 'normal')).lower()
    right_type2 = str(right_pokemon.get('type_2', '')).lower() if right_pokemon.get('type_2') else None

    left_defense = int(left_pokemon.get('defense', 0) or 0)
    left_sp_defense = int(left_pokemon.get('special_defense', 0) or 0)

    # Calculate damage (simplified formula)
    # Left Pokemon attacking Right Pokemon
    left_physical_damage = max(1, int((left_attack * 1.2 / right_defense) * 10))
    left_special_damage = max(1, int((left_sp_attack * 1.2 / right_sp_defense) * 10))

    # Apply type effectiveness
    left_best_damage = max(left_physical_damage, left_special_damage)
    for ltype in [left_type1, left_type2]:
        if ltype:
            adv = calculate_type_advantage(ltype, right_type1)
            if right_type2:
                adv = max(adv, calculate_type_advantage(ltype, right_type2))
            left_best_damage = int(left_best_damage * adv)

    # Right Pokemon attacking Left Pokemon
    right_physical_damage = max(1, int((right_attack * 1.2 / left_defense) * 10))
    right_special_damage = max(1, int((right_sp_attack * 1.2 / left_sp_defense) * 10))

    # Apply type effectiveness
    right_best_damage = max(right_physical_damage, right_special_damage)
    for rtype in [right_type1, right_type2]:
        if rtype:
            adv = calculate_type_advantage(rtype, left_type1)
            if left_type2:
                adv = max(adv, calculate_type_advantage(rtype, left_type2))
            right_best_damage = int(right_best_damage * adv)

    # Store damage calculator data in UI for access
    ui.left_damage_to_right = left_best_damage
    ui.right_damage_to_left = right_best_damage

    # Display damage info
    damage_text = f"DAMAGE CALCULATOR\n\n"
    damage_text += f"{left_name} → {right_name}: ~{left_best_damage} DMG\n"
    damage_text += f"{right_name} → {left_name}: ~{right_best_damage} DMG\n\n"

    if left_best_damage > right_best_damage:
        damage_text += f"{left_name} has the advantage!"
    elif right_best_damage > left_best_damage:
        damage_text += f"{right_name} has the advantage!"
    else:
        damage_text += "Balanced matchup!"

    # Create a message box to display damage
    msg = QtWidgets.QMessageBox(window) if window else QtWidgets.QMessageBox()
    msg.setWindowTitle("Damage Calculator")
    msg.setText(damage_text)
    msg.setIcon(QtWidgets.QMessageBox.Information)
    msg.setStyleSheet("""
        QMessageBox { background-color: white; }
        QMessageBox QLabel { color: black; }
        QPushButton { color: black; background-color: rgba(255, 255, 255, 220); padding: 5px 15px; border-radius: 4px; }
        QPushButton:hover { background-color: #2196F3; color: white; }
    """)
    msg.exec_()


def _display_pokemon_card(ui, pokedex, pokemon_data, side):
    """Display pokemon data on the battle card (left or right)."""
    name = pokemon_data.get('pokemon', 'Unknown')
    name_cap = name.capitalize()
    pokemon_no = int(pokemon_data.get('pokedex_no', 0))

    # Store Pokemon number for cry playback
    if side == "left":
        ui.current_pokemon_no_left = pokemon_no
    else:
        ui.current_pokemon_no_right = pokemon_no

    ptype = pokemon_data.get('type_1', 'normal')
    if ptype:
        ptype = str(ptype).capitalize()
    else:
        ptype = 'Normal'

    total_stats = sum([
        pokemon_data.get('hp', 0) or 0,
        pokemon_data.get('attack', 0) or 0,
        pokemon_data.get('defense', 0) or 0,
        pokemon_data.get('sp_attack', 0) or 0,
        pokemon_data.get('sp_defense', 0) or 0,
        pokemon_data.get('speed', 0) or 0,
    ])

    # Get individual stats
    hp = pokemon_data.get('hp', 0) or 0
    attack = pokemon_data.get('attack', 0) or 0
    defense = pokemon_data.get('defense', 0) or 0
    sp_attack = pokemon_data.get('special_attack', 0) or 0
    sp_defense = pokemon_data.get('special_defense', 0) or 0

    # Update UI based on side
    if side == "left":
        ui.left_name.setText(name_cap)
        ui.left_hp.setText(f"HP: {int(hp)}")
        ui.left_atk.setText(f"Attack: {int(attack)}")
        ui.left_def.setText(f"Defense: {int(defense)}")
        ui.left_spa.setText(f"Sp. Attack: {int(sp_attack)}")
        ui.left_spd.setText(f"Sp. Defense: {int(sp_defense)}")
        ui.left_stats.setText(f"Total: {total_stats}")

        # Set type badge color
        type_color = TYPE_COLORS.get(ptype.lower(), "#999999")
        ui.left_type.setText(ptype)
        ui.left_type.setStyleSheet(f"background-color: {type_color}; color: white; font-size: 10pt; font-weight: bold; border-radius: 4px; padding: 2px;")

        # Set second type badge if it exists
        ptype_2 = pokemon_data.get('type_2')
        if ptype_2:
            import pandas as pd
            if pd.notna(ptype_2):
                ptype_2 = str(ptype_2).capitalize()
                type_color_2 = TYPE_COLORS.get(ptype_2.lower(), "#999999")
                ui.left_type_2.setText(ptype_2)
                ui.left_type_2.setStyleSheet(f"background-color: {type_color_2}; color: white; font-size: 10pt; font-weight: bold; border-radius: 4px; padding: 2px;")
                ui.left_type_2.show()
            else:
                ui.left_type_2.hide()
        else:
            ui.left_type_2.hide()

        # Load sprite from database
        sprite_data = pokemon_data.get("sprite")
        if sprite_data:
            pixmap = QtGui.QPixmap()
            pixmap.loadFromData(sprite_data)
            if not pixmap.isNull():
                scaled = pixmap.scaled(136, 106, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
                icon = QtGui.QIcon(scaled)
                ui.left_sprite.setIcon(icon)
                ui.left_sprite.setIconSize(QtCore.QSize(136, 106))
    else:
        ui.right_name.setText(name_cap)
        ui.right_hp.setText(f"HP: {int(hp)}")
        ui.right_atk.setText(f"Attack: {int(attack)}")
        ui.right_def.setText(f"Defense: {int(defense)}")
        ui.right_spa.setText(f"Sp. Attack: {int(sp_attack)}")
        ui.right_spd.setText(f"Sp. Defense: {int(sp_defense)}")
        ui.right_stats.setText(f"Total: {total_stats}")

        # Set type badge color
        type_color = TYPE_COLORS.get(ptype.lower(), "#999999")
        ui.right_type.setText(ptype)
        ui.right_type.setStyleSheet(f"background-color: {type_color}; color: white; font-size: 10pt; font-weight: bold; border-radius: 4px; padding: 2px;")

        # Set second type badge if it exists
        ptype_2 = pokemon_data.get('type_2')
        if ptype_2:
            import pandas as pd
            if pd.notna(ptype_2):
                ptype_2 = str(ptype_2).capitalize()
                type_color_2 = TYPE_COLORS.get(ptype_2.lower(), "#999999")
                ui.right_type_2.setText(ptype_2)
                ui.right_type_2.setStyleSheet(f"background-color: {type_color_2}; color: white; font-size: 10pt; font-weight: bold; border-radius: 4px; padding: 2px;")
                ui.right_type_2.show()
            else:
                ui.right_type_2.hide()
        else:
            ui.right_type_2.hide()

        # Load sprite from database
        sprite_data = pokemon_data.get("sprite")
        if sprite_data:
            pixmap = QtGui.QPixmap()
            pixmap.loadFromData(sprite_data)
            if not pixmap.isNull():
                scaled = pixmap.scaled(136, 106, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
                icon = QtGui.QIcon(scaled)
                ui.right_sprite.setIcon(icon)
                ui.right_sprite.setIconSize(QtCore.QSize(136, 106))
