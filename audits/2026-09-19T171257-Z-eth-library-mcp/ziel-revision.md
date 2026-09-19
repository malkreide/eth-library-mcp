# Warum das Ziel-Gate anschlaegt, und was gemessen ist

`aggregate_results.py validate` endet mit exit 1:

```
HEAD moved during the audit: 32ac730127e5 at init, 9260a21683b0 now.
The report mixes findings from two different trees.
```

Der Findings-Satz selbst ist sauber: `expected_count 60`, `found_count 60`,
`missing []`, `unexpected []`, `empty []`. Angeschlagen hat allein die
Ziel-Revision.

## Die Ursache ist bekannt und liegt beim Auditor

Waehrend des Laufs wurde jedes eintreffende Check-Ergebnis committet und
gepusht -- 26 Commits, weil der Arbeitsbaum sonst zwischen den Wach-Zyklen
unsauber geblieben waere. Jeder dieser Commits bewegt HEAD, und das Gate
vergleicht HEAD.

## Was das Gate nicht unterscheidet, und die Messung schon

```bash
git diff --stat 32ac730..HEAD -- . ':(exclude)audits'
# leer

# Negativkontrolle -- greift derselbe Befehl ueberhaupt?
git diff --stat 32ac730..HEAD -- .
# 86 files changed, 1481 insertions(+)   (alle unter audits/)
```

Der auditierte Baum -- `src/`, `tests/`, `scripts/`, `docs/`, `pyproject.toml`,
`server.json`, die READMEs, `SECURITY.md`, `Dockerfile`, `.github/` -- ist
bitgleich mit `32ac730`. Gewachsen ist ausschliesslich `audits/`, also die
Ablage der Messergebnisse selbst.

Die Befunde beschreiben damit **einen** Baum, nicht zwei. Der Satz «The report
mixes findings from two different trees» trifft hier nicht zu.

## Warum trotzdem nicht `--skip-target-check`

Der Skill nennt den Reflex, das Flag bei jedem Anschlag zu setzen, ausdruecklich
als den Weg, auf dem auch der Fall abgeschaltet wird, auf den es ankommt. Das
Gate bleibt deshalb scharf und rot, und diese Datei traegt die Messung, die es
entkraeftet. Wer den Lauf nachvollzieht, sieht beides: den Anschlag und den
Grund.

## Was daraus fuer den naechsten Lauf folgt

Der eigentliche Fehler war nicht das Committen, sondern **wohin**. Ein
Audit-Lauf, der seine Zwischenstaende in dasselbe Repository schreibt, das er
auditiert, bewegt zwangslaeufig die Revision, gegen die er misst. Zwei Auswege,
beide ohne den Guard zu schwaechen:

- Die Rohergebnisse ausserhalb des Arbeitsbaums sammeln und erst nach
  `verify-target` in einem einzigen Commit ablegen.
- Oder `audit_init.py` eine Pfadliste mitgeben, die es beim Revisionsvergleich
  ausnimmt -- das waere ein Befund fuer das Skill-Repo, nicht fuer dieses.

Die zweite Fassung ist die bessere: Sie macht die Unterscheidung, die diese
Datei von Hand trifft, zu einer Eigenschaft des Werkzeugs.
