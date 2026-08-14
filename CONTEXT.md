# Next Move Theory Distribution

Vocabulary for the canon, skills, and the package through which people install and use them.

## Language

**Canon**:
The authoritative Next Move Theory methodology corpus consumed by the skills.
_Avoid_: Knowledge base, documentation bundle

**Skill source**:
The single authoritative editable version of a skill, shared across supported agent clients.
_Avoid_: Claude copy, Codex copy

**Plugin**:
The self-contained installable distribution that carries the skills and its pinned Canon without adding files to a Consumer project.
_Avoid_: Project installer, local skill copy

**Consumer project**:
A user's repository from which the installed Plugin is invoked; it is not part of the Plugin's source or installation target.
_Avoid_: Target directory, host repo

**Client adapter**:
A generated compatibility layer for a capability that genuinely differs between supported agent clients.
_Avoid_: Platform-specific skill copy

**Legacy installer**:
The transitional project-mutating installation path retained temporarily for existing users.
_Avoid_: Primary installer
