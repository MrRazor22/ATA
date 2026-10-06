param (
    [switch]$CheckOnly
)

$RepoRoot = Split-Path -Parent $PSScriptRoot
$SkillSource = Join-Path $RepoRoot "skills\pfd\SKILL.md"
$GlobalSkill = "$env:USERPROFILE\.gemini\config\skills\pfd\SKILL.md"

Write-Host "=== Primitive-First Design (PFD) Sync Tool ===" -ForegroundColor Cyan

# 1. Sync SKILL.md to Global Antigravity Config
if (Test-Path $SkillSource) {
    $GlobalDir = Split-Path -Parent $GlobalSkill
    if (-not (Test-Path $GlobalDir)) {
        New-Item -ItemType Directory -Path $GlobalDir -Force | Out-Null
    }
    
    if ($CheckOnly) {
        $srcHash = (Get-FileHash $SkillSource).Hash
        $dstHash = if (Test-Path $GlobalSkill) { (Get-FileHash $GlobalSkill).Hash } else { "NONE" }
        if ($srcHash -eq $dstHash) {
            Write-Host "[OK] Global SKILL.md is 100% in sync." -ForegroundColor Green
        } else {
            Write-Host "[MISMATCH] Global SKILL.md needs update!" -ForegroundColor Yellow
        }
    } else {
        Copy-Item -Path $SkillSource -Destination $GlobalSkill -Force
        Write-Host "[SYNCED] skills/pfd/SKILL.md -> $GlobalSkill" -ForegroundColor Green
    }
} else {
    Write-Host "[ERROR] Could not find source: $SkillSource" -ForegroundColor Red
}

# 2. Check Git Status
Push-Location $RepoRoot
try {
    Write-Host "`nGit Status:" -ForegroundColor Cyan
    git status -s
} finally {
    Pop-Location
}

Write-Host "`nSync operation completed successfully." -ForegroundColor Cyan
