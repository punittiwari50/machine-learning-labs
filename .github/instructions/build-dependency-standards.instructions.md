---
description: "Use when creating or modifying multi-module Maven, Gradle, Python, or Node.js projects. Enforces parent-managed versions, child-module dependency-only declarations, and latest stable dependency maintenance."
applyTo: ["**/pom.xml", "**/*.gradle", "**/*.gradle.kts", "**/settings.gradle", "**/settings.gradle.kts", "**/gradle/libs.versions.toml", "**/pyproject.toml", "**/requirements.txt", "**/requirements-*.txt", "**/poetry.lock", "**/uv.lock", "**/package.json", "**/package-lock.json", "**/pnpm-workspace.yaml", "**/pnpm-lock.yaml", "**/yarn.lock"]
---

# Build & Dependency Standards (Maven / Gradle / Python / Node.js)

## Objective

Use a parent-first dependency model for easier maintenance:
- Parent project controls versions and shared dependency management.
- Submodules declare only what they use (artifact coordinates), without hardcoding versions.
- Keep dependencies on latest stable releases after compatibility verification.

---

## Project Structure Rules (Required)

- Do not create one flat project that mixes many unrelated dependencies and subprojects.
- Organize by bounded module ownership: each module/package has a single business responsibility.
- Keep shared concerns in dedicated shared modules (`common`, `core`, or `shared-*`) rather than cross-importing random files.
- Keep dependency direction clear: app/service modules depend on shared/domain modules, never the reverse.
- Every module must have a clear entry point, build file, tests, and ownership scope.

### Recommended Layout Patterns

#### Maven / Gradle

```text
root-parent/
  pom.xml or settings.gradle(.kts)
  modules/
    shared-core/
    shared-observability/
    service-a/
    service-b/
```

#### Python

```text
root/
  pyproject.toml
  packages/
    shared_core/
    shared_observability/
    service_a/
    service_b/
  tests/
```

#### Node.js

```text
root/
  package.json
  pnpm-workspace.yaml (or npm/yarn workspaces)
  packages/
    shared-core/
    shared-observability/
  apps/
    service-a/
    service-b/
```

---

## Maven Multi-Module Standard

### Parent `pom.xml` (root)

- Packaging is `pom`.
- Defines `<modules>` list.
- Defines versions in one place using `<dependencyManagement>`.
- Defines plugin versions in `<pluginManagement>`.

```xml
<project>
  <modelVersion>4.0.0</modelVersion>
  <groupId>com.example</groupId>
  <artifactId>platform-parent</artifactId>
  <version>1.0.0</version>
  <packaging>pom</packaging>

  <modules>
    <module>service-a</module>
    <module>service-b</module>
  </modules>

  <properties>
    <java.version>21</java.version>
    <spring.boot.version>3.5.0</spring.boot.version>
  </properties>

  <dependencyManagement>
    <dependencies>
      <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-dependencies</artifactId>
        <version>${spring.boot.version}</version>
        <type>pom</type>
        <scope>import</scope>
      </dependency>
    </dependencies>
  </dependencyManagement>

  <build>
    <pluginManagement>
      <plugins>
        <plugin>
          <groupId>org.apache.maven.plugins</groupId>
          <artifactId>maven-compiler-plugin</artifactId>
          <version>3.14.0</version>
        </plugin>
      </plugins>
    </pluginManagement>
  </build>
</project>
```

### Submodule `pom.xml`

- Inherit from parent.
- Declare dependencies without versions when managed by parent/BOM.
- Never duplicate managed versions in child modules.

```xml
<project>
  <parent>
    <groupId>com.example</groupId>
    <artifactId>platform-parent</artifactId>
    <version>1.0.0</version>
  </parent>

  <artifactId>service-a</artifactId>

  <dependencies>
    <dependency>
      <groupId>org.springframework.boot</groupId>
      <artifactId>spring-boot-starter-web</artifactId>
    </dependency>
  </dependencies>
</project>
```

---

## Gradle Multi-Module Standard

### Root project

- Centralize versions in Version Catalog (`gradle/libs.versions.toml`) and/or platform module.
- Configure common repositories/plugins in root.
- Subprojects consume aliases/platform constraints only.

`settings.gradle.kts`:

```kotlin
rootProject.name = "platform-parent"
include("service-a", "service-b")
```

`gradle/libs.versions.toml`:

```toml
[versions]
spring-boot = "3.5.0"

[libraries]
spring-boot-starter-web = { module = "org.springframework.boot:spring-boot-starter-web" }
```

### Submodule `build.gradle.kts`

- Declare dependencies via `libs` aliases or platform.
- Do not hardcode versions in submodule unless explicitly exempted.

```kotlin
dependencies {
    implementation(libs.spring.boot.starter.web)
}
```

---

## Python Multi-Module Standard

### Parent project (root)

- Use one central dependency source at root:
  - `pyproject.toml` for Poetry/UV/PDM style projects, or
  - root `requirements.txt`/constraints file for pip-based projects.
- Pin and manage shared versions at root only.
- Child packages inherit or reference root constraints; avoid module-level version drift.

Root `pyproject.toml` example:

```toml
[project]
name = "platform-parent"
version = "1.0.0"
requires-python = ">=3.12"
dependencies = [
  "fastapi>=0.115.0",
  "pydantic>=2.11.0",
]

[tool.uv]
package = true
```

### Child module/package

- Declare only module-specific dependencies.
- Do not re-pin shared versions already managed in root constraints.
- If an override is unavoidable, document the reason and expiry plan.

---

## Node.js Multi-Module Standard

### Parent workspace (root)

- Use a root workspace manifest (`package.json` with `workspaces`, or `pnpm-workspace.yaml`).
- Keep shared versions centrally controlled:
  - npm/pnpm: `overrides`
  - yarn: `resolutions`
- Keep common dev tools (lint/test/build) in root `devDependencies`.

Root `package.json` example:

```json
{
  "name": "platform-parent",
  "private": true,
  "workspaces": ["apps/*", "packages/*"],
  "overrides": {
    "typescript": "5.8.0"
  },
  "devDependencies": {
    "typescript": "5.8.0"
  }
}
```

### Child package (`apps/*` or `packages/*`)

- Declare only package-specific runtime dependencies.
- Avoid duplicating shared tool versions managed at root.
- Prefer workspace protocol (`workspace:*`) for internal package links.

---

## Latest Stable Dependency Policy

- Prefer latest stable (non-alpha, non-beta, non-rc) versions.
- Upgrade centrally in parent/version catalog only.
- Validate via test/lint/build before merge.
- Avoid submodule-level version overrides except temporary, documented exceptions.

---

## Anti-Patterns (Disallowed)

- Version duplication across modules.
- Different versions of the same dependency across sibling submodules.
- Declaring plugin versions separately in each submodule.
- Hardcoding snapshot/pre-release dependencies without explicit approval.
- Re-pinning centrally managed Python dependencies in child packages.
- Re-pinning centrally managed Node.js toolchain dependencies in workspace packages.
- Single flat project structure that mixes unrelated subprojects and dependencies in one module.
- Random cross-module imports with no clear ownership or layering.

---

## Quality Gates

- [ ] Parent controls dependency and plugin versions.
- [ ] Submodules declare dependency coordinates only (versionless where managed).
- [ ] Single source of truth for versions (`dependencyManagement` or version catalog).
- [ ] Python dependencies are centrally managed (root `pyproject.toml` or root constraints file).
- [ ] Node.js workspace dependencies are centrally managed (root `overrides`/`resolutions` where applicable).
- [ ] Dependencies are on latest stable versions compatible with the codebase.
- [ ] Project structure is modular and organized; no flat single-project-with-everything layout.
- [ ] Coding structure follows module ownership and clear dependency direction.

---

## Verification Commands

Run relevant commands based on build tool.

### Maven

```bash
# Fail build on dependency convergence issues
mvn -q -DskipTests enforcer:enforce -Denforcer.rules=dependencyConvergence

# Report available updates (apply at parent only)
mvn -q -DskipTests versions:display-dependency-updates versions:display-plugin-updates
```

### Gradle

```bash
# Report available updates (apply at root/version catalog only)
./gradlew -q dependencyUpdates

# Inspect resolved dependency trees for all modules
./gradlew -q dependencies
```

### Python

```bash
# Validate dependency graph consistency
python -m pip check

# Show outdated packages (upgrade centrally)
python -m pip list --outdated
```

### Node.js

```bash
# Show outdated packages in workspace (upgrade centrally at root)
npm outdated

# Inspect dependency graph for duplicates/conflicts
npm ls --all
```
