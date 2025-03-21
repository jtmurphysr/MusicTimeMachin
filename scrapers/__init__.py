"""
Music Time Machine - Scrapers Package

This package contains scraper classes for different music chart sources.
It provides a modular approach to adding support for various music charts.

The scrapers are responsible only for data extraction, with playlist creation
handled by the separate PlaylistBuilder class. This separation of concerns makes
the system more maintainable and extensible.

Available Scrapers:
- BillboardTop100Scraper: Scrapes Billboard Hot 100 charts for any date
- SoundCloudEDMScraper: Scrapes the current SoundCloud Top EDM charts
- AppleMusicEDMScraper: Scrapes the current Apple Music EDM Hits playlist
- TraxsourceDeepHouseScraper: Scrapes the current Traxsource Deep House top tracks

All scrapers inherit from BaseMusicScraper to ensure a consistent interface.
""" 