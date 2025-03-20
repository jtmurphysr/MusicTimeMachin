# Changelog

All notable changes to the Music Time Machine project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.1] - 2023-10-28

### Added
- Added today's date to the default SoundCloud EDM playlist name for better organization

### Changed
- Updated dependencies to their latest versions:
  - beautifulsoup4 from 4.12.2 to 4.13.3
  - lxml from 4.9.3 to 5.3.1
  - requests from 2.31.0 to 2.32.3
  - spotipy from 2.23.0 to 2.25.1
  - python-dotenv from 1.0.0 to 1.0.1
  - Added additional dependency specifications for better compatibility

### Fixed
- Fixed a string formatting bug in the SoundCloud default playlist name that prevented the date from being displayed correctly

## [2.0.0] - 2023-10-27

### Added
- Support for SoundCloud top EDM charts
- Object-oriented design with base scraper class
- Modular architecture with scrapers package
- User interface for selecting chart source
- Track list saving to text files
- Return of playlist URL to user after creation
- Improved error handling and user feedback
- CHANGELOG.md to track project changes

### Changed
- Complete code refactoring to use class-based architecture
- Updated Spotify redirect URI from localhost to 127.0.0.1
- Improved README with more comprehensive documentation
- Enhanced user interaction flow
- Better error handling throughout the application

### Fixed
- Fixed potential issues with Spotify authentication
- Improved error handling for chart scraping

## [1.0.0] - 2023-10-20

### Added
- Initial release
- Billboard Hot 100 chart scraping
- Spotify song matching
- Playlist creation functionality
- Basic command-line interface
- Environment variable management 