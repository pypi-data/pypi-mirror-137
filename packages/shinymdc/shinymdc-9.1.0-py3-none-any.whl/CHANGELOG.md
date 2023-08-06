# Changelog

All notable changes to this project will be documented in this file. See [standard-version](https://github.com/conventional-changelog/standard-version) for commit guidelines.

## [9.1.0](https://github.com/jayanthkoushik/mdc/compare/v9.0.0...v9.1.0) (2022-02-07)


### Features

* add `mathify` script to render latex math ([5384422](https://github.com/jayanthkoushik/mdc/commit/538442287a683ec381586dab8804d3864e5a4c35))
* allow reading input from stdin ([62e0b56](https://github.com/jayanthkoushik/mdc/commit/62e0b56d590a0fcbd29f96c77356831b7b85c69c))

## [9.0.0](https://github.com/jayanthkoushik/mdc/compare/v8.0.0...v9.0.0) (2021-12-14)


### ⚠ BREAKING CHANGES

* streamline code with new `corgy`

### Bug Fixes

* prevent error on output target being in nonexistent folder ([4ddd2a5](https://github.com/jayanthkoushik/mdc/commit/4ddd2a54ba282456704b49afb94a12c9d0118587))


* streamline code with new `corgy` ([a080baa](https://github.com/jayanthkoushik/mdc/commit/a080baa0c971f84e7b15a035202a42223245934b))

## [8.0.0](https://github.com/jayanthkoushik/mdc/compare/v7.1.1...v8.0.0) (2021-10-19)


### ⚠ BREAKING CHANGES

* change cache interface

### Features

* store build output for faster rebuilds ([cc9fc4a](https://github.com/jayanthkoushik/mdc/commit/cc9fc4ae9596da5b99c4085956e629e8c0f613f8))


* change cache interface ([0c657be](https://github.com/jayanthkoushik/mdc/commit/0c657be2795251c3e17c3e9371ee92567207d6b6))

### [7.1.1](https://github.com/jayanthkoushik/mdc/compare/v7.1.0...v7.1.1) (2021-10-11)


### Bug Fixes

* use textwidth/height instead of pagewidth/height in templates ([bb84872](https://github.com/jayanthkoushik/mdc/commit/bb84872540c48854958c8cc89e64b1553e078363))

## [7.1.0](https://github.com/jayanthkoushik/mdc/compare/v7.0.0...v7.1.0) (2021-09-21)


### Features

* support Python 3.7 and 3.8 ([99865f0](https://github.com/jayanthkoushik/mdc/commit/99865f079bc2d27f0471fbd576b80691b0c6366d))

## [7.0.0](https://github.com/jayanthkoushik/mdc/compare/v6.0.0...v7.0.0) (2021-09-17)


### ⚠ BREAKING CHANGES

* migrate to corgy (Python 3.9+ now required)

### Bug Fixes

* restrict temporary directory to be within pwd ([efaee3b](https://github.com/jayanthkoushik/mdc/commit/efaee3bd00ab4940fd53af4e86fdd1cbcecea182))
* update templates to fix issues caused by pandoc/crossref updates ([13db53a](https://github.com/jayanthkoushik/mdc/commit/13db53a1c087bdd26a37efb0d90ff26d5f793bc6))


* migrate to corgy (Python 3.9+ now required) ([322d19b](https://github.com/jayanthkoushik/mdc/commit/322d19b45f3f1a686f8e38d11832a89a322ffe4f))

## [6.0.0](https://github.com/jayanthkoushik/mdc/compare/v5.2.0...v6.0.0) (2021-01-05)


### ⚠ BREAKING CHANGES

* **templates:** update simple/stylish fonts

### Features

* **templates:** update simple/stylish fonts ([4a1fb44](https://github.com/jayanthkoushik/mdc/commit/4a1fb4412afa4581974508ee7ba0973613131891))


### Bug Fixes

* **templates:** enable french spacing ([9f7bfde](https://github.com/jayanthkoushik/mdc/commit/9f7bfde430ec271058385531d42ba5a15ccf6bd4))
* **templates:** set max width/height for figures ([839f216](https://github.com/jayanthkoushik/mdc/commit/839f216521a9d0cd91eefbd04f0f18c0faf9d6a2))

## [5.2.0](https://github.com/jayanthkoushik/mdc/compare/v5.1.0...v5.2.0) (2020-10-11)


### Features

* add appendix support ([0518ecf](https://github.com/jayanthkoushik/mdc/commit/0518ecfa85e65c8ffc6a14d3e6de88473feb384c))
* add template for stubs ([05868f4](https://github.com/jayanthkoushik/mdc/commit/05868f49aacf01631ea9520c7491a432c4e0497b))

## [5.1.0](https://github.com/jayanthkoushik/mdc/compare/v5.0.0...v5.1.0) (2020-10-10)


### Features

* allow disabling read from .mdc folder ([ac03a73](https://github.com/jayanthkoushik/mdc/commit/ac03a73cb908c637bf88ce636f09e2b721930a22))


### Bug Fixes

* **templates:** maintain aspect ratio of figures ([cbe0023](https://github.com/jayanthkoushik/mdc/commit/cbe002391130296c16b3781cba0f2f5c89650b04))
* **templates:** provide italics as bold for garamond ([0ddc8a9](https://github.com/jayanthkoushik/mdc/commit/0ddc8a95b39298985cd45f3509f2ff9ed74add65))
* **templates:** use mbox for names ([9e6c5c5](https://github.com/jayanthkoushik/mdc/commit/9e6c5c541ff4e5d149a77580f78ebb1ce9a67517))
* **templates:** workaround pandoc multiline tables ([cc7455b](https://github.com/jayanthkoushik/mdc/commit/cc7455bfcc21bf081f356bd2f20a91af8f88e044))
* allow endfirsthead to be absent in tables ([ea1f4d5](https://github.com/jayanthkoushik/mdc/commit/ea1f4d52860e0e0e57eb48bf194dd1bb2dcf9ecf))
* handle tables when writing to stdout ([ccb06d9](https://github.com/jayanthkoushik/mdc/commit/ccb06d9fe72ae7f9a55a6b7cb8d803208c0eb44f))

## [5.0.0](https://github.com/jayanthkoushik/mdc/compare/v4.0.0...v5.0.0) (2020-09-29)


### ⚠ BREAKING CHANGES

* do complete rehaul ([609c171](https://github.com/jayanthkoushik/mdc/commit/609c171e700a82e4511dab8a0ccaf181b59550ae))

	Major changes:
	 1. Fix table processing: use standard table env instead of longtable
	 2. Disable pandoc wrapping
	 3. Change default pandoc source format to plain markdown
	 4. Change default sans serif font from Futura to Source Pro Sans
	 5. Add functionality to two column templates for switching between
			figure/figure* and table/table*
	 6. Fine-tune float placement
	 7. Add test file test/main.md

## [4.0.0](https://github.com/jayanthkoushik/mdc/compare/v3.1.0...v4.0.0) (2020-09-08)


### ⚠ BREAKING CHANGES

* use standard-version instead of bumpversion

### Bug Fixes

* correct version import ([6aaa7a8](https://github.com/jayanthkoushik/mdc/commit/6aaa7a8b89a55b296f261ae5bc814db4bfcf4bfe))
