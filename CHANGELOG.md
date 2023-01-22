# Changelog

<!--next-version-placeholder-->

## v2.0.3 (2023-01-21)
### Fix
* **notify.py:** Replace assert check with an if statement (deepsource) ([`897d2a6`](https://github.com/tim83/timtools/commit/897d2a6c2797f21080b485d8776a622e1a4da52a))

## v2.0.2 (2023-01-12)
### Fix
* **notify.py:** Make bot creation compatible with async version of python-telegram-bot ([`5248735`](https://github.com/tim83/timtools/commit/5248735a7cefbdba20ec089b90d3f32da62a3f47))

## v2.0.1 (2022-12-14)
### Performance
* **bash.py:** Use build-in dict.update() instead of manually checking keys ([`077bbf3`](https://github.com/tim83/timtools/commit/077bbf3a67d56a9d574559183793a959b399bbc1))

## v2.0.0 (2022-12-14)
### Feature
* **bash.py:** Add the ability to pass extra arguments directly to subprocess.Popen ([`3837433`](https://github.com/tim83/timtools/commit/383743338f2c4c77616d3f1da2989ccc6ff6e55c))
* **bash.py:** Remove run_bash link to run and add deprecation warning ([`853e955`](https://github.com/tim83/timtools/commit/853e95581d650b68da3d15094fb95cb38e4a4aef))

### Breaking
* timtools.bash.run_bash will no longer work and instead just give a DeprecationWarning  ([`853e955`](https://github.com/tim83/timtools/commit/853e95581d650b68da3d15094fb95cb38e4a4aef))

## v1.6.2 (2022-11-13)
### Fix
* **settings.py:** Fix dummy tests and add tests for it ([`d5b6789`](https://github.com/tim83/timtools/commit/d5b6789e61285375af277fc898e4b7851abcbd82))

## v1.6.1 (2022-11-13)
### Fix
* **settings.py:** Allow programs to use a dummy config in tests ([`4ca3b21`](https://github.com/tim83/timtools/commit/4ca3b21ba9f6707dae4cb06052d3cf59e64f357d))

## v1.6.0 (2022-10-29)
### Feature
* **settings.py:** Allow checking multiple config files ([`8348d84`](https://github.com/tim83/timtools/commit/8348d84e2760704e1e9d2a9856ee2f64bf0a5456))

## v1.5.0 (2022-10-26)
### Feature
* **settings.py:** Allow using global config ([`c6ebc02`](https://github.com/tim83/timtools/commit/c6ebc02968d81e22cb9a4ee5e42fdc840f788b7d))

## v1.4.0 (2022-09-22)
### Feature
* **notify.py:** Add commandline interface for notify ([`19521d8`](https://github.com/tim83/timtools/commit/19521d89948be110a9918dae141dcff6963804a4))

## v1.3.5 (2022-09-22)
### Fix
* **notify.py:** Fix missing import for logger ([`044b36b`](https://github.com/tim83/timtools/commit/044b36bcba118514b0541a5ce4d11b5bb5400d60))
* **notify.py:** Fix bad quotes ([`86bf26a`](https://github.com/tim83/timtools/commit/86bf26a4610f3998bea52850e3a3cd27811e8bdf))

## v1.3.4 (2022-05-17)
### Fix
* **notify.py:** Fix use of Path objects for sending files over telegram ([`28594ed`](https://github.com/tim83/timtools/commit/28594ed7a217b2de9635a17cff85f5c6b25f1057))

## v1.3.3 (2022-04-06)
### Fix
* **locations.py): Make pylint happy\nfix(.pre-commit-config.yml:** Update flake8 and disable unit tests on commit ([`bc4060b`](https://github.com/tim83/timtools/commit/bc4060be4cd1895e2b78005d6c67de80a1a7da01))

## v1.3.2 (2022-03-26)
### Fix
* Limit to python3.8 ([`48c49f8`](https://github.com/tim83/timtools/commit/48c49f8874b2e042991432ed090e26b055e3f067))
* Allow python 3.6 ([`f6bccca`](https://github.com/tim83/timtools/commit/f6bcccabad3c3866b60656ae80564cda85437633))

## v1.3.1 (2022-03-17)
### Fix
* **bash.py:** Fix timeout by not using with ([`af8a0e2`](https://github.com/tim83/timtools/commit/af8a0e206565c2da59fe33c34ae34a9aa1872c86))

## v1.3.0 (2022-03-17)
### Feature
* Use pylint ([`25beabb`](https://github.com/tim83/timtools/commit/25beabb647adbcf03da7ca586bc054e4f31e8c29))

### Fix
* **ci.yml:** Typo ([`570c1bd`](https://github.com/tim83/timtools/commit/570c1bddc0d9ea32062d4510b102a70b771f07db))

## v1.2.1 (2022-03-01)
### Fix
* **__init__.py:** Prevent circular import ([`b229b58`](https://github.com/tim83/timtools/commit/b229b58b422455bfc4ce7573b9bc111227f5b688))

## v1.2.0 (2022-02-19)
### Feature
* Add automated CI ([`f2e555e`](https://github.com/tim83/timtools/commit/f2e555ebcfbaea425438262737cc8c3e072ba8aa))

### Fix
* **notify.py:** Prevent immediate errors when no config is present ([`fc42d42`](https://github.com/tim83/timtools/commit/fc42d429d5bb52f96855721ccb3c6772514d5e44))
* Enable importing with missing config ([`ca3a7f2`](https://github.com/tim83/timtools/commit/ca3a7f2abe70be83ff2935ec4fba247a32558e94))
