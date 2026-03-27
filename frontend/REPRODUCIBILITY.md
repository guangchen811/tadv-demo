# Frontend Reproducibility Guide

## Python vs Node.js Comparison

| Concept | Python (Poetry/UV) | Node.js (npm) | Node.js (pnpm) |
|---------|-------------------|---------------|----------------|
| **Version file** | `.python-version` | `.nvmrc` | `.nvmrc` |
| **Lock file** | `poetry.lock` / `uv.lock` | `package-lock.json` | `pnpm-lock.yaml` |
| **Config file** | `pyproject.toml` | `package.json` | `package.json` |
| **Install command** | `poetry install` / `uv sync` | `npm ci` | `pnpm install --frozen-lockfile` |
| **Add dependency** | `poetry add <pkg>` | `npm install <pkg>` | `pnpm add <pkg>` |
| **Dev dependency** | `poetry add --group dev <pkg>` | `npm install -D <pkg>` | `pnpm add -D <pkg>` |
| **Update all** | `poetry update` | `npm update` | `pnpm update` |
| **Run script** | `poetry run <cmd>` | `npm run <cmd>` | `pnpm run <cmd>` |

## Current Setup (npm)

### ✅ What's Configured

1. **`.nvmrc`** - Pins Node.js to v20.11.0
   ```bash
   nvm use  # Auto-selects correct Node version
   ```

2. **`package.json` engines** - Enforces minimum versions
   ```json
   "engines": {
     "node": ">=20.11.0",
     "npm": ">=10.0.0"
   }
   ```

3. **`.npmrc`** - Strict reproducibility settings
   ```ini
   save-exact=true      # No ^ or ~ in package.json
   engine-strict=true   # Fail if Node/npm version mismatches
   package-lock=true    # Always use lock file
   ```

4. **`package-lock.json`** - Exact dependency tree (committed to git)

### 📋 Recommended Workflow

**First-time setup:**
```bash
# 1. Use correct Node version
nvm install
nvm use

# 2. Install exact dependencies
npm ci

# 3. Verify environment
node --version
npm --version
```

**Adding a new dependency:**
```bash
npm install <package>
git add package.json package-lock.json
git commit -m "Add <package> dependency"
```

**On a new machine:**
```bash
git clone <repo>
cd frontend
nvm use
npm ci  # Not 'npm install'!
```

## 🚀 Upgrade to pnpm (Optional)

If you want even stricter reproducibility (closer to Poetry/UV):

### Installation
```bash
npm install -g pnpm
```

### Migration
```bash
# Remove node_modules and package-lock.json
rm -rf node_modules package-lock.json

# Install with pnpm
pnpm install

# Commit pnpm-lock.yaml
git add pnpm-lock.yaml
git commit -m "Migrate to pnpm"
```

### Benefits over npm
- **Faster:** Reuses packages across projects
- **Stricter:** Better dependency resolution
- **Disk efficient:** Hard links instead of copies
- **Phantom dependencies:** Prevents importing uninstalled packages

### Usage
```bash
pnpm install                        # Install from lock file
pnpm add <package>                  # Add dependency
pnpm add -D <package>               # Add dev dependency
pnpm update                         # Update all packages
pnpm run dev                        # Run script
pnpm install --frozen-lockfile      # CI mode (like npm ci)
```

## 🐳 Docker Alternative (Most Reproducible)

For maximum reproducibility, use Docker:

```dockerfile
# Dockerfile
FROM node:20.11.0-alpine

WORKDIR /app

# Copy dependency files
COPY package.json package-lock.json ./

# Install exact dependencies
RUN npm ci --only=production

# Copy source
COPY . .

# Build
RUN npm run build

# Run
CMD ["npm", "run", "preview"]
```

```bash
# Build image
docker build -t tadv-frontend .

# Run container
docker run -p 3000:3000 tadv-frontend
```

## 🔍 Verification

Check your environment is correct:

```bash
# Verify Node version
node --version
# Expected: v20.11.0 or higher

# Verify npm version
npm --version
# Expected: 10.0.0 or higher

# Verify dependencies are installed
npm ls --depth=0
# Should show all packages from package.json

# Verify build works
npm run build
# Should complete without errors
```

## 📝 Best Practices

### ✅ Do's
- **Commit lock files** (`package-lock.json` or `pnpm-lock.yaml`)
- **Use `npm ci`** in CI/production (not `npm install`)
- **Pin Node version** in `.nvmrc`
- **Update lock file** when adding packages
- **Use exact versions** for critical dependencies

### ❌ Don'ts
- **Don't commit `node_modules/`**
- **Don't manually edit lock files**
- **Don't use `npm install` in production**
- **Don't use global packages** for project dependencies
- **Don't mix package managers** (npm + pnpm in same project)

## 🔧 Troubleshooting

### "Wrong Node version"
```bash
nvm use
# Or install if needed
nvm install
nvm use
```

### "Dependencies out of sync"
```bash
rm -rf node_modules package-lock.json
npm install
```

### "Build fails"
```bash
# Check Node version
node --version

# Clear cache
npm cache clean --force

# Reinstall
rm -rf node_modules
npm ci
```

---

**Summary:** With `.nvmrc` + `package-lock.json` + `.npmrc`, npm provides reproducibility similar to Poetry/UV. For stricter control, consider migrating to pnpm.
