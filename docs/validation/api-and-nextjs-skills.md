# API and Next.js skill validation scenarios

Use these scenarios to evaluate the canonical skills, not to create a test suite
for a consuming application. Use minimal fixtures in temporary environments.
Give an evaluator the same request and fixture before and after a guidance change;
keep the expected decisions below out of the evaluator's prompt. Record its actual
decisions and artifacts separately from metadata/link checks.

| ID | Request and fixture | Expected decision |
| --- | --- | --- |
| B4.1 | Extend an Express app with routes/controllers/services and direct Prisma calls. | Preserve that organization; do not introduce repositories or classes. |
| B4.2 | Extend an API with a different functional folder arrangement. | Reuse its existing boundaries rather than impose the example's folders. |
| B6.1 | Implement a POST currently accepting a Prisma input type with arbitrary relations. | Define a runtime-validated HTTP contract with allowed fields and explicitly map it to persistence. |
| B4.3 | Extend protected routes using typed `res.locals.user`. | Reuse and type that request context; locals are not automatically an HTTP response. |
| B4.4 | Extend protected routes using typed `req.user`. | Preserve that context rather than migrate it to locals. |
| B6.2 | An authorized administrator creates a target user with a role field. | Derive caller identity from verified context; validate the target role and permission to assign it. |
| B2 | Add a custom profile route alongside a library's native signup/profile/email/delete/credential routes. | Map both sets of mutation paths and apply product policies without disabling all native routes by default. |
| B3 | Login overlaps deactivation and session revocation. | Inspect session insertion, revocation, hooks, caches, and transaction boundaries; an initial activity check alone is insufficient. |
| B2.1 | General and authentication limiters both return `429`. | Inspect scope, units, overrides, storage, and `Retry-After`; retain protection during verification. |
| B5 | Only the API package needs a dependency or Prisma setup change; frontend has a separate manifest/lockfile. | Use the consuming package's dependency and migration workflow; preserve applied migrations and generated output. |
| B1/F2.1 | The user excludes automated tests; a manifest has a test command but no test files. | Run applicable static checks and safe behavior checks; report missing/unrun automation without creating a suite or changing CI gates. |
| B1/F2.2 | A relevant automated suite exists and no scope override is given. | Run relevant tests and required repository checks; report actual results. |
| F1.1 | Next.js SSR and browser access a separate cookie API with different public/internal URLs and custom session fields. | Reuse the auth client, configure browser credentials, inspect cookie/origin policy, forward only intended credentials to a trusted backend, and validate/derive additional session fields. |
| F1.2 | Next.js uses a token or another existing authentication integration. | Preserve it; do not force cookies, a particular library, or global state. |
| B4.5 | Business models exist but CRUD endpoints do not. | Inspect registered routes and behavior; do not claim endpoints exist merely because schemas do. |

## Repository checks

- Run `python scripts/validate.py` and `python -m unittest discover -s tests -v`
  (use `python3` if that is the available Python executable).
- Check all relative reference paths and route every new reference from its
  entrypoint. Preserve skill names, frontmatter, and existing reference paths.
- Review fragments against the declared framework version and label them as
  adaptable examples, not complete applications.
- Keep consuming-project roles, paths, package versions, and release-phase test
  decisions out of universal guidance.
- For distribution checks, install both skills into a temporary repository with
  `--target both`, compare both copies with the canonical files, and remove only
  fixtures created for that check.

Publication and updating real consuming repositories are separate release steps.
Do not treat repository checks or a scenario review as proof of runtime behavior
in those applications.

## Guidance evaluation — 2026-09-26

A read-only evaluator received six combined scenarios covering the cases above
and read the current skills before edits. It then reread the updated backend and
frontend guidance separately using the same scenario inputs. The implementation
plan and this expected-decision table were withheld from that evaluator.

| Scenario group | Baseline observation | Decision after the update |
| --- | --- | --- |
| Express structure and identity | Convention preservation implied the right choice, but context alternatives and schema-only routing were implicit. | Reuse typed locals or request identity, trace actual route registration, and preserve existing boundaries. |
| Target roles and HTTP input | Caller versus target roles was ambiguous; Prisma input and native auth routes needed additional judgment. | Authorize the actor, validate the target role, map permitted HTTP fields, and inventory native mutation paths. |
| Sessions and rate limits | Concurrency guidance was generic; lifecycle races and overlapping limiters were absent. | Trace session insertion/revocation/hooks/caches and limiter scope/storage/units without assuming an initial check solves the race. |
| Package and Prisma setup | Package/lockfile ownership and generator configuration were implicit. | Inspect the consuming package and installed Prisma setup; distinguish validation, generation, migration creation, and application. |
| Verification scope | Gates did not explicitly resolve exclusions or distinguish scripts from suites. | Honor an explicit exclusion with applicable static/safe behavior checks, or run the relevant existing suite without an override; disclose actual results. |
| Next.js authentication | SSR forwarding, deployment URLs, cookie policy, and custom fields required extra judgment. | Reuse the client, separate public/internal configuration, verify cookie availability and trusted forwarding, and preserve token alternatives. |

The evaluator reported no material remaining scenario gaps; a separate final
review found no material plan or technical inconsistencies. These results assess
guidance retrieval and proposed decisions from textual fixtures, not completed
application implementations, runtime behavior, or repeated behavioral benchmarks.

Repository verification passed using `python3`: metadata validation for all three
skills, all 14 existing unit tests, relative reference existence/routing, unchanged
frontmatter, and `git diff --check`. Temporary installation of both updated skills
into both targets matched every canonical file; repeating installation reported
all four copies as up to date. No real consuming repository was synchronized.
