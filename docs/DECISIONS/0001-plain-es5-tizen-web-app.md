# 0001. Plain ES5 Tizen web app without a framework or build step

- Status: Accepted
- Date: 2026-10-25

## Context
The target TVs (2018, Tizen 4.0) run Chromium M56 and have little memory. The
launcher is restarted from scratch every time the user returns to it, so
start-up time matters more than developer convenience.

## Decision
Ship one `index.html` with inline ES5 and plain CSS, packaged directly with
`tizen package`. No framework, no transpiler, no bundler.

## Alternatives considered
- Tizen .NET or native app: needs a different toolchain and certificate path
  and offers no extra capability a launcher can use on this TV (see
  `HOME_REPLACEMENT.md`).
- Modern JS with a transpiler: adds a build step and size for a few hundred
  lines of code.

## Consequences
Easy to read, package and debug on the device. Modern syntax and CSS features
(grid, ES modules) are unavailable; contributors must keep to ES5.
