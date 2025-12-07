<!--
Sync Impact Report:
- Version: 1.0.0 → 1.0.1 (patch: fill ratification/amendment metadata)
- Modified principles: none (no policy language changes)
- Added sections: none
- Removed sections: none
- Templates inspected / updated:
	✅ .specify/templates/plan-template.md (checked + language note added)
	✅ .specify/templates/spec-template.md (checked + language note added)
	✅ .specify/templates/tasks-template.md (checked + language note added)
	✅ .specify/templates/checklist-template.md (checked + language note added)
	✅ .specify/templates/agent-file-template.md (checked + language note added)
- Follow-up TODOs: none
-->

# SDD-Demo Constitution

## Core Principles

### I. Respect the Brownfield Project (Non-Negotiable)

All refactoring or modification of existing, working code is strictly prohibited unless explicitly requested by the user. Only precisely targeted minimal changes to the requested portions are allowed. The existing architecture, patterns, and code style must be preserved. Refactoring is forbidden unless the user explicitly requests "refactor" or equivalent.

Rationale: This is a production brownfield project. Unnecessary changes risk breaking existing functionality and destabilizing the team. Safety of ongoing work depends on respecting the current codebase.

### II. Minimal-Change Principle

Every change must be the minimal modification necessary to achieve the stated objective. Avoid touching unrelated files, functions, or lines of code. Preserve existing comments, formatting, and structure unless explicitly required to change.

Rationale: Minimizing change surface reduces risk, simplifies reviews, and keeps the brownfield system stable.

### III. Require Explicit Approval

Code changes, architectural decisions, and dependency updates require explicit user approval before implementation. Provide options and wait for confirmation. Do not modify repository structure, add new libraries, or alter build configuration without clear approval.

Rationale: The user retains control over all changes to protect production stability and ensure consistency with team standards.

### IV. Testing Discipline

Existing tests must continue to pass after changes. New features should include tests when requested. Do not modify or remove existing test files unless explicitly instructed.

Rationale: The test suite protects the system against regressions. Maintaining test coverage is critical in a brownfield project.

### V. Dependencies & Naming Conventions

Follow the codebase's existing patterns and naming conventions. Use the project's existing dependency set. Do not upgrade major versions or introduce new frameworks without explicit approval.

Rationale: Stability of the technical stack matters. major version changes can create cascade-breaking changes across the repository.

## Change Classification

### Allowed Changes (with user request)
- Fixes to specific functions/components
- New features implemented in new files
- Security dependency patches (with approval)
- Documentation updates
- Adding new tests (not modifying existing tests)

### Forbidden Changes (unless explicitly requested)
- Refactoring currently working code
- Altering repo structure or architecture
- Changing coding patterns or conventions
- Upgrading major versions of dependencies
- Removing or reorganizing existing features

## Development Workflow

### Before Changes
1. Read the request carefully
2. Identify the minimal set of files requiring modification
3. Propose specific changes when unclear
4. Wait for explicit approval when scope is ambiguous

### During Implementation
1. Modify only the requested parts
2. Preserve existing code style and structure
3. Run tests to confirm existing behavior continues to work
4. Validate no unintended side effects

### After Changes
1. Report precisely what was changed and why
2. Confirm tests still pass
3. Await user verification before considering the task complete

## Governance

This constitution takes precedence over other development guidelines in this repository. Any AI agent, developer, or tool working on this codebase must follow these principles.

Amendments: Constitution changes require explicit user request and documented rationale. Versioning follows semantic versioning (MAJOR.MINOR.PATCH).

Compliance: Every code change must be validated against these principles before being implemented. If uncertain, ask the user rather than assume.

Emergency Override: The user can temporarily suspend the constitution for a specific request by stating "ignore constitution" or similar.

**Version**: 1.0.1 | **Ratified**: 2025-12-07 | **Last Amended**: 2025-12-07
