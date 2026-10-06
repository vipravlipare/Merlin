# Sprint 0: what the setup teaches

Setup gives you a repeatable place to build and a way to detect mistakes. It does not build the application. Assistant-prepared infrastructure is useful, but you should say “I reviewed and learned this setup” until you personally explain, modify and verify it. Your reported 34/35 quiz result is encouraging evidence; the missed concept, practical explain-back and whiteboard still matter.

## Each part, its app value and the engineering lesson

| Part | Why the future app needs it | SWE / system-design understanding to demonstrate |
|---|---|---|
| One Ubuntu/WSL checkout | Code, Python environments and Linux tools agree on one filesystem. | Distinguish the Windows host, Linux environment and editor. Linux parity reduces platform differences; it does not guarantee all-device portability. Explorer and VS Code WSL access the same files. |
| Git and GitHub | Changes can be reviewed, recovered and shared. CI tests an identifiable commit. | Commit is local history, push publishes it, clone fetches committed files. Ignored/untracked local state is absent from a clone. Review before publication. |
| Jira and the schedule | Work has a visible next outcome and bounded scope. | Track acceptance evidence, limit WIP and stop at time caps. A task is Done because its checks pass, not because its title exists. Unknown actual minutes remain unknown. |
| Account MFA and SSH | Protect the accounts used to host work and changes. | MFA resists stolen-password use; GitHub SSH authenticates Git operations only. Jira/browser authentication is separate. Keep recovery material private. |
| Python/uv and Node/pnpm | Predictable tool versions and dependencies support later backend/frontend work. | Python/Node are runtimes; uv/pnpm manage environments/packages. A lock records resolution, but does not install packages or prove features. We currently have no application dependencies. |
| Docker images and containers | Databases can run without installing their server packages into Ubuntu. | An image is a packaged filesystem and startup metadata; a container is its running instance. Containers share a host kernel; they are not complete separate virtual machines. Pins prevent silent image drift. |
| Docker Compose | Services, network, ports, limits and volumes have one committed contract. | Compose declares how services run together. Service DNS is for containers; published loopback ports are for Ubuntu clients. Health dependencies are different from application authentication. |
| PostgreSQL | Planned durable notes/tasks/owner relationships need constraints and transactions. | Relational storage uses rows, tables, keys and relationships. PostgreSQL is the server; psql is a client. Commit/rollback control an all-or-nothing group of writes. Per-user authorization is still future code. |
| Redis | A separate disposable service is ready for a later justified cache or queue use. | Caching holds reusable results to avoid repeated work. A cache can be lost without losing authoritative data. PONG proves response, not application caching or durability. Current Redis snapshot/AOF writes are disabled. |
| Named volumes | Container replacement must not erase the database. | Containers and persisted data have different lifetimes. Prove the same volume and cluster return; a healthy new empty database is not retention. A volume is not a backup; restore testing remains separate. |
| .env and loopback | Private local inputs stay out of source control; remote access is limited. | Config/secret boundaries are explicit. Loopback means local-only binding, not protection from other local processes or Docker administrators. Existing database passwords do not change when initialization variables change. |
| Health and negative tests | Detect availability and incorrect access rules before feature work. | Readiness, authentication and retention are separate hypotheses. Correct credentials must succeed and wrong ones must explicitly be rejected; a timeout is not evidence of password security. |
| Doctor | A repeatable diagnostic shows the first failed setup boundary. | Return a failing exit status for required failures, safe fixes without secrets, and honest N/A for unbuilt features. Automation must be tested against failure cases, not just the happy path. |
| README and SETUP | Someone else can understand scope and repeat startup. | Document prerequisites, committed inputs, private configuration, exact commands, cleanup and limits. Public claims must match observed implementation. |
| CI | Every pushed commit gets independent setup checks in a clean runner. | Pin tools/actions, use minimal permissions and synthetic credentials, avoid private learner volumes, and clean up the runner's resources. A green setup workflow does not certify an unbuilt API. |
| Unmodified fresh clone | Tests whether hidden working-directory state was accidentally required. | Follow committed instructions without editing source/Compose. Install documented host prerequisites separately, generate new private inputs, isolate resources, and record the exact commit and results. |
| Review, rituals and deferrals | Keeps the project small enough to finish and safe to resume. | Reserve time, swap scope instead of adding hours, name blockers and distinguish operational completion from learning mastery. AWS, DSA and optional tools retain their stated deferrals. |

## How these pieces connect

Windows hosts Ubuntu/WSL and Docker Desktop. VS Code and Codex operate on `/home/vipra/Merlin`. Git records source/configuration/docs; uv selects Python and its locked environment. Compose starts PostgreSQL/Redis on a private container network and publishes loopback ports. PostgreSQL keeps its files in a named volume; Redis is disposable under the current policy. A future learner-written API will connect through these boundaries and must enforce authentication, ownership and transactions itself. Doctor tests local setup; CI runs independent checks against synthetic isolated resources. A fresh clone proves the documented path does not secretly require the original working folder.

The main design decision is one local development environment and a small number of clear responsibilities. It costs less operational effort than multiple backend services or several overlapping databases. The trade-off is that production transport, least-privilege application roles, capacity, backup/restore and deployment still need deliberate work when they become relevant.

📚 Learn first: [Docker Compose model](https://docs.docker.com/compose/intro/compose-application-model/), services/networks/volumes; [PostgreSQL transactions](https://www.postgresql.org/docs/17/tutorial-transactions.html), all-or-nothing; [GitHub Actions concepts](https://docs.github.com/en/actions/get-started/understand-github-actions), jobs/steps; stop before deployment/advanced features.
↩ Return: explain each boundary in your own words and draw it without this page. Use existing learning/ritual time; no extra hours or DSA requirement. Assistant answers do not count as your explain-back.

## Remaining learner evidence — five quick answers

1. What does a fresh clone lack that the working directory may already contain, and how do our instructions supply it safely?
2. Why must correct/wrong PostgreSQL passwords, health and cluster retention have separate tests?
3. Why can two clones use the same committed Compose file without sharing PostgreSQL data now?
4. What does a green setup CI run prove, and which application features does it not prove?
5. Why is the named PostgreSQL volume valuable but insufficient as a backup?

Grade each answer: 0 missing/incorrect, 1 partly correct, 2 correct with the reason. A pass requires at least 8/10 and no unresolved misconception about secret publication, password rejection or destructive volume cleanup. Retest missed concepts; draw host/container/storage boundaries in 60 seconds. Record actual minutes or “unknown”; learner deferred DSA remains uncommitted. Practical verification is recorded in Part 17. This page provides teaching and a rubric, not invented learner responses.
