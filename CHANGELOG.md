# Changelog

All notable changes to the Music Time Machine project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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