#!/usr/bin/env bash
#
# SessionStart-Hook: meldet, wie viele Commits der ausgecheckte Stand hinter
# origin/<default-branch> liegt. Bei 0 schweigt er.
#
# WARUM: Ein veralteter Klon hat am 3.8.2026 zweimal eine rote CI erzeugt,
# deren Ursache nicht im Diff stand — die fehlenden Commits waren jeweils
# genau die, die das Gate einfuehrten, an dem der Branch scheiterte. Gesucht
# wurde dabei in den falschen Dateien. Die Pruefung hier kostet eine Sekunde
# und ersetzt diese Fehlersuche.
#
# OBERSTE REGEL: Dieser Hook blockiert die Session nie.
# Kein Netz, kein Remote, detached HEAD, flatterndes DNS, fehlendes `timeout`,
# leeres Repo — jeder dieser Faelle geht still durch, Exit-Code 0, keine
# Ausgabe. Ein Hook, der bei Netzproblemen die Arbeit anhaelt, wird nach dem
# zweiten Mal abgeschaltet und schuetzt danach gar nichts. Deshalb:
#   - kein `set -e` (ein fehlgeschlagenes git wuerde den Hook mit != 0 beenden)
#   - `exec </dev/null`, damit nichts jemals auf eine Eingabe wartet
#   - jeder Netzaufruf unter `timeout`
#   - alles in einer Funktion, deren Ergebnis verworfen wird; `exit 0` am Ende
#
# Der Default-Branch wird ermittelt, nicht als "main" angenommen: im Portfolio
# heissen drei Server ihren Standard-Branch `master`. Laesst er sich nicht
# ermitteln, schweigt der Hook, statt zu raten.

set -u
exec </dev/null

# Sekunden pro Netzaufruf. Im Normalfall faellt genau einer an (ls-remote);
# der Fetch laeuft nur, wenn dabei schon feststeht, dass Commits fehlen.
NETZ_TIMEOUT="${CLAUDE_CLONE_CHECK_TIMEOUT:-5}"

# git darf unter keinen Umstaenden nach Zugangsdaten fragen.
export GIT_TERMINAL_PROMPT=0
export GIT_ASKPASS=true
export SSH_ASKPASS=true
export GIT_SSH_COMMAND="ssh -oBatchMode=yes -oConnectTimeout=3"
unset GIT_DIR GIT_WORK_TREE

pruefe() {
    command -v git >/dev/null 2>&1 || return 0

    local wurzel
    wurzel="${CLAUDE_PROJECT_DIR:-$PWD}"
    [ -d "$wurzel" ] || return 0
    wurzel=$(git -C "$wurzel" rev-parse --show-toplevel 2>/dev/null) || return 0
    [ -n "$wurzel" ] || return 0
    cd "$wurzel" || return 0

    # Leeres Repo ohne Commits: nichts zu vergleichen.
    git rev-parse --verify --quiet HEAD >/dev/null 2>&1 || return 0

    local remote
    if git remote get-url origin >/dev/null 2>&1; then
        remote=origin
    else
        remote=$(git remote 2>/dev/null | head -n 1)
    fi
    [ -n "$remote" ] || return 0

    # `timeout` ist auf manchen Systemen (macOS ohne coreutils) nicht da. Dann
    # wird gar nicht erst ins Netz gegriffen — lieber ohne Netz auf den zuletzt
    # geholten Stand zurueckfallen als ohne Zeitgrenze haengen.
    local zeitgrenze=""
    if command -v timeout >/dev/null 2>&1; then
        zeitgrenze=timeout
    elif command -v gtimeout >/dev/null 2>&1; then
        zeitgrenze=gtimeout
    fi

    # --- Default-Branch und Remote-Stand in einem Zug ---------------------
    # `ls-remote --symref HEAD` liefert beides: den Namen des Default-Branches
    # und die SHA, auf der er steht. Das ist die belastbare Quelle; der lokal
    # gecachte refs/remotes/<remote>/HEAD kann eine Umbenennung verpasst haben.
    local zweig="" fern_sha="" ausgabe=""
    if [ -n "$zeitgrenze" ]; then
        ausgabe=$("$zeitgrenze" "$NETZ_TIMEOUT" git ls-remote --symref "$remote" HEAD 2>/dev/null)
        zweig=$(printf '%s\n' "$ausgabe" |
            sed -n 's|^ref: refs/heads/\([^[:space:]]*\)[[:space:]]*HEAD$|\1|p' | head -n 1)
        fern_sha=$(printf '%s\n' "$ausgabe" |
            sed -n 's|^\([0-9a-f]\{7,\}\)[[:space:]]*HEAD$|\1|p' | head -n 1)
    fi

    # Rueckfall ohne Netz: der zuletzt geholte Stand. Er kann alt sein und
    # untertreibt dann — aber was er meldet, fehlt wirklich.
    local gecacht=""
    if [ -z "$zweig" ]; then
        gecacht=$(git symbolic-ref --quiet "refs/remotes/$remote/HEAD" 2>/dev/null)
        zweig="${gecacht#refs/remotes/$remote/}"
        [ "$zweig" = "$gecacht" ] && zweig=""
    fi
    # Nicht ermittelbar -> schweigen. Nicht auf "main" raten.
    [ -n "$zweig" ] || return 0

    # --- Vergleichspunkt bestimmen ----------------------------------------
    local ziel=""
    if [ -n "$fern_sha" ] && git cat-file -e "${fern_sha}^{commit}" 2>/dev/null; then
        # Objekt schon da: kein Fetch noetig (der haeufige Fall "aktuell").
        ziel="$fern_sha"
    elif [ -n "$fern_sha" ] && [ -n "$zeitgrenze" ] &&
        "$zeitgrenze" "$NETZ_TIMEOUT" git fetch --quiet "$remote" "$zweig" 2>/dev/null; then
        ziel=FETCH_HEAD
    elif git rev-parse --verify --quiet "refs/remotes/$remote/$zweig" >/dev/null 2>&1; then
        ziel="refs/remotes/$remote/$zweig"
    else
        return 0
    fi

    local zaehler voraus zurueck
    zaehler=$(git rev-list --left-right --count "HEAD...$ziel" 2>/dev/null) || return 0
    voraus=${zaehler%%[!0-9]*}
    zurueck=${zaehler##*[!0-9]}
    case "$zurueck" in
    '' | *[!0-9]*) return 0 ;;
    esac
    [ "$zurueck" -gt 0 ] 2>/dev/null || return 0

    local hier
    hier=$(git symbolic-ref --quiet --short HEAD 2>/dev/null) ||
        hier="detached HEAD @ $(git rev-parse --short HEAD 2>/dev/null)"

    local nachsatz=""
    [ "${voraus:-0}" -gt 0 ] 2>/dev/null && nachsatz=", lokal $voraus voraus"

    printf 'Klon veraltet: %s Commit(s) hinter %s/%s (HEAD: %s%s).\n' \
        "$zurueck" "$remote" "$zweig" "$hier" "$nachsatz"
    printf '  Nachziehen vor der Arbeit: git fetch %s %s && git merge FETCH_HEAD\n' \
        "$remote" "$zweig"
    printf '  Grund: ein veralteter Klon erzeugte am 3.8.2026 zweimal eine rote CI,\n'
    printf '  deren Ursache nicht im Diff stand — es fehlten genau die Commits, die\n'
    printf '  das Gate einfuehrten, an dem der Branch scheiterte.\n'
    [ -n "$gecacht" ] && printf '  (Remote nicht erreichbar; Stand des letzten Fetch — es koennen mehr sein.)\n'
    return 0
}

if [ -n "${CLAUDE_CLONE_CHECK_DEBUG:-}" ]; then
    pruefe || true
else
    pruefe 2>/dev/null || true
fi

exit 0
