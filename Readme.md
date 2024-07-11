# Conjugatizer

Conjugatizer is a program that conjugates verbs in a language. This can be used as a backend for a quiz or memorizing program.

The data is in text files in the Markdown format. There are a couple of special tags. The single hashmark (#) titles have their special tag plus arbitrary information. All other lines have a fixed format that does not allow arbitrary information. The exception is comment lines with a triple hashmark: `### Added on 2024/1/1`.

- `# Conjugations {arbitrary information}` : All the content of the file before this title is ignored. Feel free to use this space for notes, comments, journals, etc. The word `Conjugations` can be followed with arbitrary information or nothing. Ex.: `# Conjugations of Spanish`.
- `## Conjugation: {tense mood} {separator} {specifier}` : The specifier is the infinitive ending that will be replaced. Ex.: `## Conjugation: present indicative for -ar`. The separator is anything surround by a whitespace on both sides. Ex.: ` - `, ` for `, ` = `. The lines following must be conjugation rules. The rules for the conjugation end when the next title line is encountered.
- `{specifier}` : The form of the specifier *must* be a dash followed by letters without any whitespace. A conjugation that simply deletes the infinitive can be specified with dash plus zero (`-0`). Ex.: `-er`.
- Conjugation rule : Each line is of the form: `{label} = {specifier}`. Ex.: `1st person singular = -o`. The labels are not parsed and are case-sensitive. `first plur.` is a different label than `First plur.`. Inconsistency will break the data parsing. For programmers: the labels are Python table keys.
- `# Pronouns {arbitrary information}` : This optional section is a list of pronouns for the labels in your conjugations. Ex.: `1st singular = yo`.
- `# Regular {arbitrary information}` : This line is followed by a verb list. Ex.: `# Regular verbs`. The list ends when the next title line is encountered.
- Verb list : One verb per line in the infinitive form. A dash, the infinitive, a `=`, and a gloss. Ex.: `- decider = to decide`. All information after the equals sign and the initial whitespace is not parsed and is returned verbatim.
- `# Irregular {arbitrary information}` : This line is followed by verb groups. The group list ends when the next title line is encountered.
- Verb groups : A verb group starts with a conjugation line (which verb the rules apply to) with a gloss at the end. This is followed by a list of rules that *differ from the regular conjugation*. This means that you can omit regular conjugation rules that are followed by that particular verb. Ex.: 
```markdown
## Conjugation: indicative of poner = to put
1st singular = pongo
```

# Notes

Sections can be added in arbitrary order and can be split up. This can be helpful for just adding stuff to the end of the file without hunting for the correct section. It also helps for making an appending editor.

# Example file

```markdown
# Spanish conjugations

This is my incredible Spanish conjugation file!

# Pronouns
1st singular = yo
2nd singular = tú
3rd singular = él/ella/usted
1st plural = nosotros
2nd plural = vosotros
3rd plural = ellos/ellas/ustedes

# Conjugations
## Conjugation: present indicative of -ar
1st singular = -o
2nd singular = -as
3rd singular = -a
1st plural = -amos
2nd plural = -áis
3rd plural = -an

## Conjugation: present indicative of -er
1st singular = -o
2nd singular = -es
3rd singular = -e
1st plural = -emos
2nd plural = -eis
3rd plural = -en

## Conjugation: present indicative of -ir
1st singular = -o
2nd singular = -es
3rd singular = -e
1st plural = -emos
2nd plural = -ís
3rd plural = -en

## Conjugation: future subjunctive of -ir
1st singular = -iere
2nd singular = -ieres
3rd singular = -iere
1st plural = -iéremos
2nd plural = -iereís
3rd plural = -ieren

# Regular verbs
cantar = to sing
escuchar = to rest
decider = to decide
limpiar = to clean
llegar = to arrive
comer = to eat
leer = to read
viver = to live
compartir = to share

# Irregular verbs
## Conjugation: present indicative of ir = to go
1st singular = voy
2nd singular = vas
3rd singular = va
1st plural = vamos
2nd plural = vais
3rd plural = van

## Conjugation: present indicative of poner = to put
1st singular = pongo

### I added some more verbs
# Regular verbs (again)
recibir = to receive
comprar = to buy
correr = to run
```

