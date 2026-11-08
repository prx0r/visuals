# Fundamental Structure — EssayViz Pack

A renderer-ready reconstruction of the supplied **Static Aspect** and complete
uploaded **Dynamic Aspect**.

## Scope

```text
27 scenes
13 static constructions
14 dynamic constructions
one persistent o/x alphabet
one dedicated capability pack
one renderer motif
```

## Files

```text
SOURCE-DYNAMIC.txt
SOURCE-STATIC-OUTLINE.md
analysis.json
storyboard.json
narration.json
PROCESS-NOTES.md
AGENT.md
skills/
MOTHERFUCKER/
tools/
SHA256SUMS
```

## Build

```bash
cd MOTHERFUCKER
node ../tools/apply-pack.mjs
node ../tools/validate.mjs ..
bash ../tools/build-film.sh
```

## Important limitation

The Static Aspect was supplied inline in the conversation. Its exact full text
is not duplicated in this compact pack; `SOURCE-STATIC-OUTLINE.md` preserves its
numbered construction. The complete uploaded Dynamic Aspect is included
verbatim as `SOURCE-DYNAMIC.txt`.
