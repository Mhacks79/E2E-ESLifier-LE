param(
    [string]$Repository = 'Mhacks79/E2E-ESLifier-LE'
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$sourceDirectory = $PSScriptRoot
$workingDirectory = Join-Path ([System.IO.Path]::GetTempPath()) ("e2e-github-publish-" + [Guid]::NewGuid().ToString('N'))

function Assert-LastCommand([string]$Description) {
    if ($LASTEXITCODE -ne 0) {
        throw "$Description failed with exit code $LASTEXITCODE"
    }
}

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    throw 'Git for Windows is required: https://git-scm.com/downloads/win'
}
if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
    throw 'GitHub CLI is required: https://cli.github.com/'
}
if (-not (Get-Command robocopy.exe -ErrorAction SilentlyContinue)) {
    throw 'Windows robocopy.exe is required.'
}

& gh auth status
Assert-LastCommand 'GitHub authentication (run gh auth login first)'
& gh auth setup-git
Assert-LastCommand 'GitHub git authentication configuration'

& gh repo view $Repository --json name --jq '.name' | Out-Null
Assert-LastCommand "Checking GitHub repository $Repository"

try {
    & git clone --branch main "https://github.com/$Repository.git" $workingDirectory
    Assert-LastCommand 'Cloning existing repository'

    # Include the exact source package and reviewer documents.
    # Do not overwrite the Git metadata in the cloned checkout.
    & robocopy.exe $sourceDirectory $workingDirectory /E /XD '.git' /NFL /NDL /NJH /NJS /NP | Out-Null
    if ($LASTEXITCODE -gt 7) {
        throw "Copying repository sources failed (robocopy exit code $LASTEXITCODE)"
    }

    & git -C $workingDirectory add --all
    Assert-LastCommand 'Staging files'

    $pending = & git -C $workingDirectory status --porcelain
    Assert-LastCommand 'Checking changes'
    if (-not $pending) {
        Write-Host 'The existing repository already contains these files. Nothing to push.'
        return
    }

    # Local checkout-only identity (does not modify global git settings).
    $login = (& gh api user --jq '.login').Trim()
    Assert-LastCommand 'Finding GitHub account name'
    & git -C $workingDirectory config user.name $login
    Assert-LastCommand 'Setting local author name'
    & git -C $workingDirectory config user.email "$login@users.noreply.github.com"
    Assert-LastCommand 'Setting local author email'

    & git -C $workingDirectory commit -m 'Publish E2E application source tree and third-party source snapshots'
    Assert-LastCommand 'Committing sources'
    & git -C $workingDirectory push origin main
    Assert-LastCommand 'Pushing main branch'

    Write-Host "Full source tree published: https://github.com/$Repository"
}
finally {
    if (Test-Path -LiteralPath $workingDirectory) {
        Remove-Item -LiteralPath $workingDirectory -Recurse -Force
    }
}
