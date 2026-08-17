# Pokédex App

A comprehensive PyQt5 desktop application for Pokémon enthusiasts. Look up any Pokémon's stats, browse by type, get raid counter recommendations, simulate battles, and build teams with persistent storage.

## Features

### 🔍 Pokémon Lookup
- Search any Pokémon by name or Pokédex number
- Trading-card-style profile display with stats, types, and abilities
- Autocomplete search with Pokédex numbers
- Arrow key navigation for browsing
- Play Pokémon cries with one click

### 📊 Type Browsing
- Browse top 10 Pokémon for any type
- Type-themed backgrounds
- Interactive type effectiveness chart
- Autocomplete type suggestions

### ⚔️ Raid Counters
- Get recommended raid counters for any Pokémon
- Weighted scoring algorithm considering attack and defense
- Type advantage analysis for both types
- Autocomplete Pokémon search

### 🎮 Battle Arena
- Simulate battles between two Pokémon
- Interactive damage calculator showing type matchups
- Type effectiveness visualization
- Randomize button for quick battles
- Click sprites to view full Pokémon profiles

### 🛠️ Team Builder
- Build custom teams of up to 6 Pokémon
- Adjustable level slider (1-100) for each Pokémon
- Save and load teams from disk (JSON persistence)
- Type coverage analysis showing strengths and weaknesses
- Export teams as PDF reports with sprites
- Sprite display for visual team composition

### 🎨 UI/UX
- Dark mode toggle with persistent preference
- Smooth animations and transitions
- Click depth effects on all buttons
- Hover effects on cards and images
- Responsive design elements
- Background music player
- Professional gradient-based design

## Technical Stack

- **Framework:** PyQt5 (Python GUI)
- **Database:** SQLite with PokéAPI data
- **Audio:** pygame mixer for Pokémon cries and background music
- **PDF Generation:** ReportLab for team exports
- **Data Source:** Official PokéAPI
- **Architecture:** Signal-slot event handling, MVC-inspired patterns

## Installation

### Requirements
- Python 3.8+
- PyQt5
- requests
- pygame
- reportlab
- pillow (PIL)
- pandas

### Setup

1. **Clone the repository:**
```bash
git clone https://github.com/tczerwin/Pokemon.git
cd Pokemon
```

2. **Install dependencies:**
```bash
pip install PyQt5 requests pygame reportlab pillow pandas
```

3. **Run the application:**
```bash
python main.py
```

## Usage

### Main Menu
Launch the app to access five main features:
- **Look Up** - Search and view individual Pokémon
- **Top 10** - Browse top Pokémon by type
- **Raid Counters** - Get counter recommendations
- **Battle!** - Simulate battles between two Pokémon
- **Team Builder** - Create and save Pokémon teams

### Look Up Page
1. Enter a Pokémon name or number
2. View stats, types, and abilities
3. Click the sprite to hear the Pokémon cry
4. Use arrow buttons to navigate nearby Pokémon

### Type Browsing
1. Select a type from the dropdown
2. View top 10 Pokémon of that type
3. Click any Pokémon to jump to its lookup page
4. View type effectiveness chart (top right)

### Raid Counters
1. Enter a raid boss Pokémon name
2. Get ranked counter recommendations
3. See type advantages displayed for each counter
4. Click counters to view their full profiles

### Battle Arena
1. Enter two Pokémon names
2. Click "Battle!" to see the winner
3. Click "Damage Calculator" for detailed damage analysis
4. Use "Randomize" for a quick random battle
5. Click sprites to view profiles

### Team Builder
1. Click "Click to add" on each slot
2. Search for a Pokémon name
3. Adjust level with slider (1-100)
4. **Save Team** - Save to disk with a custom name
5. **Load Team** - Load previously saved teams
6. **Type Coverage** - Analyze team strengths/weaknesses
7. **Export PDF** - Generate a visual team report

## File Structure

```
Pokemon/
├── main.py                 # Application entry point & window management
├── mainpage.py            # Main menu UI
├── look_up.py             # Pokémon lookup page
├── top10.py               # Type browsing page
├── raidcounters.py        # Raid counter recommendations
├── battle.py              # Battle arena simulator
├── team_builder.py        # Team builder UI
├── type_chart.py          # Type effectiveness chart
├── PokemonDatabase.py     # Database & API integration
├── teams.py               # Team persistence manager
├── img/                   # Images and resources
│   ├── pokemon.png
│   ├── ProfPic2026.png
│   ├── Pokemon.mp3
│   └── poke_background.jpg
└── README.md              # This file
```

## Key Algorithms

### Raid Counter Scoring
Combines attack power and defensive matchups:
- **Attack Score:** 70% weight on attacker's attack stat
- **Type Advantage:** 1.5x multiplier for super-effective attacks
- **Defense:** 1.25x multiplier for resisting opponent's attacks
- **Final Score:** Attack × Type Advantage × Defensive Multiplier

### Damage Calculator
Simplified damage formula based on:
- Attack stat vs. Opponent's defense
- Special attack vs. Special defense
- Type effectiveness multipliers
- Estimated damage range output

### Type Advantage System
- Hardcoded advantage dictionary covering all 18 types
- Super-effective attacks: 1.5x damage
- Resistant types: 0.67x damage reduction
- Checks both types for dual-type Pokémon

## Features in Detail

### Autocomplete Search
- Case-insensitive matching
- Shows Pokémon names with Pokédex numbers
- Popup-style completion menu
- Available on: Lookup, Top 10, Raid Counters, Battle, Team Builder

### Team Persistence
Teams saved as JSON:
```json
{
  "name": "My Team",
  "pokemon": [
    {"name": "Pikachu", "level": 50},
    {"name": "Charizard", "level": 75},
    ...
  ]
}
```

### PDF Export
Generated PDFs include:
- Team name and creation date
- Individual Pokémon sprites and stats
- Type information
- High-quality formatting suitable for sharing

### Background Music
- Loops continuously during app usage
- Configurable volume (20%)
- PyQt5 QMediaPlayer integration
- Supports .mp3 format

## Customization

### Change Background Music
Replace `img/Pokemon.mp3` with your own audio file.

### Modify Type Colors
Edit `TYPE_COLORS` dictionary in `PokemonDatabase.py`:
```python
TYPE_COLORS = {
    'fire': '#FF5722',
    'water': '#2196F3',
    ...
}
```

### Adjust UI Colors
Modify button and widget stylesheets in respective page files.

## Known Limitations

- Requires internet connection for initial Pokémon cry downloads
- Cries cached temporarily; clearing may require re-download
- PDF export requires ReportLab and Pillow
- Windows path handling may differ; tested primarily on macOS

## Future Enhancements

- [ ] Move type favorites/bookmarks
- [ ] Advanced stat calculator
- [ ] Generation filtering
- [ ] Ability descriptions
- [ ] Shiny sprite variants
- [ ] Gender differences
- [ ] Web-based version
- [ ] Mobile companion app

## Performance

- Initial load: ~2-3 seconds (database population)
- Pokémon lookup: <100ms
- Battle calculation: <50ms
- PDF export: 2-5 seconds depending on team size

## Troubleshooting

**Issue:** "Pokemon.mp3 not found"
- Solution: Ensure `img/Pokemon.mp3` exists in the project directory

**Issue:** Pokémon cries not playing
- Solution: Check internet connection (required for first-time cry download)
- Verify pygame is properly installed: `pip install pygame`

**Issue:** PDF export fails
- Solution: Install missing libraries: `pip install reportlab pillow`

**Issue:** Database connection errors
- Solution: Verify SQLite3 is installed and accessible

## Contributing

Contributions welcome! Areas for improvement:
- UI/UX enhancements
- Performance optimization
- Additional Pokémon data fields
- Bug fixes and error handling

## License

MIT License - Feel free to use, modify, and distribute.

## Author

Taylor Czerwinski

## Acknowledgments

- **PokéAPI** - Comprehensive Pokémon data source
- **PyQt5** - Cross-platform GUI framework
- **The Pokémon Company** - Original Pokémon data and media

## Contact

For questions, issues, or suggestions:
- Email: taylorczerwinski@gmail.com
- GitHub: [@tczerwin](https://github.com/tczerwin)
- LinkedIn: [Taylor Czerwinski](https://www.linkedin.com/in/taylor-czerwinski-bb0048156)
