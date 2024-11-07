# Funbiance

Funbiance enhances your entertainment experience by creating dynamic ambient lighting effects that match the colors displayed on your screen. Perfect for movies, gaming, or any immersive visual content.

## Features

- Real-time color sampling and synchronization
- Support for non-primary monitor displays
- Integration with Philips Hue smart lighting
- Native Linux desktop support (KDE Wayland tested)

## Requirements

- Linux desktop environment with XDG Desktop Portal support (KDE tested)
- Python 3.x
- Philips Hue bridge and compatible lights (optional)
- Multiple monitors for display sync (optional)

## Installation

Currently only available as source code. To install and run:

```bash
git clone https://github.com/npapke/funbiance.git
cd funbiance
pip install -r requirements.txt
python -m funbiance
```

## Usage
Documentation coming soon

## Development Status
This project is under active development. Features and APIs may change frequently. Currently provided as source code only with no release artifacts.

### Major outstanding issues
There is no way to enrol a Hue bridge from the application.  Enrollment has to be done manually.
See [Jupyter Notebook](doc/streaming_experiment.ipynb) for an example of how do this.

Selection of the Hue Entertainment Area is not yet implemented.  It is hardcoded.  See [ambiance_hue.py](funbiance/ambiance_hue.py).

### Future Enhancements
All lights in the entertainment area are currently driven to the same color.  This should be changed so that each light has its own color
based on screen region.


## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## Known Issues
Currently only tested on KDE Plasma desktop environment
Additional desktop environments need testing/validation
More details to come as development progresses

## License
License details to be added

## Acknowledgments
To be added

---

Note: This project is in active development. Documentation will be updated as features are implemented and stabilized.

For more information or to report issues, please visit the GitHub repository.