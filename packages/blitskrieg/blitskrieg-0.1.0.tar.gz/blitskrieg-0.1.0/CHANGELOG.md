# Changelog
All notable changes to this project will be documented in this file.

The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0]

### Added
- protobuf definition
- gRPC server
- dockerization and compose files
- `unix_helper` utility script
- support for bitcoind
- support for boltlight
- support for c-lightning
- support for eclair
- support for electrs
- support for electrum
- support for lnd
- `Blitskrieg` service: `CreateStack`, `GetInfo`, `RemoveStack`
- `Bitcoin` service: `GetAddress`, `GenTransactions`, `MineBlock`, `Send`
- `Lightning` service: `FundNodes`
- `bli`: a CLI for blitskrieg with bash completion

[Unreleased]: https://gitlab.com/hashbeam/blitskrieg/compare/0.1.0...develop
[0.1.0]: https://gitlab.com/hashbeam/blitskrieg/compare/6d39b47f...0.1.0
