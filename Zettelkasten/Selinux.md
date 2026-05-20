SELinux is a security framework that implements Mandatory Access Control (MAC) at the [[Kernel]] level, sitting between applications and the [[Operating System]] core. It enforces security policies through labels assigned to processes and files, restricting access based on predefined rules rather than traditional discretionary permissions

SELinux operates via policy rules that define exactly what processes can access (e.g., files, other processes) based on labels like `type`, `user`, and `security level` docs.redhat.com. Unlike traditional Unix permissions, it controls access at a granular level—so a compromised process can only access resources explicitly allowed by its domain

**How it is used**:

- **Labeling**: Every process and file has a security context (e.g., `system_u:system_r:httpd_t:s0`).
- **Policy enforcement**: Runs in `enforcing` mode (active restrictions) or `permissive` mode (logs violations but doesn’t block actions)
- **Integration**: Deeply baked into the [[Linux]] [[Kernel]] (e.g., in RHEL, SELinux is enabled by default as core security infrastructure

**Why it matters for security**:

- Mitigates privilege escalation: If a service like Apache is compromised, attackers cannot access user home directories unless explicitly permitted
- Enforces [[Data]] integrity: Prevents unauthorized modification of files by isolating processes into secure domains
- Extends beyond user-level controls: Security decisions rely on labels rather than just user/group permissions