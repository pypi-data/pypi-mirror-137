# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.2] - 2022-02-03
### Fixed
- Non-existing files in the public namespace erroneously raised interal server errors.

## [0.2.1] – 2021-12-07
### Changed
- Allow Django 4.0

## [0.2.0] - 2021-10-24
### Changed
- Provide mechanism to make files in a public namespace accessible without a token.

## [0.1.2.post1] - 2021-05-17
### Changed
- Amend mistakes in changelog

## [0.1.2] - 2021-05-17
### Changed
- Combine timestamp into token parameter
- (Dev) Move settings handling into separate module

## [0.1.1] - 2021-05-16
### Fixed
- Fall back to current time if file does not exist to get mtime

## [0.1.0] - 2021-05-16
### Added
- Initial release, as described in readme

[Unreleased]: https://edugit.org/AlekSIS/libs/django-titofisto/-/tree/master
[0.1.0]: https://edugit.org/AlekSIS/libs/django-titofisto/-/tags/0.1.0
[0.1.1]: https://edugit.org/AlekSIS/libs/django-titofisto/-/tags/0.1.1
[0.1.2]: https://edugit.org/AlekSIS/libs/django-titofisto/-/tags/0.1.2
[0.1.2.post1]: https://edugit.org/AlekSIS/libs/django-titofisto/-/tags/0.1.2.post1
[0.2.0]: https://edugit.org/AlekSIS/libs/django-titofisto/-/tags/0.2.0
[0.2.1]: https://edugit.org/AlekSIS/libs/django-titofisto/-/tags/0.2.1
[0.2.2]: https://edugit.org/AlekSIS/libs/django-titofisto/-/tags/0.2.2
