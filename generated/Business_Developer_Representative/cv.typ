// ── CV Template – auto-cv ──────────────────────────────────────────────────
#let data = json("cv_data.json")

#set document(title: data.nom + " – CV")
#set page(paper: "a4", margin: 0pt)
#set text(font: ("Liberation Sans", "Arial", "Helvetica Neue", "Helvetica"), size: 10pt, lang: "fr")
#set par(leading: 0.55em)

// ── Couleurs ────────────────────────────────────────────────────────────────
#let navy    = rgb("#1C2E4A")
#let accent  = rgb("#3A7BD5")
#let light   = rgb("#F4F6FB")
#let mid     = rgb("#DCE4F0")
#let muted   = rgb("#6B7A99")

// ── Helpers ─────────────────────────────────────────────────────────────────
#let tag(t) = box(
  fill: mid, inset: (x: 5pt, y: 2pt), radius: 3pt,
  text(size: 8pt, fill: navy, weight: "medium", t)
)

#let section-title(t) = {
  v(10pt)
  text(size: 11pt, weight: "bold", fill: accent, t)
  line(length: 100%, stroke: 0.5pt + accent)
  v(4pt)
}

#let exp-entry(poste: "", entreprise: "", dates: "", description: "") = {
  grid(
    columns: (1fr, auto),
    text(weight: "bold", size: 10pt, poste),
    text(size: 9pt, fill: muted, dates),
  )
  text(size: 9pt, fill: muted, style: "italic", entreprise)
  v(2pt)
  text(size: 9pt, description)
  v(6pt)
}

// ── Sidebar ──────────────────────────────────────────────────────────────────
#let sidebar-content = {
  set text(fill: white)

  // Photo
  if data.photo != "" {
    align(center, {
      box(
        clip: true,
        radius: 50pt,
        width: 90pt,
        height: 90pt,
        image(data.photo, width: 90pt, height: 90pt, fit: "cover"),
      )
    })
  } else {
    // Placeholder initiales
    align(center, box(
      fill: accent,
      radius: 50pt,
      width: 90pt,
      height: 90pt,
      align(center + horizon,
        text(size: 28pt, weight: "bold", fill: white,
          data.nom.split(" ").map(w => w.at(0)).join("")
        )
      )
    ))
  }

  v(14pt)
  align(center, text(size: 14pt, weight: "bold", data.nom))
  v(2pt)
  align(center, text(size: 9pt, style: "italic", fill: mid, data.titre))

  v(18pt)

  // Contact
  text(size: 9pt, weight: "bold", fill: mid, "CONTACT")
  line(length: 100%, stroke: 0.4pt + mid)
  v(5pt)

  let contact-row(icon, val) = {
    if val != "" {
      grid(
        columns: (14pt, 1fr),
        gutter: 4pt,
        text(size: 9pt, fill: mid, icon),
        text(size: 9pt, fill: white, val),
      )
      v(3pt)
    }
  }

  contact-row("✉", data.email)
  contact-row("✆", data.telephone)
  contact-row("⌂", data.ville)
  if data.at("linkedin", default: "") != "" {
    contact-row("in", data.linkedin)
  }
  if data.at("github", default: "") != "" {
    contact-row("⊕", data.github)
  }

  v(16pt)

  // Compétences
  text(size: 9pt, weight: "bold", fill: mid, "COMPÉTENCES")
  line(length: 100%, stroke: 0.4pt + mid)
  v(5pt)

  for skill in data.competences {
    box(
      fill: rgb("#2A4A7A"),
      inset: (x: 6pt, y: 3pt),
      radius: 3pt,
      text(size: 8.5pt, fill: white, skill)
    )
    h(3pt)
  }

  // Langues
  if data.at("langues", default: ()).len() > 0 {
    v(16pt)
    text(size: 9pt, weight: "bold", fill: mid, "LANGUES")
    line(length: 100%, stroke: 0.4pt + mid)
    v(5pt)
    for lang in data.langues {
      grid(
        columns: (1fr, auto),
        text(size: 9pt, fill: white, lang.langue),
        text(size: 9pt, fill: mid, lang.niveau),
      )
      v(3pt)
    }
  }
}

// ── Main content ─────────────────────────────────────────────────────────────
#let main-content = {
  // Accroche
  if data.at("accroche", default: "") != "" {
    box(
      fill: light,
      inset: 10pt,
      radius: 4pt,
      width: 100%,
      text(size: 9.5pt, style: "italic", fill: navy, data.accroche)
    )
    v(8pt)
  }

  // Expériences
  if data.at("experiences", default: ()).len() > 0 {
    section-title("Expériences professionnelles")
    for exp in data.experiences {
      exp-entry(
        poste: exp.poste,
        entreprise: exp.at("entreprise", default: ""),
        dates: exp.at("dates", default: ""),
        description: exp.at("description", default: ""),
      )
    }
  }

  // Projets
  if data.at("projets", default: ()).len() > 0 {
    section-title("Projets")
    for proj in data.projets {
      text(weight: "bold", size: 10pt, proj.nom)
      h(6pt)
      for tech in proj.at("technologies", default: ()) {
        tag(tech)
        h(3pt)
      }
      v(3pt)
      text(size: 9pt, proj.at("description", default: ""))
      v(6pt)
    }
  }

  // Formation
  if data.at("formation", default: ()).len() > 0 {
    section-title("Formation")
    for f in data.formation {
      grid(
        columns: (1fr, auto),
        text(weight: "bold", size: 10pt, f.diplome),
        text(size: 9pt, fill: muted, f.at("dates", default: "")),
      )
      text(size: 9pt, fill: muted, style: "italic", f.at("etablissement", default: ""))
      v(6pt)
    }
  }
}

// ── Layout 2 colonnes ────────────────────────────────────────────────────────
#grid(
  columns: (33%, 67%),
  // Sidebar
  rect(
    fill: navy,
    height: 100%,
    width: 100%,
    inset: (x: 16pt, y: 20pt),
    sidebar-content,
  ),
  // Contenu principal
  rect(
    fill: white,
    height: 100%,
    width: 100%,
    inset: (x: 20pt, y: 20pt),
    main-content,
  ),
)
