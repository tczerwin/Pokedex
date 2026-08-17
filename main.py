"""
Entry point for the Pokedex app.

This is the only file that imports mainpage.py, top10.py, look_up.py,
and raidcounters.py, and the only place that owns the shared
PokemonDatabase connection. That's what avoids circular imports: none of
those four files import each other directly -- they just build their
widgets and expose plain functions that take the pokedex as an argument.
Window-switching is handled here via callbacks connected to each button.

Run this file (not mainpage.py, top10.py, look_up.py, or
raidcounters.py) to start the app:
    python main.py
"""

import sys

from PyQt5 import QtWidgets, QtCore, QtGui, QtMultimedia

from PokemonDatabase import PokemonDatabase
from mainpage import Ui_MainWindow as Ui_MainPage, set_background as set_mainpage_background, load_image
from top10 import Ui_Top10, handle_top
from look_up import Ui_MainWindow, handle_lookup, set_background as set_lookup_background
from raidcounters import Ui_RaidCounters, handle_raid_counters
from battle import Ui_Battle, handle_battle, load_pokemon_card
from type_chart import Ui_TypeChart
from team_builder import Ui_TeamBuilder
from teams import TeamManager


class GlobalKeyEventFilter(QtCore.QObject):
    """Global event filter to capture arrow keys anywhere in the app."""

    def __init__(self, pokedex_app):
        super().__init__()
        self.pokedex_app = pokedex_app

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.KeyPress:
            if self.pokedex_app.lookup_window and self.pokedex_app.lookup_window.isVisible():
                if event.key() == QtCore.Qt.Key_Left:
                    import look_up
                    look_up._navigate_pokemon(self.pokedex_app.lookup_ui, self.pokedex_app.pokedex, -1)
                    return True
                elif event.key() == QtCore.Qt.Key_Right:
                    import look_up
                    look_up._navigate_pokemon(self.pokedex_app.lookup_ui, self.pokedex_app.pokedex, 1)
                    return True
        return super().eventFilter(obj, event)


class LoadTeamDialog(QtWidgets.QDialog):
    """Custom dialog for loading teams with delete option."""

    def __init__(self, parent, team_names, team_manager):
        super().__init__(parent)
        self.team_manager = team_manager
        self.selected_team = None
        self.setup_ui(team_names)

    def setup_ui(self, team_names):
        self.setWindowTitle("Load Team")
        self.setGeometry(100, 100, 400, 300)

        layout = QtWidgets.QVBoxLayout()

        # Label
        label = QtWidgets.QLabel("Select a team:")
        layout.addWidget(label)

        # List widget
        self.team_list = QtWidgets.QListWidget()
        self.team_list.addItems(team_names)
        self.team_list.itemSelectionChanged.connect(self.on_selection_changed)
        layout.addWidget(self.team_list)

        # Buttons row
        button_layout = QtWidgets.QHBoxLayout()

        delete_btn = QtWidgets.QPushButton("Delete")
        delete_btn.clicked.connect(self.delete_team)
        button_layout.addWidget(delete_btn)

        button_layout.addStretch()

        load_btn = QtWidgets.QPushButton("Load")
        load_btn.clicked.connect(self.load_team)
        button_layout.addWidget(load_btn)

        cancel_btn = QtWidgets.QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def on_selection_changed(self):
        """Called when selection changes."""
        pass

    def delete_team(self):
        """Delete the selected team."""
        current_item = self.team_list.currentItem()
        if not current_item:
            QtWidgets.QMessageBox.warning(self, "No Selection", "Please select a team to delete.")
            return

        team_name = current_item.text()
        reply = QtWidgets.QMessageBox.question(
            self,
            "Delete Team",
            f"Are you sure you want to delete '{team_name}'?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )

        if reply == QtWidgets.QMessageBox.Yes:
            try:
                self.team_manager.delete_team(team_name)
                row = self.team_list.row(current_item)
                self.team_list.takeItem(row)
                QtWidgets.QMessageBox.information(self, "Deleted", f"Team '{team_name}' deleted successfully.")
            except Exception as e:
                QtWidgets.QMessageBox.warning(self, "Error", f"Error deleting team: {str(e)}")

    def load_team(self):
        """Load the selected team."""
        current_item = self.team_list.currentItem()
        if not current_item:
            QtWidgets.QMessageBox.warning(self, "No Selection", "Please select a team to load.")
            return

        self.selected_team = current_item.text()
        self.accept()

    def get_selected_team(self):
        """Get the selected team name."""
        return self.selected_team


class AddPokemonDialog(QtWidgets.QDialog):
    """Custom dialog for adding Pokemon to a slot with level selection."""

    def __init__(self, parent, slot_num, pokedex=None):
        super().__init__(parent)
        self.pokemon_name = None
        self.level = 50
        self.pokedex = pokedex
        self.setup_ui(slot_num)

    def setup_ui(self, slot_num):
        self.setWindowTitle(f"Add Pokemon to Slot {slot_num}")
        self.setGeometry(100, 100, 350, 200)

        layout = QtWidgets.QVBoxLayout()

        # Pokemon name input
        name_label = QtWidgets.QLabel("Pokemon name or number:")
        layout.addWidget(name_label)

        self.name_input = QtWidgets.QLineEdit()
        self.name_input.setPlaceholderText("e.g., Pikachu or 25")
        layout.addWidget(self.name_input)

        # Add autocomplete for Pokemon names
        if self.pokedex:
            try:
                conn = self.pokedex.get_connection()
                cursor = conn.cursor()
                cursor.execute("SELECT pokemon, pokedex_no FROM pokedex ORDER BY pokedex_no")
                pokemon_list = [f"{row[0].capitalize()} (#{row[1]})" for row in cursor.fetchall()]
                conn.close()

                completer = QtWidgets.QCompleter(pokemon_list)
                completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
                completer.setCompletionMode(QtWidgets.QCompleter.PopupCompletion)
                self.name_input.setCompleter(completer)
            except Exception as e:
                pass

        # Level selection
        level_layout = QtWidgets.QHBoxLayout()
        level_label = QtWidgets.QLabel("Level:")
        level_layout.addWidget(level_label)

        self.level_spinbox = QtWidgets.QSpinBox()
        self.level_spinbox.setMinimum(1)
        self.level_spinbox.setMaximum(100)
        self.level_spinbox.setValue(50)
        self.level_spinbox.valueChanged.connect(self.on_level_changed)
        level_layout.addWidget(self.level_spinbox)

        level_layout.addStretch()
        layout.addLayout(level_layout)

        # Level slider for visual feedback
        self.level_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.level_slider.setMinimum(1)
        self.level_slider.setMaximum(100)
        self.level_slider.setValue(50)
        self.level_slider.sliderMoved.connect(self.on_slider_moved)
        layout.addWidget(self.level_slider)

        # Buttons
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addStretch()

        ok_btn = QtWidgets.QPushButton("Add")
        ok_btn.clicked.connect(self.add_pokemon)
        button_layout.addWidget(ok_btn)

        cancel_btn = QtWidgets.QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def on_level_changed(self, value):
        """Sync slider with spinbox."""
        self.level_slider.blockSignals(True)
        self.level_slider.setValue(value)
        self.level_slider.blockSignals(False)
        self.level = value

    def on_slider_moved(self, value):
        """Sync spinbox with slider."""
        self.level_spinbox.blockSignals(True)
        self.level_spinbox.setValue(value)
        self.level_spinbox.blockSignals(False)
        self.level = value

    def add_pokemon(self):
        """Validate and accept."""
        pokemon_name = self.name_input.text().strip()
        if not pokemon_name:
            QtWidgets.QMessageBox.warning(self, "Error", "Please enter a Pokemon name or number.")
            return

        # Strip Pokedex number from autocomplete selection
        if " (#" in pokemon_name:
            pokemon_name = pokemon_name.split(" (#")[0]

        self.pokemon_name = pokemon_name
        self.level = self.level_spinbox.value()
        self.accept()

    def get_pokemon_name(self):
        """Get the entered Pokemon name."""
        return self.pokemon_name

    def get_level(self):
        """Get the selected level."""
        return self.level


class PokedexApp:
    """Owns the QApplication, the shared database, and window switching."""

    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.pokedex = PokemonDatabase()
        self.team_manager = TeamManager()

        self.mainpage_window = None
        self.top10_window = None
        self.lookup_window = None
        self.lookup_ui = None
        self.raid_window = None
        self.battle_window = None
        self.type_chart_window = None
        self.team_builder_window = None
        self.team_builder_ui = None

        # Install global event filter for arrow keys
        self.key_filter = GlobalKeyEventFilter(self)
        self.app.installEventFilter(self.key_filter)

        # Set up background music
        import os
        self.music_player = QtMultimedia.QMediaPlayer()
        self.music_player.setVolume(20)  # Set volume to 20% (quiet)

        # Create a playlist to loop the music
        self.playlist = QtMultimedia.QMediaPlaylist()
        self.playlist.setPlaybackMode(QtMultimedia.QMediaPlaylist.Loop)
        self.music_player.setPlaylist(self.playlist)

        # Add the Pokemon.mp3 file with absolute path
        script_dir = os.path.dirname(os.path.abspath(__file__))
        music_path = os.path.join(script_dir, "img", "Pokemon.mp3")

        if os.path.exists(music_path):
            music_file = QtCore.QUrl.fromLocalFile(music_path)
            media_content = QtMultimedia.QMediaContent(music_file)
            self.playlist.addMedia(media_content)

            # Start playing
            self.music_player.play()
        else:
            pass

    def _close_other_windows(self, keep):
        for attr in ("mainpage_window", "top10_window", "lookup_window", "raid_window", "battle_window", "team_builder_window"):
            if attr == keep:
                continue
            window = getattr(self, attr)
            if window is not None:
                window.close()
                setattr(self, attr, None)

    def show_mainpage(self):
        self.mainpage_window = QtWidgets.QMainWindow()
        ui = Ui_MainPage()
        ui.setupUi(self.mainpage_window)
        set_mainpage_background(ui, "poke_background.jpg")

        # Load images
        load_image(ui.pokemon_pic, "img/pokemon.jpg", max_width=400, max_height=300)
        load_image(ui.ash_pic, "img/ash.png", max_width=150, max_height=150)

        ui.lookup_b1.clicked.connect(self.show_lookup)
        ui.top10_b1.clicked.connect(self.show_top10)
        ui.raidcounters_b1.clicked.connect(self.show_raid_counters)
        ui.compete_b1.clicked.connect(self.show_compete)
        ui.team_builder_b1.clicked.connect(self.show_team_builder)

        self.mainpage_window.show()

        self._close_other_windows("mainpage_window")

    def show_type_chart(self):
        if self.type_chart_window is None or not self.type_chart_window.isVisible():
            self.type_chart_window = QtWidgets.QMainWindow()
            ui = Ui_TypeChart()
            ui.setupUi(self.type_chart_window)

            # Position window to the right side of the screen
            screen = self.app.primaryScreen()
            screen_rect = screen.geometry()
            window_width = 800
            window_height = 650

            # Position on the right side with some margin
            x = screen_rect.right() - window_width - 20
            y = screen_rect.top() + 50

            self.type_chart_window.move(x, y)
            self.type_chart_window.show()
        else:
            self.type_chart_window.raise_()
            self.type_chart_window.activateWindow()

    def show_team_builder(self):
        # Only create the team builder window once
        if self.team_builder_window is None:
            self.team_builder_window = QtWidgets.QMainWindow()
            ui = Ui_TeamBuilder()
            ui.setupUi(self.team_builder_window)
            self.team_builder_ui = ui

            # Wire up navigation buttons
            ui.lookup_b1.clicked.connect(self.show_lookup)
            ui.battle_b1.clicked.connect(self.show_compete)
            ui.raid_b1.clicked.connect(self.show_raid_counters)
            ui.top_b1.clicked.connect(self.show_top10)

            # Wire up team management buttons
            ui.save_btn.clicked.connect(self._save_team)
            ui.load_btn.clicked.connect(self._load_team_dialog)
            ui.coverage_btn.clicked.connect(self._show_type_coverage)
            ui.export_btn.clicked.connect(self._export_team_pdf)

            # Wire up pokemon slot buttons
            for i in range(6):
                getattr(ui, f"pokemon_name_{i}").clicked.connect(
                    lambda checked=False, idx=i: self._add_pokemon_to_slot(idx)
                )
                getattr(ui, f"remove_{i}").clicked.connect(
                    lambda checked=False, idx=i: self._remove_pokemon_from_slot(idx)
                )

        self.team_builder_window.show()
        self._close_other_windows("team_builder_window")

    def _add_pokemon_to_slot(self, slot_idx):
        """Search for Pokemon to add to slot with level selection."""
        dialog = AddPokemonDialog(self.team_builder_window, slot_idx + 1, self.pokedex)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            text = dialog.get_pokemon_name()
            level = dialog.get_level()

            poke_data = self.pokedex.get_pokemon_by_name(text)
            if poke_data is None:
                try:
                    result = self.pokedex.get_pokemon_by_number(int(text))
                    if result is not None and not result.empty:
                        poke_data = result.iloc[0].to_dict()
                except:
                    pass
            elif hasattr(poke_data, 'empty') and not poke_data.empty:
                poke_data = poke_data.iloc[0].to_dict()

            if poke_data is not None:
                pokemon_name = str(poke_data.get('pokemon', text)).title()
                self.team_builder_ui.pokemon_name_dict = getattr(self.team_builder_ui, 'pokemon_name_dict', {})
                self.team_builder_ui.pokemon_name_dict[slot_idx] = pokemon_name

                # Update button
                getattr(self.team_builder_ui, f"pokemon_name_{slot_idx}").setText(pokemon_name)

                # Set level slider - the signal will update the label automatically
                level_slider = getattr(self.team_builder_ui, f"level_slider_{slot_idx}")
                level_slider.setValue(level)

                # Load sprite
                sprite_data = poke_data.get("sprite")
                if sprite_data is not None:
                    pixmap = QtGui.QPixmap()
                    pixmap.loadFromData(sprite_data)
                    if not pixmap.isNull():
                        pixmap = pixmap.scaled(44, 44, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
                        icon = QtGui.QIcon(pixmap)
                        getattr(self.team_builder_ui, f"sprite_{slot_idx}").setIcon(icon)
                        getattr(self.team_builder_ui, f"sprite_{slot_idx}").setIconSize(QtCore.QSize(44, 44))
            else:
                QtWidgets.QMessageBox.warning(self.team_builder_window, "Not Found", "Pokemon not found!")

    def _remove_pokemon_from_slot(self, slot_idx):
        """Remove Pokemon from slot."""
        self.team_builder_ui.pokemon_name_dict = getattr(self.team_builder_ui, 'pokemon_name_dict', {})
        if slot_idx in self.team_builder_ui.pokemon_name_dict:
            del self.team_builder_ui.pokemon_name_dict[slot_idx]

        getattr(self.team_builder_ui, f"pokemon_name_{slot_idx}").setText("Click to add")
        getattr(self.team_builder_ui, f"sprite_{slot_idx}").setIcon(QtGui.QIcon())

    def _add_lookup_pokemon_to_team(self):
        """Add the currently viewed Pokemon from lookup to the team builder."""
        if not self.lookup_ui or not hasattr(self.lookup_ui, 'name') or not hasattr(self.lookup_ui, 'current_pokemon_no'):
            QtWidgets.QMessageBox.warning(self.lookup_window, "Error", "No Pokemon selected!")
            return

        pokemon_name = self.lookup_ui.name.text().strip()
        pokemon_no = self.lookup_ui.current_pokemon_no

        if not pokemon_name or pokemon_name == "???":
            QtWidgets.QMessageBox.warning(self.lookup_window, "Error", "No Pokemon selected!")
            return

        # Show team builder
        self.show_team_builder()

        # Find first empty slot
        if self.team_builder_ui:
            for i in range(6):
                slot_name = getattr(self.team_builder_ui, f"pokemon_name_{i}")
                if slot_name.text() == "Click to add":
                    # Add the Pokemon to this slot with default level 50
                    self.team_builder_ui.pokemon_name_dict = getattr(self.team_builder_ui, 'pokemon_name_dict', {})
                    self.team_builder_ui.pokemon_name_dict[i] = pokemon_name

                    # Update button
                    slot_name.setText(pokemon_name)

                    # Load sprite using Pokedex number (more reliable than name lookup)
                    poke_data = self.pokedex.get_pokemon_by_number(pokemon_no)
                    if poke_data is not None:
                        # Handle Pandas Series/DataFrame
                        if hasattr(poke_data, 'empty'):
                            if not poke_data.empty:
                                poke_data = poke_data.iloc[0].to_dict()
                            else:
                                poke_data = None
                        elif not isinstance(poke_data, dict):
                            poke_data = None

                        if isinstance(poke_data, dict):
                            sprite_data = poke_data.get("sprite")
                            if sprite_data is not None:
                                pixmap = QtGui.QPixmap()
                                pixmap.loadFromData(sprite_data)
                                if not pixmap.isNull():
                                    pixmap = pixmap.scaled(44, 44, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
                                    icon = QtGui.QIcon(pixmap)
                                    getattr(self.team_builder_ui, f"sprite_{i}").setIcon(icon)
                                    getattr(self.team_builder_ui, f"sprite_{i}").setIconSize(QtCore.QSize(44, 44))

                    QtWidgets.QMessageBox.information(
                        self.team_builder_window,
                        "Added",
                        f"{pokemon_name} added to slot {i + 1}!"
                    )
                    return

            QtWidgets.QMessageBox.warning(
                self.team_builder_window,
                "Team Full",
                "All team slots are full!"
            )

    def _save_team(self):
        """Save current team."""
        team_name = self.team_builder_ui.team_name_input.text().strip()
        if not team_name:
            QtWidgets.QMessageBox.warning(self.team_builder_window, "Error", "Please enter a team name!")
            return

        pokemon_name_dict = getattr(self.team_builder_ui, 'pokemon_name_dict', {})
        if not pokemon_name_dict:
            QtWidgets.QMessageBox.warning(self.team_builder_window, "Error", "Please add at least one Pokemon!")
            return

        team_data = []
        for i in range(6):
            if i in pokemon_name_dict:
                level = getattr(self.team_builder_ui, f"level_slider_{i}").value()
                team_data.append({
                    "name": pokemon_name_dict[i].lower(),
                    "level": level
                })

        self.team_manager.save_team(team_name, team_data)
        QtWidgets.QMessageBox.information(self.team_builder_window, "Success", f"Team '{team_name}' saved!")

    def _load_team_dialog(self):
        """Load team dialog with delete option."""
        try:
            team_names = self.team_manager.get_team_names()
            if not team_names:
                QtWidgets.QMessageBox.warning(self.team_builder_window, "No Teams", "No saved teams found!")
                return

            dialog = LoadTeamDialog(self.team_builder_window, team_names, self.team_manager)
            if dialog.exec_() == QtWidgets.QDialog.Accepted:
                team_name = dialog.get_selected_team()
                if team_name:
                    self._load_team(team_name)
        except Exception as e:
            QtWidgets.QMessageBox.warning(self.team_builder_window, "Error", f"Error loading teams: {str(e)}")

    def _show_type_coverage(self):
        """Show type coverage for the current team."""
        from PokemonDatabase import TYPE_ADVANTAGE

        # Collect all Pokemon in team from UI buttons
        team_pokemon = []
        for i in range(6):
            name_btn = getattr(self.team_builder_ui, f"pokemon_name_{i}")
            pokemon_name = name_btn.text().strip()
            if pokemon_name and pokemon_name != "Click to add":
                team_pokemon.append(pokemon_name)

        if not team_pokemon:
            QtWidgets.QMessageBox.warning(self.team_builder_window, "Error", "Add Pokemon to your team first!")
            return

        covered_types = set()
        weak_to_types = set()

        for pokemon_name in team_pokemon:
            poke_data = self.pokedex.get_pokemon_by_name(pokemon_name)

            if poke_data is not None:
                # Handle Pandas Series/DataFrame
                if hasattr(poke_data, 'empty'):
                    if poke_data.empty:
                        continue
                    poke_data = poke_data.iloc[0].to_dict()
                elif hasattr(poke_data, 'to_dict'):
                    poke_data = poke_data.to_dict()

                type1 = str(poke_data.get('type_1', 'normal')).lower()
                type2 = poke_data.get('type_2')
                if type2:
                    type2 = str(type2).lower()

                # Find what this pokemon is strong against
                if type1 in TYPE_ADVANTAGE:
                    covered_types.update(TYPE_ADVANTAGE[type1])
                if type2 and type2 in TYPE_ADVANTAGE:
                    covered_types.update(TYPE_ADVANTAGE[type2])

                # Find what this pokemon is weak to
                for attack_type, defender_types in TYPE_ADVANTAGE.items():
                    if type1 in defender_types or (type2 and type2 in defender_types):
                        weak_to_types.add(attack_type)

        message = "Type Coverage:\n\n"
        message += f"Strong Against: {', '.join(sorted(covered_types)).title() if covered_types else 'None'}\n\n"
        message += f"Weak To: {', '.join(sorted(weak_to_types)).title() if weak_to_types else 'None'}"

        QtWidgets.QMessageBox.information(self.team_builder_window, "Type Coverage", message)

    def _export_team_pdf(self):
        """Export team stats to PDF."""
        team_name = self.team_builder_ui.team_name_input.text().strip()
        if not team_name:
            QtWidgets.QMessageBox.warning(self.team_builder_window, "Error", "Please enter a team name!")
            return

        pokemon_name_dict = getattr(self.team_builder_ui, 'pokemon_name_dict', {})
        if not pokemon_name_dict:
            QtWidgets.QMessageBox.warning(self.team_builder_window, "Error", "Please add at least one Pokemon!")
            return

        # Get file save location
        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self.team_builder_window,
            "Export Team",
            f"{team_name}_stats.pdf",
            "PDF Files (*.pdf)"
        )

        if not file_path:
            return

        try:
            from reportlab.lib.pagesizes import letter, A4
            from reportlab.lib import colors
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.units import inch
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
            from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
            from datetime import datetime

            # Collect team data
            import io
            from PIL import Image

            team_pokemon = []
            temp_images = []

            for i in range(6):
                if i in pokemon_name_dict:
                    pokemon_name = pokemon_name_dict[i]
                    level = getattr(self.team_builder_ui, f"level_slider_{i}").value()
                    poke_data = self.pokedex.get_pokemon_by_name(pokemon_name)

                    if poke_data is not None:
                        if hasattr(poke_data, 'empty') and not poke_data.empty:
                            poke_data = poke_data.iloc[0].to_dict()
                        elif not isinstance(poke_data, dict):
                            continue

                        if isinstance(poke_data, dict):
                            # Try to load sprite image
                            sprite_path = None
                            sprite_data = poke_data.get("sprite")
                            if sprite_data is not None:
                                try:
                                    img = Image.open(io.BytesIO(sprite_data))
                                    # Save to temporary file
                                    temp_file = f"/tmp/pokemon_sprite_{len(temp_images)}.png"
                                    img.save(temp_file)
                                    sprite_path = temp_file
                                    temp_images.append(temp_file)
                                except:
                                    sprite_path = None

                            team_pokemon.append({
                                'name': pokemon_name,
                                'level': level,
                                'data': poke_data,
                                'sprite_path': sprite_path
                            })

            # Create PDF
            doc = SimpleDocTemplate(file_path, pagesize=letter)
            story = []
            styles = getSampleStyleSheet()

            # Title
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                textColor=colors.HexColor('#1a1a1a'),
                spaceAfter=12,
                alignment=TA_CENTER
            )
            story.append(Paragraph(f"{team_name} - Team Stats", title_style))
            story.append(Paragraph(f"Exported: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
            story.append(Spacer(1, 0.3*inch))

            # Team table with sprites
            from reportlab.platypus import Image as RLImage

            team_data = [['Sprite', 'Pokemon', 'Lvl', 'Type 1', 'Type 2', 'Ht', 'Wt', 'HP', 'Atk', 'Def', 'SpA', 'SpD', 'Spe', 'Total']]

            total_stats = {'hp': 0, 'attack': 0, 'defense': 0, 'special_attack': 0, 'special_defense': 0, 'speed': 0}

            for idx, poke in enumerate(team_pokemon, 1):
                data = poke['data']
                hp = int(data.get('hp', 0))
                atk = int(data.get('attack', 0))
                df = int(data.get('defense', 0))
                spa = int(data.get('special_attack', 0))
                spd = int(data.get('special_defense', 0))
                spe = int(data.get('speed', 0))
                total = hp + atk + df + spa + spd + spe

                total_stats['hp'] += hp
                total_stats['attack'] += atk
                total_stats['defense'] += df
                total_stats['special_attack'] += spa
                total_stats['special_defense'] += spd
                total_stats['speed'] += spe

                type1 = str(data.get('type_1', 'Unknown')).title()
                type2 = str(data.get('type_2', '')).title() if data.get('type_2') else ''
                height = f"{data.get('height', 0)}m"
                weight = f"{data.get('weight', 0)}kg"

                # Add sprite image
                sprite_cell = ''
                if poke['sprite_path']:
                    try:
                        sprite_cell = RLImage(poke['sprite_path'], width=0.5*inch, height=0.5*inch)
                    except:
                        sprite_cell = ''

                row = [
                    sprite_cell,
                    poke['name'],
                    str(poke['level']),
                    type1,
                    type2,
                    height,
                    weight,
                    str(hp),
                    str(atk),
                    str(df),
                    str(spa),
                    str(spd),
                    str(spe),
                    str(total)
                ]
                team_data.append(row)

            # Add averages
            avg_count = len(team_pokemon) if team_pokemon else 1
            avg_total = (total_stats['hp'] + total_stats['attack'] + total_stats['defense'] +
                        total_stats['special_attack'] + total_stats['special_defense'] + total_stats['speed']) // avg_count

            team_data.append([
                '',
                'AVERAGE',
                '',
                '',
                '',
                '',
                '',
                f"{total_stats['hp']//avg_count}",
                f"{total_stats['attack']//avg_count}",
                f"{total_stats['defense']//avg_count}",
                f"{total_stats['special_attack']//avg_count}",
                f"{total_stats['special_defense']//avg_count}",
                f"{total_stats['speed']//avg_count}",
                str(avg_total)
            ])

            team_table = Table(team_data, colWidths=[0.6*inch, 1.1*inch, 0.4*inch, 0.65*inch, 0.65*inch, 0.45*inch, 0.45*inch, 0.4*inch, 0.4*inch, 0.4*inch, 0.4*inch, 0.4*inch, 0.4*inch, 0.5*inch])
            team_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4CAF50')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#E8F5E9')),
                ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#CCCCCC')),
                ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.white, colors.HexColor('#F5F5F5')]),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
            ]))
            story.append(team_table)
            story.append(Spacer(1, 0.3*inch))

            # Type coverage
            from PokemonDatabase import TYPE_ADVANTAGE
            covered_types = set()
            weak_to_types = set()

            for poke in team_pokemon:
                data = poke['data']
                type1 = str(data.get('type_1', 'normal')).lower()
                type2 = data.get('type_2')
                if type2:
                    type2 = str(type2).lower()

                if type1 in TYPE_ADVANTAGE:
                    covered_types.update(TYPE_ADVANTAGE[type1])
                if type2 and type2 in TYPE_ADVANTAGE:
                    covered_types.update(TYPE_ADVANTAGE[type2])

                for attack_type, defender_types in TYPE_ADVANTAGE.items():
                    if type1 in defender_types or (type2 and type2 in defender_types):
                        weak_to_types.add(attack_type)

            story.append(Paragraph("Type Coverage", styles['Heading2']))
            story.append(Paragraph(f"<b>Strong Against:</b> {', '.join(sorted(covered_types)).title() if covered_types else 'None'}", styles['Normal']))
            story.append(Paragraph(f"<b>Weak To:</b> {', '.join(sorted(weak_to_types)).title() if weak_to_types else 'None'}", styles['Normal']))

            # Build PDF
            doc.build(story)

            # Clean up temporary image files
            import os
            import platform
            import subprocess

            for temp_file in temp_images:
                try:
                    os.remove(temp_file)
                except:
                    pass

            # Open the PDF automatically
            try:
                if platform.system() == 'Darwin':  # macOS
                    subprocess.Popen(['open', file_path])
                elif platform.system() == 'Windows':
                    os.startfile(file_path)
                elif platform.system() == 'Linux':
                    subprocess.Popen(['xdg-open', file_path])
            except Exception as e:
                pass

            QtWidgets.QMessageBox.information(self.team_builder_window, "Success", f"Team exported to:\n{file_path}")
        except ImportError:
            QtWidgets.QMessageBox.warning(self.team_builder_window, "Error", "reportlab or PIL library not installed. Please install with: pip install reportlab pillow")
        except Exception as e:
            QtWidgets.QMessageBox.warning(self.team_builder_window, "Error", f"Failed to export PDF:\n{str(e)}")

    def _load_team(self, team_name):
        """Load a saved team."""
        team_data = self.team_manager.load_team(team_name)
        if not team_data:
            QtWidgets.QMessageBox.warning(self.team_builder_window, "Error", "Could not load team!")
            return

        # Clear current team
        self.team_builder_ui.pokemon_name_dict = {}
        for i in range(6):
            getattr(self.team_builder_ui, f"pokemon_name_{i}").setText("Click to add")
            getattr(self.team_builder_ui, f"sprite_{i}").setIcon(QtGui.QIcon())

        # Set team name
        self.team_builder_ui.team_name_input.setText(team_name)

        # Load team data
        for i, pokemon_info in enumerate(team_data[:6]):
            pokemon_name = pokemon_info.get("name", "").strip()
            level = pokemon_info.get("level", 50)

            if not pokemon_name:
                continue

            # Try to find the pokemon
            poke_data = self.pokedex.get_pokemon_by_name(pokemon_name)

            if poke_data is not None:
                # Handle Pandas Series/DataFrame
                if hasattr(poke_data, 'empty'):
                    if poke_data.empty:
                        continue
                    poke_data = poke_data.iloc[0].to_dict()
                elif hasattr(poke_data, 'to_dict'):
                    poke_data = poke_data.to_dict()

                pokemon_display_name = str(poke_data.get('pokemon', pokemon_name)).title()
                self.team_builder_ui.pokemon_name_dict[i] = pokemon_display_name

                getattr(self.team_builder_ui, f"pokemon_name_{i}").setText(pokemon_display_name)
                getattr(self.team_builder_ui, f"level_slider_{i}").setValue(level)

                # Load sprite
                sprite_data = poke_data.get("sprite")
                if sprite_data is not None:
                    try:
                        pixmap = QtGui.QPixmap()
                        pixmap.loadFromData(sprite_data)
                        if not pixmap.isNull():
                            pixmap = pixmap.scaled(44, 44, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
                            icon = QtGui.QIcon(pixmap)
                            getattr(self.team_builder_ui, f"sprite_{i}").setIcon(icon)
                            getattr(self.team_builder_ui, f"sprite_{i}").setIconSize(QtCore.QSize(44, 44))
                    except:
                        pass  # Sprite loading failed, just skip

    def show_top10(self):
        self.top10_window = QtWidgets.QMainWindow()
        ui = Ui_Top10()
        ui.setupUi(self.top10_window)

        def on_top10_pokemon_click(pokemon_name):
            """When a pokemon is clicked in top10, switch to lookup and display it."""
            self.show_lookup()
            if self.lookup_ui:
                import look_up
                poke_data = self.pokedex.get_pokemon_by_name(pokemon_name)
                if poke_data:
                    look_up._display_pokemon_data(self.lookup_ui, self.pokedex, poke_data)

                    # Set up sprite click handler and carousel buttons
                    try:
                        self.lookup_ui.sprite.clicked.disconnect()
                        self.lookup_ui.sprite_left_btn.clicked.disconnect()
                        self.lookup_ui.sprite_right_btn.clicked.disconnect()
                    except TypeError:
                        pass

                    self.lookup_ui.sprite.clicked.connect(
                        lambda: look_up._play_pokemon_cry(self.lookup_ui.current_pokemon_no)
                    )
                    self.lookup_ui.sprite_left_btn.clicked.connect(
                        lambda: look_up._navigate_pokemon(self.lookup_ui, self.pokedex, -1)
                    )
                    self.lookup_ui.sprite_right_btn.clicked.connect(
                        lambda: look_up._navigate_pokemon(self.lookup_ui, self.pokedex, 1)
                    )

        # Add autocomplete for Pokemon types
        from PokemonDatabase import TYPE_COLORS
        type_list = [type_name.capitalize() for type_name in TYPE_COLORS.keys()]
        type_list.sort()

        type_completer = QtWidgets.QCompleter(type_list)
        type_completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        type_completer.setCompletionMode(QtWidgets.QCompleter.PopupCompletion)
        ui.type.setCompleter(type_completer)

        ui.type.returnPressed.connect(
            lambda: handle_top(ui, self.pokedex, on_pokemon_click=on_top10_pokemon_click)
        )
        ui.battle_b1.clicked.connect(self.show_compete)
        ui.lookup_b1.clicked.connect(self.show_lookup)
        ui.raidCounters_b1.clicked.connect(self.show_raid_counters)
        ui.team_b1.clicked.connect(self.show_team_builder)
        ui.type_chart_b1.clicked.connect(self.show_type_chart)

        self.top10_window.show()

        # Close other windows but keep team_builder_window to preserve team data
        for attr in ("mainpage_window", "lookup_window", "raid_window", "battle_window"):
            window = getattr(self, attr)
            if window is not None:
                window.close()
                setattr(self, attr, None)

    def show_lookup(self):
        self.lookup_window = QtWidgets.QMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(self.lookup_window)
        self.lookup_ui = ui
        set_lookup_background(ui)

        # Load Pokemon #1 by default
        import look_up
        default_pokemon = self.pokedex.get_pokemon_by_number(1)
        if default_pokemon is not None and not default_pokemon.empty:
            poke_data = default_pokemon.iloc[0].to_dict()
            look_up._display_pokemon_data(ui, self.pokedex, poke_data)
            # Connect sprite click handler for cry sound
            ui.sprite.clicked.connect(lambda: look_up._play_pokemon_cry(ui.current_pokemon_no))
            # Connect carousel buttons (left/right arrows)
            ui.sprite_left_btn.clicked.connect(lambda: look_up._navigate_pokemon(ui, self.pokedex, -1))
            ui.sprite_right_btn.clicked.connect(lambda: look_up._navigate_pokemon(ui, self.pokedex, 1))

        # Add autocomplete for Pokemon names with Pokedex numbers
        conn = self.pokedex.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT pokemon, pokedex_no FROM pokedex ORDER BY pokedex_no")
        pokemon_list = [f"{row[0].capitalize()} (#{row[1]})" for row in cursor.fetchall()]
        conn.close()

        completer = QtWidgets.QCompleter(pokemon_list)
        completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        completer.setCompletionMode(QtWidgets.QCompleter.PopupCompletion)
        ui.lookup_line.setCompleter(completer)

        ui.lookup_line.returnPressed.connect(
            lambda: handle_lookup(ui, self.pokedex)
        )
        ui.battle_b1.clicked.connect(self.show_compete)
        ui.top_b1.clicked.connect(self.show_top10)
        ui.counters_b1.clicked.connect(self.show_raid_counters)
        ui.team_b1.clicked.connect(self.show_team_builder)
        ui.add_to_team_btn.clicked.connect(self._add_lookup_pokemon_to_team)

        self.lookup_window.show()
        self.lookup_window.setFocus()

        # Close other windows but keep team_builder_window to preserve team data
        for attr in ("mainpage_window", "top10_window", "raid_window", "battle_window"):
            window = getattr(self, attr)
            if window is not None:
                window.close()
                setattr(self, attr, None)

    def show_raid_counters(self):
        self.raid_window = QtWidgets.QMainWindow()
        ui = Ui_RaidCounters()
        ui.setupUi(self.raid_window)
        # NOTE: unlike look_up.py, raidcounters.py's own retranslateUi()
        # already calls set_background() internally (same pattern as
        # top10.py), so it doesn't need to be called again here.

        def on_raid_counter_click(pokemon_name):
            """When a counter pokemon is clicked, switch to lookup and display it."""
            self.show_lookup()
            if self.lookup_ui:
                import look_up
                poke_data = self.pokedex.get_pokemon_by_name(pokemon_name)
                if poke_data:
                    look_up._display_pokemon_data(self.lookup_ui, self.pokedex, poke_data)

                    # Set up sprite click handler and carousel buttons
                    try:
                        self.lookup_ui.sprite.clicked.disconnect()
                        self.lookup_ui.sprite_left_btn.clicked.disconnect()
                        self.lookup_ui.sprite_right_btn.clicked.disconnect()
                    except TypeError:
                        pass

                    self.lookup_ui.sprite.clicked.connect(
                        lambda: look_up._play_pokemon_cry(self.lookup_ui.current_pokemon_no)
                    )
                    self.lookup_ui.sprite_left_btn.clicked.connect(
                        lambda: look_up._navigate_pokemon(self.lookup_ui, self.pokedex, -1)
                    )
                    self.lookup_ui.sprite_right_btn.clicked.connect(
                        lambda: look_up._navigate_pokemon(self.lookup_ui, self.pokedex, 1)
                    )

        ui.raid_pokemon.returnPressed.connect(
            lambda: handle_raid_counters(ui, self.pokedex, on_pokemon_click=on_raid_counter_click)
        )
        ui.battle_b1.clicked.connect(self.show_compete)
        ui.lookup_b1.clicked.connect(self.show_lookup)
        ui.top_b1.clicked.connect(self.show_top10)
        ui.team_b1.clicked.connect(self.show_team_builder)
        ui.type_chart_b1.clicked.connect(self.show_type_chart)

        # Add autocomplete for Pokemon names with Pokedex numbers
        conn = self.pokedex.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT pokemon, pokedex_no FROM pokedex ORDER BY pokedex_no")
        pokemon_list = [f"{row[0].capitalize()} (#{row[1]})" for row in cursor.fetchall()]
        conn.close()

        completer = QtWidgets.QCompleter(pokemon_list)
        completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        completer.setCompletionMode(QtWidgets.QCompleter.PopupCompletion)
        ui.raid_pokemon.setCompleter(completer)

        self.raid_window.show()

        # Close other windows but keep team_builder_window to preserve team data
        for attr in ("mainpage_window", "lookup_window", "top10_window", "battle_window"):
            window = getattr(self, attr)
            if window is not None:
                window.close()
                setattr(self, attr, None)

    def show_compete(self):
        self.battle_window = QtWidgets.QMainWindow()
        ui = Ui_Battle()
        ui.setupUi(self.battle_window)

        def on_left_pokemon():
            """Load left pokemon when Enter is pressed."""
            name = ui.left_input.text().strip()
            if name:
                # Strip Pokedex number from autocomplete selection
                if " (#" in name:
                    name = name.split(" (#")[0]
                load_pokemon_card(ui, self.pokedex, name, "left")

        def on_right_pokemon():
            """Load right pokemon when Enter is pressed."""
            name = ui.right_input.text().strip()
            if name:
                # Strip Pokedex number from autocomplete selection
                if " (#" in name:
                    name = name.split(" (#")[0]
                load_pokemon_card(ui, self.pokedex, name, "right")

        def on_battle():
            """Handle battle button click."""
            handle_battle(ui, self.pokedex, self.battle_window)

        def on_randomize():
            """Randomize two pokemon and battle them."""
            import random

            # Get all pokemon from database
            conn = self.pokedex.get_connection()
            import pandas as pd
            all_pokemon = pd.read_sql("SELECT pokemon FROM pokedex", conn)
            conn.close()

            if len(all_pokemon) < 2:
                return

            # Pick two random pokemon
            random_pokemon = random.sample(list(all_pokemon['pokemon']), 2)

            # Fill in the inputs and load the pokemon
            ui.left_input.setText(random_pokemon[0])
            load_pokemon_card(ui, self.pokedex, random_pokemon[0], "left")

            ui.right_input.setText(random_pokemon[1])
            load_pokemon_card(ui, self.pokedex, random_pokemon[1], "right")

            # Start the battle
            handle_battle(ui, self.pokedex, self.battle_window)

        def on_left_sprite_click():
            """Navigate to lookup when left sprite is clicked."""
            left_name = ui.left_name.text()
            if left_name and left_name != "Pokemon 1":
                self.show_lookup()
                if self.lookup_ui:
                    import look_up
                    poke_data = self.pokedex.get_pokemon_by_name(left_name)
                    if poke_data:
                        look_up._display_pokemon_data(self.lookup_ui, self.pokedex, poke_data)

                        # Set up sprite click handler and carousel buttons
                        try:
                            self.lookup_ui.sprite.clicked.disconnect()
                            self.lookup_ui.sprite_left_btn.clicked.disconnect()
                            self.lookup_ui.sprite_right_btn.clicked.disconnect()
                        except TypeError:
                            pass

                        self.lookup_ui.sprite.clicked.connect(
                            lambda: look_up._play_pokemon_cry(self.lookup_ui.current_pokemon_no)
                        )
                        self.lookup_ui.sprite_left_btn.clicked.connect(
                            lambda: look_up._navigate_pokemon(self.lookup_ui, self.pokedex, -1)
                        )
                        self.lookup_ui.sprite_right_btn.clicked.connect(
                            lambda: look_up._navigate_pokemon(self.lookup_ui, self.pokedex, 1)
                        )

        def on_right_sprite_click():
            """Navigate to lookup when right sprite is clicked."""
            right_name = ui.right_name.text()
            if right_name and right_name != "Pokemon 2":
                self.show_lookup()
                if self.lookup_ui:
                    import look_up
                    poke_data = self.pokedex.get_pokemon_by_name(right_name)
                    if poke_data:
                        look_up._display_pokemon_data(self.lookup_ui, self.pokedex, poke_data)

                        # Set up sprite click handler and carousel buttons
                        try:
                            self.lookup_ui.sprite.clicked.disconnect()
                            self.lookup_ui.sprite_left_btn.clicked.disconnect()
                            self.lookup_ui.sprite_right_btn.clicked.disconnect()
                        except TypeError:
                            pass

                        self.lookup_ui.sprite.clicked.connect(
                            lambda: look_up._play_pokemon_cry(self.lookup_ui.current_pokemon_no)
                        )
                        self.lookup_ui.sprite_left_btn.clicked.connect(
                            lambda: look_up._navigate_pokemon(self.lookup_ui, self.pokedex, -1)
                        )
                        self.lookup_ui.sprite_right_btn.clicked.connect(
                            lambda: look_up._navigate_pokemon(self.lookup_ui, self.pokedex, 1)
                        )

        # Add autocomplete for Pokemon names with Pokedex numbers
        conn = self.pokedex.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT pokemon, pokedex_no FROM pokedex ORDER BY pokedex_no")
        pokemon_list = [f"{row[0].capitalize()} (#{row[1]})" for row in cursor.fetchall()]
        conn.close()

        completer = QtWidgets.QCompleter(pokemon_list)
        completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        completer.setCompletionMode(QtWidgets.QCompleter.PopupCompletion)
        ui.left_input.setCompleter(completer)
        ui.right_input.setCompleter(completer)

        ui.left_input.returnPressed.connect(on_left_pokemon)
        ui.right_input.returnPressed.connect(on_right_pokemon)
        ui.clear_button.clicked.connect(on_randomize)
        ui.battle_button.clicked.connect(on_battle)
        def on_left_cry():
            """Play cry for left Pokemon."""
            import look_up
            if hasattr(ui, 'current_pokemon_no_left'):
                look_up._play_pokemon_cry(ui.current_pokemon_no_left)

        def on_right_cry():
            """Play cry for right Pokemon."""
            import look_up
            if hasattr(ui, 'current_pokemon_no_right'):
                look_up._play_pokemon_cry(ui.current_pokemon_no_right)

        ui.left_sprite.clicked.connect(on_left_sprite_click)
        ui.right_sprite.clicked.connect(on_right_sprite_click)
        ui.left_cry_btn.clicked.connect(on_left_cry)
        ui.right_cry_btn.clicked.connect(on_right_cry)
        ui.lookup_b1.clicked.connect(self.show_lookup)
        ui.raid_b1.clicked.connect(self.show_raid_counters)
        ui.top_b1.clicked.connect(self.show_top10)
        ui.team_b1.clicked.connect(self.show_team_builder)
        ui.type_chart_b1.clicked.connect(self.show_type_chart)

        self.battle_window.show()

        # Close other windows but keep team_builder_window to preserve team data
        for attr in ("mainpage_window", "lookup_window", "top10_window", "raid_window"):
            window = getattr(self, attr)
            if window is not None:
                window.close()
                setattr(self, attr, None)

    def run(self):
        self.show_mainpage()
        sys.exit(self.app.exec_())


if __name__ == "__main__":
    PokedexApp().run()
