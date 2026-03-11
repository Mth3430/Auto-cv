// ── Lettre de motivation – auto-cv ─────────────────────────────────────────
#let data = json("letter_data.json")

#set document(title: data.nom + " – Lettre de motivation")
#set page(paper: "a4", margin: (x: 2.5cm, y: 2.5cm))
#set text(font: ("Liberation Sans", "Arial", "Helvetica Neue", "Helvetica"), size: 10.5pt, lang: "fr")
#set par(leading: 0.7em, justify: true)

#let navy  = rgb("#1C2E4A")
#let accent = rgb("#3A7BD5")
#let muted = rgb("#6B7A99")

// En-tête
#grid(
  columns: (1fr, auto),
  {
    text(size: 16pt, weight: "bold", fill: navy, data.nom)
    linebreak()
    text(size: 10pt, fill: muted, style: "italic", data.titre)
    linebreak()
    v(4pt)
    text(size: 9pt, fill: muted, data.email + " · " + data.telephone + " · " + data.ville)
  },
  align(right, {
    text(size: 9pt, fill: muted, "Montpellier, le " + data.at("date", default: ""))
  }),
)

line(length: 100%, stroke: 1pt + accent)
v(20pt)

// Objet
text(weight: "bold", "Objet : ")
text("Candidature – " + data.at("poste_vise", default: "") + " chez " + data.at("entreprise", default: ""))
v(20pt)

// Formule d'appel
text("Madame, Monsieur,")
v(12pt)

// Corps
text(data.corps)

v(20pt)

// Formule de politesse
text("Dans l'attente de vous rencontrer, je vous adresse mes meilleures salutations.")
v(20pt)

text(weight: "bold", data.nom)
